# Tarayıcı Yedeği (API anahtarı olmadan)

Amaç: Kullanıcı API anahtarı almadan, tek seferlik ve düşük hacimli ihtiyaçta Unsplash arama sayfasından görsel bulup yüksek çözünürlükte indirmek. Headless Chrome + CDP kullanır; npm paketi gerekmez (Node.js >= 21, Chrome/Edge/Brave, Python >= 3.10).

> **Uyum uyarısı:** Bu yol Unsplash API'sini kullanmaz; API Kılavuzu'nun hotlink/atıf kuralları yerine Unsplash web sitesi otomasyonu devreye girer. Site otomasyonu Unsplash Terms kapsamında risk taşır (**doğrulanmalı**). Yalnız kullanıcı açıkça isterse, az sayıda görsel için ve toplu kazıma yapmadan kullan. Üretim için API anahtarı + `ara`/`indir` yolu tercih edilir.

## Ticari güvenlik (varsayılan)

- Varsayılan `--kullanim-turu ticari`; `plus.unsplash.com` zaten atlanır.
- Python motoru URL + alt açıklama + fotoğrafçı üzerinden ticari kapıyı uygular; kişi/logo/marka/eser/hassas içerik/özel mülk riski varsa görseli **indirmez**, çıkış kodu 8 verir.
- İndirilen görsel gözle denetlenmeden ve `onayla --karar uygun` ile `credits.json`'a işlenmeden ticari sayfaya eklenmez.
- Editoryal içerik yalnız `--kullanim-turu editorial` ile ve ticari reklam dışında kullanılır; Unsplash+ yine yasaktır.

## Komut

```powershell
node scripts/unsplash_tarayici.mjs --sorgu "modern office" --adet 2 --ad hakkimizda --klasor assets/img --genislik 2400 --format webp --kalite 92 --kullanim-turu ticari --yon landscape
```

- `--adet` 1-6 (varsayılan 3); düşük hacim için küçük tut.
- `--genislik` 320-3200 (varsayılan 2400), `--kalite` 1-100 (varsayılan 92), `--format` webp|jpg.
- `--sorgu` İngilizce ve somut olmalı. `--ad` verilmezse sorgudan ASCII slug üretilir; birden fazla görselde `-1`, `-2` sonekleri eklenir.
- `--tarayici` ile Chrome/Edge yolu; `UNSPLASH_PYTHON` ile Python yolu verilebilir.
- Aynı komutu tekrar çalıştırmak önbellekten döner (Python motoru); dosya varsa yeniden indirilmez.

## Akış

