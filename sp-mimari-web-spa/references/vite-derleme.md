# vite-derleme — build modeli, dist, env, bütçe

> Bu dosya sp-mimari-web-spa becerisinin references dosyasıdır; gövdedeki 2. bölümün ayrıntısını taşır. Sürüm iddiaları burada tutulmaz; çalışma anında resmî kaynaktan doğrulanır.

## 1. Model

1.1. Node yalnız geliştirme ve derleme zamanında çalışır; üretimde Node çalışmaz.
1.2. Çalışma zamanı iki parçadır: LiteSpeed'in sunduğu statik dist ve PHP API. Başka çalışma zamanı bileşeni eklenmez.
1.3. Vite geliştirmede HMR verir; üretim çıktısı statik dosyalardır.
1.4. React istemci yönlendirme kullanır; sunucu tarafı render yoktur.

## 2. Proje ve bağımlılık

2.1. Kaynak ağacı, package.json ve lockfile sürüm kontrolündedir; node_modules ve dist depoda tutulmaz.
2.2. Kurulum lockfile'a göre yapılır; sürüm aralığı bırakılmaz, sürüm pinlenir; yeni bağımlılık gerekçelenir.
2.3. CDN'den script, stil veya font yüklenmez; tüm istemci kütüphaneleri npm paketidir.
2.4. Bağımlılık denetimi release'de çalıştırılır; bilinen kritik açık varken release yapılmaz.
2.5. Node, Vite ve React sürümleri çalışma anında resmî kaynaktan doğrulanır; beceriye sürüm yazılmaz.

## 3. Build

3.1. Release build'i temizdir: hata ve uyarı yoktur.
3.2. Build çıktısı hash'li varlıklarla dist/ altına yazılır; index.html varlık adlarını taşır.
3.3. Çıktı yeniden üretilebilir: aynı lockfile ve komut aynı sonucu verir; kaynak haritaları üretime çıkmaz veya erişilemez konumda tutulur.
3.4. Build ortam değişkenlerini build-time okur; istemciye gömülen değerler yalnız kamuya açık olanlardır.
3.5. dist içinde Node bağımlılığı, dev aracı, test dosyası ve secret bulunmaz; release öncesi statik tarama yapılır.
3.6. dist sürümlü artefakt olarak saklanır; dağıtım ve rollback aynı artefaktı kullanır.

## 4. Bütçe

4.1. JS ve CSS toplamı için proje bundle bütçesi tanımlıdır; değer beceriye gömülmez, release kaydında ölçülür.
4.2. Bütçe aşımı kök neden giderilmeden release edilmez; önce kod bölme ve gereksiz bağımlılık temizliği uygulanır.
4.3. İlk yükleme için kritik olmayan parçalar ayrılır; tüm kütüphane tek pakete yığılmaz.
4.4. Ölçüm komutu ve sonucu kayda geçer; tahmin veya sözlü beyan kanıt sayılmaz.

## 5. Geliştirme

5.1. Geliştirmede Vite dev sunucusu ve PHP API birlikte çalışır; API çağrıları dev proxy veya aynı origin üzerinden yönlenir.
5.2. Geliştirmede prod build ve deploy çalıştırılmaz; mikro değişiklikte HMR ve etkilenen test yeterlidir.
5.3. Dev ve prod davranışı ayrıştırılır; dev'e özgü hata ayıklama kodu üretime giremez.

## 6. Release doğrulaması

6.1. Build temizliği, dist içeriği, Node'suz çalışma ve bütçe ölçümü release kapılarıdır (references/kabul-kapilari.md).
6.2. Vite ve React davranışı sürüm dokümanından doğrulanır; varsayım yapılmaz.
