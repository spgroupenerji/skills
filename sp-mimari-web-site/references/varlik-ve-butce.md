# Varlık, Barındırma ve Bütçe

Bu dosya sp-mimari-web-site gövdesinin 2 ve 3. bölümlerini açar: dizin düzeni, erişim kuralları, statik önce ilkesi, stil/JS/font/görsel bütçesi, önbellek ve dağıtım. Sürüm, API ve barındırıcı davranışı varsayılmaz; her biri çalışma anında doğrulanır.

## 1. Barındırma ve ortam

1.1. Site tek web kökünden yayınlanır; çalışma zamanı dosyası kök dışına yazılmaz, yazılabilir alan yalnız veri/ ve log/ dizinleridir.
1.2. HTTPS zorunludur; HTTP isteği 301 ile HTTPS'e yönlendirilir, sertifika yenileme izlenir.
1.3. Sunucu güncel HTTP sürümünü ve Brotli (yoksa gzip) sıkıştırmayı sunar; destek ve yapılandırma anahtarları barındırıcı belgesinden doğrulanır.
1.4. PHP dalı proje kaydında sabitlenir; sürüm ve destek takvimi çalışma anında resmî kaynaktan doğrulanır; dinamik sürüm etiketi kullanılmaz.
1.5. PHP yalnız ortak parça include etme ve form uçları için kullanılır; framework, Composer ve ORM varsayılan değildir, gerekçesiz eklenmez.
1.6. Üretimde hata görüntüleme kapalıdır; hata ayrıntısı yalnız sunucu loguna yazılır, istemciye genel Türkçe mesaj döner.
1.7. Ortam değişkenleri ve sırlar .env veya secret manager'dan okunur; .env web kökünde değilse de erişime kapalıdır ve sürüm kontrolünde izlenmez.

## 2. Dizin düzeni ve erişim

2.1. Kök düzeni: index sayfaları, robots.txt, .htaccess, assets/, parcalar/, veri/, log/, .env.
2.2. assets/css/site.css tek stil kaynağıdır; assets/js/app.js, assets/img ve assets/font aynı düzenin parçasıdır.
2.3. parcalar/ yalnız include edilen PHP parçalarını taşır: head, meta, header, footer, form bileşenleri. Bu dizine doğrudan HTTP isteği yasaktır.
2.4. veri/ ve log/ web erişimine kapalıdır; .env, .sql, .md ve yedek dosyaları da doğrudan istenemez, dizin listeleme kapalıdır.
2.5. .htaccess ile en az şunlar yapılandırılır: dizin listeleme kapalı, dizinlerin doğrudan isteğine ret, HTTP'den HTTPS'e 301, sıkıştırma, varlık ve HTML önbellek başlıkları, güvenlik başlıkları için sunucu desteği.
2.6. Erişim kuralları release'te canlı istekle doğrulanır: parcalar/, veri/ ve log/ altındaki bir dosya 403 veya 404 dönmelidir.
2.7. .htaccess yalnız Apache/LiteSpeed uyumlu sunucuda etkilidir; farklı sunucuda eşdeğer yapılandırma proje kaydında yazılır.

## 3. Statik önce ve PHP kullanımı

3.1. İçerik sayfaları sunucuda tam HTML olarak üretilir; ana içerik JavaScript ile oluşturulmaz.
3.2. Ortak HTML parçaları include ile kullanılır; aynı meta, header veya footer sayfalara kopyalanmaz.
3.3. Etkileşim ihtiyacı önce HTML/CSS ile çözülür; gerekiyorsa küçük vanilla JS eklenir, SPA ve istemci tarafı yönlendirici kullanılmaz.
3.4. Veritabanı varsayılan olarak yoktur; yalnız form veya lead saklama zorunluluğunda açılır (references/veri-tabani.md).
3.5. Yeni bağımlılık eklenmeden önce standart kütüphane veya mevcut yardımcı aranır; zorunluysa gerekçe tek cümleyle yazılır.
3.6. Sayfa başına tek h1 ve semantik yapı korunur; erişilebilirlik değişmezdir, JS kapalıyken de temel içerik ve form etiketleri okunur.

## 4. Stil kaynağı

4.1. Stil tek dosyada, assets/css/site.css içinde elle yazılır; derleme adımı, PostCSS, CSS CDN'i, harici CSS ve @import yoktur.
4.2. Tasarım değerleri :root altında CSS değişkeni olarak tanımlanır; bileşenler bu değişkenleri okur, sayfa içinde dağınık ham değer bırakılmaz.
4.3. Kullanılmayan token ve ölü CSS kuralı release öncesi temizlenir; geliştirme sırasında biriken temizlik release kapısında kapatılır.
4.4. Varlık sürümlemesi dosya adındaki hash veya sürüm damgasıyla yapılır; build aracı yoktur, hash elle veya dağıtım betiğiyle üretilir.

