# Sanat Yönü ve Tasarım Paketi

> `sp-dizayn-web-site` gövdesi §3 ve §4'ü açar: ziyaretçi işi, referans yöntemi, konsept seçimi, tek dünya, kompozisyon, tipografi/palet rolleri, design package, erken treatment ve makine kalıpları.
> Sınır: barındırma, SEO altyapısı, stil/JS/font/görsel bütçesi ve release kapıları `sp-mimari-web-site` ile `kabul-kapilari` alanındadır; bu dosya tasarım kararını ve kanıtını tanımlar.
> Runtime zero-build dir: tek `assets/css/site.css`, `:root` tokenları; Node/CDN yok. Görsel, video ve ses çevrimdışı üretilip statik varlık olarak teslim edilir.
> Doğrulama: araç, sürüm ve sağlayıcı iddiası taşınmaz; ortam araçları çalışma anında keşfedilir ve yetenekleri doğrulanır.

## 1. Ziyaretçinin işi ve bölüm sırası

1.1. Tasarımdan önce tek cümle yazılır: ziyaretçi buraya ne yapmaya geldi? Cümle bölüm sırasını belirler; süsleme değildir.
1.2. İş türü sırayı belirler: seçmek (seçenekler erken ve yan yana, gerçek veya başlangıç fiyatı), güvenmek (kişiler ve kanıt erken, yöntem sonra), mekânı hissetmek (hero taşır; sonra oda/menü/saat/konum), anlamak (sade "nedir", üç adım, maliyet), işi görmek (eser sayfayı doldurur, araya az söz girer).
1.3. Bölüm listesi etiketle değil cümleyle yazılır: "Odalar: her odanın manzarasını gösteren üç yan yana kart".
1.4. Liste her landing sayfası gibi okunuyorsa (özellikler, yorumlar, fiyatlar, SSS, iletişim) ziyaretçi işine göre yeniden sıralanır.
1.5. Tek CTA çapası seçilir; her bölüm aynı çapaya akar.
1.6. Mobil sıra ayrı doğrulanır: küçük ekranda ilk üç bölüm aynı işi görüyor mu, sıra anlam kaybediyor mu.
1.7. Eksik malzeme varsayımı tek satırda yazılır; lorem ipsum ve uydurma içerik yasaktır.

## 2. Araştırma ve referans yöntemi

2.1. Üç-beş site incelenir; her biri için "hangi işi nasıl çözmüş" sorusuna tek cümle cevap yazılır.
2.2. Alınan şey ilkedir: hiyerarşi, ritim, kanıt yerleşimi, tipografi kararı. Kompozisyon, metin ve görsel kopyalanmaz.
2.3. Referansın iş türü kendi iş türüyle karşılaştırılır; farklı işin çözümü doğrudan taşınmaz.
2.4. Rekabet paritesi ile fark ayrılır: parite ziyaretçinin beklediği asgari şeydir, fark tek imzadan gelir.
2.5. Ağ yoksa yerel arşiv ve kullanıcı örnekleri kullanılır; erişilemeyen site referans sayılmaz.
2.6. Her referans için kaynak ve erişim tarihi not edilir; hatırlanan izlenim kanıt değildir.
2.7. Gerçek olmayan referans, uydurma metrik ve marka dışı iddia kullanılmaz.
2.8. Ölçüt referans sayısı değil çıkarılan ilkedir; her site en az bir uygulanabilir ilke bırakmalıdır.

## 3. İki-üç konsept yönü ve seçim

3.1. Konsept sayısı iki veya üçtür; her biri gerçekten farklı dünya, fikir ve kompozisyon önerir. Aynı düzenin renk/font varyasyonu konsept değildir.
3.2. Her konsept tek paragrafla yazılır: dayandığı tek gerçek kelime, taşıyıcı görsel özne, imza öğe, zirve ve kapanış.
3.3. Her konsept "hero tek cümleyle heyecanlı anlatılabiliyor mu" testinden geçer; anlatılamıyorsa kamera süsüdür.
3.4. Özgünlük testi: imza tedavi bir rakibe aynen taşınabiliyorsa kişilik yoktur.
3.5. Seçim ölçütleri: ziyaretçi işine hizmet, kanıtlanabilir fark, mevcut medya yeteneğiyle üretilebilirlik, telefon ve azaltılmış harekette ayakta kalma.
3.6. Seçim kullanıcıyla yapılır; onaylanan yön design package'a girer, diğerleri gerekçesiyle reddedilmiş olarak kayda geçer.
3.7. Konsept aşamasında tam medya üretimi yapılmaz; yön kanıtı erken treatment ile verilir (§8).
3.8. Yetenek sınırı gerçektir: zor detay (yüz, el, tanıdık ürün) araç yeteneği doğrulanmadan konseptin merkezine konmaz; gerekirse kompozisyon kısıtlanır, özne gizlenmez.

## 4. Tek dünya, tek imza, zirve ve kapanış

