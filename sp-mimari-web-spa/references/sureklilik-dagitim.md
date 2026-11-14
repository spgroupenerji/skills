# sureklilik-dagitim — mevcut DB ve deploy koruma, smoke, rollback

> Bu dosya sp-mimari-web-spa becerisinin references dosyasıdır; gövdedeki 6. bölümün ayrıntısını taşır. Yalnız release tetiklendiğinde yüklenir.

## 1. Süreklilik ilkeleri

1.1. Mevcut MySQL veritabanı ve mevcut deploy/ mekanizması (GitHub kancası + `git merge --ff-only`) korunur; yerine ikinci dağıtım hattı kurulmaz.
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

3.1. Sıra: `npm run yayin`, kök çıktı diff kontrolü, commit (kaynak + çıktı), push, GitHub kancası, `git merge --ff-only`, smoke.
3.2. Atomiklik commit düzeyindedir: kaynak ve yayın çıktısı aynı commit'te gider; sunucu ikisini tek birleştirmeyle alır. Ayrı dizin veya sembolik bağlantıyla geçiş yoktur.
3.3. Rollback hedefi önceki yayın commit'idir; `git revert` + push, kanca geri çeker; sunucuda elle dosya geri alınmaz.
3.4. Yayınlanmış geçmiş yeniden yazılmaz; force-push ve rebase yasaktır, sunucu yalnız ileri sarımlı birleştirir.
3.5. Canlı dizin elle düzenlenmez; ortam dosyası ve kullanıcı verileri dağıtımda ezilmez; `uploads/` kapsam dışıdır ve kanca öncesi `_yedek` arşiviyle korunur.
3.6. Dağıtım sırasında elle SQL çalıştırılmaz; şema hattan uygulanır.
3.7. Dağıtım sonrası PHP OPcache temizlenir (kanca birleştirme sonrası) ve sağlık kontrolü yapılır.

## 4. Smoke ve rollback

4.1. Ön smoke: build temizliği, sözleşme testleri, kök yayın statik taraması, bundle bütçesi, ikinci çalıştırmada idempotent fark kontrolü.
4.2. Son smoke: derin bağlantı 200, /api/* PHP yanıtı, oturumsuz korumalı uç 401, CSRF'siz POST 403, giriş ve bir listeleme akışı, eksik varlık 404.
4.3. Smoke başarısızsa rollback: yayın commit'ini `git revert` ile geri al ve push et; kanca çeker; veri göçü geriye dönük uyumluysa veri geri alınmaz.
4.4. Rollback adımı yazılıdır ve tatbikatla doğrulanır; sözlü tarif yeterli değildir.
4.5. Sonuçlar release kaydına yazılır; başarısız smoke release'i kapatır.

## 5. İzleme ve kanıt

5.1. Dağıtım sonrası hata oranı, 5xx ve oturum hataları kısa süre izlenir.
5.2. Sağlık ucu ve smoke çıktıları release kaydına eklenir.
5.3. Geri alma kararı ve gerekçesi aynı kayda yazılır.
