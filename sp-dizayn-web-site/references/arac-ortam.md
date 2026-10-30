# Araç Zinciri ve Ortam — beceri eşlemesi, keşif ve kanıt

> sp-dizayn-web-site eki; gövde 7 ve 8'in ayrıntısıdır. Hangi işin hangi beceri veya MCP ile yapılacağını, kanıtı ve erişim hatasında ne yapılacağını tanımlar.
> Kural: araç adı ve doğrulama hedefi yazılır; çağrı protokolü/parametre yazılmaz. Her araç runtime'da keşfedilir; gömülü envanter karar dayanağı değildir; onaysız harcama yapılmaz.

## 1. Keşif ve doğrulama

1.1. Üç kanıt katmanı: katalogda ad, fiziksel dizinde SKILL.md, canlı çağrıda yanıt. Üçü tamamlanmadan araç var sayılmaz.
1.2. Keşif sırası: beceri kataloğu → beceri dizinleri → MCP listesi ve tek canlı çağrı → PATH araçları → proje araç zinciri.
1.3. MCP bağlantısı canlı çağrıyla sınanır; hedef uygulama kapalıysa araç kullanılamaz. Yerel araç için sürüm veya zararsız bir örnek çalıştırılır.
1.4. Envanter satırı: ihtiyaç, aday, çağrı yolu, kanıt türü, yedek ve tarih. Kanıtsız satır "doğrulanmalı" taşır; iş başında tazelenir.

## 2. Aşama → beceri eşlemesi

Tablodaki adlar kurulu beceriler ve bağlanabilir MCP'lerdir; çağrı biçimi runtime'dadır. Bir satırda birden fazla ad varsa sıra öneridir, hepsi birden çağrılmaz.

| Aşama | Birincil | Ne zaman / sınır | Çıktı ve kanıt |
| --- | --- | --- | --- |
| Brief ve niyet | brainstorming, sp-sozlesme, research | Kapsam belirsiz, yeni/yeniden tasarım, çok adımlı iş | Onaylı brief, karar notu |
| Sanat yönü | design-taste-frontend, frontend-design, hallmark, ui-ux-pro-max, awesome-design-md, brand-intake, design-system, sp-zen-dizayn | Yeni sayfa, AI-slop kırma, token sistemi, marka dili, Apple-klasik | Yön sheet, design package, ekran |
| Denetim ve cila | impeccable, emil-design-eng, break-ui | İlk build sonrası denetim, cila, mikro etkileşim, en kötü veri | Puan, bulgu, düzeltme |
| Metin | brand, insan editör | Ses/ton; ayrı copy becerisi yok | Copy deck, editör kanıtı |
| Motion ve scroll | animate, motion-design-principles, apple-design, gsap-core, gsap-scrolltrigger, gsap-timeline, gsap-plugins, gsap-utils, gsap-performance, animation-performance | Karar, ilke, jest, scroll/timeline, jank | Motion spec, trace, ekran |
| 3B ve WebGL | title-sequence-3d, img2threejs, web-sims, blender MCP, threejs-devtools-mcp | Başlık sekansı, model, simülasyon, varlık, canlı inceleme | Sahne, GLB, ekran, trace |
| Sinematik site | 10k-websites, prototype | Uçtan uca kare dizisi/video/depth motoru; yerleşim denemesi | Engine kopyası, önizleme |
| Video ve ses | hyperframes, remotion-best-practices, media-use, sound-design, sound-effects, ffmpeg/Pillow | Site dışı offline medya, encode, poster, mix | MP4, WebP, poster, ölçüm |
| QA | chrome-devtools, a11y-debugging, debug-optimize-lcp, mobile-native, verification-before-completion | DOM/konsol/ağ/trace, a11y, LCP, mobil, kapanış | Rapor, ekran, ölçüm |
| Mimari ve yayın | sp-mimari-web-site | Barındırma, SEO, form, bütçe, release | Mimari karar, canlı smoke |
| Meta ve hafıza | writing-for-agents, writing-skills, mem-search | Kural/beceri düzenleme, geçmiş karar | Belge, kayıt kimliği |

## 3. Sanat yönü: öncelik ve çakışma

3.1. Brief markayı, paleti veya tipografiyi sabitliyorsa önce o uygulanır; design-taste-frontend yalnız kompozisyon verir ve marka değerlerini korur.
3.2. Yeni sayfada tam yön: design-taste-frontend ana; frontend-design konsept dili; hallmark yalnız yeni sayfa veya adı geçtiğinde; ui-ux-pro-max yalnız veri araması; design-system yalnız token/bileşen sözleşmesi.
3.3. impeccable ilk build'den sonra denetim, cila, audit, polish ve overdrive için; yönü tek başına kurmaz. overdrive, animate ve delight belgelenmiş komutlardır, "gizli" değildir; sinematik mimarinin yerine geçmez.
3.4. sp-zen-dizayn yalnız Apple klasik estetiği açıkça istenirse yüklenir. Aynı sayfada iki yön sahibi olmaz; çakışmada design package ve kullanıcı onayı üstündür.

## 4. Motion ve 3B: sıra

4.1. Sıra: animate (karar) → motion-design-principles (12 ilke) veya apple-design (his) → gsap-* ya da vanilya (uygulama) → animation-performance/gsap-performance (jank) → chrome-devtools (kanıt).
4.2. GSAP API ve parametreleri gsap-* becerisinden veya context7'den doğrulanır; bu dosya kod örneği taşımaz.
4.3. title-sequence-3d video başlık sekansı, img2threejs referanstan model, web-sims simülasyon videosu içindir; blender MCP yalnız bağlıysa varlık üretir; threejs-devtools-mcp bağlı değilse chrome-devtools ekran/trace ile yetinilir.
4.4. Sinematik karar ve mimari references/sinematik-katman.md dosyasındadır; burada yalnız araç seçimi vardır.

