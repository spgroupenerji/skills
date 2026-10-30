# Kabul Kapıları — web sitesi tasarımı

> `sp-dizayn-web-site` eki. Hem tasarım kalitesini hem teknik tabanı ölçülebilir hâle getirir. Tasarım puanı ile teknik skor ayrı kanıtlardır; biri diğerinin yerine geçmez.

## 0. Mod ayrımı

0.1. Taban kontroller (içerik, erişilebilirlik, performans, SEO, çalışırlık) her modda geçerlidir; release kapıları yalnız release veya risk tetiklediğinde tam kanıt ister.
0.2. Tasarım puanı ilk önizlemede ve cilalı teslimde ayrı verilir; teknik skor yaratıcı puan yerine geçmez.

## 1. Sekiz boyutlu tasarım değerlendirmesi (1-10)

Aşağıdaki sekiz başlık ilk önizlemede ve cilalı teslimde ayrı ayrı puanlanır. Her puan tek cümlelik kanıtla yazılır; kanıtsız puan verilmez.

| Boyut | 10 nedir | Tipik eksik |
| --- | --- | --- |
| Bakış açısı | Markanın kendi dünyasından gelen, başka siteye taşınamayacak net bir kişilik | Jenerik ajans/kurumsal ton |
| Tipografi | Karakterli display + sakin gövde; bilinçli ölçek; başlık hareketi okunabilir plato bırakır | Varsayılan font, keyfi punto, taşan başlık |
| Renk | Rol tabanlı palet, dünyayla uyumlu, vurgu nadir ve işlevsel | Mor-mavi gradient, her yerde vurgu |
| Hiyerarşi | Her ekranda tek odak ve sonraki adım; ölçek/densite ritmi; tekrar gerekçeli | Aynı kart ızgarası, her bölümde CTA |
| Görseller | Tutarlı kimlik, ışık ve malzeme; kompozisyonlu sahneler; bozulma yok | Stok görsel, hero kırpıntısı filler |
| Hareket | Görsel, tipografi ve etkileşim tek deneyim; film varsa kuyruk eşleşmesi doğrulanmış | Rastgele giriş animasyonu, sürekli döngü |
| Mobil | Telefon için ayrı düşünülmüş kompozisyon; her vuruş ve kontrol çalışır | Masaüstünün küçültülmüş hâli |
| Cila | Hızlı yüklenir, konsol sıfır, taşma yok, form ve fallback'ler çalışır | Layout shift, kırık görsel, sahte başarı mesajı |

Kural: 10 üzerinden 8+ hedeflenir; en zayıf üç boyut ve her biri için tek somut iyileştirme yazılır. Teknik bir araç skoru (Lighthouse vb.) yaratıcı kalite puanı sayılmaz.

## 2. İçerik ve insan dili kapısı

2.1. Her metin, onaylanan design package ile birebir aynıdır; build sırasında yeniden yazılmaz.
2.2. Stok AI kalıbı taraması temizdir: "sadece X değil", "günümüzün hızlı dünyasında", "kusursuz deneyim", "yenilikçi çözümler", "tutkuyla", "sınırları zorlamak", "unlock/elevate/seamless/empower" ve benzeri.
2.3. Her iddia gerçek kaynağa dayanır; uydurma müşteri, ödül, sayı, adres veya yorum yoktur.
2.4. Tek CTA vardır; aynı ifadeyle en fazla üç kez tekrarlanır.
2.5. Türkçe imlâ tamdır; form etiketleri, hata ve başarı mesajları insan dilindedir.

## 3. Erişilebilirlik tabanı

- Semantik landmark'lar (`nav`, `main`, `footer`), tek `h1`, atlanmayan başlık sırası, skip link.
- Klavye ile tüm işlev; görünür `:focus-visible`; odak tuzağı yalnız modalda. Kontrast: gövde 4,5:1; büyük metin, kenar ve ikon 3:1.
- Dokunma hedefi kaba işaretçide en az 44px, her durumda 24x24 CSS px.
- `prefers-reduced-motion` altında hareketli her öğenin tasarlanmış final durumu vardır.
- Görsellerde anlamlı `alt`, dekoratif görselde boş `alt`; form alanları görünür etiketli. 320px genişlikte yatay kaydırma yok; 360/768/1440/1920 genişliklerde taşma yok.

## 4. Performans ve varlık tabanı

