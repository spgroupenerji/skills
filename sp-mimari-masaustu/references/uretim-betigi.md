# Üretim Betiği Sözleşmesi

> Gövde §3 ve §4'ün ayrıntısı: tek giriş noktası, parametreler, adım sırası, hata ve idempotans.

## 1. Giriş noktası

1.1. Tek giriş noktası vardır: damga, derleme, kopyalama, temizlik ve doğrulama aynı betikten yürür.
1.2. İkinci betik, kopya betik ve elle yapılan adım yoktur; zorunlu bir adım betikte tanımlıdır.
1.3. Betik proje kökünden çalışır; göreli yollar proje köküne göre çözülür, mutlak makine yolu gömülmez.
1.4. Betik sürüm kontrolündedir; derleme çıktısı ve release klasörü sürüm kontrolü dışındadır.

## 2. Parametreler

2.1. Uygulama adı parametredir; varsayılanı proje adıdır, `app-pdf` yalnız örnektir.
2.2. Çıktı klasörü parametredir; varsayılanı release klasörüdür.
2.3. Temiz derleme bayrağı parametredir ve varsayılan olarak kapalıdır.
2.4. Sır, kullanıcı yolu ve makineye özgü değer parametre olarak istenmez; sırlar ortamdan okunur ve günlüğe yazılmaz.
2.5. Parametre doğrulanmadan hiçbir adım başlamaz.

## 3. Ön kontrol

3.1. Derleme aracı ve sürüm alt sınırı doğrulanır; sürüm ve gereksinim resmî kaynaktan doğrulanır, varsayılmaz.
3.2. MuPDF C çekirdeği için gerekli yerel araç zinciri ve sistem bileşenleri doğrulanır.
3.3. Disk alanı ve çıktı klasörünün yazılabilirliği doğrulanır.
3.4. Eksik bileşen varsa betik derlemeye başlamadan, eksik bileşen ve çözüm yolu gösteren Türkçe mesajla durur.

## 4. Adım sırası

4.1. Damga üretimi: biçim ve saat dilimi kurallarına göre tek damga üretilir (bkz. references/surum-damgasi.md).
4.2. Derleme: release profili kullanılır; ilk derlemede GPUI ve MuPDF C çekirdeği sıfırdan derlenir, sonraki derlemeler artımlıdır.
4.3. Çıktı kontrolü: derleme çıktısı var, boyutu sıfırdan büyük ve çalıştırılabilir uzantıdadır.
4.4. Geçici kopya: çıktı, hedef klasörde damgasız geçici ada kopyalanır; kopya boyutu kaynakla karşılaştırılır.
4.5. Atomik taşıma: geçici dosya nihai damgalı ada tek işlemle taşınır; aynı ad varsa üzerine yazılır.
4.6. Temizlik: yeni artefakt doğrulandıktan sonra önceki damgalı sürümler silinir (bkz. references/artefakt-ve-temizlik.md).
4.7. Doğrulama: ad ve damga biçimi, tek dosya kuralı, sürüm eşitliği ve çalıştırma smoke'u kontrol edilir.
4.8. Rapor: damga, derleme türü, süre sınıfı, dosya adı, boyut ve smoke sonucu yazılır.

## 5. Hata yönetimi

5.1. İlk hata betiği durdurur; sonraki adımlar çalıştırılmaz.
5.2. Başarıda çıkış kodu 0, hatada sıfır dışı çıkış kodu döner.
5.3. Hata mesajı Türkçe, kısa ve eyleme dönüktür; hangi adımın neden durduğunu söyler.
5.4. Kısmi sonuç bırakılmaz: geçici dosya ve yarım artefakt temizlenir.
5.5. Başarısız derleme veya kopyalamada mevcut eski artefakt korunur; silme yapılmaz.
5.6. Hata ayrıntısı kullanıcıya stack trace veya makine yolu olarak gösterilmez; günlükte tutulur.

## 6. Idempotans ve tekrar çalıştırma

6.1. Betik art arda iki kez çalıştırılabilir; her çalıştırma tek artefakt bırakır ve çıkış kodu 0 olur.
6.2. Aynı dakika içindeki iki çalıştırma aynı damgayı üretir; üzerine atomik yazma nedeniyle ikinci dosya oluşmaz.
6.3. Farklı dakikadaki çalıştırma yeni damga üretir ve önceki artefakt temizlik adımında kaldırılır.
6.4. Yarım kalmış önceki çalıştırmadan kalan geçici dosya, yeni çalıştırmanın ön kontrolünde temizlenir.

## 7. Günlük ve süre raporu

7.1. Her adımın başında tek satır ilerleme bilgisi verilir; hata ayrıntısı yalnız hata anında yazılır.
7.2. İlk derleme ile artımlı derleme süresi ayrı raporlanır; kullanıcı ilk derlemenin uzun süreceğini önceden bilir.
7.3. Günlükte sır, parola, kişisel veri ve kullanıcıya ait tam dosya yolu bulunmaz.

## 8. Yasaklar

- Elle kopyalama veya elle damga yazma.
- İkinci betik ya da betik dışı zorunlu adım.
- Derleme adımını atlayıp eski çıktıyı kopyalama.
- Betiğe mutlak yol, sır veya makineye özgü değer gömme.
- Hata durumunda eski artefaktı silme.

## 9. Kontrol listesi

- [ ] Tek giriş noktası; ikinci betik ve elle adım yok.
- [ ] Parametreler dışarıdan; mutlak yol ve sır gömülü değil.
- [ ] Ön kontrol araç zinciri ve C çekirdeği gereksinimlerini doğruluyor.
- [ ] Adım sırası gövde §3.2 ile aynı.
- [ ] Hata sıfır dışı kodla duruyor, geçici/yarım dosya bırakmıyor.
- [ ] İki kez çalıştırma tek artefakt ve başarıyla bitiyor.
