# Araç (Tool) Tasarımı

> Gövde §4'ün ayrıntısı. Şema biçimi ve SDK API'si çalışma anında doğrulanır.

## 1. Araç sınırı
1.1. Araç iş akışını temsil eder: "kayıt oluştur", "raporu dışa aktar", "durumu getir".
1.2. Düşük seviye eylem (tıklama, koordinat, ham denetim) araç olmaz; gerekliyse iş akışı aracının içinde kalır.
1.3. Aynı işi yapan iki araç yoktur; ad ve kapsam çakışmaz.
1.4. Araç adı ASCII, kararlı ve tekil; yeniden adlandırma kırıcı değişikliktir.

## 2. Açıklama şablonu
2.1. Amaç: ne yapar, hangi işi tamamlar.
2.2. Kullanım: hangi durumda çağrılır, hangi durumda çağrılmaz.
2.3. Girdi: alan biçimi, birim, aralık, varsayılan.
2.4. Yan etki: yazma, dışa gönderme, silme; geri alınabilir mi.
2.5. Hata: doğrulama, yetki, bulunamadı, çakışma.
2.6. Açıklama Türkçe ve kısa; modelin karar vereceği ayrımı içerir.

## 3. Şema
3.1. Parametreler tipli modelden üretilir; serbest nesne ve `any` yoktur.
3.2. Zorunlu ve isteğe bağlı alanlar açık; varsayılan değer şemada görünür.
3.3. Sınırlar şemada: uzunluk, aralık, desen; iş kuralı doğrulaması ayrıca uygulamada.
3.4. `description` alanı her parametrede dolu; örnek değer geçerli biçimi gösterir.
3.5. Şema değişikliği sürüm notuna yazılır; eski istemci kırılıyorsa uyumluluk yolu tanımlanır.

## 4. Davranış
4.1. Girdi sınırda doğrulanır: tip, uzunluk, aralık, izin.
4.2. Yazma araçları idempotenttir veya idempotency anahtarı taşır.
4.3. Yıkıcı işlem uygulama içinde ayrıca Türkçe onay ister; modelin çağrısı onay değildir.
4.4. Toplu işlemde üst sınır ve sayfalama vardır; sınırsız liste dönmez.
4.5. Sonuç kısa ve yapılandırılmış; sır, token ve PII içermez; büyük çıktı özetlenir ve kesme bildirilir.
4.6. Araç düzeyi hata ile protokol hatası ayrılır; yığın izi ve iç yol sızmaz.
4.7. Çağrılar eşzamanlı gelebilir; sıraya duyarlı işler tek kuyrukta serileştirilir.
4.8. Uzun iş ilerleme bildirir ve iptal edilebilir; iptal GUI tarafında da uygulanır.

## 5. Katalog ve sürüm
5.1. Araç listesi tek manifestten üretilir; manifest özeti sürüm el sıkışmasında taşınır.
5.2. Kullanımdan kaldırma: önce açıklamada işaretle, sonra kaldır; sessiz kaldırma yok.
5.3. Araç sayısı iş yüküne göre sınırlı tutulur; aynı amaca hizmet eden araç çoğaltılmaz.

## 6. Kontrol listesi
- [ ] Araçlar iş akışı düzeyinde; düşük seviye UI aracı yok.
- [ ] Her araç için açıklama ve parametre açıklamaları dolu.
- [ ] Şemada serbest nesne/any yok; sınırlar tanımlı.
- [ ] Yazma/yıkıcı işlem idempotency ve onay kuralına uyuyor.
- [ ] Sonuç boyutu ve hata ayrımı test edildi.