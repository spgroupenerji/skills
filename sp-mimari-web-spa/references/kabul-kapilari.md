# kabul-kapilari — geliştirme hızlı kontrolü ve release kapıları

> Bu dosya sp-mimari-web-spa becerisinin references dosyasıdır; gövdedeki 7. ve 8. bölümlerin kapı ayrıntısını taşır. Kapılar yalnız release veya risk sınıfı tetiklediğinde yüklenir; sürüm ve hash değerleri beceriye gömülmez.

## 1. İlkeler

1.1. Her kapı komut veya araç, beklenen sonuç ve tarihle kayda geçer.
1.2. Doğrulanamayan sonuç "doğrulanmalı" etiketiyle raporlanır; sözlü beyan kanıt yerine geçmez.
1.3. Başarısız kapıda release durur; istisna yalnız yazılı ve tarihli gerekçeyle açılır.
1.4. Atlanan kapı geçti sayılmaz; gerekçesiyle listelenir.

## 2. Geliştirme hızlı kontrolü (varsayılan)

2.1. Değişen dosyalarda tip kontrolü veya lint ve etkilenen testler çalışır.
2.2. Vite dev sunucusunda HMR ile ana akış kontrol edilir; API çağrıları PHP'ye gider.
2.3. Dev modda tam prod build, bundle ölçümü ve deploy yapılmaz.
2.4. Tarayıcı kontrolü Chrome DevTools ile yapılır: Console hatasızlığı, Network 4xx/5xx, erişilebilirlik sekmesi.
2.5. Hızlı kontrol tam ölçüm değildir; release kanıtı yerine geçmez.

## 3. Release — build ve dist

3.1. Lockfile'a göre kurulum ve npm run build temizdir: hata ve uyarı yoktur.
3.2. dist Node gerektirmez; statik sunucudan servis edilerek doğrulanır.
3.3. Bundle bütçesi ölçülmüş ve aşılmamıştır; sonuç kayıtlıdır.
3.4. dist içinde secret, ortam dosyası izi, kaynak haritası ve dev aracı yoktur; CDN referansı yoktur.
3.5. lockfile değişmişse gerekçe ve bağımlılık denetimi kaydı vardır.

## 4. Release — yönlendirme ve güvenlik

4.1. Derin bağlantı 200 döner ve index.html içerir.
4.2. /api/* PHP yanıtı verir; bilinmeyen API yolu JSON 404 döner.
4.3. Eksik statik varlık 404 döner; POST fallback'e düşmez.
4.4. CSRF'siz POST 403; oturumsuz korumalı uç 401; yetkisiz istek 403.
4.5. Oturum çerezi HttpOnly, Secure ve SameSite taşır; girişte oturum kimliği yenilenir.
4.6. CSP, HSTS, nosniff ve Referrer-Policy başlıkları doğrulanır; script-src içinde unsafe-inline ve unsafe-eval yoktur.
4.7. Erişilebilirlik ölçümü yapısal tasarım becerisinin kontrol listesine göre tamamlanmış ve kaydedilmiştir; ihlal varsa release edilmez.

## 5. Release — süreklilik ve dağıtım

5.1. Mevcut veritabanı ve deploy/ hattı kullanılmıştır; ikinci hat kurulmamıştır.
5.2. Göçler numaralı ve geriye dönük uyumludur; yedek ve onay kayıtlıdır.
5.3. Ön ve son smoke listesi çalıştırılmış; sonuçlar kayıtlıdır.
5.4. Rollback hedefi (önceki dist ve önceki API commit'i) kayıtlıdır.
5.5. Smoke başarısızlığında rollback adımı uygulanmış veya release kapatılmıştır.
5.6. Dağıtım sonrası OPcache temizliği ve sağlık kontrolü kayıtlıdır.

## 6. Kanıt biçimi

6.1. Release kaydı şu alanları taşır: tarih, kapsam, komut veya araç, beklenen sonuç, gerçek sonuç, karar.
6.2. Ölçüm dosyaları proje docs dizininde tutulur; beceriye sayı kopyalanmaz.
6.3. Sözleşme testi ve smoke çıktıları aynı kayda bağlanır.