1. Headless Chrome geçici profille açılır (gerçek Chrome UA'sı, `deviceScaleFactor=2`).
2. `https://unsplash.com/s/photos/<sorgu>` adresine gidilir; consent varsa kapatılır.
3. Sayfa 3 kez kaydırılır; `figure` kartlarından fotoğraf bağlantısı, görsel URL'si, fotoğrafçı adı/profili ve fotoğraf sayfası çıkarılır.
4. `plus.unsplash.com` (Unsplash+) görselleri lisans belirsizliği nedeniyle atlanır.
5. Her seçilen görsel için Python motoru çağrılır: `baglantidan-indir` URL'yi `w=<genislik>&q=<kalite>&fm=<bicim>&fit=max` ile yeniden kurar, `ixid` korunur, eski `crop/cs/w` boyut parametreleri temizlenir.
6. Görsel imzası doğrulanır, atomik yazılır, `credits.json` kaydı `kaynak: "tarayici"` ve ticari durum bilgisiyle güncellenir; UTM'li atıf HTML'i üretilir.
7. Ticari kullanım öncesi görsel gözle denetlenir; uygunsa `onayla --karar uygun` ile kayda geçirilir, değilse kullanılmaz.

## Çıktı ve kodlar

JSON: `durum`, `kaynak: "tarayici"`, `sorgu`, `sayfa`, `sayi`, `sonuclar[] `(her görsel için Python çıktısı), `hatalar[] `ve `uyari`.

| Kod | Anlam |
| --- | --- |
| 0 | En az bir görsel indirildi |
| 2 | Kullanım/argüman hatası |
| 3 | Chrome veya Python bulunamadı |
| 4 | Sayfada uygun görsel bulunamadı (teşhis bilgisi stderr'de) |
| 5 | CDP/ağ/indirme hatası; hiçbiri indirilemedi |
| 8 | Ticari risk: tüm adaylar engelli veya premium; görsel indirilmedi |

Kendini test (ağ/tarayıcı gerekmez): `node scripts/unsplash_tarayici.mjs --kendini-test`

## Chrome DevTools MCP alternatifi

Ajan oturumunda `chrome-devtools` MCP varsa tarayıcıyı MCP üzerinden de kullanabilirsin:

1. `navigate_page` ile `https://unsplash.com/s/photos/<sorgu>?orientation=landscape` aç, yükleme bitene kadar bekle.
2. `evaluate_script` ile aşağıdaki ifadeyi çalıştır (fotoğraf kartlarını döndürür):

```js
() => Array.from(document.querySelectorAll('figure')).map((figure) => {
  const link = figure.querySelector('a[href^="/photos/"]');
  const img = link && link.querySelector('img');
  if (!link || !img) return null;
  const temiz = (s) => String(s || '').replace(/\s+/g, ' ').trim();
  const yazarLinkleri = Array.from(figure.querySelectorAll('a[href^="/@"]'));
  const yazar = yazarLinkleri.find((a) => temiz(a.textContent)) || yazarLinkleri[0];
  const avatar = figure.querySelector('img[alt^="Go to "]');
  const parca = (link.getAttribute('href') || '').split('/').pop() || '';
  const aday = parca.includes('-') ? parca.split('-').pop() : parca;
  return {
    id: /^[A-Za-z0-9_-]{5,40}$/.test(aday) ? aday : '',
    fotografSayfasi: 'https://unsplash.com' + link.getAttribute('href').split('?')[0],
    fotografci: yazar ? temiz(yazar.textContent) : (avatar ? temiz(avatar.alt).replace(/^Go to /, '').replace(/'s profile$/, '') : ''),
    profil: yazar ? 'https://unsplash.com' + yazar.getAttribute('href') : '',
    gorsel: img.currentSrc || img.src,
    plus: (img.currentSrc || img.src).includes('plus.unsplash.com'),
  };
}).filter(Boolean)
```

3. Seçtiğin her görsel için Python motorunu çağır:

```powershell
python scripts/unsplash_gorsel.py baglantidan-indir --url "<gorsel-url>" --ad "<seo-ad>" --genislik 2400 --kalite 92 --format webp --fotografci "<fotografci>" --profil-url "<profil>" --fotograf-sayfasi "<foto-sayfasi>" --aciklama "<alt-metin>" --kullanim-turu ticari --fotograf-id "<id>" --sorgu "<sorgu>"
```

4. Ticari kullanım öncesi görseli gözle denetle; uygunsa `python scripts/unsplash_gorsel.py onayla --id "<id>" --ad "<seo-ad>" --karar uygun --onaylayan "<ad>"` çalıştır; değilse kullanma.

MCP tarayıcısı kalıcı profil kullandığı için consent/oturum durumunu kontrol et; sayfa yapısı değişirse kart seçicilerini güncelle (**doğrulanmalı**).

## Sorun giderme

| Belirti | Çözüm |
| --- | --- |
| Kart bulunamadı / 4 | Stderr'deki teşhis (başlık, adres, figure sayısı) sayfa yapısını gösterir; sorguyu İngilizce yap, sayfayı yenile, şablon değişmişse seçiciyi güncelle |
| Headless engeli | Chrome UA zaten gerçek; yine olursa MCP tarayıcıyla dene, sayfayı elle doğrula |
| Chrome yok / 3 | `--tarayici "C:\...\chrome.exe"` veya Edge/Brave kur |
| Python yok / 3 | Python >= 3.10 kur veya `UNSPLASH_PYTHON` ile yolu ver |
| CDN 403/404 / 5 | URL'nin süresi dolmuş olabilir; sayfayı yenileyip yeni URL ile tekrar dene |
| Unsplash+ atlandı | Unsplash+ lisansı ayrıdır; API/abonelik olmadan kullanma |
| Ticari engel / 8 | Kişi/logo/marka/eser/hassas içerik riski; farklı aday seç veya editoryal modu kullan; görsel indirilmedi |

## Doğrulama notu

2026-10-31 canlı testte modern office aramasından XORfEIs_LTk kimlikli görsel, 2400 genişlikte WebP (451.840 bayt) olarak indirildi; fotoğrafçı, UTM'li atıf ve `credits.json` üretildi. Bu kanıt DOM'un o günkü yapısına aittir; Unsplash şablonu değişebilir.
