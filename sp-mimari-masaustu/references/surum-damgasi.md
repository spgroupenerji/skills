# Sürüm Damgası

> Gövde §2 ve §7'nin ayrıntısı: biçim, tek kaynak, dört tüketici, saat dilimi ve eşitlik.

## 1. Biçim

1.1. Damga `vYYYYMMDDHHMM` biçimindedir: küçük v öneki ve on iki haneli tarih-saat.
1.2. Hane sırası yıl, ay, gün, saat ve dakikadır; saniye ve salise yoktur.
1.3. Ek harf, ayraç, boşluk ve alt çizgi kullanılmaz; değer ASCII ve sıralanabilir kalır.
1.4. Örnek biçim: `v202610301530`.

## 2. Tek üretim noktası

2.1. Damga yalnız üretim betiğinde, derleme başlamadan önce bir kez üretilir.
2.2. Uygulama kodu, yardımcı araç ve elle işlem damga hesaplamaz; betik dışında ikinci üretici yoktur.
2.3. Derleme başına tek damga üretilir; aynı derlemede ikinci damga üretilmez.
2.4. Damga değeri betik içinde tek değişkende tutulur ve tüm adımlara bu değer geçirilir.

## 3. Yayılım: tek kaynak, dört tüketici

3.1. Dosya adı: artefakt adındaki damga.
3.2. Uygulama içi sürüm: derleme sırasında uygulamaya aktarılan sürüm bilgisi.
3.3. Hakkında ekranı: kullanıcıya gösterilen sürüm değeri.
3.4. Release kaydı: derleme raporundaki damga.
3.5. Dört tüketici aynı değeri taşır; hiçbirinde ikinci sürüm sabiti veya türetilmiş farklı biçim yoktur.

## 4. Saat dilimi politikası

4.1. Proje tek saat dilimi politikası tanımlar; tercih UTC'dir.
4.2. Yerel saat kullanılacaksa yaz saati geçişindeki tekrar ve atlama yazılı olarak belgelenir.
4.3. Aynı damganın iki farklı ana karşılık gelmemesi esastır; çakışma riski varsa UTC kullanılır.
4.4. Politika tek yerde tanımlanır; ortam değişkeniyle sessizce değiştirilmez.

## 5. Yaşam döngüsü

5.1. Üret: damga betikte oluşturulur ve biçim doğrulanır.
5.2. Aktar: damga uygulamaya derleme öncesinde tek kaynaktan verilir.
5.3. Derle: uygulama sürüm bilgisini bu değerle taşır.
5.4. Doğrula: dosya adı, uygulama içi sürüm ve Hakkında değeri karşılaştırılır.
5.5. Damga hatalıysa elle düzeltilmez; betik yeniden çalıştırılıp yeni derleme üretilir.
5.6. Yayınlanmış damga geriye dönük değiştirilmez; yeni derleme yeni damga alır.

## 6. Eşitlik doğrulaması

6.1. Betik, dosya adındaki damgayı uygulama içi sürümle karşılaştırır.
6.2. Hakkında ekranındaki değer de aynı damgayı göstermelidir; farklıysa artefakt yayınlanmaz.
6.3. Karşılaştırma birebir dize eşitliğidir; büyük-küçük harf veya biçim dönüşümü yapılmaz.
6.4. Eşitlik kanıtı release kaydına yazılır.

## 7. Yasaklar

- Elle yazılmış veya elle düzeltilmiş damga.
- Koda gömülü ikinci sürüm sabiti.
- Dosya adına bir damga, uygulamaya başka sürüm bilgisi verme.
- Aynı derlemede iki damga üretme.
- Damgayı zamandan bağımsız sabitleme.

## 8. Kontrol listesi

- [ ] Biçim `vYYYYMMDDHHMM`; sıralanabilir ve ASCII.
- [ ] Damga yalnız betikte, derleme başına bir kez üretiliyor.
- [ ] Dosya adı, uygulama içi sürüm, Hakkında ve release kaydı aynı değeri taşıyor.
- [ ] Saat dilimi politikası tek yerde ve yazılı.
- [ ] Eşitlik doğrulaması betikte otomatik.
- [ ] Elle damga yazma ve ikinci sürüm kaynağı yok.
