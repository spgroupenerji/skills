# Form, Lead ve Güvenlik

Bu dosya sp-mimari-web-site gövdesinin 5. bölümünü açar: form akışı, sunucu doğrulaması, CSRF ve otomasyon koruması, veri saklama, e-posta, sır/log ve güvenlik başlıkları. Her sürüm ve API davranışı çalışma anında doğrulanır.

## 1. Form akışı

1.1. Form POST ile sunucu ucuna gönderilir; veri GET parametresinde taşınmaz.
1.2. Yalnız amaca gerekli alanlar toplanır; özel nitelikli kişisel veri, kart bilgisi ve parola alanı tanıtım formunda bulunmaz.
1.3. Her alan görünür etiket taşır; hata mesajı alanın yanında, Türkçe ve eyleme dönüktür.
1.4. İstemci doğrulaması kullanıcı deneyimi içindir; sunucu doğrulaması zorunludur ve tek doğru kaynaktır.
1.5. Başarılı gönderim POST/Redirect/GET veya tek kullanımlık belirteçle yeniden gönderime karşı korunur.

## 2. Sunucu doğrulaması

2.1. Tip, uzunluk, biçim ve izinli değer kümesi doğrulanır; bilinmeyen alan reddedilir.
2.2. E-posta ve telefon normalize edilir; satır sonu, başlık enjeksiyonu ve kontrol karakterleri reddedilir.
2.3. Hata yanıtı stack trace, dosya yolu, SQL veya iç ayrıntı içermez; teknik ayrıntı sunucu loguna yazılır.
2.4. Kullanıcıya gösterilen tüm metin Türkçe ve imlâ kurallarına uygundur; alan adı ve hata nedeni açık yazılır.
2.5. Doğrulama kuralları tek yerde tanımlanır; form ucu ve istemci aynı kuralı farklı biçimde yorumlamaz.

## 3. CSRF ve otomasyon koruması

3.1. Durum değiştiren her POST CSRF belirteci taşır; belirteç sunucuda üretilir, süre ve tek kullanım denetlenir.
3.2. Belirteç taşıyan HTML paylaşımlı önbelleğe alınmaz; token istek anında üretiliyorsa önbellek no-store olur.
3.3. Honeypot alanı ve zaman tuzağı kullanılır; doldurulmuş veya insan dışı gönderim reddedilir, kullanıcıya genel hata döner.
3.4. Hız sınırı IP ve form anahtarına göre uygulanır; aşımda 429 ve Türkçe mesaj döner, sessiz yutma yapılmaz.
3.5. Üçüncü taraf CAPTCHA varsayılan değildir; zorunluysa gizlilik etkisi, CSP ve SRI sonuçları gerekçelenir.

## 4. Veri saklama ve erişim katmanı

4.1. Form verisi saklanacaksa yalnız gerekli kolonlar açılır; şema ve göç kuralları references/veri-tabani.md dosyasındadır.
4.2. Veritabanı erişimi yalnız veri erişim katmanından yapılır; şablon ve sunum dosyalarında SQL bulunmaz.
4.3. Tüm sorgular hazırlanmış deyimle çalışır; SQL metnine değer birleştirme yasaktır.
4.4. Lead için amaç, hukuki sebep ve saklama süresi aydınlatma metninde belgelenir; süre sonunda silme veya anonimleştirme işi tanımlıdır.
4.5. Yıkıcı işlem öncesi yedek alınır; geri yükleme bir kez denenerek kanıtlanır.

## 5. E-posta gönderimi

5.1. Gönderim alan adı SPF, DKIM ve DMARC kayıtlarıyla kimlik doğrulanmış olur; kayıtların varlığı DNS üzerinden doğrulanır.
5.2. Gönderim veritabanı transaction'ı dışında yapılır: önce commit, sonra gönderim; gönderim hatası loglanır, kullanıcıya Türkçe sonuç döner.
5.3. Kullanıcı girdisi e-posta başlığına ham girmez; konu ve şablon sabittir, adres alanı doğrulanmış tek adrese gider.
5.4. Gönderim hızı sınırlanır; tekrar denemede idempotency anahtarı kullanılır ve aynı bildirim iki kez üretilmez.

## 6. Sır ve log yönetimi

6.1. Sırlar yalnız .env veya secret manager'da tutulur; .env sürüm kontrolüne ve web erişimine kapalıdır, dosya izni kısıtlıdır.
6.2. Loglarda parola, token, kart verisi ve kişisel veri maskelenir; form gövdesi ve e-posta içeriği loga yazılmaz.
6.3. Log dosyaları web'den erişilemez; rotasyon ve saklama süresi tanımlıdır.
6.4. Debug modu üretimde kapalıdır; hata ayrıntısı yalnız sunucu loguna gider.

## 7. Güvenlik başlıkları

7.1. HTTPS zorunludur; HTTP isteği 301 ile HTTPS'e yönlendirilir, HSTS başlığı verilir.
7.2. CSP nonce veya hash tabanlıdır; default-src 'self' olur, script-src yalnız kendi kaynak ve zorunlu istisnayı içerir, object-src 'none' ve frame-ancestors 'none' kullanılır.
7.3. unsafe-inline ve unsafe-eval kullanılmaz; zorunlu istisna varsa gerekçesi ve kaynağı proje kaydına yazılır.
7.4. Token veya nonce taşıyan HTML no-store ile sunulur; statik HTML hash tabanlı CSP ile önbelleklenebilir.
7.5. nosniff, Referrer-Policy ve Permissions-Policy her yanıtta bulunur; sunucu imza başlıkları üretimde kapalıdır.
7.6. SRI yalnız zorunlu istisnada kullanılır; sürüm ve SRI değeri çalışma anında resmî kaynaktan doğrulanır, elle tahmin edilmez.

## 8. Dosya yükleme

8.1. Lead formunda dosya alanı varsayılan olarak yoktur; gerekiyorsa uzantı, MIME ve boyut doğrulanır.
8.2. İstemci dosya adına güvenilmez; ad sunucuda üretilir ve dosya web kökü dışında saklanır.
8.3. Yüklenen içerik çalıştırılmaz; indirme Content-Disposition ile yapılır.

## 9. Doğrulama

9.1. Başlık kontrolü canlı yanıtta yapılır: HTTPS yönlendirmesi, HSTS, CSP, nosniff, Referrer-Policy ve Permissions-Policy görünür.
9.2. CSRF'siz istek, honeypot doldurulmuş istek ve geçersiz alan reddedilir; yanıtlar Türkçe ve iç ayrıntısızdır.
9.3. Veritabanı erişiminde hazırlanmış deyim ve PDO bayrakları kanıtlanır; loglarda kişisel veri bulunmaz.
9.4. SPF, DKIM ve DMARC kayıtları DNS'te doğrulanır; test gönderimi ulaşır.
9.5. Form ucu, başlıklar ve CSP davranışı çalışma anında doğrulanır; varsayım yapılmaz.
