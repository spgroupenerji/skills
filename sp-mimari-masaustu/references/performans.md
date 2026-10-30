# Performans ve Erişilebilirlik Ölçümü

> Gövde §7'nin ölçüm ayrıntısı: kare bütçesi, P95 ve erişilebilirlik kanıtı.

## 1. Hedefler

1.1. Hedef 120 Hz'dir; garanti değildir. Kare bütçesi 1000/120 ms (yaklaşık 8,3 ms) olup düzen, boya, GPU ve kompozitör maliyetini kapsar.
1.2. Yalnız çizim süresi ölçüm sayılmaz; tam kare süresi ölçülür.

## 2. Ölçüm koşulları

2.1. Ölçüm release derlemesinde, tam pencerede ve temsili veriyle yapılır.
2.2. FPS izleme katmanı çekirdek yeniden dışa aktarım yüzeyinde olmayabilir; ayrı bağımlılık olarak eklenir, sağlayıcı ve sürüm resmî kaynaktan doğrulanır.
2.3. Ortam bilgisi kaydedilir: güç modu, dikey eşitleme, DPI ölçeği, ekran yenileme hızı.
2.4. Animasyonlu ekran, yoğun liste ve etkileşim akışı ayrı ölçülür.

## 3. Rapor

3.1. Rapor ortalama değil kare süresi dağılımı ve P95 içerir.
3.2. P95 kare bütçesinin altında olmalıdır; aşım yazılı gerekçe ve release kaydı olmadan kabul edilmez.
3.3. Önce ve sonra karşılaştırması aynı koşullarda ve aynı veriyle yapılır.

## 4. Erişilebilirlik ölçümü

4.1. Erişilebilirlik ağacında her etkileşimli öğe rol, ad, durum ve eylemleriyle doğrulanır.
4.2. Başsız ağaç testi tek başına kanıt değildir; IME ve ekran okuyucu gerçek pencere testi gerekir.
4.3. WCAG 2.2 AA hedefi tasarım becerisinde tanımlıdır; mimari ölçüm erişilebilirlik gerilemesi olmadığını kanıtlar.

## 5. Regresyon

5.1. Performans regresyonu şüphesinde ölçüm üç kez tekrarlanır; medyan ve P95 birlikte değerlendirilir.
5.2. Optimizasyon yalnız ölçümle doğrulanan darboğazda yapılır; ölçümsüz optimizasyon yoktur.
5.3. Regresyon kabul edilmezse yayın durur; istisna release kaydında gerekçelenir.

## 6. Dev modu

6.1. Dev modda FPS ölçümü zorunlu değildir; render veya eşzamanlılığa dokunan değişiklikte hedefli ölçüm yapılır.

## 7. Kontrol listesi

- [ ] Ölçüm release, tam pencere ve temsili veriyle yapıldı.
- [ ] Rapor kare süresi dağılımı ve P95 içeriyor.
- [ ] P95 kare bütçesinin altında; aşım gerekçeli kayıtlı.
- [ ] Erişilebilirlik ağacı rol, ad, durum ve eylemleri doğruluyor.
- [ ] IME ve ekran okuyucu gerçek pencere testi kayıtlı.
- [ ] Ölçüm ortamı (güç modu, DPI, yenileme) kayıtlı.
