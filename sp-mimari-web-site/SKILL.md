---
name: sp-mimari-web-site
description: "Statik ve SEO odaklı tanıtım sitelerinin mimarisini tanımlar; barındırma, PHP ortak parçalar, elle yazılmış site.css, varlık ve JS bütçesi, SEO/indeksleme, lead formu güvenliği, opsiyonel MySQL ve release kapılarını kapsar. Tanıtım/landing sitesi kurulumunda, SEO ve Core Web Vitals düzeninde, PHP form ucu ve lead saklamada, site yayına almada kullanılır. Oturumlu panel veya SCADA uygulamasında, yalnız görsel tasarım veya estetik dil talebinde, Rust masaüstünde kullanılmaz."
version: "v202610302324"
---

# sp-mimari-web-site

Herkese açık, oturumsuz, statik öncelikli tanıtım sitesinin mimarisi. Amaç hızlı, indekslenebilir ve güvenli bir site; panel, oturum ve uygulama kabuğu bu becerinin dışındadır.

## 0. Ortak çalışma ilkeleri (kaynak: AGENTS-tr; bilinçli kopya)

0.1. Öncelik: kullanıcının güncel yazılı talimatı > AGENTS-tr > bu beceri > model bilgisi.
0.2. Mod: varsayılan geliştirmedir; release/prod kapıları yalnız risk sınıfı veya açık yayın isteğiyle yüklenir.
0.3. Değişmezler: güvenlik, erişilebilirlik, veri bütünlüğü, sır yönetimi ve Türkçe imlâ her modda korunur.
0.4. Bilgi: sürüm, API ve davranış varsayılmaz; çalışma anında context7 veya resmî kaynaktan doğrulanır; doğrulanamayan "doğrulanmalı" etiketiyle verilir.
0.5. Araç: işe göre seçilir, gerektiğinde hibrit kullanılır; erişim hatasında tanı, basit çözüm, çözülemezse işe başlamadan bildir (sp-sozlesme 1.3, 2.2 ve §4).
0.6. Kanıt: kanıtsız "tamamlandı" yoktur; kabul kapıları yalnız release veya risk tetiklediğinde yüklenir.

## 1. Kapsam ve seçim

1.1. Kapsam: herkese açık, oturumsuz, SEO ve satış odaklı tanıtım siteleri; PHP yalnız ortak parça dahil etme ve form uçları için kullanılır.
1.2. Kapsam dışı: oturum, panel, SCADA, e-ticaret sepeti, SPA ve Node tabanlı derleme; bunlar ayrı beceri veya ayrı anayasa konusudur.
1.3. Varsayılan yığın: statik HTML + elle yazılmış site.css + küçük vanilla JS; veritabanı varsayılan olarak yoktur, yalnız form veya lead zorunluluğunda açılır.
1.4. Karar sırası: önce statik çözüm, sonra PHP include, en son form ve veritabanı; her ek katman gerekçelenir.
1.5. Yeni projede ilk adım kapsam ve sürüm doğrulamasıdır; pinlenen sürüm ve destek takvimi proje kaydına yazılır, doğrulanmamış sürüm kullanılmaz.
1.6. Gövde karar verir, ayrıntı referanstadır: yalnız ilgili referans dosyası tetiklendiğinde bütünüyle okunur.

## 2. Barındırma, statik önce ve varlık dizinleri

2.1. Site tek web kökünden yayınlanır; web kökü dışına çalışma zamanı dosyası yazılmaz. Yazılabilir tek alan veri/ ve log/ dizinleridir, ikisi de HTTP erişimine kapalıdır.
2.2. Dizin düzeni sabittir: assets/css/site.css tek stil kaynağı, assets/js/app.js, assets/img, assets/font, parcalar/, veri/, log/; ortak HTML parçaları yalnız include ile kullanılır.
2.3. Derleme yoktur: Node, bundler, PostCSS, CSS CDN'i ve serbest style bloğu kullanılmaz; stil tek dosyada elle yazılır, tasarım değerleri kökte CSS değişkeni olarak tanımlanır.
2.4. İçerik sayfaları sunucuda tam HTML olarak üretilir; ana içerik istemcide JavaScript ile oluşturulmaz ve JS kapalıyken metin ile bağlantılar okunabilir kalır.
2.5. Barındırıcı HTTPS, güncel HTTP sürümü, Brotli (yoksa gzip) ve önbellek başlıkları sunar; sürüm ve destek bilgisi çalışma anında barındırıcı belgesinden doğrulanır.
2.6. Önbellek: hash'li varlık uzun ömürlü ve immutable, HTML kısa ömürlüdür; form tokenı veya CSP nonce'u taşıyan HTML paylaşımlı önbelleğe alınmaz.
2.7. Dizin erişimi ve başlık kuralları .htaccess ile yapılandırılır; release'te doğrudan istek testiyle kanıtlanır.

