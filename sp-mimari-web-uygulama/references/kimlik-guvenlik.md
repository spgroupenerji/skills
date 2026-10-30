# kimlik-guvenlik — oturum, yetki, CSRF, yükleme, sırlar

> Bu dosya sp-mimari-web-uygulama becerisinin references dosyasıdır; gövdedeki 2. ve 4. bölümlerin ayrıntısını taşır. Başlık ve CSP değerleri beceriye gömülmez; release anında resmî kaynaktan doğrulanır.

## 1. Oturum

1.1. Oturum çerezi proje öneklidir; strict mode, yalnız çerez, httponly ve samesite=Lax açıktır; HTTPS'te secure zorunludur.
1.2. Girişte oturum kimliği yenilenir (session_regenerate_id(true)); eski kimlik kullanılamaz.
1.3. Hareketsizlik ve mutlak oturum süreleri tanımlıdır; süre aşımında oturum sunucuda sonlandırılır ve kullanıcı girişe yönlendirilir.
1.4. Oturum verisi istemcide taşınmaz; çerez yalnız kimlik taşır.
1.5. Çıkışta oturum verisi ve çerez sunucu tarafında geçersiz kılınır.

## 2. Parola

2.1. Parolalar bcrypt (cost en az 12) veya argon2id ile hashlenir; düz metin parola hiçbir katmanda (log, hata, denetim, yedek) bulunmaz.
2.2. Parola sıfırlama belirteci tek kullanımlıktır, sürelidir ve sabit zamanlı karşılaştırılır.
2.3. Parola alanı hiçbir log ve hata mesajına yazılmaz.

## 3. CSRF

3.1. Durum değiştiren her istekte CSRF zorunludur; GET, HEAD ve OPTIONS muaftır.
3.2. Belirteç gövde alanı ve X-CSRF-Token başlığıyla taşınır; taşıyıcılardan biri eksik veya geçersizse istek 403 döner.
3.3. Doğrulama hash_equals ile sabit zamanlı yapılır.
3.4. htmx isteklerinde belirteç tek istemci sözleşmesinden (configRequest) eklenir; modül içinde ikinci başlık kopyası yoktur.

## 4. Yetki

4.1. Yetki rol tabanlıdır ve roller tek katalogda tanımlıdır; sayfa, menü ve API aynı katalogdan beslenir.
4.2. Yetkisiz istek 403 döner ve denetim kaydına yazılır; yetki denetimi veri kapsamında SQL katmanında da uygulanır.
4.3. Rol kontrolü istemciye bırakılmaz; istemci yalnız görünürlüğü yönetir.
4.4. Yetki yükseltme gerektiren işlemler ayrıca açık onay ister.

## 5. Hız sınırı ve denetim

5.1. Giriş ve parola sıfırlama uçlarında ayrı hız sınırları vardır; eşik aşımı 429 döner.
5.2. Denetim kaydı fail-closed çalışır: yazılamayan denetim işlemi tamamlanmaz.
5.3. Yalnız adı açıkça geçen okuma eylemleri denetim dışıdır; varsayılan loglanır.
5.4. Denetim kaydı kim, ne, ne zaman ve sonuç alanlarını taşır; parola, token ve kişisel veri maskelenir.

## 6. Yükleme

6.1. Yükleme boyut, MIME türü ve dosya imzası doğrulanmadan kabul edilmez; istemci dosya adına güvenilmez.
6.2. Dosya adı sunucuda üretilir; uzantı beyaz listeye göre doğrulanır.
6.3. Yükleme dizini sürüm dışıdır, script çalıştırmaya kapalıdır ve yalnız doğrulanmış dosya olarak sunulur.
6.4. Yükleme hatası Türkçe ve alanı işaret eden mesajla döner.

## 7. Sırlar ve maskeleme

7.1. Sırlar yalnız ortam değişkeni dosyasından veya secret manager'dan gelir; kod, depo, log ve hata mesajında düz metin sır yoktur.
7.2. Ortam dosyası sürüm dışıdır ve depoya girmez; yükleyici mevcut ortam değişkenlerini ezmez.
7.3. Loglarda parola, token, kart ve kişisel veri [MASKELI] olarak maskelenir; maskesiz kayıt güvenlik ihlalidir.
7.4. Anahtar rotasyonu ve erişim izinleri release kaydında belgelenir.

## 8. Release başlıkları

8.1. HTTPS zorunludur; HTTP istekleri kalıcı yönlendirme ile HTTPS'e taşınır.
8.2. HSTS includeSubDomains ve sabit max-age ile yayınlanır; X-Content-Type-Options: nosniff ve Referrer-Policy eksiksizdir.
8.3. CSP'de script-src içinde unsafe-inline ve unsafe-eval yoktur; object-src none ve frame-ancestors none olur. Stil katmanı için gereken izin gerekçelendirilir ve motor davranışı resmî kaynaktan doğrulanır.
8.4. Başlık değerleri ve SRI hash'leri beceriye gömülmez; release anında resmî kaynaktan alınır ve kayda geçer.
8.5. Başlık doğrulaması release kapısıdır; gövdedeki mod sözleşmesine göre yüklenir.
