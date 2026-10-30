---
name: sp-unsplash-gorsel-indirme
description: "Şu durumlarda yükle: site/uygulama için Unsplash'ten görsel aranacak, ticari kullanıma uygunluk denetlenecek, beğenilen fotoğraf assets/img altına SEO adlı WebP/JPG olarak indirilecek, görsel onayı ve credits.json kaydı gerekecekse; 'Unsplash görsel bul/indir' istendiğinde veya mevcut görsel atıf/ticari onay kaydı denetleneceğinde. Genel görsel üretimi ve Unsplash dışı kaynaklarda yüklenmez."
version: "v202610310029"
---
# sp-unsplash-gorsel-indirme

Site veya uygulama için Unsplash'ten uygun fotoğrafı bulur, seçilen fotoğrafı SEO adlı WebP/JPG varlıklara indirir ve atıf kaydı üretir. Uygulama aracı: `scripts/unsplash_gorsel.py` (yalnız Python standart kütüphanesi, ek paket gerekmez, Python ≥3.10). Bu skill görselin kaynağını ve uyumunu yönetir; sayfa tasarımı, layout ve animasyon kararları ilgili tasarım/mimari skill'lerine aittir.

## 0. Değişmez kurallar

- API anahtarı gizlidir: yalnız `UNSPLASH_ACCESS_KEY` ortam değişkeni veya proje kökündeki `.env` dosyası. Anahtarı komuta, çıktıya, loga, commit'e, sohbete yazma.
- API anahtarı yoksa önce anahtar alınmasını öner. Yalnız kullanıcı açıkça isterse ve düşük hacimde tarayıcı yedeği kullanılabilir; bu yol API Kılavuzu yerine geçmez, Unsplash site otomasyonu riski taşır (ayrıntı: `references/tarayici-yedegi.md`).
- Unsplash API kuralı (2026-10-30 doğrulandı): API kullanımında `photo.urls` hotlink zorunludur; indirme benzeri eylemde `photo.links.download_location` çağrılmalıdır; atıf ve UTM zorunludur. Ayrıntı: `references/unsplash-api-kurallari.md`. Yayın öncesi kuralı context7 (`/websites/unsplash`) veya resmî belgeden yeniden doğrula.
- Üretim sitesinde varsayılan yol **hotlink + görünür atıf**tır. Yerel indirme yalnız kullanıcı açıkça isterse yapılır; API kılavuzu hotlink istediğinden bu karar ve sorumluluk kullanıcıya aittir. Kurumsal görsel altyapısı gerekiyorsa çözüm Unsplash API ekibiyle görüşülmelidir; bunu kullanıcıya bildir.
- `credits.json` atıf kaydının tek doğruluk kaynağıdır; silinmez, elle bozulmaz, repoda tutulur.
- URL'lerdeki `ixid` parametresi korunur; araç bunu otomatik korur, elle URL kısaltılmaz.
- UTM/uygulama adı "Unsplash" içermez; `--uygulama-adi` için kayıtlı uygulama adını kullan (kılavuz yasağı).
- **Ticari güvenlik varsayılan ve pazarlıksızdır:** ticari kullanımda marka/logo, tanınabilir kişi, sanat eseri/telifli iş, özel mülk ve hassas içerik riski taşıyan görsel indirilmez; `plus.unsplash.com`/`premium_photo` asla indirilmez. İndirilen her görsel gözle denetlenmeden ve `onayla --karar uygun` ile `credits.json`'a işlenmeden ticari sayfaya eklenmez. Ayrıntı: `references/ticari-guvenlik.md`.

## 1. Ön koşul kontrolü

1. Python sürümünü doğrula: `python --version` (≥3.10).
2. Anahtar var mı: ortam değişkeni veya proje kökü `.env`. `.env` `.gitignore` içinde değilse ekle.
3. Kotayı bil: demo modunda saatlik 50 JSON isteği, production onayında 1000; görsel CDN istekleri kotaya sayılmaz.
4. Anahtar yoksa kullanıcıdan iste; anahtarı mesajda veya repoda gösterme. Anahtarsız `ara` çağrısı çıkış kodu 3 verir. Kullanıcı anahtar veremiyorsa ve açıkça istiyorsa düşük hacimli tarayıcı yedeğine geç (`references/tarayici-yedegi.md`); aksi halde çevrimdışı testlerle ilerle.

## 2. İş akışı

