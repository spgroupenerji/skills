# litespeed-yonlendirme — /api ve SPA fallback

> Bu dosya sp-mimari-web-spa becerisinin references dosyasıdır; gövdedeki 3. bölümün ayrıntısını taşır. Sunucu davranışı çalışma anında gerçek yanıtlarla doğrulanır.

## 1. Yönlendirme sözleşmesi

1.1. İstek sırası: /api/* PHP'ye; var olan statik dosya doğrudan; diğer GET ve HEAD yolları index.html'e.
1.2. Fallback yalnız GET ve HEAD için çalışır; POST, PUT, PATCH ve DELETE fallback'e düşmez; 404 veya 405 döner.
1.3. Var olmayan varlık (uzantılı yol veya varlık dizini) index.html yerine 404 döner.
1.4. Bilinmeyen /api/* yolu PHP tarafında JSON 404 döner; HTML gövde dönmez.
1.5. /api dışındaki bilinmeyen yollar SPA'ya devredilir; derin bağlantı 200 döner.

## 2. Sunucu yapılandırması

2.1. Kurallar .htaccess içinde sıralıdır: önce /api yönlendirmesi, sonra gerçek dosya/dizin koşulu, sonra fallback. Sıra değiştirilmez.
2.2. Fallback koşulu yalnız istenen yol gerçek dosya veya dizin değilse çalışır; mevcut varlıklar ezilmez.
2.3. Dizin listeleme, nokta dosyaları ve yedek/uzantı dosyaları HTTP'ye kapalıdır.
2.4. PHP işleyicisi /api yoluna bağlanır; API dışına PHP çalıştırma izni verilmez.
2.5. Sunucu yapılandırması sürüm kontrolündedir; elle panel değişikliği kayda geçer.
2.6. LiteSpeed'in Apache uyumlu kuralları kullanılır; davranış sürüme göre varsayılmaz, gerçek istekle doğrulanır.

## 3. Önbellek ve başlıklar

3.1. index.html no-cache veya no-store ile servis edilir; kullanıcıya özel veri içermez.
3.2. Hash'li varlıklar uzun ömürlü ve immutable önbellekle sunulur.
3.3. API yanıtları önbelleklenmez; kimlik doğrulamalı veri önbellek anahtarına girmez.
3.4. MIME türleri doğru verilir; bilinmeyen türde içerik kehaneti yapılmaz.

## 4. Doğrulama

4.1. Derin bağlantı (örnek: /panel/rapor/42) curl ile 200 döner ve index.html içerir.
4.2. Var olan /api ucu PHP yanıtı verir; bilinmeyen /api yolu JSON 404 döner.
4.3. Sağlık ucu yanıtı doğrulanır; API'nin PHP tarafından çalıştığı kanıtlanır.
4.4. Eksik statik varlık 404 döner; POST fallback'e düşmez.
4.5. Yönlendirme tablosu release kapısında yeniden doğrulanır (references/kabul-kapilari.md).
