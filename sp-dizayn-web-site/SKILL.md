---
name: sp-dizayn-web-site
description: "Şu durumlarda kullan: herkese açık tanıtım, kurumsal, landing veya portfolyo sitesi tasarlama/yeniden tasarlama; Awwwards tarzı sinematik scroll, scrollytelling, kare dizisi veya WebGL sahne; site metni, görsel/video/ses üretimi; tasarım denetimi ve cilası. Kullanma: panel/SPA/Rust masaüstü, yalnız mimari veya veri işi, yalnız estetik dil tarifi (sp-zen-dizayn)."
version: "v202610302324"
---

# sp-dizayn-web-site

Herkese açık bir sitenin tasarım ve üretim sözleşmesi: ziyaretçinin işini yapan, tek dünyası ve tek imzası olan, insan diliyle yazılmış, ölçülebilir biçimde hızlı ve erişilebilir bir site.

## 0. Disiplin

0.1. Öncelik: kullanıcı talimatı > AGENTS-tr > bu beceri > model bilgisi.
0.2. Beceri disiplini: işe uyan beceri yüklenmeden uygulamaya geçilmez (using-superpowers); süreç önce: brainstorming (niyet/onay), writing-plans (çok adım), verification-before-completion (kapanış). Her yükleme tek satırda beyan edilir.
0.3. Değişmezler: güvenlik, erişilebilirlik, veri bütünlüğü, sır ve Türkçe imlâ.
0.4. Bilgi: sürüm/API/araç davranışı varsayılmaz; context7 veya resmî kaynak; doğrulanamayan "doğrulanmalı".
0.5. Kanıt: tasarım puanı, teknik skor, ekran ve ölçüm ayrıdır; kanıtsız "tamamlandı" yoktur.

## 1. Sınır ve teslim modeli

1.1. En üst seviye; özgün sanat yönü, gerçek malzeme, net hiyerarşi, insan metni ve sağlam mühendisliğin birleşimidir; efekt veya süs miktarı değildir.
1.2. Site mimarisi, barındırma, SEO altyapısı, JS/GPU bütçesi ve release kapıları sp-mimari-web-site alanındadır; bu beceri tasarım, içerik, medya ve sinematik deneyimin üretim orkestrasyonunu yönetir.
1.3. Panel/SPA ve Rust masaüstü ayrı becerilerdedir; yalnız estetik dil sp-zen-dizayn, yapısal uygulama arayüzü sp-dizayn-web-uygulama alanındadır.
1.4. Performans, erişilebilirlik ve gerçek içerik tabandır; sanat gerekçesi bu tabanı esnetmez.
1.5. Varsayılan teslim zero-build'dir: tek assets/css/site.css, :root tokenları, çalışma anında Node/CDN yok; görsel, video, ses ve 3B varlıklar çevrimdışı üretilip statik teslim edilir.
1.6. Sinematik istisna kapılıdır: yalnız anlatı gerektiriyorsa ve proje kaydında onaylıysa self-host GSAP/ScrollTrigger, Lenis ve gerekirse Three.js kullanılabilir; CDN yok, ayrı JS/GPU bütçesi, üç durumlu fallback ve reduced-motion zorunludur. Bütçe istisnası sp-mimari-web-site'ta proje bazlı onayla açılır (references/sinematik-katman.md).

## 2. Keşif

2.1. Ziyaretçinin işi tek cümleyle yazılır: seçmek, güvenmek, hissetmek, anlamak veya işi görmek. Bölüm sırası bu cümleden türer.
2.2. Ham malzeme toplanır: gerçek metin, logo, fotoğraf/video, ölçülebilir iddialar, marka tonu ve mevcut site baseline'ı. Eksik malzeme varsayımı tek satırda yazılır; lorem ipsum ve uydurma içerik yasaktır.
2.3. Üç-beş referans incelenir, ilke çıkarılır; kompozisyon kopyalanmaz, erişilemeyen site referans sayılmaz.
2.4. Ortam keşfedilir: kullanılabilir beceri, MCP ve yerel araçlar denenir; envanter references/arac-ortam.md dosyasındadır.
2.5. Gerçek olmayan referans, sahte metrik, uydurma yorum ve marka dışı iddia kullanılamaz; örnek marka açıkça işaretlenir.

