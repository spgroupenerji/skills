# SEO ve İndeksleme

Bu dosya sp-mimari-web-site gövdesinin 4. bölümünü açar: semantik HTML, meta parçası, yapısal veri, robots/sitemap, URL politikası ve doğrulama. Arama motoru davranışı ve sürüm iddiaları varsayılmaz; resmî kaynaktan doğrulanır.

## 1. Semantik HTML

1.1. Her sayfa sunucuda tam HTML olarak üretilir; ana içerik JavaScript ile oluşturulmaz.
1.2. Başlık hiyerarşisi atlanmaz ve sayfada tam olarak bir h1 bulunur; alt başlıklar h2 ve h3 ile devam eder.
1.3. header, nav, main ve footer gibi anlamlı bölgeler kullanılır; main sayfada tektir.
1.4. Bağlantı metni hedefini açıklar; "buraya tıklayın" ve boş bağlantı kullanılmaz.
1.5. Dil özniteliği doğru verilir; karışık dilli içerik kendi dil özniteliğini taşır.

## 2. Ortak meta parçası

2.1. title, description, canonical, robots, Open Graph ve Twitter Card etiketleri tek ortak parçadan üretilir; sayfalarda elle çoğaltılmaz.
2.2. Canonical mutlaktır ve sayfanın kalıcı adresini gösterir; sorgu parametreleri canonical'a yazılmaz.
2.3. Open Graph ve Twitter alanları boş bırakılmaz; başlık, açıklama ve görsel her sayfada doludur.
2.4. robots meta yalnız gerektiğinde kullanılır; noindex sayfa sitemap'e girmez ve canonical çelişkisi üretilmez.
2.5. Sayfa başlığı ve açıklaması sayfaya özgüdür; şablon metni kopyalanmaz.

## 3. Yapısal veri (JSON-LD)

3.1. Organization ve WebSite her sitede bulunur; iletişim ve adres bilgisi gerçek verilerdir.
3.2. BreadcrumbList her iç sayfada bulunur; görünen gezinme ile tutarlıdır.
3.3. Product veya FAQPage yalnız uygun sayfada ve gerçek içerikle kullanılır; uydurma puan, yorum veya fiyat yazılmaz.
3.4. JSON-LD betiği sayfa sonunda veya head içinde tek blok halinde durur; CSP hash/nonce politikasına uyar.
3.5. Doğrulama resmî yapısal veri doğrulayıcısıyla ve zengin sonuç testiyle yapılır; araç davranışı çalışma anında teyit edilir.

## 4. robots.txt ve sitemap.xml

4.1. robots.txt kökte bulunur, 200 döner ve sitemap adresini bildirir.
4.2. robots.txt ile veri/log/parcalar dizinlerini ayrıca kapatmak gerekmez; bu dizinler zaten HTTP erişimine kapalıdır.
4.3. sitemap.xml dağıtım sırasında üretilir; sürüm kontrolüne eklenmez ve elle commit edilmez.
4.4. sitemap yalnız 200 dönen kalıcı adresleri içerir; noindex ve yönlendirme hedefleri sitemap'e girmez.
4.5. lastmod gerçek içerik değişiklik tarihini taşır; uydurma veya her dağıtımda değişen tarih yazılmaz.
4.6. Üretim yöntemi tek bir betik veya komut olarak proje kaydında tanımlanır; dağıtım adımıyla birlikte çalışır.
4.7. llms.txt isteğe bağlıdır; kullanılıyorsa kökte durur ve aynı üretim kaynağından beslenir.

## 5. URL ve yönlendirme

5.1. Adresler kalıcı, okunur ve ASCII slug biçimindedir; Türkçe karakter URL'de taşınmaz, transliterasyon kullanılır.
5.2. Adres değişikliği 301 haritasıyla tek atlamada yapılır; 302 ve zincirleme yönlendirme kabul edilmez.
5.3. Eski adresten yeni adrese eşleme tablosu sürüm kontrolünde tutulur ve dağıtımda uygulanır.
5.4. Sondaki eğik çizgi politikası tekildir; aynı içerik iki farklı URL biçiminde 200 dönmez.
5.5. Çok dilli sitede hreflang bağlantıları karşılıklıdır; eksik veya tek yönlü hreflang yayına alınmaz.

## 6. Performans ve indeksleme ilişkisi

6.1. LCP görseli tasarım aşamasında belirlenir ve render-blocking kaynakla geciktirilmez.
6.2. CLS'yi tetikleyen geç yüklenen font, görsel veya reklam yerleşimi yoktur; yer tutucu alan ayrılmadan dinamik içerik eklenmez.
6.3. Ana içerik JS'e bağımlı değildir; JavaScript kapalıyken sayfa indekslenebilir kalır.
6.4. Canonical, robots ve sitemap birbiriyle tutarlıdır; aynı sayfa için çelişen sinyal üretilmez.
6.5. Sayfa hızı ve CWV eşikleri release kapılarında ölçülür; eşiği aşan sürüm geri alınır.

## 7. Doğrulama listesi

7.1. Sayfa 200 döner; kaynakta title, canonical, OG/Twitter ve JSON-LD blokları görünür.
7.2. robots.txt 200 döner ve sitemap satırı içerir; sitemap 200 döner ve tüm URL'ler 200'dür.
7.3. Her sayfada tek h1 vardır; başlık sırası bozulmamıştır.
7.4. 301 haritası test edilir; her eski adres tek atlamada yeni adrese ulaşır.
7.5. hreflang çift yönlüdür; hedef URL'ler 200 döner.
7.6. Yapısal veri doğrulayıcısında hata yoktur; görünen içerikle çelişen alan bulunmaz.
7.7. git ls-files sitemap.xml boştur; sitemap dağıtımda üretilmiştir.
