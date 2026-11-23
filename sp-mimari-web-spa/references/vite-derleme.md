# vite-derleme — build modeli, kök yayın, env, bütçe

> Bu dosya sp-mimari-web-spa becerisinin references dosyasıdır; gövdedeki 2. bölümün ayrıntısını taşır. Sürüm iddiaları burada tutulmaz; çalışma anında resmî kaynaktan doğrulanır.

## 1. Model

1.1. Node yalnız geliştirme ve derleme zamanında çalışır; üretimde Node çalışmaz.
1.2. Çalışma zamanı üç parçadır: LiteSpeed'in kökten sunduğu derleme çıktısı, PHP API ve Python arka plan veri servisi. Dördüncü bir çalışma zamanı bileşeni eklenmez.
1.3. Vite geliştirmede HMR verir; üretim çıktısı statik dosyalardır.
1.4. React istemci yönlendirme kullanır; sunucu tarafı render yoktur.

## 2. Proje ve bağımlılık

2.1. Kaynak ağacı, package.json ve lockfile sürüm kontrolündedir; node_modules depoda tutulmaz; yayın çıktısı (kök `index.html` + `public/`) depoda tutulur; elle konan medya `assets/` git'te izlenir.
2.2. Kurulum lockfile'a göre yapılır; sürüm aralığı bırakılmaz, sürüm pinlenir; yeni bağımlılık gerekçelenir.
2.3. CDN'den script, stil veya font yüklenmez; tüm istemci kütüphaneleri npm paketidir.
2.4. Bağımlılık denetimi release'de çalıştırılır; bilinen kritik açık varken release yapılmaz.
2.5. Node, Vite ve React sürümleri çalışma anında resmî kaynaktan doğrulanır; beceriye sürüm yazılmaz.

## 3. Yayın iskeleti ve build

3.1. Vite kökü `spa/`'dır ve kaynak düzdür: `spa/index.html` giriş kabuğu, `spa/main.tsx`, `spa/App.tsx`, `spa/ortak.tsx`, `spa/stil.css`, `spa/sayfa/`. `src/` katmanı yoktur; kök `index.html` ile `spa/index.html` iki ayrı dosyadır.
3.2. `vite.config` hedefi depo köküdür: `root: 'spa'`, `build.outDir: '..'`, `build.assetsDir: 'public'`, `build.emptyOutDir: false`, `base: '/'`.
3.3. Kök `public/` yalnız build çıktısıdır: hash'li JS/CSS ve içeri alınmış varlıklar buraya yazılır; elle dosya konmaz, kaynak ağacında aynı adda dizin bulunmaz.
3.4. Vite'ın `publicDir` seçeneği `spa/public/` dizinidir; içeriği dönüştürülmeden `outDir` köküne kopyalanır. Kök `public/` ile aynı dizin değildir ve karıştırılmaz; kullanılmıyorsa `publicDir: false` yazılır.
3.5. `assets/` elle konan medyadır (görsel, video): build buraya yazmaz, buradan silmez ve dosya adına hash eklemez; içerik git'te izlenir.
3.6. `emptyOutDir` açıkça `false` yazılır: kök dışı hedefte Vite varsayılanı zaten `false`'tur ve uyarı verir; açık değer uyarıyı kapatır ve kökün boşaltılmasını koşulsuz engeller.
3.7. Bayat çıktı silme yayın komutunun işidir: `npm run yayin` önce `public/` dizinini siler, sonra build çalıştırır, kök `index.html` ile `public/` dizinini stage eder; elle kopyalama veya ikinci yayın betiği yoktur.
3.8. Çıktı yeniden üretilebilir: aynı lockfile ve komut aynı sonucu verir; ikinci çalıştırma çalışma ağacında fark bırakmaz.
3.9. Kökte tek HTML girişi `index.html`'dir; PHP girişleri beyaz listededir (references/litespeed-yonlendirme.md 2.4) ve kökte `index.php` yayınlanmaz.
3.10. Kaynak haritaları ve dev araçları yayına çıkmaz; çıktıda Node bağımlılığı, test dosyası ve secret bulunmaz; release öncesi statik tarama yapılır.
3.11. Build ortam değişkenlerini build-time okur; istemciye gömülen değerler yalnız kamuya açık olanlardır.
3.12. Dağıtım ve rollback aynı commit'i kullanır; ayrı artefakt arşivi tutulmaz.

## 4. Bütçe

4.1. JS ve CSS toplamı için proje bundle bütçesi tanımlıdır; değer beceriye gömülmez, release kaydında ölçülür.
4.2. Bütçe aşımı kök neden giderilmeden release edilmez; önce kod bölme ve gereksiz bağımlılık temizliği uygulanır.
4.3. İlk yükleme için kritik olmayan parçalar ayrılır; tüm kütüphane tek pakete yığılmaz.
4.4. Ölçüm komutu ve sonucu kayda geçer; tahmin veya sözlü beyan kanıt sayılmaz.

## 5. Geliştirme

5.1. Geliştirmede `spa/` kökünde Vite dev sunucusu ve PHP API birlikte çalışır; API çağrıları dev proxy veya aynı origin üzerinden yönlenir.
5.2. Geliştirmede prod build ve deploy çalıştırılmaz; mikro değişiklikte HMR ve etkilenen test yeterlidir.
5.3. Dev ve prod davranışı ayrıştırılır; dev'e özgü hata ayıklama kodu üretime giremez.
5.4. Geliştirmede Python servisi API'den bağımsız ayrı süreçtir; API veri deposundaki son geçerli durumu döner, veri yoksa bunu hata olarak bildirir.

## 6. Release doğrulaması

6.1. Build temizliği, kök yayın içeriği, Node'suz çalışma ve bütçe ölçümü release kapılarıdır (references/kabul-kapilari.md).
6.2. Vite ve React davranışı sürüm dokümanından doğrulanır; varsayım yapılmaz.
