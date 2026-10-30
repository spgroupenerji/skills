# guvenlik-oturum — aynı origin, oturum, CSRF, başlıklar, tedarik zinciri

> Bu dosya sp-mimari-web-spa becerisinin references dosyasıdır; gövdedeki 4. bölümün ayrıntısını taşır. Başlık değerleri ve sürüm davranışı beceriye gömülmez; release anında gerçek yanıtla doğrulanır.

## 1. Aynı origin ve CORS

1.1. React ve API aynı alan adındadır; CORS başlığı yapılandırılmaz, başka origin'den gelen istemci kabul edilmez.
1.2. API yalnız aynı origin isteğini işler; Origin ve Referer kontrolü ek savunma katmanıdır, tek başına yetki sayılmaz.
1.3. Farklı port veya alt alan adı istisnası yoktur; istisna gerekiyorsa ters proxy ile aynı origin'e taşınır.
1.4. CORS açılması talebi reddedilir; gerekçesi yazılı olsa bile oturum/CSRF modeli zayıflatılmaz.

## 2. Oturum

2.1. Oturum çerezi HttpOnly, Secure ve SameSite ile ayarlanır; çerez adı proje öneklidir.
2.2. Girişte oturum kimliği yenilenir; eski kimlik geçersiz kılınır.
2.3. Her korumalı API isteği oturumu sunucuda doğrular; istemcideki durum yetki yerine geçmez.
2.4. Hareketsizlik ve mutlak süre tanımlıdır; süre aşımı 401 döner ve kullanıcı yeniden girişe yönlendirilir.
2.5. Çıkışta oturum verisi ve çerez sunucu tarafında geçersiz kılınır.
2.6. Rol ve veri kapsamı denetimi sunucudadır; istemci yalnız görünürlüğü yönetir.

## 3. CSRF

3.1. Durum değiştiren her istekte CSRF zorunludur; GET, HEAD ve OPTIONS muaftır.
3.2. Belirteç oturuma bağlıdır; bootstrap yanıtından veya çerezden alınır ve X-CSRF-Token başlığıyla gönderilir.
3.3. Sunucu belirteci sabit zamanlı karşılaştırır; eksik veya geçersiz belirteç 403 döner.
3.4. Belirteç istemci kodunda sabitlenmez; oturum yenilendiğinde yeniden alınır.
3.5. CSRF doğrulaması oturum doğrulamasından sonra ve iş kuralından önce çalışır.

## 4. Girdi, çıktı ve hata

4.1. Girdi sunucuda şemaya göre doğrulanır; tip, uzunluk, format ve yetki kontrol edilir.
4.2. React varsayılan kaçışı korunur; dangerouslySetInnerHTML yalnız güvenilir ve sanitize edilmiş içerikle kullanılır.
4.3. Hata kodları ayrışır: 400 veya 422 doğrulama, 401 oturum, 403 yetki veya CSRF, 404 bulunamadı, 409 çakışma, 429 hız sınırı, 500 sistem.
4.4. Hata gövdesi Türkçe mesaj ve alan listesi taşır; yığın izi, dosya yolu ve veritabanı ayrıntısı istemciye sızmaz.
4.5. Hassas uçlarda hız sınırı ve denetim kaydı vardır; denetim yazımı başarısızsa işlem tamamlanmaz.
4.6. Parola, token ve kişisel veri loglarda maskelenir.

## 5. Secret ve tedarik zinciri

5.1. Secret istemci paketine girmez; build-time ortam değişkenleri yalnız kamuya açık değerleri taşır.
5.2. API anahtarları ve veritabanı parolaları PHP tarafında ortam değişkeninden gelir; depoya ve dist'e yazılmaz.
5.3. lockfile sürüm kontrolündedir; kurulum lockfile'a göre yapılır; sürümler pinlidir.
5.4. CDN veya doğrulanmamış kaynaktan script, stil, font yüklenmez.
5.5. Yeni bağımlılık gerekçelenir ve denetlenir; bilinen kritik açık varken release yapılmaz.
5.6. dist içinde secret, token ve ortam dosyası izi bulunmaz; release öncesi statik tarama yapılır.

## 6. Release başlıkları

6.1. HTTPS zorunludur; HSTS includeSubDomains ve sabit max-age ile yayınlanır.
6.2. CSP: script-src self, unsafe-inline ve unsafe-eval yok; connect-src yalnız kendi API; frame-ancestors none.
6.3. X-Content-Type-Options nosniff ve Referrer-Policy eksiksizdir.
6.4. Başlık değerleri, CSP ve çerez davranışı release anında gerçek yanıtla ve resmî kaynakla doğrulanır; varsayım yapılmaz.
6.5. Başlık doğrulaması release kapısıdır (references/kabul-kapilari.md).