## 3. JavaScript, font ve görsel bütçesi

3.1. JavaScript vanilla ve defer ile yüklenir; framework, SPA yönlendirici ve üçüncü taraf betik CDN'i yoktur. Tek istisna zorunlu ikon yükleyicisidir: sürüm sabitlenir, SRI eklenir, CSP kaynak listesine yazılır; sürüm ve SRI çalışma anında resmî kaynaktan doğrulanır.
3.2. Sayfa başına toplam JavaScript bütçesi 30 KB gzip'tir; bütçeyi aşan sürüm 3.2.1 istisnası olmadan kabul edilmez, ölçüm ağ panelindeki transfer toplamından alınır.
3.2.1. Sinematik istisna: sp-dizayn-web-site sinematik katmanı proje kaydında onaylıysa, yalnız ilgili sayfa için JS bütçesi proje kaydında ayrı tanımlanır. Varsayılan 30 KB ve CDN yasağı korunur; kütüphaneler self-host edilir, üçüncü taraf lisansı doğrulanır, fallback ve reduced-motion zorunludur. İstisna sayfa bazlıdır, site geneline yayılmaz.
3.3. Tipografi varsayılan olarak sistem font yığınıdır; marka fontu zorunluysa yalnız self-host woff2 alt kümesi kullanılır, en fazla iki dosya yüklenir, her dosya preload ve font-display swap taşır; harici font CDN'i ve @import yasaktır.
3.4. Görseller AVIF veya WebP sunulur, desteklemeyen tarayıcı için picture içinde geri dönüş biçimi bulunur; her img etiketinde width ve height zorunludur.
3.5. LCP görseli fetchpriority ve preload ile yüklenir; katlanma altı görseller lazy taşır. Hero video poster ile başlar, preload none, muted ve playsinline olur; mobilde statik görsel sunulur ve duraklatma denetimi bulunur.
3.6. Bütçe ölçümü geliştirmede ağ paneliyle yapılır; release eşiği ve CWV kanıtı kabul kapılarındadır (references/kabul-kapilari.md).
3.7. Varlık, barındırma ve bütçe ayrıntısı: references/varlik-ve-butce.md.

## 4. SEO ve indeksleme

4.1. Her sayfa semantik HTML ile sunulur; başlık hiyerarşisi atlanmaz, sayfada tam olarak bir h1 bulunur ve içerik sunucudan gelir.
4.2. Canonical, Open Graph, Twitter Card ve meta etiket seti tek ortak parçadan üretilir; sayfalarda elle çoğaltılmaz, zorunlu alanlar boş bırakılmaz.
4.3. JSON-LD zorunludur: Organization ve WebSite her sitede, BreadcrumbList iç sayfalarda, Product veya FAQPage yalnız uygun sayfalarda; uydurma veri yazılmaz.
4.4. robots.txt kökte bulunur ve sitemap adresini bildirir; sitemap.xml dağıtım sırasında üretilir, sürüm kontrolüne ve commit'e girmez.
4.5. Kalıcı adres değişikliği 301 haritasıyla yapılır; 302 ve zincirleme yönlendirme yoktur, çok dilli sitede hreflang karşılıklıdır.
4.6. SEO ayrıntısı ve doğrulama: references/seo.md.

## 5. Form, lead, e-posta, sır, log ve güvenlik başlıkları