- İlk yükleme bütçesi proje kaydında tanımlıdır ve aşılmaz; JS toplamı site mimarisi bütçesine uyar. LCP ≤ 2,5 sn ve CLS ≤ 0,1 lab ile ölçülür; INP alan verisi veya etkileşim trace'iyle ölçülür, yoksa "doğrulanmalı" yazılır.
- Görseller WebP/AVIF, görüntülenen boyutta, `width`/`height` tanımlı; hero dışı `loading=lazy`.
- Hero video poster ile başlar, sessizdir, kullanıcı kontrolü vardır; mobilde statik alternatif.
- Tek `assets/css/site.css`, `:root` tokenları; Node, CDN, harici font CDN'i ve ikinci stil dosyası yok.
- Sinematik varsa: JS/GPU bütçesi proje kaydında onaylıdır; kütüphaneler self-host ve lisansı doğrulanmıştır; reduced-motion, video/WebGL yokluğu ve JS kapalı testleri geçmiştir.
- Hash'li varlıklar uzun ömürlü, HTML kısa ömürlü önbelleklenir; kaynak haritası ve sır istemciye gitmez.

## 5. SEO ve yapısal taban

Altyapı (meta, canonical, JSON-LD, sitemap, robots, yönlendirme) sp-mimari-web-site'tadır; burada tasarım çıktısı kontrol edilir:
- Gerçek title/description/canonical/OG; tek h1 ve görsel hiyerarşiyle aynı başlık sırası.
- JSON-LD uydurma veri taşımaz; içerik JS kapalıyken okunur; hreflang karşılıklı.

## 6. Çalışırlık ve yayın kapısı

Yayın prosedürü, geri alma ve alan izleme sp-mimari-web-site'tadır; burada canlı çıktının smoke kontrolü yapılır:
- Konsol/ağ/404 sıfır; form istemci + sunucu doğrulamalı, demo form "gönderildi" diyemez.
- Menü, galeri, video, modal klavye ve dokunmayla çalışır; HTTPS, canlı URL 200, canonical/OG, robots doğrulanır.
- Emülasyon gerçek telefon sayılmaz; fiziksel cihaz yoksa "doğrulanmalı".

## 7. Kanıt biçimi

1. Ekran görüntüleri: hero, temsili alt bölüm, telefon; 360/768/1440/1920 kesitleri.
2. Lighthouse mobil raporu: Performance ve Accessibility puanları; SEO/En iyi uygulamalar ayrı.
3. DevTools Performance trace'i: uzun görev ve kare düşmesi kontrolü.
4. Konsol listesi: sıfır hata/uyarı (bilinçli uyarılar gerekçeli).
5. Kontrast ve hedef boyutu ölçümleri; klavye turu notu.
6. Metin taraması: yasak kalıp eşleşmeleri ve insan editör onayı.
7. Yayın smoke çıktısı: HTTP durum kodları, canlı URL, form testi.
8. Sinematik kanıt: trace özeti (frame süresi ve uzun görev), üç fallback ekranı (tam, reduced motion, WebGL/video yok), gerçek cihaz notu, kare dizisinde ileri/geri/rastgele seek tutarlılığı.

## 8. Durdurucu koşullar

- Uydurma iddia, sahte referans veya sahte form başarısı.
- Erişilebilirlik tabanının ihlali; reduced-motion final durumunun yokluğu.
- Bütçe aşımı veya konsol hatası; kırık görsel/video.
- Onaysız metin değişikliği; design package ile çelişen build.
- Gerçek cihaz/alan verisi kanıtı olmadan "doğrulandı" beyanı.

## 9. Kanıt şablonu

| Kapı | Araç veya komut | Çıktı | Sonuç |
| --- | --- | --- | --- |
| Taban (konsol, 404, form) | chrome-devtools | Konsol/ağ listesi, form testi | Geçti/Kaldı |
| Tasarım (8 boyut) | Ekranlar ve değerlendirme | Hero, alt bölüm, telefon | Puan ve en zayıf üç madde |
| Erişilebilirlik ve performans | a11y-debugging, trace, Lighthouse | Odak/kontrast, LCP/CLS, INP trace | Geçti/Kaldı |
| Sinematik ve yayın | trace, cihaz, canlı URL | Frame, üç fallback, seek, HTTP/OG | Geçti/Kaldı |
