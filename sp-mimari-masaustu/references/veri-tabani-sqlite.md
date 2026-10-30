# SQLite Sözleşmesi

> Gövde §6'nın ayrıntısı: motor, bağlantı, yazıcı, göç, sorgu, bütünlük ve gizlilik.

## 1. Motor ve sahiplik

1.1. SQLite tek gömülü veritabanı motorudur; istemci-sunucu, harici servis veya bulut veritabanı kullanılmaz.
1.2. Veritabanı erişimi yalnız `depo/` katmanındadır; `ui/` ve `domain/` SQLite paketini içe aktaramaz.
1.3. Paket gömülü derleme özelliğiyle gelir; sistem SQLite kütüphanesine bağlanılmaz. Sürüm ve özellik resmî manifestten doğrulanır.
1.4. Veritabanı yolu platform veri dizininden çözülür; mutlak yol gömülmez. Dosya izinleri yalnız geçerli kullanıcıya yazma verir.
1.5. Veritabanı yalnız yerel diskte tutulur; WAL dosyaları ağ paylaşımında veya eşzamanlanan klasörde açılmaz.

## 2. Bağlantı ve ayarlar

2.1. Açılışta günlük kipi WAL yapılır; seçilen kip testte doğrulanır.
2.2. Yabancı anahtar zorlaması açılışta açıkça açılır; motorun varsayılanına güvenilmez.
2.3. Bekleme süresi sıfırdan büyük tek adlandırılmış sabite ayarlanır; sabit `depo/` modülünde tanımlanır.
2.4. WAL kipinde eşzamanlama normal düzeydir; tam dayanım yalnız güç kesintisi senaryosunda yazılı gerekçeyle seçilir.
2.5. Bağlantı açılış sırası tek yerde tanımlanır; ayarlar bağlantı kurulduktan sonra ve ilk sorgudan önce uygulanır.

## 3. Yazıcı disiplini

3.1. Tek yazıcı ilkesi geçerlidir: tüm yazmalar tek arka plan yürütücüsünden sırayla geçer; ikinci yazıcı açılmaz.
3.2. UI iş parçacığında veritabanı çağrısı yapılmaz; sonuç sınırlı kapasiteli kanalla UI'ye taşınır.
3.3. Transaction içinde ağ çağrısı, dosya G/Ç ve uzun hesaplama yapılmaz; işlem yalnız veritabanı değişikliklerini kapsar.
3.4. Kullanıcı onayı bekleyen transaction açık bırakılmaz; onay işlem öncesi alınır.
3.5. Toplu yazma tek transaction'da toplu ekleme ile yapılır; kayıt başına transaction açılmaz.

## 4. Göç

4.1. Göçler kod içinde tanımlanır ve açılışta atomik olarak en son sürüme uygulanır; harici komut satırı aracı veya elle çalıştırılan SQL betiği kullanılmaz.
4.2. Her göç tek mantıksal değişiklik taşır; tablo ile indeksi aynı göçte tutmak bu tanıma uygundur.
4.3. Göç zinciri testte doğrulanır; doğrulanmamış göç yayına girmez.
4.4. Şema sürümü motorun sürüm alanıyla izlenir ve göç kütüphanesi dışında değiştirilmez.
4.5. Yıkıcı göç (tablo veya kolon düşürme, veri daraltma) öncesi dosya yedeği alınır ve yedek bütünlük kontrolünden geçirilir; geri dönüş yedekle karşılanır.
4.6. Veri kaybı riski taşıyan göç öncesi kullanıcıya Türkçe uyarı gösterilir ve açık onay alınır; onay yoksa göç uygulanmaz.
4.7. Göç hatasında uygulama yarım şemayla çalışmaz; hata Türkçe raporlanır ve kurtarma yolu (yedekten dönüş) sunulur. Dev modda sıfırlama bayrağı kullanılabilir.
4.8. Zaman damgaları UTC unix milisaniye tam sayı olarak saklanır; büyük ikili içerik veritabanına gömülmez, dosya yolu referansı tutulur.

## 5. Sorgular

5.1. Tüm sorgular hazırlanmış ifadeyle çalışır; değerler metin birleştirmeyle SQL'e gömülmez.
5.2. `SELECT *` yasaktır; yalnız gerekli kolonlar yazılır.
5.3. Her listeleme sorgusu adlandırılmış sabit bir `LIMIT` taşır; sınırsız sonuç döndürülmez.
5.4. Döngü içinde sorgu (N+1) yoktur; ilişkili veri tek sorguda veya toplu `IN` listesiyle alınır.
5.5. Filtre veya sıralama kullanan sorgu için indeks tanımlanır ve plan `EXPLAIN QUERY PLAN` ile doğrulanır.
5.6. İndeksi devre dışı bırakan fonksiyon sarmalı ve baştan jokerli `LIKE` filtresi kullanılmaz.
5.7. Sayfalama `LIMIT` ve imleç (son kimlik) ile yapılır; büyük tabloda derin `OFFSET` kullanılmaz.

## 6. Bütünlük, gizlilik ve hata

6.1. Açılışta bütünlük kontrolü çalıştırılır; beklenen sonuç dışında çalışmaya devam edilmez.
6.2. Yedek açık bağlantı üzerinden tutarlı kopya alınarak üretilir; WAL yardımcı dosyalarını elle kopyalamak yasaktır.
6.3. Kişisel veri içeren kolonlar işaretlenir ve loglara yazılmaz; zorunlu logda maskeleme uygulanır.
6.4. Parola ve token gibi sırlar veritabanında saklanmaz; zorunluysa secret manager'da tutulur ve veritabanına yalnız referans yazılır.
6.5. Hata durumunda transaction geri alınır ve yarım durum bırakılmaz; hata sessizce yutulmaz.
6.6. Veritabanı hatası kullanıcıya Türkçe ve eyleme dönük mesajla gösterilir; SQL metni, dosya yolu ve sürücü ayrıntısı sızdırılmaz.
6.7. Bağlantı ve yazma hataları yapısal logda hata düzeyinde kaydedilir; log kaydına parola veya kişisel veri yazılmaz.

## 7. Dev modu

7.1. Dev modda şema prototipi için geçici veritabanı ve sıfırlama bayrağı kullanılabilir; kullanıcı verisi varsa yedek ve onay kuralları yine geçerlidir.
7.2. Dev modda indeks ve plan doğrulaması yalnız büyük veya yavaş sorgularda hedeflenir.

## 8. Kontrol listesi

- [ ] Açılış testi WAL, yabancı anahtar ve bekleme süresi değerlerini doğruluyor.
- [ ] Veritabanı erişimi yalnız `depo/` altında eşleşiyor (grep).
- [ ] Göç zinciri testte doğrulanmış; yıkıcı göç yedeği ve bütünlük kontrolü kayıtlı.
- [ ] Hazırlanmış ifade dışında SQL üretimi yok; `SELECT *` yok; listeleme `LIMIT` taşıyor.
- [ ] Filtre ve sıralama sorguları `EXPLAIN QUERY PLAN` ile incelenmiş.
- [ ] Bütünlük kontrolü ve yedekten geri yükleme testi geçmiş.
