# veri-tabani — MySQL erişimi, şema, sorgu, göç

> Bu dosya sp-mimari-web-uygulama becerisinin references dosyasıdır; gövdedeki 3. ve 7. bölümlerin veri ayrıntısını taşır. Sürüm ve kolasyon adları beceriye gömülmez; sunucuda doğrulanır.

## 1. Bağlantı ve kodlama

1.1. Bağlantı PDO ile kurulur; emülasyonlu hazırlanmış deyim kapalıdır, istisna modu açıktır ve sabit timeout vardır.
1.2. Tek PDO örneği kullanılır; sorgu başına yeni bağlantı açılmaz.
1.3. Bağlantı karakter kümesi sunucu, şema ve oturum düzeyinde utf8mb4'tür; farklı karakter kümesi reddedilir.
1.4. Türkçe sıralama yalnız sunucuda doğrulanan utf8mb4 kolasyonuyla karşılanır; doğrulanmamış kolasyon adı yapılandırmaya girmez.
1.5. Bağlantı bilgileri ve parolalar ortam değişkeni veya secret manager'dan gelir; kod ve loglarda düz metin parola yoktur.
1.6. Uygulama kullanıcısı yalnız gerekli DML yetkisine sahiptir; DDL yetkisi göç kullanıcısında ayrıdır; GRANT ALL verilmez.
1.7. Dinamik SQL yasaktır; her sorgu hazırlanmış deyim ve bağlı parametreyle çalışır; değer SQL metnine birleştirilmez.
1.8. Sorgu ve kilit bekleme süreleri oturum düzeyinde üst sınırla tanımlıdır; süresiz bekleyen sorgu üretimde çalışmaz.

## 2. Şema ve indeks

2.1. Her tabloda birincil anahtar vardır; anlamsız yedek anahtar çoğaltması kabul edilmez.
2.2. İlişkiler yabancı anahtar kısıtıyla tanımlanır; uygulama katmanı varsayımı kısıt yerine geçmez.
2.3. Kolon tipleri en dar ve anlamlı tiptir; sınırsız metin yalnız ölçülmüş gerekçeyle açılır.
2.4. WHERE, JOIN ve ORDER BY içinde kullanılan kolonlar indeksle desteklenir; indeks ayrı göçle eklenir.
2.5. İndeksli kolonda fonksiyon, dönüşüm veya ifade kullanılmaz; gereksinim kolon tipi veya türetilmiş kolonla çözülür.
2.6. Baştan jokerli LIKE araması yasaktır; ihtiyaç tam metin indeksi veya önek aramasıyla karşılanır.
2.7. Bileşik indeks sırası sorgu desenine göre tanımlanır; aynı kolon kümesini tekrarlayan mükerrer indeks bırakılmaz.

## 3. Sorgu disiplini

3.1. SELECT * yasaktır; her sorguda yalnız ihtiyaç duyulan kolonlar açıkça listelenir.
3.2. Döngü içinde ardışık sorgu (N+1) yasaktır; ilişkili veri tek JOIN veya gruplu IN sorgusuyla çekilir.
3.3. Gereksiz DISTINCT ve sıralamasız sonuç kümesinde ORDER BY kullanılmaz; ikisi de ölçülmüş gereksinimle eklenir.
3.4. Yeni veya değişen karmaşık sorgu EXPLAIN ile doğrulanır; büyük tabloda tam tablo taraması gösteren plan kabul edilmez.
3.5. Toplu ekleme ve güncelleme tek toplu deyimle yapılır; kayıt başına ayrı deyim açılmaz.
3.6. İlişkili veride JOIN esastır; alt sorgu ancak EXPLAIN maliyeti JOIN'den düşükse kullanılır.
3.7. Tüm listeleme uçlarında sayfalama zorunludur; aşılması imkânsız maksimum kayıt limiti tanımlıdır.
3.8. Büyük hacimlerde sabit maliyetli imleç tabanlı sayfalama kullanılır.
3.9. Her sayfalama isteğinde toplam kayıt yeniden hesaplanmaz; toplam önbellekten sunulur veya tasarım toplam gerektirmez.

## 4. İşlem ve kilit

4.1. Birden fazla satır veya tabloyu etkileyen her yazma transaction içinde yürütülür; kısmi başarı bırakan işlem kabul edilmez.
4.2. Hata anında ROLLBACK çalışır ve geri alma yapısal loga yazılır.
4.3. Transaction içinde harici ağ çağrısı, dosya G/Ç ve uzun iş mantığı yürütülmez.
4.4. Eşzamanlı güncellemede sürüm kolonlu iyimser veya senaryoya uygun kötümser kilitleme uygulanır.
4.5. Kilit edinme sırası servis genelinde aynı hiyerarşidedir; döngüsel bağımlılık yoktur.
4.6. Deadlock hatası sınırlı sayıda, üstel geri çekilmeli yeniden denemeyle karşılanır.
4.7. Transaction yönetimi merkezi sarmalayıcıdadır; alt fonksiyon kendi transaction'ını açmaz.

## 5. Göç disiplini

5.1. Tüm şema değişiklikleri numaralı göç dosyalarıyla sürüm kontrolünde tutulur; elle ALTER yasaktır.
5.2. Her göç dosyası tek yapısal değişiklik içerir; bağımsız değişiklikler tek dosyada birleştirilmez.
5.3. Her göç çift yönlüdür; up ve down blokları eksiksiz tanımlanmadan göç çalıştırılamaz.
5.4. Göç sırası korunur; numara atlaması reddedilir.
5.5. DROP ve geri dönüşsüz dönüşümler yalnız veri güvenli alana alındıktan sonra uygulanır.
5.6. Veri kaybı riski taşıyan göç öncesi yedek alınır ve açık onay kayda geçer.
5.7. Göçler yalnız dağıtım hattından çalıştırılır; uygulama çalışırken elle şema değiştirilemez.

## 6. Erişim, denetim, yedek

6.1. Veri erişimi rol tabanlıdır; her rol yalnız yetkisi dâhilindeki veri kapsamını görür; yetki denetimi SQL katmanında da uygulanır.
6.2. Denetim kaydı gerektiren okuma ve yazmalar fail-closed çalışır; denetim yazımı başarısızsa işlem tamamlanmaz.
6.3. Loglarda parola, token ve kişisel veri maskelenir; maskesiz veritabanı logu güvenlik ihlalidir.
6.4. Yedekleme politikası yazılıdır; geri yükleme tatbikatı kayda geçirilmeden politika geçerli sayılmaz.
6.5. Yedek dosyaları web'den erişilemez konumda tutulur ve şifrelenir; yedek içinde açık parola bulunmaz.

## 7. Release doğrulaması

7.1. Sunucu sürümü, karakter kümesi, kolasyon, EXPLAIN kayıtları, göç numaraları ve kullanıcı yetkileri release'de kanıtlanır.
7.2. Kapı komutları references/kabul-kapilari.md altındadır; sürüm ve kolasyon adları beceriye gömülmez.
7.3. Büyük tablo sorgularında plan kaydı yoksa release durur; sözlü beyan kanıt yerine geçmez.
