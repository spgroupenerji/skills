// unsplash_tarayici.mjs
// API anahtarı olmadan Unsplash arama sayfasını headless Chrome + CDP ile tarar,
// görselleri yüksek çözünürlükte indirmek için Python indirme motorunu çağırır.
// Gereksinim: Node.js >= 21 (yerleşik WebSocket/fetch), Chrome/Edge/Brave, Python >= 3.10.
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir, platform } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';
import assert from 'node:assert/strict';

const BETIK = fileURLToPath(new URL('./unsplash_gorsel.py', import.meta.url));
const VARSAYILAN_ADET = 3;
const AZAMI_ADET = 6;
const VARSAYILAN_GENISLIK = 2400;
const VARSAYILAN_KALITE = 92;
const VARSAYILAN_KLASOR = 'assets/img';
const VARSAYILAN_UYGULAMA = 'sp-gorsel-indirme';
const ZAMAN_ASIMI_MS = 30000;
const INDIRME_ZAMAN_ASIMI_MS = 120000;
const KAYDIRMA_SAYISI = 3;
const KAYDIRMA_BEKLEME_MS = 1200;
const YUKLEME_BEKLEME_MS = 2500;
const INDIRME_ARASI_MS = 700;
const PORT_TABANI = 9300;
const PORT_ARALIGI = 700;
const TARAYICI_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36';

const KOD = {
  TAMAM: 0,
  KULLANIM: 2,
  ORTAM: 3,
  SONUC_YOK: 4,
  AG: 5,
  DOGRULAMA: 6,
  TICARI: 8,
};

class KullanimHatasi extends Error {}
class OrtamHatasi extends Error {}
class SonucYokHatasi extends Error {}
class AgHatasi extends Error {}

function uyu(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const TURKCE = {
  'ç': 'c', 'Ç': 'c', 'ğ': 'g', 'Ğ': 'g', 'ı': 'i', 'İ': 'i',
  'ö': 'o', 'Ö': 'o', 'ş': 's', 'Ş': 's', 'ü': 'u', 'Ü': 'u',
};

function slugUret(metin) {
  const cevrilmis = String(metin || '').replace(/[çÇğĞıİöÖşŞüÜ]/g, (harf) => TURKCE[harf]);
  const ascii = cevrilmis.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const slug = ascii.replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60);
  return slug || 'unsplash-gorsel';
}

function fotografIdCikar(href) {
  const temiz = String(href || '').split('?')[0].replace(/\/+$/, '');
  const parca = temiz.split('/').pop() || '';
  if (!/^[A-Za-z0-9_-]{5,200}$/.test(parca)) return '';
  if (!parca.includes('-')) return parca.length <= 40 ? parca : '';
  const aday = parca.split('-').pop() || '';
  return /^[A-Za-z0-9_-]{5,40}$/.test(aday) ? aday : '';
}

function aramaAdresi(sorgu, yon) {
  const temel = 'https://unsplash.com/s/photos/' + encodeURIComponent(sorgu);
  return yon ? temel + '?orientation=' + encodeURIComponent(yon) : temel;
}

function secimleriAyikla(kartlar, adet) {
  const gorulen = new Set();
  const secilen = [];
  for (const kart of kartlar || []) {
    if (!kart || !kart.gorsel || !kart.fotografSayfasi || kart.plus) continue;
    const kimlik = kart.id || kart.fotografSayfasi;
    if (gorulen.has(kimlik)) continue;
    gorulen.add(kimlik);
    secilen.push(kart);
    if (secilen.length >= adet) break;
  }
  return secilen;
}