## 5. JavaScript bütçesi

5.1. JavaScript vanilla yazılır ve defer ile yüklenir; framework, SPA yönlendirici ve jQuery benzeri kütüphane kullanılmaz.
5.2. Sayfa başına toplam JavaScript bütçesi 30 KB gzip'tir; ölçüm transfer toplamından alınır, bütçeyi aşan sürüm kabul edilmez.
5.3. Üçüncü taraf betik CDN'i yasaktır. Tek istisna zorunlu ikon yükleyicisidir: sürüm sabitlenir, SRI eklenir, CSP script-src ve gerekli bağlantı kaynaklarına eklenir; sürüm ve SRI çalışma anında resmî kaynaktan doğrulanır.
5.4. İstisna dışında hiçbir harici betik, izleyici veya çerçeve yüklenmez; analitik gerekiyorsa çerezsiz ve kişisel veri toplamayan çözüm seçilir, CSP ve gizlilik etkisi gerekçelenir.
5.5. JS yalnız davranışı güçlendirir; kritik içerik, form etiketi ve gezinme JS'e bağımlı değildir.
5.6. Ölçüm: ağ panelinde sayfa başına JS transferi; release'te gzip/Brotli toplamı bütçeyle karşılaştırılır.

## 6. Font bütçesi

6.1. Varsayılan tipografi sistem font yığınıdır; web font zorunlu değildir.
6.2. Marka fontu zorunluysa yalnız self-host woff2 alt kümesi kullanılır; en fazla iki dosya yüklenir.
6.3. Her font dosyası preload ve font-display swap taşır; harici font CDN'i ve CSS @import yasaktır.
6.4. Font yüklemesi CLS'ye yol açmaz; fallback metrikleri tanımlanır ve görünür metin font değişiminde kaymaz.

## 7. Görsel ve medya bütçesi

7.1. Görseller AVIF veya WebP sunulur; desteklemeyen tarayıcı için picture içinde geri dönüş biçimi bulunur.
7.2. Her img etiketinde width ve height zorunludur; en-boy oranı belirtilmeyen görsel kabul edilmez.
7.3. LCP görseli sayfa tasarımında belirlenir, fetchpriority ve preload ile yüklenir; ilk görünümde lazy olmaz, katlanma altı görseller lazy taşır.
7.4. Hero video poster ile başlar; preload none, muted, playsinline taşır, sesli otomatik oynatılamaz, mobilde statik görsel sunulur ve kullanıcıya duraklatma denetimi verilir.
7.5. Bütçe aşılırsa dekoratif görsel kaldırılır; LCP görselini küçültmek yerine kompozisyon sadeleştirilir.
7.6. Görsel ve video dosyaları web kökünde assets/img altında tutulur; kaynak dosyalar ve ağır ara dosyalar dağıtıma girmez.

## 8. Önbellek ve dağıtım

8.1. Hash'li varlık Cache-Control: public, max-age=31536000, immutable ile sunulur.
8.2. HTML kısa ömürlüdür; form tokenı veya CSP nonce'u taşıyan HTML paylaşımlı önbelleğe alınmaz, gerekirse no-store kullanılır.
8.3. Sıkıştırma Brotli, desteklenmiyorsa gzip ile yapılır; sıkıştırmanın açık olduğu release'te başlıkla doğrulanır.
8.4. sitemap.xml dağıtım sırasında üretilir ve sürüm kontrolüne girmez; robots.txt kökte izlenir.
8.5. Dağıtım adımı tekrarlanabilir olmalıdır: dosya kopyalama, önbellek temizliği, sitemap üretimi ve başlık kontrolü aynı sırayla yapılır.

## 9. Doğrulama

9.1. Geliştirmede php -l, tarayıcıda sayfa açma ve ağ panelinde bütçe kontrolü yeterlidir; her mikro değişiklikte derleme veya test koşulmaz.
9.2. Release'te references/kabul-kapilari.md bölüm 1, 2 ve 5 uygulanır.
9.3. Barındırma sürümü, HTTP sürümü, Brotli ve PHP dalı gibi her iddia çalışma anında doğrulanır; doğrulanamayan "doğrulanmalı" işaretlenir.
