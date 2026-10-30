# Medya Üretimi

> sp-dizayn-web-site gövde 6'nın ayrıntısı: görsel, video, ses ve 3B varlık üretimi, teslim, arıza, lisans ve kanıt. Medya offline üretilip statik teslim edilir; site runtime'da üretmez, derlemez, CDN/Node kullanmaz. Sinematik mimari references/sinematik-katman.md'dedir; sürüm/model/API runtime'da doğrulanır.

## 1. Üretim öncesi yetenek keşfi ve karar ağacı

1.1. Medya yalnız açık bir ihtiyaç varsa üretilir: hero filmi, bölüm görseli, ürün kanıtı, ses veya anlatı gerektiren 3B. Süs için üretim yapılmaz.
1.2. Önce medya yeteneği envanteri çıkarılır: görsel/video üretimi, ses kaynağı, yerel encode, tarayıcı doğrulama ve ölçüm. Genel keşif, kanıt katmanları ve erişim tanısı arac-ortam.md dosyasındadır; medya kararı bu envantere dayanır.
1.3. Ücretli üretici, API anahtarı, kota ve abonelik varsayılmaz (arac-ortam.md). Harcama yalnız kullanıcı onayıyla yapılır; onay yoksa ücretsiz, yerel ve statik yola düşülür.
1.4. Karar ağacı sırayla işletilir: yeterli gerçek varlık varsa üretim yapılmaz; görsel gerekli ama üretici yoksa CSS/SVG/tipografi/doku ile statik kompozisyon; video gerekli ama üretici yoksa poster veya kodla kare dizisi; 3B yalnız anlatı zorunluysa; ses yalnız açık istek veya onaylı deneyim parçasıysa (varsayılan sessiz).
1.5. Üretici seçilecekse güncel yetenek ve kalite meta veriden doğrulanır; model adı dondurulmaz. Karşılaştırma aynı brief ve ölçütle yapılır.
1.6. Pahalı yol yalnız temsili pilot ve onaylı bütçeyle açılır; üretim sağlayıcısı tek seçilir, doğrulama/encode/ölçüm için hibrit araç kullanılabilir.
1.7. Yetenek yoksa veya yetmezse sonuç tasarım olarak tamamlanır; üretilemeyen medya yerine tasarlanmış statik çözüm konur ve sınır kayda geçer. Erişim hatasında tanı arac-ortam.md'dedir; çözülemezse işe başlamadan bildirilir.

## 2. Görsel üretimi

2.1. Tek çekim kuralı: ışık yönü, lens hissi, palet ve malzeme bir kez yazılır; bütün görseller aynı gün aynı yerde çekilmiş gibi okunur. Sayfa ve hero tek dünyadır.
2.2. Tekrarlanan ürün, kişi veya mekân için yetkili kimlik referansı seçilir; değişmezler yazılır (adet, oran, malzeme, birleşim, yerleşim). Kasıtlı hikâye değişiklikleri değişmezlerden ayrı tutulur.
2.3. Referanslara rol verilir: kimlik, kompozisyon veya doku kalitesi. Tek kompozisyon otoritesi kullanılır; birden çok görüş birleştirilerek kolaj üretilmez.
2.4. En zor detay önce incelenir: yüz, el, yazı, bitki bağlantısı, tekrar eden parça ve tanıdık ürün. Kaynak çözünürlükte kırpılarak hem geniş hem telefon sunumunda kontrol edilir; üretim yayılmadan bu kontrol yapılır.
2.5. Hero üç kare olarak tasarlanır:
2.5.1. REST: bitiş ve poster karesi; ürün yerleşmiş, ışık varılmış, başlık için sakin alan ayrılmış.
2.5.2. OPEN: açılış; kendi başına ekran görüntüsüne değer, REST'ten farklı kamera, ölçek ve durum.
2.5.3. EVENT: orta olay; enerjinin tepesi, hareketin en yoğun anı; sakin orta kare filmi sakinleştirir.
2.5.4. Ekran görüntüsü testi: üç kare yan yana konduğunda farklı çekimler gibi durmalı; biri diğerinin kırpıntısıysa hareket küçüktür.
2.6. Telefon ayrı kompozisyondur: 9:16 açılış, her olay, her dönüş ve bitiş yeniden kurulur. Kırpma ancak her vuruş ve metin alanı yaşıyorsa kullanılır; başlık satırları telefona göre yeniden yazılır.
2.7. Metin için sakin bölge üretimden önce kararlaştırılır; eylem o bölgeye girmez. Boş alan dünyanın parçası olarak tarif edilir; karanlık panel veya boş kutu istemek görüntüyü bozar.
2.8. Gerçek kişi fotoğrafı yalnız kullanıcının kendi fotoğrafı veya açık izinli kişi için kullanılır; başka kişinin fotoğrafıysa üretimden önce sorulur. Kimlik korunur, kompozisyon izinsiz değiştirilmez.
2.9. Onaylı ürün işareti ve yazı korunur; istenmeyen metin, logo ve filigran yoktur. Kurgusal marka açıkça işaretlenir.
2.10. Üretim defteri: seçilen kare sürümü, referanslar, kabul ve ret gerekçeleri; reddedilen veya değiştirilen medya onaylanmıştan ayrı tutulur.