4.1. Tek dünya: palet, tipografi, ışık, malzeme ve hareket öznenin kendi dünyasından türetilir; sayfa ile hero aynı yerde geçiyormuş gibi okunur.
4.2. Tek imza: yalnız bu sitede olan bir öğe; kaldırıldığında sayfa değişmiyorsa o süstür, imza değildir.
4.3. İmza öznenin işleyişinden doğar: bir rotayı izleyen çizgi, katlanan kart gibi açılan menü, sayan fiyat. Hazır efekt listesi imza yerine geçmez.
4.4. Tek zirve: sayfanın en iyi görseli, en geniş alanı ve çevresindeki sessizlik tek ana ayrılır; genellikle hero sonu veya ilk alt bölüm.
4.5. Destek anlar ölçek ve yoğunluk farkıyla ilgiyi taşır; her bölüm aynı güçte olmaz.
4.6. Kapanış tasarlanır: son ekran CTA, marka cümlesi ve gerçek iletişim bilgisi taşır; artık footer kabul edilmez.
4.7. Tekrar yalnız karşılaştırma gerektiğinde kullanılır; komşu bölümlerin işi farklıdır.
4.8. Dünya tutarlılığı telefon ve azaltılmış harekette de korunur; statik kompozisyon boşluk değil, tasarlanmış son durumdur.

## 5. Kompozisyon

5.1. Ölçek kontrastı bilinçlidir: büyük başlık ve görsel gerçek yer kaplar; altı ekran boşluk büyük başlığın gerekçesi değildir.
5.2. Ritim: komşu bölümler farklı iş görür. İfade, sinematik görsel, sabitlenmiş sahne, galeri, dizin ve sakin kanıt bölümü bir olasılık sözlüğüdür, zorunlu sıra değildir.
5.3. Yoğunluk dalgalanır: yoğun bölümün ardından nefes bölümü gelir; her bölüm aynı dolulukta olmaz.
5.4. Asimetri, örtüşme, tam bleed ve ızgarayı kıran görsel yalnız özneyi güçlendiriyorsa kullanılır; sayı tutturmak için değil.
5.5. Her bölümün anlamlı odağı vardır: görülmeye değer bir şey, anlaşılır bir açıklama veya yapılacak bir eylem. Süs odak değildir.
5.6. Boşluk ölçeği 4px'in katıdır: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128. Başlık üstü boşluk altından büyüktür.
5.7. Bölüm dolgusu ekranla büyür; telefon masaüstü havasını devralmaz.
5.8. Satırlar taban çizgisinde hizalanır; ortalanmış kutu yığını kompozisyon değildir.
5.9. Derinlik örtüşme, yumuşak gölge, ince kenar ışığı ve ölçekten gelir; her şeye çerçeve koymak derinlik değildir.
5.10. Telefon karşılığı aynı anda çizilir; kırpma yeterli değilse 9:16 kompozisyon yeniden kurulur.
5.11. Her bölümün oturmuş kırpıntısı geniş, ultra geniş ve telefon genişliğinde denetlenir; tam sayfa küçük görüntü zayıf odağı gizler.

## 6. Tipografi ve palet rolleri

6.1. İki aile yeter: karakterli display ve sakin gövde; üçüncü yalnız küçük etiket için.
6.2. Varsayılan sistem yüzü display olarak kullanılmaz; gerçek font dosyaları (italik dahil) teslim edilir, sahte eğik yasaktır.
6.3. Palet rolleri tokenla tanımlanır: zemin, panel, ana metin, ikincil metin, çizgi, tek vurgu, vurgu hover, vurgu soluk.
6.4. Zemin ve metin tonu hero'dan örneklenir; tuval saf siyah veya saf beyaz olmaz.
6.5. Vurgu nadirdir: CTA, odak halkası ve bir-iki vurgu anı. Her yerde olan vurgu vurgu değildir.
6.6. Kontrast tabanı ölçülür: gövde metni 4,5:1, büyük metin ve kontrol kenarı 3:1.
6.7. Gövde 17-20 px, satır uzunluğu 45-75 karakter, satır yüksekliği yaklaşık 1,5-1,65; ölçü metin öğesinde `ch` ile alınır.
6.8. Büyük başlıkta negatif, küçük etikette pozitif harf aralığı; tek sayısal tracking değeri her yüzü kurtarmaz.
6.9. Koyu zeminde açık metin ağır görünür: biraz daha hafif ağırlık, biraz daha aralık ve satır yüksekliği kullanılır.
6.10. Metin görüntü üstündeyse okunabilirlik sistemi kurulur: yerel scrim, gerçek gölge ve en kötü kareye göre kontrast ölçümü.
6.11. Font sayısı ve bütçesi `sp-mimari-web-site` alanındadır; tasarım kararı bu sınıra uyar, sınırı esnetmez.

## 7. Design package alanları

