---
name: sp-dizayn-web-site
description: "Herkese açık web siteleri için en üst seviye tasarım ve üretim orkestrasyonu: ziyaretçinin işi, sanat yönü, insan dili metin, görsel/video/ses üretimi, sinematik kaydırma, site.css zero-build uygulaması ve ölçülebilir kalite kapıları. Şu durumlarda kullan: tanıtım/kurumsal/landing sitesi tasarlama veya yeniden tasarlama, sinematik deneyim, site metni ve medya üretimi. Kullanma: panel/SPA/Rust masaüstü, yalnız mimari veya veri işi, yalnız estetik dil tarifi (sp-zen-dizayn)."
version: "v202610300600"
---

# sp-dizayn-web-site

Herkese açık bir sitenin tasarım ve üretim sözleşmesi. Hedef şablon değil, bu markaya ait bir deneyimdir: ziyaretçinin işini yapan, tek dünyası ve tek imzası olan, insan diliyle yazılmış, ölçülebilir biçimde hızlı ve erişilebilir bir site.

## 0. Ortak çalışma ilkeleri (kaynak: AGENTS-tr; bilinçli kopya)

0.1. Öncelik: kullanıcı talimatı > AGENTS-tr > bu beceri > model bilgisi.
0.2. Mod: varsayılan geliştirme; release/prod kapıları yalnız risk sınıfı veya açık yayın isteğiyle yüklenir.
0.3. Değişmezler: güvenlik, erişilebilirlik, veri bütünlüğü, sır yönetimi ve Türkçe imlâ her modda korunur.
0.4. Bilgi: sürüm, API ve araç davranışı varsayılmaz; çalışma anında context7 veya resmî kaynaktan doğrulanır; doğrulanamayan "doğrulanmalı" etiketiyle verilir.
0.5. Araç: işe göre seçilir, gerektiğinde hibrit kullanılır; erişim hatasında tanı, basit çözüm, çözülemezse işe başlamadan bildir (sp-sozlesme 1.3, 2.2, §4).
0.6. Kanıt: kanıtsız "tamamlandı" yoktur; kabul kapıları yalnız release veya risk tetiklediğinde yüklenir.

## 1. Amaç ve sınır

1.1. En üst seviye; özgün sanat yönü, gerçek malzeme, net hiyerarşi, insan metni ve sağlam mühendisliğin birleşimidir; efekt veya süs miktarı değildir.
1.2. Site mimarisi, barındırma, SEO altyapısı ve release kapıları sp-mimari-web-site alanındadır; bu beceri tasarım, içerik ve üretim orkestrasyonunu yönetir.
1.3. Panel/SPA ve Rust masaüstü ayrı becerilerdedir; yalnız estetik dil tarifi sp-zen-dizayn, yapısal uygulama arayüzü sp-dizayn-web-uygulama alanındadır.
1.4. Performans, erişilebilirlik ve gerçek içerik tabandır; sanat gerekçesi bu tabanı esnetmez.
1.5. Üretimde zero-build: tek `assets/css/site.css`, `:root` tokenları, Node/CDN yok; görsel, video ve ses offline üretilip statik varlık olarak teslim edilir.

## 2. Keşif (tasarımdan önce)

2.1. Ziyaretçinin işi tek cümleyle yazılır: seçmek, güvenmek, hissetmek, anlamak veya işi görmek. Bölüm sırası bu cümleden türer.
2.2. Ham malzeme toplanır: gerçek başlık/metin, logo, fotoğraf/video, ölçülebilir iddialar, marka tonu ve mevcut sitenin baseline'ı. Eksik malzeme varsayımı tek satırda yazılır; lorem ipsum ve uydurma içerik yasaktır.
2.3. Referans araştırması yapılır: üç-beş site, neyin neden işe yaradığı ilke olarak çıkarılır; kompozisyon kopyalanmaz.
2.4. Ortam keşfedilir: görsel/video/ses/3B üretimi, tarayıcı doğrulaması ve ölçüm için hangi beceri ve araçlar gerçekten kullanılabilir; varsayılmaz, denenir.
2.5. Gerçek olmayan referans, sahte metrik, uydurma yorum ve marka dışı iddia kullanılamaz; örnek marka açıkça işaretlenir.