## 3. Sanat yönü ve kompozisyon

3.1. Tek dünya: palet, tipografi, ışık, malzeme, ses ve hareket öznenin kendi dünyasından türetilir; sayfa ve hero aynı yerde geçiyormuş gibi okunur.
3.2. Tek imza, tek zirve, tasarlanmış kapanış: yalnız bu sitede olan bir öğe; en iyi görselin ayrıldığı tek an; son ekranın CTA ve marka sesiyle kapanışı.
3.3. Kompozisyon stüdyo gibi kurulur: ölçek ve yoğunluk ritmi, asimetri, örtüşme, tam bleed ve nefes; komşu bölümlerin işi farklıdır, aynı iskelet tekrarlanmaz.
3.4. Tipografi: karakterli display yüzü ve sakin gövde; varsayılan sistem yüzü display olarak kullanılmaz; gerçek font dosyaları teslim edilir; ölçek ve satır uzunluğu okunabilir.
3.5. Renk rolleri tokenla tanımlanır (zemin, yüzey, metin, ikincil metin, çizgi, tek vurgu); vurgu nadirdir, ham hex kullanılmaz, kontrast ölçülür.
3.6. Görsel amaçlıdır: hero kırpıntısı filler değildir; tutarlı kimlik, ışık ve malzeme taşıyan ayrı sahneler üretilir.
3.7. Makine yapımı kalıplardan kaçınılır: aynı ikonlu kart ızgarası, her bölümde numara, gradient başlık, sahte sosyal kanıt, emoji ikon, her yerde cam kart, her şeyin ortalanması.

## 4. Üretim hattı ve tasarım paketi

4.1. Sıra: brief ve malzeme → araştırma → iki-üç gerçekten farklı konsept → design package → erken görsel treatment → metin → medya → build → QA → yayın.
4.2. Design package tek yaşayan belgedir: ziyaretçi işi, cümleyle bölüm listesi, imza, palet tokenları, tipografi, hero/film planı, alt bölüm outline'ı, birebir metinler, sinematik mod/bütçe/fallback ve kabul kanıtı.
4.3. Erken treatment hero, temsili bir alt bölüm ve telefon görünümünü gerçek tipografi ve hareketle gösterir; onaylanmadan geniş medya üretimine geçilmez.
4.4. Onaylar taşınır; yön veya kapsam maddi olarak değişirse yeni onay alınır.

## 5. Metin

5.1. Metin ayrı akıştır: ayrı subagent ve insan editör geçişi; build metni yeniden yazmaz, birebir bağlar.
5.2. Alıcı dili ve marka sesiyle yazılır; satırlar bir kaydırma lokması boyundadır; tek CTA en fazla üç kez aynı ifadeyle görünür.
5.3. Stok AI kalıpları yasaktır; tam liste references/metin-insan-dili.md dosyasındadır.
5.4. Her iddia kanıtlıdır: gerçek sayı, isim, mekân, süre veya müşteri; uydurma referans ve metrik yoktur.
5.5. Türkçe imlâ tamdır; form etiketleri, hata/başarı mesajları ve mikro metin de insan dilidir.

## 6. Medya, hareket ve sinematik katman