7.1. Design package tek yaşayan belgedir; build onu birebir tüketir, yeniden yazmaz.
7.2. Omurga: ziyaretçi işi, cümleyle bölüm listesi, imza, zirve ve destek anlar.
7.3. Önerme: öznenin dünyasından tek gerçek kelime veya fikir; her bölüm, etkileşim ve kapanış cümlesi bu fikre hizmet eder.
7.4. Token: rol adlarıyla `:root` değişkenleri; değerler onaylı görselden sonra kesinleşir.
7.5. Tipografi ve hareket: yüzler, ağırlıklar, ölçek ilişkisi, geniş/telefon satır kırılımları, her ana başlığın film işareti ve oturduğu okuma durumu.
7.6. Hero/film planı: önce bitiş (poster) karesi tasarlanır; açılış ve olay aynı dünyanın yeni çekimleridir; kelimeler için sakin bölge üretimden önce ayrılır; telefon için ayrı plan yazılır.
7.7. Alt bölüm outline: her bölümün amacı, kompozisyonu, görseli ve birebir metni; SSS gerçek itirazları alıcının sözüyle yanıtlar.
7.8. Birebir metin: paketteki her görünür satır aynen uygulanır; build yeniden yazmaz.
7.9. Vektör katmanı: elle çizilen SVG motif, çizgi ve ayırıcılar ile soluk parçacıkların yeri; azaltılmış harekette son durum gösterilir.
7.10. Kanıt: erken treatment, seçilen yön, masaüstü/telefon kırpıntıları, işaret haritası, önce/sonra puanı ve açık sınırlar.
7.11. Sayılar başlangıç değeridir: band aralığı ve plato uzunluğu test sonucu değişirse güncellenir; kesinlik yanılsaması yazılmaz.
7.12. Sınırlar açık yazılır: fiziksel cihazda görülmediyse "doğrulanmalı"; e-posta teslimi ile site yayını ayrı durumlardır.

## 8. Erken görsel treatment ve onay kapıları

8.1. Yön yazıyla değil çalışan treatment ile gösterilir: gerçek tipografi ve amaçlanan hareketle hero, temsili bir alt bölüm ve telefon görünümü.
8.2. Treatment storyboard tablosu değildir; kullanıcı ölçeği, kompozisyonu, atmosferi ve hareketi bakarak yargılayabilmelidir.
8.3. Onaylı varlık varsa treatment'a girer; geçici görsel varsa etiketlenir ve nihai sadakat kanıtı sayılmaz.
8.4. Onaylanmadan geniş medya üretimine geçilmez; erken treatment kapısı maliyeti düşürür.
8.5. Onaylar taşınır; yön veya kapsam maddi değişirse yeni onay alınır.
8.6. Kullanıcıya ölçek, atmosfer ve kompozisyon üç-beş cümleyle anlatılır; kullanıcıdan teknik doğrulama istenmez.
8.7. Bağımsız gözden geçiren varsa en zayıf hero dışı bölüm ve nedeni sorulur; yoksa eleştirel öz-inceleme kanıtla kaydedilir.
8.8. Karşılaştırma yalnız maddi fark taşıyan alternatifle ve bir kez yapılır; kozmetik varyasyon onay kapısı açmaz.
8.9. Ücretli araç, API anahtarı ve dış servis varsayılmaz; yetenek yoksa tasarlanmış statik yola düşülür ve kullanıcı bilgilendirilir.

## 9. Makine yapımı görünen kalıplar

9.1. Aynı ikonlu, aynı ölçülü kart sırası bölümden bölüme tekrar etmez.
9.2. Komşu iki bölüm aynı iskeleti kullanmaz: küçük etiket, büyük başlık, paragraf, aynı ızgara.
9.3. Her bölüme numara ("01 / Odalar"), "aşağı kaydır" oku ve gradient başlık yazılmaz.
9.4. Uydurma sayı, müşteri logosu, yorum ve ödül yoktur; kurgusal markada örnek içerik açıkça işaretlenir.
9.5. Varsayılan paletler ancak öznenin dünyası gerçekten oradaysa kullanılır: krem+serif+terra, siyaha yakın+asit yeşili, mor-mavi degrade, ince çizgi brutalizmi.
9.6. Emoji ikon, her yerde cam kart ve her şeyin ortalanması yoktur.
9.7. Her bölüme süs veya buton eklemek ritim kurmak değildir.
9.8. Gerçek olmayan dashboard, sahte canlı sayaç ve doldurma metni yoktur.
9.9. Stok yapay zekâ işaretleri (fazla parlak, dokusuz, tekrar eden yüz/el) kabul edilmez; zor detay doğrulanmadan merkez olmaz.
9.10. Aynı CTA farklı sözlerle tekrarlanmaz; tek CTA en fazla üç kez aynı ifadeyle görünür.
9.11. Bölüm boşluğu içerik yokluğunu gizlemek için kullanılmaz; büyük boşluk büyük içerikle eşleşir.

## Kaynak ve sınır

- Dayanak: 10k-websites tasarım, design-package, checklist ve prompt-law referansları; WCAG AA eşikleri (https://www.w3.org/TR/WCAG22/).
- Teknik kapılar ve bütçeler bu dosyada tekrarlanmaz; `kabul-kapilari` ve `sp-mimari-web-site` dosyalarına başvurulur.
- Araç, sağlayıcı ve sürüm adı gömülmez; ortam yeteneği çalışma anında doğrulanır, doğrulanamayan "doğrulanmalı" işaretlenir.