5.1. Form yalnız amaca gerekli alanları toplar; özel nitelikli kişisel veri ve kart bilgisi tanıtım formunda toplanmaz, POST ile sunucu ucuna gönderilir, istemci doğrulaması sunucu doğrulamasının yerine geçmez.
5.2. Her form ucu CSRF belirteci, hız sınırı, honeypot ve sunucu tarafı alan doğrulaması içerir; hata mesajı Türkçe ve alanın yanındadır, iç ayrıntı istemciye sızmaz.
5.3. Sırlar yalnız .env veya secret manager'dadır; .env sürüm kontrolüne ve web erişimine kapalıdır, loglarda parola, token ve kişisel veri maskelenir, form gövdesi ve e-posta içeriği loglanmaz.
5.4. E-posta gönderimi SPF, DKIM ve DMARC ile kimlik doğrulanmış olur; gönderim veritabanı transaction'ı dışında ve commit sonrası yapılır.
5.5. Üretimde tüm HTML yanıtları CSP (nonce veya hash tabanlı), HSTS, nosniff, Referrer-Policy ve Permissions-Policy taşır; unsafe-inline ve unsafe-eval kullanılmaz, üretimde HTTPS zorunludur.
5.6. Lead verisi için amaç, hukuki sebep ve saklama süresi aydınlatma metninde belgelenir; süre sonunda kayıt silinir veya anonimleştirilir; veritabanı erişimi yalnız veri erişim katmanındandır.
5.7. Form güvenliği ayrıntısı: references/form-guvenlik.md; veri katmanı: references/veri-tabani.md.

## 6. Mod sözleşmesi (geliştirme / release)

6.1. Geliştirme varsayılandır: site.css elle yazılır, derleme yoktur, localhost HTTP üzerinde çalışılır ve her mikro değişiklikte build veya test çalıştırılmaz; doğrulama php -l ve tarayıcı kontrolüdür.
6.2. Geliştirmede form ucu iskeleti CSRF, honeypot ve sunucu doğrulamasıyla birlikte kurulur; gerçek gönderim testi zararsız test adresi ve test veritabanıyla yapılır.
6.3. Release/prod kapıları yalnız risk sınıfı veya açık yayın isteğiyle açılır; kapı listesi references/kabul-kapilari.md dosyasındadır.
6.4. Release kapsamı: HTTPS/HSTS, CSP ve SRI, gzip/Brotli bütçesi, lab CWV ölçümü ve varsa alan verisi, robots/sitemap, dizin erişim testi, yedek ve geri dönüş adımı, sürüm/API doğrulaması.
6.5. Yeni sitede alan verisi henüz yoktur: yayın öncesi lab ölçümü zorunlu, alan verisi yayın sonrası izlenir; eşiği aşan sürüm geri alınır.
6.6. Ortamlar ayrıdır: dev, staging ve prod farklı yapılandırma kullanır; prod'da debug kapalıdır ve hata sunucu loguna yazılır.
6.7. Sürüm damgası `vYYYYMMDDHHMM` biçimindedir: küçük v öneki ve on iki haneli yıl-ay-gün-saat-dakika; nokta, tire, alt çizgi, iki nokta ve boşluk kullanılmaz. Damga dağıtım betiğinde yayın anında bir kez üretilir, çalışma anında hesaplanmaz, elle yazılmaz ve düzeltilmez. Bilgi/hakkında sayfasındaki sürüm satırı, release kaydı ve aynı adlı tag birebir aynı değeri taşır; farklıysa yayın kabul edilmez.

## 7. Sınır ve referanslar

7.1. Sınır: panel ve oturum mimarisi, estetik dil ve görsel tasarım kuralları bu becerinin dışındadır; yalnız erişilebilirlik, Türkçe imlâ ve veri/güvenlik değişmezleri burada bağlayıcıdır. Sitenin yaratıcı yönü, metni ve medyası sp-dizayn-web-site alanındadır.
7.2. Referanslar tetiklendiğinde tam okunur: varlik-ve-butce (barındırma, dizin, bütçe, önbellek), seo (indeksleme, yapısal veri, sitemap), form-guvenlik (form, CSRF, e-posta, sır, başlıklar), veri-tabani (opsiyonel MySQL, göç, KVKK), kabul-kapilari (release kapıları).
7.3. Şüphede kalınan her sürüm, API veya davranış çalışma anında doğrulanır; doğrulanamayan bilgi "doğrulanmalı" etiketiyle teslim edilir.
7.4. Teslimde hangi referansların okunduğu ve hangi kapıların çalıştığı komut ve özet çıktıyla kanıtlanır.
