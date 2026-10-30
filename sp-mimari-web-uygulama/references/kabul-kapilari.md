# kabul-kapilari — geliştirme hızlı kontrolü ve release kanıtları

> Bu dosya sp-mimari-web-uygulama becerisinin references dosyasıdır; gövdedeki 8. ve 9. bölümlerin kapı ayrıntısını taşır. Kapılar yalnız release veya risk sınıfı tetiklediğinde yüklenir. Sürüm, SRI hash'i ve başlık değerleri beceriye gömülmez; çalışma anında resmî kaynaktan doğrulanır.

## 1. İlkeler

1.1. Her kapı komut veya araç, beklenen sonuç ve tarihle kayda geçer.
1.2. Doğrulanamayan sonuç "doğrulanmalı" etiketiyle raporlanır; sözlü beyan kanıt yerine geçmez.
1.3. Başarısız kapıda release durur; istisna yalnız yazılı ve tarihli gerekçeyle açılır.
1.4. Aynı kapı iki farklı araçla kanıtlanmaz; her kanıt kendi aracıyla üretilir.

## 2. Geliştirme hızlı kontrolü (varsayılan)

2.1. Değişen PHP dosyaları sözdizimi denetiminden geçer: php -l.
2.2. Statik grep seti: SELECT *, controller ve sayfa dizinlerinde PDO veya SQL metni, style= kullanımı, keyfi değer kalıpları, emoji, ikinci ikon seti, harici script, dinamik sürüm etiketi.
2.3. Tarayıcı kontrolü Chrome DevTools ile yapılır: Console hatasızlığı, Network 4xx/5xx, Accessibility sekmesi, reduced-motion emülasyonu, 320px yatay kaydırma.
2.4. Geliştirmede CSP, HSTS, SRI ve gzip kapıları çalıştırılmaz; bunlar release kapısıdır.
2.5. Hızlı kontrol tam ölçüm değildir; release kaydı yerine geçmez.

## 3. Release — ortam ve sürüm

3.1. Çalışma zamanı sürümü kayıtlı pin ile karşılaştırılır; sürüm numarası beceriye yazılmaz, envanterden okunur.
3.2. Oturum ini değerleri (strict mode, yalnız çerez, httponly, samesite, secure) ve uzantı envanteri doğrulanır.
3.3. Veritabanı sürümü, karakter kümesi ve kolasyonu sunucuda doğrulanır.
3.4. Ortam envanteri kaydı olmadan dağıtım yapılmaz.
3.5. Bilgi/hakkında sayfasındaki sürüm damgası `vYYYYMMDDHHMM` biçimindedir; release kaydı ve aynı adlı tag ile birebir aynıdır.

## 4. Release — güvenlik

4.1. Giriş ve yönetim uçlarında HSTS, CSP, nosniff ve Referrer-Policy başlıkları doğrulanır.
4.2. CSP script-src içinde unsafe-inline ve unsafe-eval yoktur; stil katmanı izni gerekçeli ve motor davranışına göre doğrulanmıştır.
4.3. CDN script etiketlerinde SRI ve crossorigin vardır; hash release anında resmî kaynaktan üretilir ve doğrulanır.
4.4. Eksik CSRF 403, yetkisiz erişim 403 ve hız sınırı aşımı 429 döner; denetim kaydı bu olayları içerir.
4.5. Ortam dosyası ve yükleme dizini HTTP'den erişilemez; yükleme dizini script çalıştırmaz.
4.6. Girişte oturum kimliği yenilenir; süre aşımı sunucuda sonlandırılır.

## 5. Release — veri ve göç

5.1. Uygulama dizinlerinde SELECT * ve emülasyonlu hazırlanmış deyim ayarı yoktur.
5.2. Yeni veya değişen karmaşık sorguların EXPLAIN kayıtları proje docs dizinindedir; tam tarama yoktur.
5.3. Göç numaraları boşluksuz, her dosyada up ve down blokları tam; elle ALTER veya DROP yoktur.
5.4. Uygulama kullanıcısında ALL PRIVILEGES yoktur; DDL yetkisi ayrı kullanıcıdadır.
5.5. BEGIN, COMMIT ve ROLLBACK yalnız merkezi sarmalayıcıda geçer; yedek ve geri yükleme tatbikatı kayıtlıdır.

## 6. Release — dağıtım ve ölçüm

6.1. Son birleştirme ff-only'dir; rollback commit'i ve sağlık kontrolü kayıtlıdır.
6.2. Kanca imzasız isteği 403 ile reddeder; panel tetiklemesi oturum, POST ve CSRF ister.
6.3. Dağıtım sonrası OPcache temizlenmiş ve sağlık kontrolü geçmiştir.
6.4. Yerel JS gzip toplamı ve toplam istemci varlığı proje bütçesine karşı ölçülmüş, sonuç kaydedilmiştir.
6.5. TTFB, API p95 ve LCP ölçümleri proje bütçesine karşı kaydedilmiştir.
6.6. Erişilebilirlik ölçümü yapısal tasarım becerisinin kontrol listesine göre tamamlanmış ve kaydedilmiştir; ihlal varsa release edilmez.
6.7. Yapısal UI ve erişilebilirlik ayrıntı kapıları tasarım becerisinin kabul kapısındadır; bu dosya yalnız ölçüm ve kayıt zorunluluğunu bağlar.

## 7. Kanıt biçimi

7.1. Release kaydı şu alanları taşır: tarih, kapsam, komut veya araç, beklenen sonuç, gerçek sonuç, karar.
7.2. Başarısız veya atlanan kapı gerekçesiyle listelenir; atlanan kapı geçti sayılmaz.
7.3. Ölçüm dosyaları proje docs dizininde tutulur; beceriye sayı kopyalanmaz.
