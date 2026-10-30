# sureklilik-dagitim — mevcut DB ve deploy koruma, smoke, rollback

> Bu dosya sp-mimari-web-spa becerisinin references dosyasıdır; gövdedeki 6. bölümün ayrıntısını taşır. Yalnız release tetiklendiğinde yüklenir.

## 1. Süreklilik ilkeleri

1.1. Mevcut MySQL veritabanı ve mevcut deploy/ mekanizması korunur; yerine ikinci dağıtım hattı kurulmaz.
1.2. Mevcut oturum ve API sözleşmeleriyle uyum gözetilir; SPA ikinci kimlik sistemi veya ikinci API katmanı kurmaz.
1.3. Mevcut yapılandırma ve ortam düzeni kullanılır; yeni anahtarlar belgelenir.
1.4. Değişiklikler eklemeli ve geri alınabilir olur; mevcut veri korunur.
1.5. Veritabanı ayrıntı disiplini mevcut panel mimarisi becerisinin alanındadır; bu dosya süreklilik ve dağıtım sınırını bağlar.

## 2. Göç

2.1. Şema değişiklikleri numaralı göç dosyalarıyla yapılır; elle ALTER yasaktır.
2.2. Göçler geriye dönük uyumludur: yeni alan veya tablo eklenir; kaldırma ayrı ve onaylı adımdır.
2.3. Yıkıcı değişiklik öncesi yedek alınır ve açık onay kayda geçer.
2.4. Göçler yalnız dağıtım hattından çalıştırılır; uygulama çalışırken elle şema değiştirilmez.
2.5. Göç sırası korunur; numara atlaması ve eksik down bloğu release engelidir.

## 3. Dağıtım

3.1. Sıra: temiz build, dist artefaktı, önceki sürümü yedekle, yeni dist'i yerleştir, PHP değişikliğini mevcut hatla uygula, smoke.
3.2. dist atomik geçer: yeni sürüm ayrı dizinde hazırlanır ve geçiş tek adımda yapılır veya sembolik bağlantıyla çevrilir.
3.3. Önceki dist ve önceki API commit'i rollback hedefi olarak kaydedilir; kayıtsız dağıtım reddedilir.
3.4. Ortam dosyası ve kullanıcı verileri dağıtımda ezilmez; yükleme dizini kapsam dışıdır.
3.5. Dağıtım sırasında elle SQL çalıştırılmaz; şema hattan uygulanır.
3.6. Dağıtım sonrası PHP OPcache temizlenir ve sağlık kontrolü yapılır.

## 4. Smoke ve rollback

4.1. Ön smoke: build temizliği, sözleşme testleri, dist statik taraması, bundle bütçesi.
4.2. Son smoke: derin bağlantı 200, /api/* PHP yanıtı, oturumsuz korumalı uç 401, CSRF'siz POST 403, giriş ve bir listeleme akışı, eksik varlık 404.
4.3. Smoke başarısızsa rollback: önceki dist'e dön, gerekirse önceki API commit'ine dön; veri göçü geriye dönük uyumluysa veri geri alınmaz.
4.4. Rollback adımı yazılıdır ve tatbikatla doğrulanır; sözlü tarif yeterli değildir.
4.5. Sonuçlar release kaydına yazılır; başarısız smoke release'i kapatır.

## 5. İzleme ve kanıt

5.1. Dağıtım sonrası hata oranı, 5xx ve oturum hataları kısa süre izlenir.
5.2. Sağlık ucu ve smoke çıktıları release kaydına eklenir.
5.3. Geri alma kararı ve gerekçesi aynı kayda yazılır.