1. **Ara:** `python scripts/unsplash_gorsel.py ara --sorgu "<İngilizce terim>" --adet 8 --yon landscape --min-genislik 1600`
   JSON'daki `sonuclar[]` alanından `id`, `kullan_url`, `atif_html`, `genislik`, `renk`, `aciklama` bilgilerini oku. Sorgu İngilizce ve somut olmalı (örn. "minimalist tech workspace blue tone"). Ticari modda `ticari_degerlendirme.durum` alanını kontrol et; `engelli` adayı hiç seçme, `manuel_dogrulama_gerekli` adayı görsel denetimle ilerlet.
2. **Seç:** sayfa konusu ve marka tonuna uygunluk, `renk` uyumu, metin için negatif alan, insan/nesne kompozisyonu, hedef yayın genişliğinin en az 2 katı çözünürlük (retina). Aynı `id` daha önce kullanıldıysa `credits.json` ile çakışmayı kontrol et.
3. **Üretimde kullan (varsayılan):** `kullan_url` değerini doğrudan `<img src>` veya `srcset` olarak kullan; `atif_html` çıktısını sayfada görünür bir yere yerleştir. İndirme yapma.
4. **Yerel varlık isteniyorsa:** `python scripts/unsplash_gorsel.py indir --id <FOTO_ID> --ad "<seo-ad>" --klasor assets/img --genislikler 640,960,1440 --format webp --kullanim-turu ticari`
   `--ad` Türkçe olabilir; araç ASCII SEO slug üretir. Çıktıdaki `dosyalar`, `srcset`, `atif_html`, `credits` alanlarını kullan. Çıktı yolları çalışma dizinine göredir.
   API anahtarı yoksa (yalnız kullanıcı açıkça istiyorsa ve düşük hacimde): `node scripts/unsplash_tarayici.mjs --sorgu "<terim>" --adet 2 --ad "<seo-ad>" --genislik 2400`. Chrome/CDP kullanır; ayrıntı ve MCP alternatifi `references/tarayici-yedegi.md`.
5. **Ticari onay (zorunlu):** indirilen görseli `read_image` veya Chrome ile aç; tanınabilir kişi/yüz, logo/marka, sanat eseri, özel mülk veya hassas içerik yoksa `python scripts/unsplash_gorsel.py onayla --id <FOTO_ID> --ad "<seo-ad>" --karar uygun --onaylayan "<ad>" --not "<denetim notu>"`; varsa `--karar uygun-degil` kullan ve görseli kullanma. Ticari sayfaya yalnız `ticari_durum: onaylandi` kaydı girer.
6. **Doğrula:** `durum` `indirildi` veya `onbellek`; dosyalar diskte ve boyutları sıfırdan büyük; `srcset` HTML'e uygun; `credits.json` güncel; atıf sayfada görünür.
7. Tekrar çalıştırma güvenlidir: aynı fotoğraf/ölçü/biçim önbellekten döner, API kotası harcanmaz. Yeniden indirmek için `--uzerine-yaz` kullan.

## 2.1 Entegrasyon yolu seçimi

| Ortam | Yol |
| --- | --- |
| Python / CLI / genel | `scripts/unsplash_gorsel.py` (bu skill) |
| PHP / WordPress arka ucu | `references/sdk-entegrasyonu.md` → `unsplash-php` |
| Node.js / Next.js sunucu tarafı | `references/sdk-entegrasyonu.md` → `unsplash-js` |
| React / Vue tarayıcı | Anahtarı istemciye koyma; kendi sunucunda proxy + `unsplash-js` |
| API anahtarı yok | `references/tarayici-yedegi.md` (düşük hacim, kullanıcı onayı) |

SDK veya tarayıcı yolu seçilse de atıf, UTM, hotlink ve (indirme varsa) `download_location` uyumu aynıdır; `credits.json` korunur. SDK sürüm/API ayrıntısı yayın öncesi context7 veya resmî README'den doğrulanır.

## 2.2 Ticari kullanım güvenliği (zorunlu)

- Varsayılan `--kullanim-turu ticari`: Unsplash+ / `premium_photo` / Getty kaynaklı görseller ve kişi, logo/marka, sanat eseri, hassas içerik, özel mülk riski taşıyan metadata **indirilmez** (çıkış 8).
- `ara` çıktısındaki `ticari_degerlendirme.durum`: `engelli` → kullanma; `manuel_dogrulama_gerekli` → görsel denetim zorunlu.
- Görseli gözle denetle; uygunsa `onayla --karar uygun --onaylayan "<ad>" --not "<not>"`, değilse `--karar uygun-degil`. `credits.json` içinde `ticari_durum` ve `ticari_onay` denetim kaydı oluşur.
- Yalnız `ticari_durum: onaylandi` olan dosya ticari sayfaya girer; onaylanmadan kullanım yasaktır.
- Editoryal içerik yalnız `--kullanim-turu editorial` ile ve ticari reklam dışında kullanılır; Unsplash+ yine yasaktır.
- Anahtar kelime taraması heuristiktir, hukuki garanti değildir; model/property release gerekiyorsa kullanıcı temin eder. Ayrıntı ve kaynaklar: `references/ticari-guvenlik.md`.

