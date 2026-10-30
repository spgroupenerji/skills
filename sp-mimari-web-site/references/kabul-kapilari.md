# Release Kabul Kapıları

Bu dosya yalnız risk sınıfı veya açık yayın isteğiyle yüklenir. Her madde komut ve özet çıktıyla kanıtlanır; çalıştırılamayan doğrulama gerekçesi ve komutuyla birlikte yazılır. Sürüm, API, EOL ve SRI iddiaları çalışma anında context7 veya resmî kaynaktan doğrulanmış olmalıdır.

## 0. Ön koşullar

0.1. Risk sınıfı ve yayın onayı kayıtlıdır; geri dönüş adımı yazılıdır.
0.2. Yedek alınmış ve geri yükleme yolu erişilebilirdir.
0.3. Kullanılan her sürüm, API ve bayrak çalışma anında doğrulanmıştır; doğrulanamayan bilgi "doğrulanmalı" etiketlidir.

## 1. Depo ve derleme

1.1. test ! -e package.json ve test ! -e node_modules doğrulanır; derleme adımı yoktur.
1.2. git ls-files çıktısında sitemap.xml, .env ve .sql bulunmaz.
1.3. Tüm PHP dosyaları php -l ile hatasız döner.
1.4. Tek stil kaynağı assets/css/site.css'tir; CSS CDN'i, harici CSS, @import ve serbest style bloğu yoktur.
1.5. Sayfa başına toplam JavaScript gzip boyutu 30 KB bütçesini aşmaz.

## 2. Barındırma ve başlıklar

2.1. curl -sI $SITE_URL/ yanıtı HTTPS, HSTS, CSP, nosniff, Referrer-Policy ve Permissions-Policy başlıklarını içerir.
2.2. HTTP isteği 301 ile HTTPS'e yönlenir; sertifika geçerlidir.
2.3. CSP'de unsafe-inline ve unsafe-eval yoktur; nonce veya hash doğru çalışır.
2.4. Token veya nonce taşıyan HTML paylaşımlı önbellekten servis edilmez.
2.5. Brotli veya gzip sıkıştırma etkindir; Content-Encoding başlığı görünür.
2.6. Hash'li varlık immutable, HTML kısa ömürlü önbellek başlığı taşır.
2.7. parcalar/, veri/ ve log/ altındaki dosyalara doğrudan istek 403 veya 404 döner.

## 3. Form ve güvenlik

3.1. CSRF belirteci olmayan POST reddedilir; honeypot doldurulmuş istek reddedilir.
3.2. Hız sınırı aşımında 429 döner; mesaj Türkçe ve iç ayrıntısızdır.
3.3. Geçersiz alan ve aşırı uzun girdi sunucuda reddedilir; istemci doğrulaması tek başına yeterli sayılmaz.
3.4. Tüm sorgular hazırlanmış deyimlidir; SQL metnine değer birleştirme ve şablon içinde SQL yoktur.
3.5. .env web erişimine kapalıdır; loglarda parola, token ve kişisel veri bulunmaz.
3.6. SPF, DKIM ve DMARC kayıtları doğrulanmıştır; test gönderimi ulaşmıştır.
3.7. Opsiyonel veritabanı varsa DAO dışında SQL yoktur, PDO bayrakları doğrudur ve yedekten geri yükleme kanıtlanmıştır.

## 4. SEO

4.1. robots.txt 200 döner ve sitemap adresini bildirir; sitemap 200 döner ve tüm URL'leri 200'dür.
4.2. Her sayfada tek h1, bozulmamış başlık sırası, canonical ve dolu Open Graph/Twitter alanları vardır.
4.3. Organization, WebSite ve uygun sayfalarda BreadcrumbList/Product/FAQPage JSON-LD doğrulayıcıda hatasızdır.
4.4. 301 haritası test edilmiştir; her eski adres tek atlamada yeni adrese ulaşır.
4.5. Çok dilli sitede hreflang karşılıklıdır; hedef URL'ler 200 döner.
4.6. sitemap.xml dağıtımda üretilmiştir; git ls-files çıktısında yoktur.

## 5. Performans

5.1. Mobil Lighthouse ölçümünde LCP 2,5 s ve CLS 0,1 eşiğini aşmaz; eşikler Google Web Vitals tanımına göre çalışma anında teyit edilir.
5.2. INP için varsa alan verisi 200 ms eşiğini aşmaz; alan verisi yoksa lab etkileşim ölçümü ve uzun görev taraması yapılır.
5.3. Sayfa başına JavaScript transferi gzip/Brotli toplamı 30 KB'yi aşmaz.
5.4. Görseller AVIF/WebP ve geri dönüş biçimiyle sunulur; width ve height alanları doludur.
5.5. LCP görseli fetchpriority ve preload taşır; katlanma altı görseller lazy'dir.
5.6. Fontlar sistem yığını veya en fazla iki self-host woff2 dosyasıdır; preload ve swap vardır.
5.7. Yayın sonrası ilk haftalarda alan verisi izlenir; eşiği aşan sürüm geri alınır.

## 6. Erişilebilirlik ve Türkçe

6.1. axe veya Lighthouse erişilebilirlik denetiminde kritik ihlal yoktur.
6.2. Metin kontrastı 4,5:1, büyük metin ve bileşen kontrastı 3:1 eşiğini karşılar.
6.3. Klavye ile tüm etkileşimler tamamlanır; odak görünürdür ve hedef boyut 24x24 CSS pikselin altına inmez.
6.4. Metin %200 yakınlaştırmada ve metin aralığı değerlerinde taşmaz.
6.5. prefers-reduced-motion tercihinde otomatik oynatma, paralaks ve geçişler durur.
6.6. Tüm kullanıcı metni Türkçe imlâ kurallarına uygundur; ğ, ü, ş, ı, ö, ç eksiksiz kullanılır.
6.7. Form etiketleri görünür ve programatik olarak bağlıdır; hata mesajı alanla ilişkilidir.

## 7. İçerik ve yayın

7.1. Yer tutucu metin, boş görsel ve kırık bağlantı yoktur; tüm iç bağlantılar 200 veya 301 döner.
7.2. canonical canlı adresi gösterir; noindex sayfa sitemap'te bulunmaz.
7.3. Yayın kaydı tutulur: hangi kapıların çalıştığı, komut ve özet çıktı.
7.4. Dağıtım sonrası ana sayfa, bir iç sayfa ve form ucu elle doğrulanır.

## 8. Yayın sonrası

8.1. İlk haftalarda hata logu, form gönderimleri ve alan verisi izlenir; beklenmeyen artışta geri dönüş adımı uygulanır.
8.2. Sitemap arama motorlarına bildirilir; indeksleme ve canonical kontrol edilir.
8.3. Yedek, geri yükleme ve sır rotasyonu erişilebilir durumdadır.
8.4. Bir sonraki sürüm için açık kalan doğrulama veya risk maddeleri proje kaydına yazılır.
