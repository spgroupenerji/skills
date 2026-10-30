# Kabul Kapıları — web sitesi tasarımı

> `sp-dizayn-web-site` eki. Hem tasarım kalitesini hem teknik tabanı ölçülebilir hâle getirir. Tasarım puanı ile teknik skor ayrı kanıtlardır; biri diğerinin yerine geçmez.

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
- Klavye ile tüm işlev; görünür `:focus-visible`; odak tuzağı yalnız modalda.
- Kontrast: gövde 4,5:1; büyük metin, kenar ve ikon 3:1.
- Dokunma hedefi kaba işaretçide en az 44px, her durumda 24x24 CSS px.
- `prefers-reduced-motion` altında hareketli her öğenin tasarlanmış final durumu vardır.
- Görsellerde anlamlı `alt`, dekoratif görselde boş `alt`; form alanları görünür etiketli.
- 320px genişlikte yatay gövde kaydırması yok; 360/768/1440/1920 genişliklerde taşma yok.

## 4. Performans ve varlık tabanı

- İlk yükleme bütçesi proje kaydında tanımlıdır ve aşılmaz; JS toplamı site mimarisi bütçesine uyar.
- LCP ≤ 2,5 sn, INP ≤ 200 ms, CLS ≤ 0,1 (lab); alan verisi yoksa "doğrulanmalı" yazılır.
- Görseller WebP/AVIF, görüntülenen boyutta, `width`/`height` tanımlı; hero dışı `loading=lazy`.
- Hero video poster ile başlar, sessizdir, kullanıcı kontrolü vardır; mobilde statik alternatif.
- Tek `assets/css/site.css`, `:root` tokenları; Node, CDN, harici font CDN'i ve ikinci stil dosyası yok.
- Hash'li varlıklar uzun ömürlü, HTML kısa ömürlü önbelleklenir; kaynak haritası ve sır istemciye gitmez.

## 5. SEO ve yapısal taban

- Gerçek `title`, meta description, canonical, Open Graph ve Twitter Card.
- Organization/WebSite JSON-LD; uygun sayfada BreadcrumbList/Product/FAQPage; uydurma veri yok.
- `robots.txt` ve `sitemap.xml` doğru; yayın ortamında indeksleme engeli yok.
- Adres değişiklikleri 301; zincirleme yönlendirme yok; çok dilli sitede hreflang karşılıklı.
- İçerik sunucudan gelir; JS kapalıyken ana metin ve bağlantılar okunabilir.

## 6. Çalışırlık ve yayın kapısı

- Konsol hatası sıfır; ağ hatası, eksik görsel ve 404 varlık yok.
- Form: istemci + sunucu doğrulaması, CSRF/honeypot, gerçek başarı ve hata durumu; demo form "gönderildi" diyemez.
- Menü, galeri, video, modal ve dil/para birimi gibi etkileşimler klavye ve dokunmayla çalışır.
- Yayın öncesi ve sonrası smoke listesi ile geri alma adımı yazılıdır.
- Yayın sonrası HTTPS, canlı URL 200, canonical/OG gerçek adres, form ucu ve robots durumu doğrulanır.
- Emülasyon gerçek telefon diye sunulmaz; fiziksel cihaz kontrolü yapılmadıysa "doğrulanmalı" yazılır.

## 7. Kanıt biçimi

1. Ekran görüntüleri: hero, temsili alt bölüm, telefon; 360/768/1440/1920 kesitleri.
2. Lighthouse mobil raporu: Performance ve Accessibility puanları; SEO/En iyi uygulamalar ayrı.
3. DevTools Performance trace'i: uzun görev ve kare düşmesi kontrolü.
4. Konsol listesi: sıfır hata/uyarı (bilinçli uyarılar gerekçeli).
5. Kontrast ve hedef boyutu ölçümleri; klavye turu notu.
6. Metin taraması: yasak kalıp eşleşmeleri ve insan editör onayı.
7. Yayın smoke çıktısı: HTTP durum kodları, canlı URL, form testi.

## 8. Durdurucu koşullar

- Uydurma iddia, sahte referans veya sahte form başarısı.
- Erişilebilirlik tabanının ihlali; reduced-motion final durumunun yokluğu.
- Bütçe aşımı veya konsol hatası; kırık görsel/video.
- Onaysız metin değişikliği; design package ile çelişen build.
- Gerçek cihaz/alan verisi kanıtı olmadan "doğrulandı" beyanı.