function tarayicilariBul() {
  const adaylar = [];
  if (process.env.UNSPLASH_TARAYICI) adaylar.push({ ad: 'UNSPLASH_TARAYICI', yol: process.env.UNSPLASH_TARAYICI });
  if (platform() === 'win32') {
    const pf = process.env.PROGRAMFILES || 'C:\\Program Files';
    const pf86 = process.env['PROGRAMFILES(X86)'] || 'C:\\Program Files (x86)';
    const yerel = process.env.LOCALAPPDATA || '';
    adaylar.push(
      { ad: 'Google Chrome', yol: join(pf, 'Google\\Chrome\\Application\\chrome.exe') },
      { ad: 'Google Chrome (x86)', yol: join(pf86, 'Google\\Chrome\\Application\\chrome.exe') },
      { ad: 'Google Chrome (User)', yol: join(yerel, 'Google\\Chrome\\Application\\chrome.exe') },
      { ad: 'Microsoft Edge', yol: join(pf86, 'Microsoft\\Edge\\Application\\msedge.exe') },
      { ad: 'Microsoft Edge (x64)', yol: join(pf, 'Microsoft\\Edge\\Application\\msedge.exe') },
      { ad: 'Brave', yol: join(pf, 'BraveSoftware\\Brave-Browser\\Application\\brave.exe') }
    );
  } else if (platform() === 'darwin') {
    adaylar.push(
      { ad: 'Google Chrome', yol: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' },
      { ad: 'Microsoft Edge', yol: '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge' },
      { ad: 'Brave', yol: '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser' }
    );
  } else {
    adaylar.push(
      { ad: 'Google Chrome', yol: '/usr/bin/google-chrome' },
      { ad: 'Chromium', yol: '/usr/bin/chromium-browser' },
      { ad: 'Chromium', yol: '/usr/bin/chromium' },
      { ad: 'Microsoft Edge', yol: '/usr/bin/microsoft-edge' },
      { ad: 'Brave', yol: '/usr/bin/brave-browser' }
    );
  }
  return adaylar.find((aday) => existsSync(aday.yol)) || null;
}

function pythonYoluBul() {
  const adaylar = [process.env.UNSPLASH_PYTHON, platform() === 'win32' ? 'python' : 'python3', 'python', 'py'].filter(Boolean);
  for (const aday of adaylar) {
    const sonuc = spawnSync(aday, ['--version'], { encoding: 'utf-8', timeout: 10000, windowsHide: true });
    if (sonuc.status === 0) return aday;
  }
  return '';
}

async function cdpBaglantisiKur(tarayiciYolu, port, profilDizini) {
  const proc = spawn(tarayiciYolu, [
    '--headless=new',
    '--disable-gpu',
    '--hide-scrollbars',
    '--mute-audio',
    '--no-first-run',
    '--no-default-browser-check',
    '--remote-debugging-port=' + port,
    '--user-agent=' + TARAYICI_UA,
    '--lang=en-US',
    '--disable-blink-features=AutomationControlled',
    '--user-data-dir=' + profilDizini,
    'about:blank',
  ], { stdio: 'ignore', windowsHide: true });
  for (let deneme = 0; deneme < 50; deneme++) {
    try {
      const yanit = await fetch('http://127.0.0.1:' + port + '/json/list');
      const sekmeler = await yanit.json();
      const sayfa = sekmeler.find((sekme) => sekme.type === 'page');
      if (sayfa && sayfa.webSocketDebuggerUrl) return { proc, wsUrl: sayfa.webSocketDebuggerUrl };
    } catch {
      // Tarayıcı henüz hazır değil.
    }
    await uyu(200);
  }
  proc.kill();
  throw new AgHatasi('Tarayıcı CDP portuna bağlanılamadı.');
}

async function cdpIstemcisi(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let sira = 0;
  const bekleyenler = new Map();
  const dinleyiciler = new Map();
  ws.onmessage = (olay) => {
    const veri = JSON.parse(olay.data);
    if (veri.id && bekleyenler.has(veri.id)) {
      const bekleyen = bekleyenler.get(veri.id);
      bekleyenler.delete(veri.id);
      if (veri.error) bekleyen.reddet(new AgHatasi(veri.error.message));
      else bekleyen.coz(veri);
    } else if (veri.method && dinleyiciler.has(veri.method)) {
      dinleyiciler.get(veri.method)(veri.params);
    }
  };
  await new Promise((coz, reddet) => {
    ws.onopen = coz;
    ws.onerror = () => reddet(new AgHatasi('CDP WebSocket bağlantısı kurulamadı.'));
  });
  const cdp = (method, params = {}) => new Promise((coz, reddet) => {
    const id = ++sira;
    bekleyenler.set(id, { coz, reddet });
    ws.send(JSON.stringify({ id, method, params }));
  });
  const olayBekle = (method, timeoutMs = ZAMAN_ASIMI_MS) => new Promise((coz) => {
    const zaman = setTimeout(() => {
      dinleyiciler.delete(method);
      coz();
    }, timeoutMs);
    dinleyiciler.set(method, (params) => {
      clearTimeout(zaman);
      dinleyiciler.delete(method);
      coz(params);
    });
  });
  return { cdp, olayBekle, kapat: () => ws.close() };
}

async function degerlendir(cdp, ifade) {
  const cevap = await cdp('Runtime.evaluate', { expression: ifade, returnByValue: true, awaitPromise: true });
  if (cevap.result && cevap.result.exceptionDetails) {
    throw new AgHatasi('Sayfa betiği hatası: ' + (cevap.result.exceptionDetails.text || 'bilinmiyor'));
  }
  return cevap.result && cevap.result.result ? cevap.result.result.value : undefined;
}

async function izinKapat(cdp) {
  const ifade = '(' + (function izinVer() {
    const dugmeler = Array.from(document.querySelectorAll('button'));
    const kabul = dugmeler.find((dugme) => /accept all|kabul et|allow all/i.test(dugme.textContent || ''));
    if (kabul) {
      kabul.click();
      return true;
    }
    return false;
  }).toString() + ')()';
  const tiklandi = await degerlendir(cdp, ifade);
  if (tiklandi) await uyu(700);
}

async function sayfaDurumu(cdp) {
  const ifade = '(' + (function durumBilgisi() {
    return {
      baslik: document.title,
      adres: location.href,
      gorselSayisi: document.images.length,
      figureSayisi: document.querySelectorAll('figure').length,
      fotoLinkSayisi: document.querySelectorAll('a[href^="/photos/"]').length,
      govdeBas: (document.body ? document.body.innerText : '').replace(/\s+/g, ' ').slice(0, 300),
    };
  }).toString() + ')()';
  return degerlendir(cdp, ifade);
}

async function kartlariTopla(cdp) {
  await cdp('Runtime.evaluate', { expression: 'window.scrollTo(0, 0)' });
  for (let sira = 0; sira < KAYDIRMA_SAYISI; sira++) {
    await cdp('Runtime.evaluate', { expression: 'window.scrollBy(0, window.innerHeight * 1.5)' });
    await uyu(KAYDIRMA_BEKLEME_MS);
  }
  await cdp('Runtime.evaluate', { expression: 'window.scrollTo(0, 0)' });
  await uyu(500);
  const ifade = '(' + (function tarayiciKartlari() {
    const temizle = (deger) => String(deger || '').replace(/\s+/g, ' ').trim();
    const kartlar = [];
    for (const figure of document.querySelectorAll('figure')) {
      const baglanti = figure.querySelector('a[href^="/photos/"]');
      const gorsel = baglanti ? baglanti.querySelector('img') : null;
      if (!baglanti || !gorsel) continue;
      const kaynak = gorsel.currentSrc || gorsel.src || '';
      if (!kaynak.includes('images.unsplash.com') && !kaynak.includes('plus.unsplash.com')) continue;
      const yazarLinkleri = Array.from(figure.querySelectorAll('a[href^="/@"]'));
      const yazar = yazarLinkleri.find((link) => temizle(link.textContent).length > 0) || yazarLinkleri[0];
      let fotografci = yazar ? temizle(yazar.textContent) : '';
      if (!fotografci) {
        const avatar = figure.querySelector('img[alt^="Go to "]');
        if (avatar) fotografci = temizle(avatar.alt).replace(/^Go to /, '').replace(/'s profile$/, '');
      }
      const href = (baglanti.getAttribute('href') || '').split('?')[0];
      const parca = href.split('/').pop() || '';
      const kimlikAdayi = parca.includes('-') ? parca.split('-').pop() : parca;
      const kimlik = /^[A-Za-z0-9_-]{5,40}$/.test(kimlikAdayi) ? kimlikAdayi : '';
      kartlar.push({
        id: kimlik,
        fotografSayfasi: 'https://unsplash.com' + href,
        fotografci: fotografci,
        profil: yazar ? 'https://unsplash.com' + yazar.getAttribute('href') : '',
        gorsel: kaynak,
        alt: temizle(gorsel.alt),
        plus: kaynak.includes('plus.unsplash.com'),
      });
    }
    return kartlar;
  }).toString() + ')()';
  return degerlendir(cdp, ifade);
}

function kartIndir(kart, ayar) {
  const argumanlar = [
    BETIK,
    'baglantidan-indir',
    '--url', kart.gorsel,
    '--ad', ayar.ad,
    '--klasor', ayar.klasor,
    '--genislik', String(ayar.genislik),
    '--format', ayar.format,
    '--kalite', String(ayar.kalite),
    '--kullanim-turu', ayar.kullanimTuru,
    '--aciklama', kart.alt || '',
    '--fotograf-id', kart.id || '',
    '--sorgu', ayar.sorgu,
    '--uygulama-adi', ayar.uygulama,
  ];
  if (kart.fotografci) argumanlar.push('--fotografci', kart.fotografci);
  if (kart.profil) argumanlar.push('--profil-url', kart.profil);
  if (kart.fotografSayfasi) argumanlar.push('--fotograf-sayfasi', kart.fotografSayfasi);
  const sonuc = spawnSync(ayar.python, argumanlar, {
    encoding: 'utf-8',
    timeout: INDIRME_ZAMAN_ASIMI_MS,
    windowsHide: true,
  });
  if (sonuc.status !== 0) {
    const hata = (sonuc.stderr || sonuc.stdout || '').trim().slice(0, 600);
    let kod = 0;
    try {
      kod = Number(JSON.parse(sonuc.stderr).kod) || 0;
    } catch {
      kod = 0;
    }
    return { basarili: false, id: kart.id, kod: kod, hata: hata || 'Python indirme motoru hata verdi.' };
  }
  try {
    return { basarili: true, veri: JSON.parse(sonuc.stdout) };
  } catch {
    return { basarili: false, id: kart.id, hata: 'Python çıktısı JSON olarak çözümlenemedi.' };
  }
}

function ayarlariDogrula(opts) {
  const sorgu = String(opts.sorgu || '').trim();
  if (!sorgu) throw new KullanimHatasi('--sorgu zorunlu.');
  const adet = Number.parseInt(opts.adet || String(VARSAYILAN_ADET), 10);
  if (!Number.isInteger(adet) || adet < 1 || adet > AZAMI_ADET) {
    throw new KullanimHatasi('--adet 1-' + AZAMI_ADET + ' aralığında olmalı.');
  }
  const genislik = Number.parseInt(opts.genislik || String(VARSAYILAN_GENISLIK), 10);
  if (!Number.isInteger(genislik) || genislik < 320 || genislik > 3200) {
    throw new KullanimHatasi('--genislik 320-3200 aralığında olmalı.');
  }
  const kalite = Number.parseInt(opts.kalite || String(VARSAYILAN_KALITE), 10);
  if (!Number.isInteger(kalite) || kalite < 1 || kalite > 100) {
    throw new KullanimHatasi('--kalite 1-100 aralığında olmalı.');
  }
  const format = opts.format || 'webp';
  if (!['webp', 'jpg'].includes(format)) throw new KullanimHatasi('--format webp veya jpg olmalı.');
  const yon = opts.yon || '';
  if (yon && !['landscape', 'portrait', 'squarish'].includes(yon)) {
    throw new KullanimHatasi('--yon landscape, portrait veya squarish olmalı.');
  }
  const kullanimTuru = opts['kullanim-turu'] || 'ticari';
  if (!['ticari', 'editorial'].includes(kullanimTuru)) {
    throw new KullanimHatasi('--kullanim-turu ticari veya editorial olmalı.');
  }
  const uygulama = opts['uygulama-adi'] || process.env.UNSPLASH_UTM_SOURCE || VARSAYILAN_UYGULAMA;
  return {
    sorgu: sorgu,
    ad: String(opts.ad || '').trim(),
    adet: adet,
    klasor: String(opts.klasor || VARSAYILAN_KLASOR),
    genislik: genislik,
    format: format,
    kalite: kalite,
    yon: yon,
    kullanimTuru: kullanimTuru,
    uygulama: uygulama,
  };
}

function kendiniTest() {
  assert.equal(slugUret('Hakkımızda Çalışma Şeklimiz'), 'hakkimizda-calisma-seklimiz');
  assert.equal(slugUret('Modern OFİS -- 2026'), 'modern-ofis-2026');
  assert.equal(fotografIdCikar('/photos/a-chair-sitting-next-to-a-plant-in-a-room-bYP89K7HX6c'), 'bYP89K7HX6c');
  assert.equal(fotografIdCikar('/photos/kisa-id'), '');
  assert.equal(aramaAdresi('modern office', 'landscape'), 'https://unsplash.com/s/photos/modern%20office?orientation=landscape');
  const deneme = secimleriAyikla([
    { id: 'a', gorsel: 'https://images.unsplash.com/a', fotografSayfasi: 'https://unsplash.com/photos/a' },
    { id: 'a', gorsel: 'https://images.unsplash.com/a2', fotografSayfasi: 'https://unsplash.com/photos/a' },
    { id: 'b', gorsel: 'https://plus.unsplash.com/b', fotografSayfasi: 'https://unsplash.com/photos/b', plus: true },
    { id: 'c', gorsel: 'https://images.unsplash.com/c', fotografSayfasi: 'https://unsplash.com/photos/c' },
  ], 5);
  assert.equal(deneme.length, 2);
  console.log(JSON.stringify({ durum: 'basarili', test: 'kendini-test', dogrulama: 6 }, null, 2));
}

async function ana() {
  let secenekler;
  try {
    secenekler = parseArgs({
      options: {
        sorgu: { type: 'string' },
        adet: { type: 'string' },
        ad: { type: 'string' },
        klasor: { type: 'string' },
        genislik: { type: 'string' },
        format: { type: 'string' },
        kalite: { type: 'string' },
        yon: { type: 'string' },
        'kullanim-turu': { type: 'string' },
        'uygulama-adi': { type: 'string' },
        tarayici: { type: 'string' },
        'kendini-test': { type: 'boolean', default: false },
      },
      allowPositionals: false,
      strict: true,
    }).values;
  } catch (hata) {
    throw new KullanimHatasi('Argüman hatası: ' + hata.message);
  }
  if (secenekler['kendini-test']) {
    kendiniTest();
    return KOD.TAMAM;
  }
  const ayar = ayarlariDogrula(secenekler);
  const tarayici = secenekler.tarayici
    ? (existsSync(secenekler.tarayici) ? { ad: 'Özel', yol: secenekler.tarayici } : null)
    : tarayicilariBul();
  if (!tarayici) throw new OrtamHatasi('Chrome/Edge/Brave bulunamadı. --tarayici ile yol verin.');
  const python = pythonYoluBul();
  if (!python) throw new OrtamHatasi('Python bulunamadı. API anahtarsız indirme için Python >= 3.10 gerekir.');
  const profilDizini = mkdtempSync(join(tmpdir(), 'unsplash-tarayici-'));
  const port = PORT_TABANI + Math.floor(Math.random() * PORT_ARALIGI);
  let proc = null;
  let istemci = null;
  try {
    const baglanti = await cdpBaglantisiKur(tarayici.yol, port, profilDizini);
    proc = baglanti.proc;
    istemci = await cdpIstemcisi(baglanti.wsUrl);
    await istemci.cdp('Page.enable');
    await istemci.cdp('Runtime.enable');
    await istemci.cdp('Emulation.setDeviceMetricsOverride', { width: 1440, height: 2000, deviceScaleFactor: 2, mobile: false });
    const adres = aramaAdresi(ayar.sorgu, ayar.yon);
    const yukleme = istemci.olayBekle('Page.loadEventFired', ZAMAN_ASIMI_MS);
    await istemci.cdp('Page.navigate', { url: adres });
    await yukleme;
    await uyu(YUKLEME_BEKLEME_MS);
    await izinKapat(istemci.cdp);
    const kartlar = await kartlariTopla(istemci.cdp);
    const secilen = secimleriAyikla(kartlar, Math.min(12, Math.max(ayar.adet * 2, ayar.adet + 3)));
    if (!secilen.length) {
      const durum = await sayfaDurumu(istemci.cdp);
      throw new SonucYokHatasi('Unsplash arama sayfasında uygun görsel bulunamadı. Teşhis: ' + JSON.stringify(durum).slice(0, 500));
    }
    const temelAd = ayar.ad || slugUret(ayar.sorgu);
    const sonuclar = [];
    const hatalar = [];
    for (let sira = 0; sira < secilen.length && sonuclar.length < ayar.adet; sira++) {
      const kart = secilen[sira];
      const ad = ayar.adet === 1 ? temelAd : temelAd + '-' + (sonuclar.length + 1);
      const islem = { ...ayar, ad: ad, python: python };
      const indirme = kartIndir(kart, islem);
      if (indirme.basarili) sonuclar.push(indirme.veri);
      else hatalar.push(indirme);
      if (sira < secilen.length - 1 && sonuclar.length < ayar.adet) await uyu(INDIRME_ARASI_MS);
    }
    const cikti = {
      durum: sonuclar.length ? 'indirildi' : 'basarisiz',
      kaynak: 'tarayici',
      sorgu: ayar.sorgu,
      sayfa: adres,
      sayi: sonuclar.length,
      sonuclar: sonuclar,
      hatalar: hatalar,
      ticari_onay_gerekli: ayar.kullanimTuru === 'ticari',
      uyari: 'Ticari güvenlik varsayılan: her görsel gözle doğrulanmalı (kişi/logo/marka/eser/özel mülk/hassas içerik yok) ve onayla --karar uygun çalıştırılmalı; onaylanmadan ticari sayfaya eklemeyin. Unsplash+ görselleri lisans nedeniyle atlandı; API anahtarsız tarayıcı yedeği düşük hacimde kullanılmalıdır.',
    };
    console.log(JSON.stringify(cikti, null, 2));
    if (sonuclar.length) return KOD.TAMAM;
    if (hatalar.length && hatalar.every((hata) => hata.kod === KOD.TICARI)) return KOD.TICARI;
    return hatalar.length ? KOD.AG : KOD.SONUC_YOK;
  } finally {
    if (istemci) istemci.kapat();
    if (proc) proc.kill();
    await uyu(400);
    try {
      rmSync(profilDizini, { recursive: true, force: true });
    } catch {
      // Geçici profil silinemezse iş akışı durmaz.
    }
  }
}

try {
  const kod = await ana();
  process.exitCode = kod;
} catch (hata) {
  const kod = hata instanceof KullanimHatasi ? KOD.KULLANIM
    : hata instanceof OrtamHatasi ? KOD.ORTAM
      : hata instanceof SonucYokHatasi ? KOD.SONUC_YOK
        : KOD.AG;
  console.error(JSON.stringify({ hata: hata.message, kod: kod }, null, 2));
  process.exitCode = kod;
}
