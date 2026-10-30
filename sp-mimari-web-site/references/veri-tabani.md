# Veri Tabanı (Opsiyonel)

Bu dosya sp-mimari-web-site gövdesinin 5.6 bölümünü açar: tanıtım sitesinde form veya lead saklama zorunluluğu doğduğunda kullanılan ilişkisel veri katmanı. Oturum, kullanıcı hesabı ve panel verisi kapsam dışıdır. Motor sürümü, EOL ve API davranışı çalışma anında doğrulanır.

## 1. Kapsam

1.1. Tanıtım sitesinde veritabanı varsayılan olarak yoktur; yalnız form veya lead saklama zorunluluğu doğduğunda açılır.
1.2. Veritabanı gerektirmeyen içerik statik HTML olarak tutulur; içerik saklamak için veritabanı açılmaz.
1.3. Oturum, kullanıcı hesabı ve panel verisi kapsam dışıdır; oturumlu uygulama ayrı anayasaya ve ayrı beceriye tabidir.
1.4. Veritabanı kararı proje kaydına gerekçesiyle yazılır; gerekçesiz katman eklenmez.

## 2. Motor ve bağlantı

2.1. İlişkisel motor kullanılır; sürüm, canlı destekli LTS dalında proje kaydında sabitlenir ve çalışma anında doğrulanır.
2.2. Erişim yalnız PDO ile yapılır; mysqli ve ham sürücü çağrıları yasaktır.
2.3. DSN charset=utf8mb4 içerir; prepared statement emülasyonu kapalı, hata modu exception olarak ayarlanır.
2.4. Bağlantı bilgileri .env veya secret manager'dan gelir; uygulama hesabı en az yetkiyle çalışır, root ile bağlanılmaz.
2.5. Bağlantı ve sorgu hataları istemciye gösterilmez; genel Türkçe hata döner, ayrıntı sunucu loguna yazılır.

## 3. Şema

3.1. Tablolar InnoDB motorunda, utf8mb4 karakter setinde ve tek proje collation'ında oluşturulur; Türkçe metin karşılaştırması testle doğrulanır.
3.2. Tablo ve kolon adları ASCII snake_case'tir; Türkçe karakter, boşluk ve büyük harf içeren tanımlayıcı yasaktır.
3.3. Her tabloda birincil anahtar bulunur; zorunlu alanlar NOT NULL ve varsayılan değerle tanımlanır.
3.4. Tarih ve saat kolonları UTC tutulur; yerelleştirme gösterim katmanında yapılır.
3.5. Şema değişikliği yalnız göç dosyasıyla yapılır; üretimde elle ALTER yasaktır.

## 4. Sorgu ve bütünlük

4.1. Tüm sorgular hazırlanmış deyimle çalıştırılır; SQL metnine değer birleştirme yasaktır.
4.2. SELECT * yasaktır; yalnız kullanılan kolonlar listelenir, döngü içinde ayrı sorgu yazılmaz.
4.3. Liste sorgularında LIMIT zorunludur; üst sınırı olmayan sorgu yayına alınmaz.
4.4. WHERE koşulu indeksli kolonda ham değerle kurulur; kolon üzerinde fonksiyon ve baştan jokerli LIKE yasaktır, karmaşık sorgu EXPLAIN ile doğrulanır.
4.5. Birden fazla tabloyu etkileyen yazma tek transaction içinde yürütülür; hata durumunda ROLLBACK zorunludur.
4.6. Transaction içinde ağ çağrısı, dosya işlemi ve e-posta gönderimi yapılmaz; eşzamanlı güncelleme version kolonuyla korunur.

## 5. Göçler

5.1. Tüm şema değişiklikleri numaralı göç dosyasıyla ve sürüm kontrolünde yapılır.
5.2. Her göç dosyası tek yapısal değişiklik içerir ve geri alma adımını belgeler.
5.3. *.sql dosyaları depoda izlenmez; göçler .php olarak tutulur, örnek şema .sql.example adıyla saklanır.
5.4. Göç çalıştırıcısı minimal PHP betiğidir; uygulanan göçleri kaydeder, tekrar çalıştırmaz ve hata durumunda durur.
5.5. Göç önce kopya veritabanında denenir; üretimde yedek ve onay sonrası çalıştırılır.

## 6. Yedek ve geri yükleme

6.1. Yıkıcı işlem öncesi yedek alınır; geri yükleme bir kez denenerek kanıtlanır.
6.2. Onay kaydı olmadan yıkıcı göç çalıştırılamaz.
6.3. Yedekler şifreli ve web erişimi dışında saklanır; saklama süresi tanımlıdır.

## 7. Lead verisi ve KVKK

7.1. Form yalnız amaca gerekli alanları toplar; özel nitelikli kişisel veri ve kart bilgisi tanıtım formunda toplanmaz.
7.2. Lead saklama süresi aydınlatma metninde belirtilir; süre sonunda kayıt silinir veya anonimleştirilir.
7.3. Amaç, hukuki sebep ve saklama süresi belgelenmeden veri toplanamaz.
7.4. Kişisel veri içeren alanlar loglarda maskelenir; form gövdesi ve e-posta içeriği loga yazılmaz.
7.5. Silme ve anonimleştirme işi tanımlı ve test edilmiştir; süre sonu işi elle hatırlamaya bırakılmaz.

## 8. Erişim katmanı

8.1. Veritabanı erişimi yalnız DAO katmanından yapılır; şablon ve sunum dosyalarında SQL bulunamaz.
8.2. DAO parametre alır, deyimi kurar ve sonucu döner; hata domain hatasına çevrilir.
8.3. Veritabanı hatası istemciye gösterilmez; kullanıcıya genel Türkçe mesaj döner.
8.4. Sorgu ve şema değişikliği aynı değişiklikte ele alınır; şema ile kod arasında sürüm uyuşmazlığı bırakılmaz.

## 9. Doğrulama

9.1. information_schema üzerinden InnoDB, utf8mb4, tek collation, birincil anahtar ve NOT NULL kontrolü yapılır.
9.2. EXPLAIN planında kritik sorgularda tam tablo taraması kalmamıştır.
9.3. git ls-files çıktısında .sql dosyası yoktur; göçler kopya veritabanında çalışmıştır.
9.4. Yedekten geri yükleme bir kez kanıtlanmıştır; loglarda kişisel veri bulunmaz.
9.5. Motor sürümü, PDO bayrakları ve collation desteği çalışma anında doğrulanır; varsayım yapılmaz.
