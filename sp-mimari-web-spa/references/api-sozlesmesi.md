# api-sozlesmesi — sözleşme-önce, tipli istemci, sözleşme testleri

> Bu dosya sp-mimari-web-spa becerisinin references dosyasıdır; gövdedeki 5. bölümün ayrıntısını taşır. API davranışı sürüm dokümanından doğrulanır; beceriye sürüm iddiası yazılmaz.

## 1. Sözleşme-önce

1.1. Her uç için metot, yol, girdi şeması, çıktı şeması, hata kodları ve yetki gereksinimi önce yazılır.
1.2. Sözleşme tek dizinde tutulur ve sürüm kontrolündedir; istemci tipleri buradan türetilir.
1.3. Uç ekleme veya değiştirme sırası: sözleşme, test, sunucu, istemci. Ters sıra yasaktır.
1.4. Sözleşmesi olmayan uç release'e çıkmaz.
1.5. Sözleşme değişikliği tek konu taşır; biçim değişikliği işlev değişikliğiyle karıştırılmaz.

## 2. Zarf ve hata sözlüğü

2.1. Başarı yanıtı veri alanı taşır; hata yanıtı kod, mesaj ve alan listesi taşır; iki biçim karışmaz.
2.2. HTTP durumu ile uygulama hata kodu uyumludur; 200 içinde hata taşınmaz.
2.3. Hata kodları sözlüğü tek yerde tanımlıdır; aynı durum farklı kodla dönmez.
2.4. Doğrulama hatası alan bazında listelenir ve Türkçe mesaj taşır.
2.5. Sunucu hatası istemciye ayrıntı vermez; izleme kimliği döner, ayrıntı sunucu logundadır.

## 3. Tipli istemci

3.1. İstemci tipleri sözleşmeden üretilir; elle yazılıyorsa tek kaynak dosyadır; any yoktur.
3.2. Çalışma zamanı yanıtları şemaya göre doğrulanır; doğrulanmayan yanıt işlenmez.
3.3. İstemci iş kuralı taşımaz; hesaplama ve yetki sunucudadır.
3.4. İstemci dört durumu tanımlar: yükleniyor, boş, hata, yetkisiz; hata mesajı kullanıcıya gösterilir.
3.5. Ortak istek katmanı CSRF başlığını, hata eşlemesini ve yetkisiz yönlendirmeyi tek yerden yönetir.

## 4. Sürümleme ve uyumluluk

4.1. API sürümü açıkça belirtilir (yol veya başlık); sürümsüz uç release'e çıkmaz.
4.2. Kırıcı değişiklik yeni sürümle gelir; istemci aynı anda yeni sürüme geçirilir.
4.3. Alan ekleme geriye uyumludur; alan kaldırma ve tip değişimi kırıcıdır.
4.4. Eski sürümün kaldırılması tarih ve kayıtla yapılır; sessizce kapatılmaz.
4.5. Sözleşme değişiklikleri changelog'da tek satırla izlenir.

## 5. Ortak davranışlar

5.1. Sayfalama, filtre ve sıralama parametreleri sözleşmede tek kez tanımlanır.
5.2. Durum değiştiren uçlarda idempotency anahtarı desteklenir; tekrarlanan istek aynı sonucu verir.
5.3. Hız sınırı ve hata kodları istemcide işlenebilir biçimde belgelenir.
5.4. Tarih, sayı ve para biçimi sözleşmede sabittir; istemci kendi biçimini üretmez.
5.5. Yetki gereksinimi her uçta açıkça yazılır; gizli varsayım bırakılmaz.

## 6. Sözleşme testleri

6.1. Her uç için başarı ve hata durumları test edilir: 401, 403, 404, 422 ve CSRF'siz istek.
6.2. Testler şema doğrulaması içerir; yanıt şeması dışına çıkan test başarısızdır.
6.3. Sözleşme değişikliğinde testler birlikte güncellenir; test kırığı görmezden gelinmez.
6.4. Test sonuçları release kaydına bağlanır; sözlü beyan kanıt sayılmaz.
6.5. Test verisi üretim verisi içermez; kişisel veri test ortamına kopyalanmaz.
