---
name: sp-dizayn-masaustu
description: "GPUI masaüstü arayüzünün yapısal tasarımını tanımlar: tema token disiplini, ölçü/boşluk/tipografi, platform bileşen ve ikon kataloğu, pencere/yerleşim durumları, hareket, erişilebilirlik ve Türkçe imlâ. Şu durumlarda kullan: GPUI arayüzü kurarken, masaüstü pencere/panel yerleşimi tasarlarken, bileşen durumlarını belirlerken. Kullanma: yalnız estetik dil tarifi istendiğinde (sp-zen-dizayn), yalnız Rust mimarisi veya paketleme işi olduğunda; bu alanlar başka becerilerindir."
version: "v202610300440"
---

# sp-dizayn-masaustu

GPUI masaüstü arayüzünün yapısal tasarımı: tema token disiplini, ölçü ve tipografi, platform bileşen ve ikon kullanımı, pencere ve yerleşim durumları, hareket, erişilebilirlik ve Türkçe metin. Beceri yapıyı ve davranışı kurar; estetik dil (renk/boşluk/tipografi hissi, materyal, derinlik, hareket karakteri) sp-zen-dizayn alanıdır ve orada aranır.

## 0. Ortak çalışma ilkeleri (kaynak: AGENTS-tr; bilinçli kopya)

0.1. Öncelik: kullanıcı talimatı > AGENTS-tr > bu beceri > model bilgisi.
0.2. Mod: varsayılan geliştirme; release/prod kapıları yalnız risk sınıfı veya açık yayın isteğiyle yüklenir.
0.3. Değişmezler: güvenlik, erişilebilirlik, veri bütünlüğü, sır yönetimi ve Türkçe imlâ her modda korunur.
0.4. Bilgi: sürüm/API/davranış varsayılmaz; çalışma anında context7 veya resmî kaynaktan doğrulanır; doğrulanamayan "doğrulanmalı" etiketiyle verilir.
0.5. Araç: işe göre seçilir, gerektiğinde hibrit kullanılır; erişim hatasında tanı → basit çözüm → çözülemezse işe başlamadan bildir (sp-sozlesme 1.3, 2.2).
0.6. Kanıt: kanıtsız "tamamlandı" yok; kabul kapıları yalnız release/risk tetikte yüklenir (kanıt ve kapanış: sp-sozlesme §4).

## 1. Kapsam ve öncelik

1.1. Bu beceri GPUI masaüstü arayüzünün yapısını kurar: tema token değerleri, ölçü, bileşen ve ikon kullanımı, pencere/yerleşim, durumlar, hareket ve erişilebilirlik.
1.2. Estetik dil bu becerinin dışındadır; istendiğinde sp-zen-dizayn yüklenir ve bu beceri onun kararını yapısal olarak uygular.
1.3. Öncelik: kullanıcı talimatı > AGENTS-tr > platform mimari becerisi > bu beceri > estetik dil.
1.4. Kullanıcının yazılı tasarım direktifi bu beceriye maddedir; çelişkide en güncel yazılı onay uygulanır.
1.5. Beceri geliştirme aşaması içindir; release ve paketleme kapıları yalnız risk sınıfı veya açık yayın isteğiyle yüklenir.
1.6. Türkçe metin: arayüz metinleri tam Türkçe imlâ ile yazılır (ğ, ü, ş, ı, ö, ç); lorem ipsum, İngilizce kalıntı ve yer tutucu metin yoktur; hata mesajı eyleme dönüktür; sayı, tarih ve para biçimi Türkçe yerelleşir.

## 2. Tema ve token disiplini

2.1. Renk, yarıçap, tipografi ve hareket değerleri yalnız tema token değerlerinden gelir; bileşen gövdesine sabit renk (hex, rgb), sabit yarıçap veya sabit süre yazılmaz.
2.2. Token alanı yoksa değer ürün temasında tanımlanır; çağrı yerine palet değeri gömülmez.
2.3. Açık ve koyu tema ayrı doğrulanır; bir temada okunmayan yüzey veya metin teslim edilmez.
2.4. Durum renkleri tek eşleme ile kullanılır: başarı emerald/green, uyarı amber/yellow, hata rose/red, bilgi sky/blue; aynı anlam için ikinci renk seçilmez.
2.5. Durum yalnız renkle anlatılmaz; metin ve ikon birlikte kullanılır.
2.6. Kontrast: metin ≥4,5:1, büyük metin ve bileşen kenarı ≥3:1; odak halkası yüksek kontrastlıdır ve odaklanan öğe kısmen de olsa görünür kalır.
2.7. Token rol tablosu, bileşen kuralları ve doğrulama adımları: references/tema-token.md.

## 3. Ölçü, boşluk ve tipografi

3.1. Boşluk baremi 4px'tir; yardımcılar 4'ün katı değer alır; ara değer yalnız tema token'ında tanımlanır, çağrı yerinde serbest piksel yazılmaz.
3.2. Dikey dolgu simetriktir; buton, girdi ve liste satırında `pt`/`pb` asimetrisi yoktur.
3.3. Tipografi ölçeği tema token değerlerinden gelir; metne serbest punto veya piksel boyutu verilmez.
3.4. Yoğun veri ekranlarında platformun boyut ölçeği kullanılır; yalnız dış kutu yüksekliğini değiştirmek yasaktır.
3.5. Yerleşim akış yardımcılarıyla kurulur; serbest mutlak konumlandırma yoktur; ölçü sınırları esnek büyümeyle verilir, sabit ölçüde kırpma yapılmaz.
3.6. Uzun açıklama ve yardım metni kırpılmadan okunur; taşan metni kesip gizlemek yasaktır.

