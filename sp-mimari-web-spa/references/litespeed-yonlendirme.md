# litespeed-yonlendirme — /api ve SPA fallback

> Bu dosya sp-mimari-web-spa becerisinin references dosyasıdır; gövdedeki 3. bölümün ayrıntısını taşır. Sunucu davranışı çalışma anında gerçek yanıtlarla doğrulanır.

## 1. Yönlendirme sözleşmesi

1.1. İstek sırası: yasak yollar reddedilir; /api/* kök api.php'ye; var olan statik dosya doğrudan; diğer GET ve HEAD yolları kök index.html'e.
1.2. Fallback yalnız GET ve HEAD için çalışır; POST, PUT, PATCH ve DELETE fallback'e düşmez; 404 veya 405 döner.
1.3. Var olmayan varlık (uzantılı yol veya varlık dizini) index.html yerine 404 döner.
1.4. Bilinmeyen /api/* yolu PHP tarafında JSON 404 döner; HTML gövde dönmez.
1.5. /api dışındaki bilinmeyen yollar SPA'ya devredilir; derin bağlantı 200 döner.
1.6. Doğrudan /api.php isteği işlenmez ve 403 döner; API yalnız /api/* üzerinden çağrılır.

## 2. Sunucu yapılandırması

2.1. Kurallar .htaccess içinde sıralıdır: önce yasak yol ve dosya reddi, sonra /api → api.php yönlendirmesi, sonra gerçek dosya/dizin koşulu, sonra fallback. Sıra değiştirilmez.
2.2. Fallback koşulu yalnız istenen yol gerçek dosya veya dizin değilse çalışır; mevcut varlıklar ezilmez.
2.3. Dizin listeleme, nokta dosyaları ve yedek/uzantı dosyaları HTTP'ye kapalıdır.
2.4. PHP çalıştırma beyaz listedir: yalnız api.php, merkez.php, deploy/deploy.php ve seo/sitemap-generator.php çalışır. config.php dahil diğer PHP dosyaları HTTP'den çalışmaz, yalnız include edilir.
2.5. Sunucu yapılandırması sürüm kontrolündedir; elle panel değişikliği kayda geçer.
2.6. LiteSpeed'in Apache uyumlu kuralları kullanılır; davranış sürüme göre varsayılmaz, gerçek istekle doğrulanır.
2.7. Şu yollar HTTP'ye kapalıdır: `spa/`, `python_daq/`, `log/`, `deploy/.env`, `.env`, `config.php`, `package.json`, `tsconfig*.json`, `vite.config.*`, `requirements.txt`, `*.sqlite*`, `*.parquet`. Kökte yalnız yayın çıktısı, `assets/` medyası ve beyaz listedeki PHP girişleri servis edilir.
2.8. /api/* yolu kök api.php dosyasına yol ve sorgu dizesi korunarak yönlendirilir; alt dizin varsayımı yapılmaz.

## 3. Önbellek ve başlıklar

3.1. index.html no-cache veya no-store ile servis edilir; kullanıcıya özel veri içermez.
3.2. `public/` altındaki hash'li varlıklar uzun ömürlü ve immutable önbellekle sunulur.
3.3. `assets/` altındaki medya hash'sizdir; dosya adı sürümlenir veya kısa ömürlü önbellek verilir, immutable işaretlenmez.
3.4. API yanıtları önbelleklenmez; kimlik doğrulamalı veri önbellek anahtarına girmez.
3.5. MIME türleri doğru verilir; bilinmeyen türde içerik kehaneti yapılmaz.

## 4. Doğrulama

4.1. Derin bağlantı (örnek: /panel/rapor/42) curl ile 200 döner ve index.html içerir.
4.2. Var olan /api ucu PHP yanıtı verir; bilinmeyen /api yolu JSON 404 döner.
4.3. Sağlık ucu yanıtı doğrulanır; API'nin PHP tarafından çalıştığı kanıtlanır.
4.4. Eksik statik varlık 404 döner; POST fallback'e düşmez.
4.5. Yönlendirme tablosu release kapısında yeniden doğrulanır (references/kabul-kapilari.md).
4.6. Deny probu: `spa/main.tsx`, `package.json`, `config.php`, `log/deploy.log` ve `python_daq/index.py` 403 döner; api.php doğrudan çağrıldığında 403 döner.
