# Pencere ve Yerleşim Spesifikasyonları

> `sp-dizayn-masaustu` eki. Pencere modeli, yerleşim iskeleti, pencere/veri durumları, yıkıcı eylem akışı, platform kısayol geleneği ve metin taşma kuralları.
> Doğrulama: pencere seçenekleri ve platform davranışı çalışma anında resmî belgeden doğrulanır; bu dosya API adı ve imzası taşımaz.

## 1. Pencere modeli

| Öğe | Kural |
| --- | --- |
| Asgari boyut | tanımlıdır; düzen bu boyuta kadar bozulmadan daralır |
| Başlangıç boyutu | asgari boyutun üstünde; ekran çalışma alanına sığar |
| Yeniden boyutlandırma | canlı ve sürekli; düzen akıcı biçimde yeniden akar |
| DPI değişimi | düzen bozulmaz; metin ve ikon keskin kalır |
| Pencere başlığı | uygulama + bölüm adı; Türkçe |

- Pencere seçenekleri platform API yüzeyinden verilir; seçenek adları çalışma anında doğrulanır.
- Ayrı pencere yalnız tanımlı akışta açılır; modal iş için yeni pencere açılmaz.
- Pencere kapanırken kaydedilmemiş değişiklik varsa onay istenir; sessiz veri kaybı yoktur.

## 2. Yerleşim iskeleti

Bölgeler: üst menü/araç çubuğu, sol gezinme, orta içerik, sağ bağlam paneli, alt durum çubuğu. Yalnız ihtiyaç duyulan bölge kurulur; boş bölge açılmaz.

- Orta içerik bölgesi büyür; gezinme ve panel bölgeleri asgari genişlikte ve yeniden boyutlandırılabilir.
- Bölünmüş panellerde kullanıcı oranı değiştirir; oran oturumlar arasında korunur.
- Kaydırma yalnız içerik bölgesinde olur; iç içe kaydırma alanı açılmaz.
- Bölge içi boşluk 16/24 px, bölgeler arası 24/32 px.
- Durum çubuğu bağlantı ve kısa durum bilgisi taşır; hata mesajı oraya tekrar yazılmaz (tek kanal).
- Araç çubuğu yalnız ekranın birincil eylemlerini taşır; ikincil eylemler menüye taşınır.

## 3. Pencere ve yerleşim durumları

| Durum | Görünüm | Kural |
| --- | --- | --- |
| Varsayılan | tüm bölgeler açık | odak içerik bölgesinde başlar |
| Asgari boyut | paneller katlanır; taşma yok | birincil görev erişilebilir kalır |
| Geniş ekran | içerik esner, okunabilir sütun korunur | boş alan doldurmak için sahte kart üretilmez |
| Odak kaybı | odak halkası korunur | durum renkleri ve metin solmaz |
| Ekran değişimi | yerleşim aynı kalır | bölgeler yeniden düzenlenmez |
| Salt-okunur | eylemler devre dışı | neden görünür metinle yazılır |

- Asgari boyutta yatay taşma ve kırpma olmaz; metin kaydırır veya alan büyür.
- Ekran değişiminde bölge sırası korunur; kullanıcı konumunu kaybetmez.

## 4. Veri durumları

| Durum | Gösterim | Eylem |
| --- | --- | --- |
| Yükleniyor | ilerleme metni veya iskelet; uzun işte iptal | iptal edilebilir işte iptal düğmesi |
| Boş | açıklama + tek birincil eylem | ilk kaydı oluştur |
| Hata | Türkçe, eyleme dönük mesaj; iç ayrıntı yok | yeniden dene |
| Çevrimdışı | kalıcı durum şeridi; son geçerli veri | yazma eylemleri devre dışı veya kuyruğa alınır |
| Salt-okunur | düzenleme eylemleri devre dışı | neden + yetki isteme yolu |

- Boş ekran bırakmak yasaktır; her durum tasarlanmış görünüme sahiptir.
- Yükleniyor durumu yanlışlıkla boş olarak gösterilmez; iki durum ayrıdır.
- Hata mesajı ne olduğunu ve ne yapılacağını söyler; yığın izi ve iç yol gösterilmez.
- Çevrimdışı yazma kuyruğa alınıyorsa kullanıcıya görünür ve geri alınabilir olur.

## 5. Yıkıcı eylem ve onay

- Geri alınamaz eylem ayrı vurgulu tehlikeli varyant ve onay diyaloğu ister.
- Onay metni sonucu Türkçe ve açık yazar; silinecek nesne ve kapsam belirtilir.
- Toplu işlemde etkilenen öğe sayısı gösterilir.
- Onay diyaloğunda odak güvenli seçenektedir; geri alınamaz eylem varsayılan değildir.
- Tek tıkla geri alınamaz silme yoktur; geri alma varsa süre ve kapsam belirtilir.
- Onay diyaloğu kapanınca odak tetikleyiciye döner.

## 6. Menü, kısayol ve platform geleneği

- macOS için cmd, Linux için ctrl gösterilir; kısayol etiketi menü öğesinde görünür.
- Kısayollar çakışmaz; kritik eylem klavyeyle erişilebilir.
- Menü ve araç çubuğu etiketleri Türkçedir; platform standart yerleşimi korunur.
- Kısayol etiketi biçimlendirilirken platform sembolleri kullanılır; metin karışık gösterilmez.

## 7. Metin, yerelleşme ve taşma

- Uzun açıklama ve yardım metni kırpılmadan okunur; kesip gizleme yoktur.
- Metin taşarsa alan büyür veya satır kaydırır; eksiltme yalnız tam metne erişim varken kullanılır.
- Sayı, tarih ve para Türkçe biçimde gösterilir; birimler ekran genelinde tutarlıdır.
- Hata mesajı alanı işaret eder ve ne yapılacağını söyler.
- Pencere başlığı ve bölüm başlıkları aynı adlandırma düzenini izler.

## 8. Doğrulama adımları

1. Pencere asgari boyuta indirilir; yatay taşma ve kırpma yoktur.
2. DPI %150 ve %200 değerlerinde düzen ve keskinlik kontrol edilir.
3. Bölünmüş panel oranı yeniden başlatma sonrası korunur.
4. Beş veri durumu gerçek veriyle açılır ve görüntüsü kayda geçirilir.
5. Yıkıcı eylem onay akışı klavyeyle tamamlanır; odak güvenli seçenektedir.
6. Menü kısayolları platforma göre doğru gösterilir.

## Kaynaklar

1. gpui-kit tasarım ilkeleri — https://gpui-kit.com/docs/design-guides
2. gpui-kit kısayol rehberi — https://gpui-kit.com/docs/keybinding
3. WCAG 2.2 (W3C Recommendation, 12 Aralık 2024) — https://www.w3.org/TR/WCAG22/