## 4. Bileşen ve ikon kullanımı

4.1. Bileşenler platform kataloğundan kullanılır; buton, girdi ve tablo gibi standart kontroller sıfırdan yazılmaz.
4.2. Varyantlar platformun varyant mekanizmasıyla seçilir; bileşenin rengi ve dolgusu elle geçersiz kılınmaz.
4.3. Boyutlar platform ölçek mekanizmasıyla verilir; bileşen içi ölçü elle sabitlenmez.
4.4. İkonlar yalnız platform varlık kataloğundan gelir; tek ikon seti Lucide'dir; yerel SVG, ikon fontu ve ikinci set yoktur.
4.5. Kritik eylem hover'a bağlanmaz; klavye ve işaretçiyle erişilebilen görünür eylem olarak sunulur.
4.6. Bileşen ve ikon kataloğunun sürümü, erişim yolu ve kullanılabilirliği çalışma anında doğrulanır; sürüm sabitleme mimari becerinin alanıdır.
4.7. Bileşen, varyant ve durum matrisi: references/tema-token.md.

## 5. Pencere, yerleşim ve durumlar

5.1. Pencere asgari boyutu tanımlıdır; düzen bu boyuta kadar bozulmadan daralır.
5.2. Bölünmüş paneller kullanıcı tarafından yeniden boyutlandırılabilir; oran oturumlar arasında korunur.
5.3. Menü, araç çubuğu ve kısayol etiketleri platform geleneğine uyar; macOS'ta cmd, Linux'ta ctrl gösterilir.
5.4. Her ekranın boş, yükleniyor, hata, çevrimdışı ve salt-okunur görünümü tasarlanır; boş ekran bırakılmaz.
5.5. Tehlikeli ve geri alınamaz eylem ayrı vurgu ve onay ister; tek tıkla geri alınamaz silme yoktur; onay metni sonucu Türkçe yazar.
5.6. Pencere durumları, yerleşim iskeleti ve durum matrisi: references/yerlesim-pencere.md.

## 6. Hareket

6.1. Hareket yalnız değişimi açıklar; dekoratif, sürekli ve otomatik animasyon yoktur.
6.2. Azaltılmış hareket tercihi desteklenir; tercih açıkken animasyon hedef duruma sıçrar.
6.3. Süre ve eğri tema hareket token değerlerinden gelir; serbest süre yazılmaz.
6.4. Animasyon kesintiye uğratılabilir; tamamlanınca kare istemi durur, boşta kare isteyen animasyon bulunmaz.
6.5. Animasyonsuz da her durum anlaşılır; anlam animasyona bağlanmaz.
6.6. Kontrol listesi ve doğrulama adımları: references/erisilebilirlik-hareket.md.

## 7. Erişilebilirlik

7.1. Hedef WCAG 2.2 AA'dır; her ekran klavye ve ekran okuyucuyla kullanılabilir.
7.2. Sekme sırası görsel okuma sırasıyla aynıdır; odaklanan öğe görünür kalır, odak gizlenmez veya kaybolmaz.
7.3. Yalnız ikon taşıyan her kontrol erişilebilir ad taşır; erişilebilirlik ağacında ad, rol ve değer doğrudur.
7.4. Tıklama hedefi en az 24x24 mantıksal pikseldir; WCAG 2.5.8 istisnası kayda geçirilir.
7.5. Pencere yeniden boyutlandırma ve DPI değişiminde düzen bozulmaz, keskinlik korunur.
7.6. Kontrol listesi ve doğrulama adımları: references/erisilebilirlik-hareket.md.

## 8. Kabul kapısı

- [ ] Sabit renk, sabit yarıçap ve sabit süre taraması kaynakta eşleşme üretmez.
- [ ] Açık ve koyu temada kontrast: metin ≥4,5:1, büyük metin ve bileşen kenarı ≥3:1.
- [ ] Klavye turunda her odak görünür; birincil görev fare olmadan tamamlanır.
- [ ] Yalnız ikonlu kontrollerin erişilebilir adı vardır.
- [ ] İkonlar platform kataloğundan gelir; yerel SVG ve ikon fontu yoktur.
- [ ] Azaltılmış harekette animasyonlar hedef duruma sıçrar.
- [ ] Pencere asgari boyutta ve yüksek DPI'da düzen bozulmadan açılır.
- [ ] Boş, yükleniyor, hata, çevrimdışı ve salt-okunur durumları gerçek veriyle açıldı.
- [ ] Yıkıcı eylem onay ister ve onay metni sonucu Türkçe yazar.
- [ ] Tüm kullanıcı metinleri Türkçe imlâ ve yerelleşme denetiminden geçti.
- [ ] Animasyonlu ekranda boşta kare isteği yoktur (kare bütçesi release ölçümüne bırakılır).