## 3. Sanat yönü ve kompozisyon

3.1. Tek dünya: palet, tipografi, ışık, malzeme ve hareket aynı kaynaktan türetilir; sayfa ve hero aynı yerde geçiyormuş gibi okunur.
3.2. Tek imza, tek zirve, tasarlanmış kapanış: bu sitede başka yerde olmayan bir öğe; en iyi görselin/alanın ayrıldığı tek an; son ekranın CTA ve marka sesiyle kapanışı.
3.3. Kompozisyon stüdyo gibi kurulur: ölçek ve yoğunluk ritmi, asimetri, örtüşme, tam bleed ve nefes; komşu bölümlerin işi farklıdır, aynı iskelet tekrarlanmaz.
3.4. Tipografi: karakterli display yüzü + sakin gövde; keyfi veya varsayılan display fontu yok; gerçek font dosyaları; başlık/gövde ölçeği ve satır uzunluğu okunabilir.
3.5. Renk rolleri tokenla tanımlanır (zemin, yüzey, metin, ikincil metin, çizgi, tek vurgu); vurgu nadirdir, ham hex kullanılmaz.
3.6. Görsel amaçlıdır: hero kırpıntısı filler değildir; tutarlı kimlik, ışık ve malzeme taşıyan ayrı sahneler üretilir.
3.7. Makine yapımı görünen kalıplardan kaçınılır: aynı ikonlu kart ızgarası, her bölümde numara, gradient başlık, sahte sosyal kanıt, emoji ikon, her yerde cam kart, her şeyin ortalanması.

## 4. Üretim hattı

4.1. Sıra: brief ve malzeme → araştırma → iki-üç gerçekten farklı konsept → design package → erken görsel treatment → metin → medya üretimi → build → QA → yayın.
4.2. Design package tek yaşayan belgedir: ziyaretçi işi, cümleyle yazılmış bölüm listesi, imza, palet tokenları, tipografi, hero/film planı, alt bölüm outline'ı, birebir metinler ve kabul kanıtı.
4.3. Erken görsel treatment hero, temsili bir alt bölüm ve telefon görünümünü gerçek tipografi ve hareketle gösterir; onaylanmadan geniş medya üretimine geçilmez.
4.4. Onaylar taşınır; yön veya kapsam maddi olarak değişirse yeni onay alınır.

## 5. Metin: insan dili, AI slop değil

5.1. Metin ayrı bir iş akışıdır: ayrı subagent ve insan editör geçişi; build metni yeniden yazmaz, birebir bağlar.
5.2. Araştırmadaki alıcı diliyle, marka sesinde yazılır; satırlar bir kaydırma lokması boyundadır; tek CTA en fazla üç kez ve aynı ifadeyle tekrarlanır.
5.3. Stok AI kalıpları yasaktır: "sadece X değil, aynı zamanda Y", "günümüzün hızlı dünyasında", "kusursuz deneyim", "yenilikçi çözümler", "tutkuyla", "sınırları zorlamak"; İngilizce karşılıkları ve tam listesi references/metin-insan-dili.md dosyasındadır.
5.4. Her iddia kanıtlıdır: gerçek sayı, isim, mekan, süre veya müşteri; uydurma referans ve metrik yoktur.
5.5. Türkçe imlâ tamdır; form etiketleri, hata/başarı mesajları ve mikro metin de insan dilidir.
5.6. Editör geçişi: sesli oku, gereksiz sıfatı kes, somutlaştır, kalıbı sil; yapay kokan her cümle yeniden yazılır.

## 6. Medya ve hareket