## 3. Araç sözleşmesi

| Komut | Ne yapar | Ağ |
| --- | --- | --- |
| `ara` | Fotoğraf arar, dosya yazmaz; seçim için JSON listesi verir | 1 JSON API isteği |
| `indir` | Seçilen fotoğrafı indirir, `credits.json` günceller | 1 ayrıntı + 1 tetikleyici + görsel CDN istekleri |
| `baglantidan-indir` | Tarayıcıdan alınan görsel URL'sini yüksek çözünürlükte indirir, `credits.json` günceller | Görsel CDN (API anahtarı gerekmez) |
| `scripts/unsplash_tarayici.mjs` | Anahtarsız: Chrome/CDP ile Unsplash arar, URL'leri `baglantidan-indir`'e verir | Unsplash sitesi + görsel CDN |
| `onayla` | Ticari görsel denetimini `credits.json`'a işler (onay/red) | Ağ yok |

Önemli bayraklar: `--adet` 1-30, `--yon` landscape/portrait/squarish, `--min-genislik`, `--renk`, `--genislikler` 320-3840, `--format` webp|jpg, `--kalite` 1-100, `--uzerine-yaz`, `--uygulama-adi` (UTM), `--env-dosyasi`. Ayrıntı ve tüm varsayılanlar için `--help`.

Ticari bayraklar: `--kullanim-turu ticari|editorial`, `baglantidan-indir --aciklama`, `onayla --karar uygun|uygun-degil --onaylayan --not`.

Çıkış kodları: `0` başarı, `2` kullanım hatası, `3` anahtar eksik/geçersiz, `4` sonuç bulunamadı, `5` API/ağ/hız limiti, `6` doğrulama/güvenlik reddi, `7` indirme tetikleyicisi başarısız (görsel indirilmedi), `8` ticari risk (görsel indirilmedi).

Güvenlik davranışı: anahtar yalnız `api.unsplash.com` isteklerine eklenir, görsel CDN'e gönderilmez; URL'ler https/Unsplash veya yerel test ile sınırlıdır; 20 MB üst sınır; görsel imzası (RIFF/WEBP veya JPEG) doğrulanır; dosyalar geçici ada yazılıp atomik taşınır, hata halinde yarım dosya bırakılmaz.

## 4. HTML entegrasyonu

```html
<img src="assets/img/hakkimizda-kapak-1440.webp"
     srcset="assets/img/hakkimizda-kapak-640.webp 640w, assets/img/hakkimizda-kapak-960.webp 960w, assets/img/hakkimizda-kapak-1440.webp 1440w"
     sizes="(max-width: 768px) 100vw, 50vw" width="1440" height="960"
     loading="lazy" decoding="async" alt="Hakkımızda ekibi modern ofiste">
<p class="fotograf-atif">Fotoğraf: <a href="PROFIL_URL?utm_source=...&amp;utm_medium=referral">Fotoğrafçı</a> /
<a href="https://unsplash.com/?utm_source=...&amp;utm_medium=referral">Unsplash</a></p>
```

- `atif_html` alanı bu paragrafın hazır halidir; HTML kaçırma aracın içinde yapılır.
- Gerçek en-boy oranını `width`/`height` olarak yaz (CLS önleme). Hero/LCP görselinde `loading="eager" fetchpriority="high"`, diğerlerinde `loading="lazy"`.
- CSS background zorunluysa en büyük dosyayı kullan, `image-set()` ile çözünürlük seç; atıf yine sayfada görünür olmalı.
- Araç kırpma yapmaz; OG/kare gibi özel oranlar CSS `object-fit` veya üst katmanla çözülür.

## 5. Uyum kontrol listesi