## 3. Video

3.1. Tek kontrollü çekim esastır: tek sürekli çekim veya bilinçli zincir. Klip sayısı drama ölçüsü değildir; yapıyı gerekli hareket ve doğrulanmış yetenek belirler.
3.2. Hareket kaydırmayla anlaşır: aşağı kaydırma aşağı, inme, açılma veya varış hissi vermeli; yukarı kaçan hareket sayfayla çatışır.
3.3. Yol sözleşmesi kaydedilir: başlangıç mesafe/yükseklik ve yön, ilerleme yolu, ön plan paralaksı, varış yönü ve hız. Paylaşılan kare kamera hızını garanti etmez; ekran görüntüsü hareket kanıtı değildir.
3.4. Bitiş önce tasarlanır: poster bitiş karesidir ve REST karesidir; alternatif zaman damgası yalnız bilinçli tercihte kullanılır. Yalnız son segment dinlenmeye varır; ara segmentler hareket içinde biter.
3.5. Sessiz master üretilir: üretim sesi kapalı, klip sessiz; yüksek kalite master ayrı, web teslimi ayrı encode edilir.
3.6. Kanıtlanmamış hareket önce temsili pilotla denenir; pilot geçmeden bağımlı klip ve formatlar üretilmez.
3.7. Join önce eşleşen kesimle kurulur; iki uç ve çevresi kare kare iki yönde incelenir. Kısa blend yalnız join'i gerçekten iyileştiriyorsa; dokuda rest-rest birleşim görünür kesim üretir, seam hareket içine alınır.
3.8. Telefon için önce ayrı dikey kaynak üretilir; kırpma yalnız her vuruş ve metin alanı doğrulanmışsa istisnadır. İki büyük video birlikte indirilmez; cihaz tek uygun kaynağı seçer.
3.9. Kare dizisi/scrub: tarayıcıda video ileri geri sarmak gerekliyse sıralı kare dizisi (ör. WebP) ve kaydırma yüzdesi eşlemesi tercih edilir; ileri, geri ve rastgele seek aynı kareyi vermelidir. Kare sayısı ve toplam boyut ölçülür.
3.10. Web encode ayrı adımdır: sık anahtar kare, B-kare yok, ses yok, hızlı başlangıç ve poster; yerel encode aracı (ör. ffmpeg) kullanılabilir. Her encode sonrası oynatma, boyut, süre ve poster doğrulanır.
3.11. Süre kısaltma veya pacing değişikliği kreatif değişimdir: onay ister; beat haritası ve kare/tipografi eşlemesi yeniden ayarlanır.

## 4. 3B ve WebGL

4.1. Sinematik karar, mod seçimi, sahne mimarisi ve performans bütçesi references/sinematik-katman.md dosyasındadır; burada yalnız üretim ve teslim kuralı vardır.
4.2. 3B varsayılan değildir; yalnız anlatı gerçek zamanlı kamera, ışık veya model etkileşimi gerektiriyorsa üretilir. Ağır 3B yerine kare dizisi, derinlikli görsel, paralaks veya CSS/SVG sahne değerlendirilir.
4.3. Teslim edilen 3B varlık için statik fallback, tek rAF, dispose, görünürlük durdurma ve bağlam kaybı yönetimi zorunludur; yetenek yoksa 3B zorlanmaz.

## 5. Ses

5.1. Varsayılan sessizdir; ses yalnız açık istek veya onaylı deneyim parçasıysa eklenir.
5.2. Kullanıcı kontrolü zorunludur: görünür oynat/durdur veya sessize al; otomatik sesli oynatma yok, ani yüksek ses yok.
5.3. Lisans: yalnız telifsiz, üretilmiş veya izinli ses kullanılır; kaynak, lisans türü ve atıf koşulu kayda geçer.
5.4. Mix ölçülür: konuşma ve müzik dengesi, tepe seviyesi, sessiz master; kırpılma ve ani sıçrama yok.
5.5. Ses yüklenemezse sayfa sessiz olarak eksiksiz çalışır; kontrol gizlenir, hata kullanıcıya sızmaz.
5.6. Ses dosyası yalnız gerektiğinde ve teslim boyutuna uygun formatta yüklenir; dekoratif ses varsayılan yüklenmez.

## 6. Format ve bütçe