6.1. Üretimden önce yetenek keşfi yapılır; araç yoksa CSS, SVG, tipografi ve gradient ile onurlu fallback kurulur.
6.2. Görsel üretimi: tutarlı kimlik referansı, tek dünya, ayrı kompozisyonlar; hero için rest/open/event kareleri; telefon için ayrı kompozisyon.
6.3. Video: tek kontrollü çekim, sessiz master, poster son kare, mobil için ayrı çekim; web için encode edilir, gerekirse kare dizisi.
6.4. Ses: varsayılan sessiz, kullanıcı kontrolünde; telifsiz veya üretilmiş; ani yüksek ses yok, mix ölçülür.
6.5. 3B/WebGL yalnız anlatı gerektiriyorsa kullanılır; fallback, tek rAF, dispose ve gizli sekmede durma zorunludur.
6.6. Hareket amaçlıdır: iki easing tokenı, yalnız transform/opacity, reduced-motion'da final durum, gizli sekmede durma.
6.7. Sinematik hero varsa tipografi film kuyruklarına bağlanır; statik hero metni ayrı yazılır; telefon koreografisi ayrı kurulur; keyfi giriş animasyonu sinematik sayılmaz.

## 7. Araç ve ortam adaptasyonu

7.1. Önce envanter: kullanılabilir beceriler, MCP sunucuları ve proje araç zinciri; her aracın ne yaptığı ve çağrılabilirliği doğrulanır.
7.2. Hibrit kullan: örneğin görsel üretimi + tarayıcı doğrulaması + encode/optimizasyon ayrı araçlarla yapılabilir; tek araç varsayılmaz.
7.3. Araç erişimi başarısızsa nedenini teşhis et (izin, kurulum, ağ, sürüm, yol), basit çözümü uygula; çözülemezse işe başlamadan kullanıcıya bildir.
7.4. Ücretli araç, API anahtarı ve dış servis varsayılmaz; kullanıcı onayı olmadan harcama yapılmaz.
7.5. Sürüm/API davranışı beceriye gömülmez; context7 veya resmî kaynaktan doğrulanır.

## 8. Orkestrasyon: her şeyi tek başına yapma

8.1. Lead işi beş iş akışına böler: araştırma/sanat yönü, metin, medya üretimi, build ve QA. Bağımsız işler paralel, bağımlı işler sıralı yürür.
8.2. Her subagent tek kapsam, net girdi artefaktı, net çıktı artefaktı, yazma kapsamı ve kabul ölçütü alır.
8.3. Aynı dosyaya iki subagent yazmaz; Lead entegre eder, kapıları kendisi çalıştırır ve görsel/teknik kanıtı kendi görür.
8.4. Subagent raporu kanıt yerine geçmez; her teslim ekran görüntüsü, ölçüm veya çalışan önizleme ile doğrulanır.

## 9. Mod ve teslim

9.1. Geliştirme: hızlı statik önizleme, görsel keşif ve hızlı düzeltme; her mikro değişiklikte build veya tam kapı yok.
9.2. Release: cilalı görsel treatment, gerçek içerik, perf/SEO/a11y/varlık kapıları ve gerçek cihaz/emülasyon kontrolü.
9.3. Runtime zero-build'dir: tek site.css, kökte tokenlar, 4px barem, Iconify lucide, harici font CDN'i yok; medya self-host ve optimize edilir.
9.4. Baseline: URL'ler 200, konsol sıfır, form doğru çalışır, meta/canonical/OG gerçek, kırık görsel yok.

## 10. Kabul ve references

10.1. Sekiz puanlı kalite değerlendirmesi (bakış açısı, tipografi, renk, hiyerarşi, görseller, hareket, mobil, cila) ve teknik kapılar references/kabul-kapilari.md dosyasındadır.
10.2. Referanslar tetiklendiğinde okunur: references/sanat-yonu.md, references/metin-insan-dili.md, references/medya-uretim.md, references/arac-ortam.md, references/orkestrasyon.md, references/kabul-kapilari.md.
10.3. Bitiş koşulu: tasarım package'ı uygulanmış, metin insan editöründen geçmiş, medya varlıkları yerinde, kapılar kanıtlı ve site mobil/masaüstünde gerçekten çalışıyor.