- [ ] Görünür atıf: fotoğrafçı adı + Unsplash bağlantısı + UTM parametreleri.
- [ ] Ticari modda görsel `engelli` değil; `credits.json` kaydı `ticari_durum: onaylandi` ve `ticari_onay` dolu.
- [ ] Görselde tanınabilir kişi/yüz, logo/marka, sanat eseri, özel mülk veya hassas içerik yok (gözle denetlendi).
- [ ] Unsplash+ / `premium_photo` / Getty kaynaklı görsel kullanılmadı.
- [ ] Model/property release gerekiyorsa kullanıcı tarafından temin edildi veya görsel değiştirildi.
- [ ] `credits.json` repoda ve güncel; fotoğraf kimliği, fotoğrafçı, lisans ve dosya listesi kayıtlı.
- [ ] `ixid` parametresi URL'lerde korunmuş.
- [ ] Üretimde hotlink mi yerel kopya mı kullanıldığı bilinçli karar; yerel kopyada kullanıcı onayı var.
- [ ] Tarayıcı yedeği kullanıldıysa: düşük hacim ve kullanıcı onayı var, `plus.unsplash.com` atlandı, `credits.json` kaydı `kaynak: "tarayici"`, atıf görünür.
- [ ] İçerik filtresi `high` kullanıldı; bu daha katıdır ama uygunsuz içeriği %100 garanti etmez, görsel gözle ve bağlama göre denetlendi.
- [ ] Görsel marka, sayfa bağlamı ve erişilebilirlik açısından uygun (`alt` metni yazıldı).
- [ ] Ticari sınırlar: değiştirilmemiş fotoğraf satışı yok, Unsplash adı/logo uygulama kimliğinde yok, Unsplash deneyimi klonlanmıyor.
- [ ] Hukuki yorum gerektiren nokta varsa `doğrulanmalı` etiketiyle kullanıcıya bildirildi.

## 6. Hata giderme

| Kod | Anlam | Eylem |
| --- | --- | --- |
| 3 | Anahtar yok/geçersiz | `.env` veya ortam değişkenini düzelt; anahtarı paylaşma |
| 4 | Uygun sonuç yok | İngilizce/somut terim, `--min-genislik` düşür, `--sayfa` artır |
| 5 | API/ağ/hız limiti | Script 1-2-4 sn ile 3 kez dener; 403/429 ise kotayı bekle, production onayı gerekebilir; 410 spam sorguda terimi değiştir |
| 6 | Doğrulama/güvenlik | URL, dosya imzası veya bozuk `credits.json`; araç bozuk manifesti yedekler, elle kontrol et |
| 7 | Tetikleyici başarısız | İndirme yapılmadı; tekrar dene; API kuralı gereği tetikleyici atlanmaz |
| 8 | Ticari risk | Görsel indirilmedi; engelli adayı kullanma, farklı aday seç; Unsplash+ asla indirilmez; manuel onayı unutma |
| 2 | Kullanım hatası | `--help` ile bayrakları kontrol et |

Tarayıcı yedeği (`unsplash_tarayici.mjs`) çıkışları: `3` Chrome/Python yok, `4` uygun görsel yok (stderr'de teşhis), `5` CDP/ağ/indirme hatası, 8 ticari risk.

## 7. Test ve bakım

- Zorunlu test: `python scripts/test_unsplash_gorsel.py` — ağsız ve anahtarsız çalışır, 20 test `OK` dönmelidir; ticari blok/onay testleri dahildir. Testler geçmeden davranış değişikliği yayınlanmaz.
- Tarayıcı betiği testi: `node scripts/unsplash_tarayici.mjs --kendini-test` (ağ/tarayıcı gerekmez) 6 doğrulama döndürmelidir.
- Canlı duman testi (anahtar varsa): `python scripts/unsplash_gorsel.py ara --sorgu "minimalist workspace" --adet 1`.
- Değişiklikte sürüm damgası (`vYYYYMMDDHHMM`), README katalog satırı ve `references/` eşitlenir; gerçek anahtar ve kişisel veri eklenmez.
- API sözleşmesi değişebilir: yayın öncesi context7 `/websites/unsplash` veya resmî belge ile doğrula; script davranışı `references/unsplash-api-kurallari.md` ile eşleşmeli.

## 8. Sınırlar

- Unsplash kaynaklı (API veya tarayıcı yedeği) görsel tedariki; AI görsel üretimi, 3B modelleme ve stok dışı kaynaklar bu skill'in dışındadır.
- Tasarım/layout/animasyon kararları tasarım ve mimari skill'lerindedir.
- Anahtarsız canlı indirme yalnız düşük hacimli tarayıcı yedeğiyle ve kullanıcı onayıyla yapılır; toplu kazıma yasak, üretim için API anahtarı tercih edilir. Çevrimdışı testler anahtarsız çalışır.
- Ticari güvenlik varsayılandır; anahtar kelime taraması ve görsel denetim hukuki garanti değildir. Reklam/kampanya, tanınabilir kişi/marka ve özel mülk içeren kullanımlarda avukata danış.
- Bu skill hukuki danışmanlık değildir; lisans ve API koşulları değişebilir, kritik kararlar `doğrulanmalı` etiketiyle kullanıcıya bırakılır.