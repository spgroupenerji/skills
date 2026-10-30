# Platform ve CI

> Gövde §7'nin platform ayrıntısı: hedef platformlar, araç zinciri, CI matrisi ve başlatma sırası.

## 1. Hedefler

1.1. Birincil hedefler macOS ve Linux'tur (Wayland ve X11); Windows ikincil hedeftir.
1.2. Asgari macOS sürümü sürümün resmî kurulum belgesinden doğrulanır.
1.3. Birincil hedeflerin davranışını değiştiren Windows özel dalı eklenmez; platform betiği ve uyarlama katmanı serbesttir.
1.4. İş kuralı katmanında platform dalı bulunmaz; platform farkı yalnız uyarlama katmanında çözülür.

## 2. Linux

2.1. Çalışan bir Vulkan sürücüsü zorunludur; yalnız yükleyici paketini kurup sürücüyü atlamak yasaktır.
2.2. GPU'suz CI ortamında yazılım Vulkan (lavapipe veya llvmpipe) istisnası kullanılır; istisna release kaydına yazılır.
2.3. Sistem paketleri kurulum belgesindeki liste ile kurulur; eksik sistem bağımlılığıyla yeşil sonuç kabul edilmez.

## 3. macOS

3.1. Xcode Command Line Tools kurulu olmalıdır; eksik araç zinciriyle derleme yapılmaz.
3.2. macOS'a özgü davranış (menü, kısayol gösterimi, dosya diyalogları) uyarlama katmanında ve platform bilgisiyle çözülür.

## 4. Araç zinciri

4.1. Asgari Rust sürümü sürümün resmî kurulum belgesinden doğrulanır; daha eski araç zinciriyle derleme reddedilir.
4.2. Alt sınırı bir platform bağımlılığı belirleyebilir; `cargo tree` çıktısıyla doğrulanır.

## 5. CI matrisi

5.1. Matris macOS ve Ubuntu işlerinden oluşur; `fail-fast: false` ile bir işin hatası diğerini iptal etmez.
5.2. Runner etiketi sabitlenir; kayan `latest` etiketi yerine sabit imaj kullanılır.
5.3. Her iki iş yeşil olmadan artefakt üretilmez.
5.4. Bağımlılık önbelleği kullanılır; önbellek hiçbir kapıyı atlatmaz.

## 6. Kanıt komutları

6.1. `cargo build --release --locked` ve `cargo test --locked`.
6.2. `cargo fmt --check` ve `cargo clippy -- -D warnings`.
6.3. Ayrı GPUI paketi bağımlılık ağacında görünmez; arayüz kiti tek sürümdedir.
6.4. Derleme sonrası çalışma zamanı yükleyici ve sistem paketleri kontrol edilir.

## 7. Başlatma sırası

7.1. Uygulama sırası: kitaplık başlatma (ilk çağrı), uygulama döngüsü, pencere açma; kesin sıra ve dönüş tipleri sürümün resmî dokümanından doğrulanır.
7.2. Pencere içeriği tek kök görünüm tipidir; kökü saran tip ve dönüş tipi sürüm dokümanından doğrulanır.
7.3. Pencere açılamazsa uygulama Türkçe hata mesajıyla sıfır dışı kodla kapanır; hata sessizce yutulmaz.

## 8. Dev modu

8.1. Geliştirmede yalnız geçerli platformda `cargo check` ve etkilenen testler çalıştırılır.
8.2. Platforma özel derleme hatasında önce araç zinciri, sistem paketleri ve platform özellik bayrakları tanılanır.

## 9. Kontrol listesi

- [ ] İki platform işi de yeşil; matris `fail-fast: false`.
- [ ] Runner imajı sabit; sistem paketleri kurulum belgesiyle kurulu.
- [ ] Vulkan yükleyici ve sürücü doğrulandı; CI istisnası kayıtlı.
- [ ] Arayüz kiti tek sürüm; ayrı GPUI paketi yok.
- [ ] Başlatma sırası ve pencere kurulumu sürüm dokümanıyla doğrulandı.
- [ ] Pencere açılamama yolu Türkçe hata ve sıfır dışı çıkış üretiyor.
