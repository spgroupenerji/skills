# php-panel — istek döngüsü, katman sınırları, kod kalitesi

> Bu dosya sp-mimari-web-uygulama becerisinin references dosyasıdır; gövdedeki 2. ve 3. bölümlerin ayrıntısını taşır.

## 1. HTTP girişi ve modül çözümlemesi

1.1. Giriş noktaları iki tanedir: sayfa istekleri ve headless API istekleri. Başka giriş dosyası oluşturulmaz; her istek bu çiftten geçer.
1.2. Modül çözümlemesi üç koşulla yapılır: desen eşleşmesi, işleyici dosyasının varlığı, sayfa varlığı. Elle tutulan izinli liste yasaktır; koşullardan biri yoksa istek reddedilir.
1.3. Headless modüller tek elemanlı açık listede tanımlanır; listede olmayan sayfasız modül 400 döner; liste tek dosyada ve tek kopyadır.
1.4. Giriş dosyası yalnız zinciri kurar; iş kuralı, sorgu ve sunum taşımaz.

## 2. Zincir sırası ve güvenlik kapıları

2.1. Sıra sabittir: gövde çözümü, desen, dosya kuralı, CSRF, oturum ve zaman aşımı, rol denetimi, denetim kaydı.
2.2. Sıra atlanamaz; kısa devre yalnız zincirin tanımlı adımında ve loglanarak yapılır.
2.3. Her adım tek sorumluluk taşır; adımlar birbirinin işini tekrar etmez.
2.4. Reddedilen istek HTTP durumu ve Türkçe kullanıcı mesajıyla döner; iç ayrıntı istemciye sızmaz.

## 3. Katalog ve katman sınırları

3.1. Sayfa, menü ve rol tanımları tek katalogdan okunur; sayfa girişi, API ve sidebar aynı kaynağı kullanır; ikinci kaynak yasaktır.
3.2. Katalog kaydı olmayan modül açılamaz; yeni modül kabuk, işleyici, katalog kaydı ve istemci sözleşmesi birlikte tamamlanır.
3.3. Sayfa dosyası ince sunum kabuğudur: başlık, eylem çubuğu ve içerik iskeletini kurar; iş kuralı ve sorgu içermez.
3.4. İş mantığı destek katmanındadır; sunum kabuğu destek katmanını çağırır, ters yön yasaktır.
3.5. SQL yalnız DAO/veri katmanında yaşar. Controller, sayfa kabuğu ve istemci kodunda SQL metni veya PDO çağrısı bulunmaz.
3.6. Tek modüle özel fonksiyon ve veri yapıları çağıran dosyada kalır; iki veya daha fazla modülün paylaştığı yan etkisiz mantık destek altında toplanır.
3.7. Ortak kütüphane üst iş mantığına bağımlı olamaz; bağımlılık yönü destek katmanından modüle doğrudur.

## 4. Tip, adlandırma ve okunabilirlik

4.1. Birinci taraf iş mantığında declare(strict_types=1) ve parametre/dönüş tip bildirimleri zorunludur.
4.2. Gerekçesiz mixed kullanımı reddedilir; dış veri sınırda doğrulanıp daraltılır.
4.3. Adlandırma amacı doğrudan açıklar; kısaltma, belirsiz ek ve sürüm eki kullanılmaz.
4.4. Tanımlayıcılar Türkçe kökenli ve ASCII'dir; dil/framework zorunlulukları, standart kütüphane, paket/API, HTTP metotları ve şema alanları özgün kalır.
4.5. Yorum yalnız standart dışı protokol, karmaşık matematik veya mimari zorunluluk gerekçesiyle yazılır; bariz mantığı tekrar eden yorum yoktur.
4.6. Ölü kod, yoruma alınmış kod, yarım bırakılmış işaret ve ulaşılamaz uç release engelidir.

## 5. Hata yönetimi ve gözlemlenebilirlik

5.1. Boş catch ve hatayı yutan blok yasaktır; her istisna sınıfı, mesajı ve yığın iziyle loglanır.
5.2. Alan hataları ile sistem hataları ayrı yönetilir; sistem hatası güvenli varsayılan veya son geçerli durumla karşılanır.
5.3. Kullanıcıya Türkçe, eyleme dönük ve alanı işaret eden mesaj gösterilir; yığın izi, dosya yolu ve veritabanı ayrıntısı istemciye sızmaz.
5.4. İstemci tarafında yakalanmamış hata ve söz redleri tek bildirim kanalına bağlanır; sessiz yutma yasaktır.
5.5. Log satırları yapısaldır (zaman, seviye, trace kimliği, modül); serbest metin birleştirmeyle log yazılmaz.

## 6. Modül tamamlama kontrolü

6.1. Yeni modül için giriş kaydı, işleyici, katalog kaydı, rol eşlemesi, istemci sözleşmesi ve hata durumları birlikte tamamlanır.
6.2. Modül açılmadan önce yetkisiz erişim 403, geçersiz gövde 400 ve oturumsuz erişim giriş yönlendirmesiyle doğrulanır.
6.3. Bu dosya kabul kapılarını içermez; release kanıtı references/kabul-kapilari.md altındadır.