6.1. Görsel teslimi: AVIF öncelik, WebP geri dönüş; kullanıldığı boyuta yakın üretilir (bölüm görseli yaklaşık 1600 px, tam kanama yaklaşık 2400 px). Keskin kenarlı arayüz görselinde kayıpsız istisna kullanılır.
6.2. Her img etiketinde gerçek width ve height bulunur; LCP görseli preload ve yüksek öncelik alır; katlanma altı görseller lazy yüklenir.
6.3. Video: poster zorunlu, preload yok, sessiz, satır içi oynatılır; mobil için ayrı dikey kaynak veya doğrulanmış kırpma sunulur. Statik alternatif gerekiyorsa poster ayrı mobil kompozisyonda üretilir; otomatik sesli video ve iki kaynağın birlikte indirilmesi yoktur.
6.4. Boyut hedefi değil ölçüm esastır: gerçek yükleme süresi ve transfer boyutu ölçülür; bütçe aşılırsa içerik ve kompozisyon sadeleşir, kalite sessizce düşürülmez.
6.5. Master'lar, ham render'lar ve ara dosyalar dağıtıma girmez; yalnız optimize edilmiş teslim varlıkları siteye eklenir.
6.6. Medya self-host edilir; harici medya barındırma, gömülü oynatıcı ve üçüncü taraf CDN bağımlılığı yoktur. Site yalnız tek assets/css/site.css ve kök tokenlarla çalışır; medya için ikinci stil kaynağı veya Node adımı açılmaz.
6.7. HTML yerleştirme, dizin, önbellek ve sayfa bütçesi kuralları sp-mimari-web-site alanındadır; bu dosya teslim edilecek varlığın biçim ve davranışını tanımlar.

## 7. Sinematik tipografi

7.1. Film varsa tipografi filme bağlanır; sahne koreografisi, okunabilir plato ve cue haritası references/sinematik-katman.md 7. maddesine göre yazılır.
7.2. Statik hero metni ayrı yazılır: reduced motion, video yokluğu veya telefon fallback'inde poster üstünde başlık, alt satır ve CTA okunur kalır.
7.3. Kare eşleme testi: aynı kare aynı tip durumunu vermeli; ileri, geri ve rastgele seek aynı sonucu üretmeli; ters kaydırmada sıçrama olmamalı.
7.4. Okunabilirlik en kötü kareye göre ölçülür; metin transform ve saydamlıkla hareket eder, reduced motion'da doğrudan final durum görünür.

## 8. Reduced motion ve medya arızası

8.1. Reduced motion açıksa video yüklenmez, animasyon final duruma atlar, statik hero görünür; içerik ve eylem eksiksizdir.
8.2. Video yüklenemezse poster, başlık ve CTA ile sayfa tam çalışır; boş kutu, kırık oynatıcı ve düzen sıçraması olmaz. Görsel yüklenemezse width/height korunur, alt metin okunur.
8.3. Ses yüklenemezse kontrol gizlenir; sayfa sessiz çalışır.
8.4. 3B/WebGL başarısız olursa statik fallback gösterilir; hata kullanıcıya sızmaz, konsol temiz kalır.
8.5. Yavaş ağda poster ilk gelir, video sonra yüklenir; LCP posteri beklemez. Arıza durumları gerçek testle kanıtlanır (medya engelleme, reduced motion, ağ kısıtlama); kod incelemesi kanıt değildir.

## 9. Lisans, atıf ve üretim kanıtı

9.1. Üretilen medyanın lisansı ve ticari kullanım hakkı sağlayıcı koşullarına bağlıdır; varsayılmaz, çalışma anında resmî kaynaktan doğrulanır ve kayda geçer.
9.2. Gerçek fotoğraf ve video yalnız kullanıcının kendisi veya açık izinli kişi için kullanılır; izin ve bağlam kaydı tutulur.
9.3. Ses ve müzikte lisans türü, kaynak ve atıf zorunluluğu kaydedilir; açık lisanslı stokta kaynak ve atıf koşulu, tanınabilir marka/kişide izin doğrulanır; atıf görünür yerde verilir.
9.4. Üretim kanıtı her varlık için tutulur: kaynak türü, üretim notu veya prompt özeti, seçilen sürüm, lisans durumu, kabul notu ve ölçüm. Lisansı doğrulanamayan medya yayınlanmaz; "doğrulanmalı" ve yayın dışı işaretlenir.
9.5. Üretim araçları, planları ve ham dosyalar sürüm kontrolü dışında tutulur; site yalnız teslim edilen varlıkları taşır. Kanıt kabul kapılarına bağlanır.
9.6. Ücretli üretimde onay, harcama ve kota kaydı üretim defterine yazılır; onaysız harcama yapılmaz. Yasal belirsizlikte varsayımla yayınlanmaz; uzman görüşü istenir ve karar kayda geçer.