## 5. MCP sunucuları

| Sunucu | Ne işe yarar | Kanıt | Sınır |
| --- | --- | --- | --- |
| chrome-devtools | DOM, konsol, ağ, ekran, trace, Lighthouse | Canlı çıktı, ölçüm | Bağlı değilse manuel tarayıcı |
| blender | 3B sahne ve varlık üretimi/incelemesi | Sahne, ekran | Uygulama ve eklenti açık değilse kullanılamaz |
| context7 | Kütüphane API ve sürüm doğrulaması | Kaynak snippet | Resmî doküman önceliklidir |
| codegraph / gitnexus | Kod yapısı, etki, süreç | Sembol, risk | Yalnız site kodu varsa |
| markitdown | Ofis/ikili belgeyi Markdown'a çevirme | Dönüşüm | Medya üretmez |
| sequential-thinking | Karmaşık karar ve plan | Karar kaydı | Kanıt değil, akıl yürütme yardımı |

## 6. Harici ve opsiyonel MCP/platformlar

6.1. Spline MCP 3B sahneyi, Framer MCP sayfa/animasyon/CMS'i ajan üzerinden düzenler; resmî uç nokta, hesap ve OAuth ister. Bağlı değilse yalnız manuel sahne/sayfa ve export yöntemi kullanılır.
6.2. threejs-devtools-mcp canlı Three.js sahnesini inceler; Three.js Resources MCP sürüm doğrulanmış rehber ve shader dönüşümü sunar; ikisi de runtime'da sınanır.
6.3. Üçüncü taraf WebSocket tabanlı 3B MCP'ler yalnız kaynak deposu ve lisansı doğrulandıktan sonra değerlendirilir; paket/dağıtım adı doğrulanmadan kurulmaz.
6.4. Spline + Framer gibi no-code yollar ayrı teslim modelidir, zero-build kapsamına girmez; MotionSites/Scrollytelling gibi şablon platformlar yalnız ilham kaynağıdır ve iddiaları doğrulanmadan kullanılmaz.
6.5. Harici MCP bağlı değilse "bağlı" sayılmaz; yalnız yöntem ve manuel adım yazılır. Kurulum, hesap ve ücret onay ister; çağrı mekaniği bu dosyaya yazılmaz.

## 7. Erişim hatasında tanı

7.1. Tanı sırası: hedef uygulama/sunucu kapalı mı, bağımlılık eksik mi, ağ mı, yetki/hesap mı, yol veya sürüm uyumsuz mu. Şıklar tek tek ayrılır.
7.2. Basit çözüm: uygulamayı aç, yalnız gerekli bağımlılığı kur, yerel veya offline alternatife geç. Ücretli hesap zorlanmaz.
7.3. Tarayıcı MCP'si bağlanmıyorsa tarayıcı açılır; 3B MCP'si için uygulama ve eklenti açılır. Açılmıyorsa manuel doğrulama yapılır ve "doğrulanmalı" işaretlenir; çözülemeyen erişimde işe başlamadan kullanıcıya bildirilir (sp-sozlesme 1.3, 2.2, §4).

## 8. Hibrit kullanım ve bütçe

8.1. Görsel hattı: yön becerisiyle kompozisyon, varlığın kullanıcıdan veya açık lisans arşivinden temini, ffmpeg/Pillow ile optimize, chrome-devtools ile sayfada doğrulama.
8.2. Hareket hattı: kod tabanlı üretim veya kullanıcı videosu, ffmpeg ile encode ve poster, tarayıcıda oynatma, seek ve reduced-motion kontrolü.
8.3. QA hattı: chrome-devtools ile ekran, konsol ve ağ; Lighthouse veya a11y denetimi; metin ve imlâ taraması; ölçüm kaydı. Tek araç tam kabul üretmez.
8.4. Zero-build sınırı: hiçbir araç siteye Node bağımlılığı, CDN kütüphanesi veya ikinci stil dosyası sokamaz; araç çıktısı assets/ altında statik varlığa dönüşür. Sinematik istisna proje kaydında onaylanır; JS/GPU bütçesi sp-mimari-web-site alanındadır, bu beceri bütçeyi kendisi değiştirmez.

## 9. Ücret, lisans, güncellik

9.1. Ücretli araç, API anahtarı, kredi ve harici hesap varsayılmaz; onaysız harcama yapılmaz.
9.2. Yalnız kendi varlığı veya açık lisanslı malzeme kullanılır; atıf zorunluysa görünür yerde verilir. Lisansı doğrulanamayan medya yayınlanmaz.
9.3. Üçüncü taraf kütüphane, motor, model ve doku lisansı çalışma anında resmî kaynaktan doğrulanır; proje kaydına yazılır.
9.4. Sürüm, API ve araç davranışı bu dosyaya gömülmez; context7 veya resmî kaynakla doğrulanır. Gerçek fotoğraf ve video yalnız sahibinin izniyle işlenir.

## 10. Anti-desenler

| Anti-desen | Neden kötü | Doğrusu |
| --- | --- | --- |
| Her aracı çağırmak | Bağlam şişer, çelişkili çıktı doğar | İşe uyan tek sahip; sıra ve kanıt |
| Araç çıktısını kanıt saymak | Doğrulanmamış teslim | Ekran, ölçüm, komut çıktısı |
| Aynı işi iki beceriye vermek | Çift yön, çift kapı | Tek sahip, design package |
| Harici MCP'yi bağlı saymak | Kurulum/hesap yok, sahte yetenek | Bağlantı sınaması; yoksa manuel yöntem |
| Lisanssız kütüphane/model kopyalamak | Hukuki ve bakım riski | Lisans doğrula, kayda geçir |