6.1. Üretimden önce yetenek keşfi yapılır; araç yoksa CSS, SVG, tipografi ve gradient ile onurlu fallback kurulur.
6.2. Görsel: tutarlı kimlik referansı, tek dünya, ayrı kompozisyonlar; hero için rest/open/event kareleri; telefon için ayrı kompozisyon.
6.3. Video: tek kontrollü çekim, sessiz master, poster son kare, mobil için ayrı çekim; web için encode edilir, gerekirse kare dizisi kullanılır.
6.4. Ses: varsayılan sessiz, kullanıcı kontrolünde; telifsiz veya üretilmiş; ani yüksek ses yok, mix ölçülür.
6.5. Sinematik katman varsayılan değildir; üç koşul (anlatı, anlaşılırlık, 60 fps/fallback) evet değilse açılmaz. Mod, süre, varlık, bütçe, fallback ve mobil koreografi design package'a yazılır (references/sinematik-katman.md).
6.6. 3B/WebGL yalnız anlatı gerektiriyorsa kullanılır; tek canvas, tek rAF, dispose, bağlam kaybı yönetimi, gizli sekmede durma ve statik fallback zorunludur.
6.7. Hareket amaçlıdır: iki easing tokenı, yalnız transform/opacity, reduced-motion'da final durum, gizli sekmede durma; scroll-jacking yok.
6.8. Sinematik hero varsa tipografi film kuyruklarına bağlanır; statik hero metni ayrı yazılır; telefon koreografisi ayrı kurulur; keyfi giriş animasyonu sinematik sayılmaz.

## 7. Araç zinciri

7.1. Beceri envanteri ve aşama eşlemesi references/arac-ortam.md dosyasındadır; her araç çağrılabilirlik ve kanıt hedefiyle doğrulanır.
7.2. Tek sahip: aynı iş iki beceriye verilmez; sıra süreç becerisi → yön → hareket → uygulama → doğrulama.
7.3. Hibrit: yön, medya, encode ve tarayıcı doğrulaması ayrı araçlarla; birinin çıktısı diğerinin kanıtı değildir.
7.4. Erişim hatasında tanı, basit çözüm, çözülemezse başlamadan bildirim.
7.5. Ücretli araç/anahtar/dış servis varsayılmaz; onaysız harcama yok; sürüm/API runtime'da doğrulanır.

## 8. Orkestrasyon

8.1. Lead işi altı akışa böler: sanat/keşif, metin, medya, build, QA ve yayın. Bağımsız işler paralel, bağımlı işler sıralı yürür.
8.2. Her subagent tek kapsam, net girdi, net çıktı, yazma kapsamı ve kabul ölçütü alır.
8.3. Aynı dosyaya iki subagent yazmaz; Lead entegre eder, kapıları çalıştırır ve kanıtı kendi görür.
8.4. Subagent raporu kanıt yerine geçmez; teslim ekran görüntüsü, ölçüm veya çalışan önizleme ile doğrulanır.

## 9. Mod ve teslim

9.1. Geliştirme: hızlı statik önizleme, görsel keşif ve hızlı düzeltme; her mikro değişiklikte tam kapı yok.
9.2. Release: cilalı treatment, gerçek içerik, perf/SEO/a11y/sinematik kapıları ve gerçek cihaz/emülasyon kontrolü.
9.3. Runtime zero-build'dir: tek site.css, kökte tokenlar, 4px barem, harici font CDN'i yok; ikonlar inline SVG veya self-host sprite; medya self-host ve optimize edilir.
9.4. Sinematik istisna yalnız onaylı proje kaydında ve gerekli sayfalarda açılır; bütçe, lisans, fallback ve geri alma yazılıdır.
9.5. Baseline: URL'ler 200, konsol sıfır, form doğru çalışır, meta/canonical/OG gerçek, kırık görsel yok.

## 10. Kabul ve references

10.1. Sekiz puanlı kalite değerlendirmesi (bakış açısı, tipografi, renk, hiyerarşi, görseller, hareket, mobil, cila) ve teknik kapılar references/kabul-kapilari.md dosyasındadır.
10.2. Referanslar tetiklendiğinde tam okunur: sanat-yonu, metin-insan-dili, medya-uretim, sinematik-katman, arac-ortam, orkestrasyon, kabul-kapilari.
10.3. Bitiş koşulu: tasarım paketi uygulanmış, metin editörden geçmiş, medya yerinde, sinematik varsa fallback ve performans kanıtlı, kapılar kanıtlı ve site mobil/masaüstünde çalışıyor.
