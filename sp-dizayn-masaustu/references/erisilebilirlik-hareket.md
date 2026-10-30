# Erişilebilirlik ve Hareket Kontrol Listesi

> `sp-dizayn-masaustu` eki. WCAG 2.2 AA eşikleri, klavye ve odak denetimi, erişilebilirlik ağacı, kontrast/DPI ve hareket kontrolünü ölçülebilir adımlara çevirir.
> Doğrulama: platform erişilebilirlik ve animasyon davranışı çalışma anında resmî belgeden doğrulanır; bu dosya API adı, imza ve sürüm iddiası taşımaz.

## 1. Bağlayıcı ölçütler

| Ölçüt | Seviye | Bu arayüzdeki karşılığı | Doğrulama |
| --- | --- | --- | --- |
| 1.3.1 Bilgi ve ilişkiler | A | başlık hiyerarşisi, etiket bağı | erişilebilirlik ağacı |
| 1.4.3 Kontrast (asgari) | AA | metin ≥4,5:1, büyük metin ≥3:1 | kontrast ölçer |
| 1.4.11 Bileşen kontrastı | AA | kenar, ikon ve odak ≥3:1 | kontrast ölçer |
| 2.1.1 Klavye | A | tüm işlev klavyeyle | klavye turu |
| 2.4.3 Odak sırası | A | odak görsel okuma sırasında | klavye turu |
| 2.4.7 Görünür odak | AA | odak halkası her zeminde görünür | klavye turu |
| 2.4.11 Odak gizlenmemesi | AA | odaklanan öğe kısmen görünür | küçük pencere turu |
| 2.5.8 Hedef boyutu | AA | ≥24x24 mantıksal piksel | ölçüm |
| 3.3.1 Hata tanımlama | A | hata alanı işaret eder, metin Türkçedir | form testi |
| 3.3.2 Etiketler | A | her kontrol etiketlidir | ağaç denetimi |
| 4.1.2 Ad, rol, değer | A | kontrol adı ve rolü doğrudur | ağaç denetimi |

## 2. Klavye turu

1. Sekme sırası menüden içeriğe, içerikten durum çubuğuna doğal sırayla ilerler.
2. Her adımda odak halkası görünürdür; odak hiçbir öğede kaybolmaz.
3. Katman açılınca odak katman içinde kalır; çıkışta tetikleyiciye döner.
4. Menü ok tuşlarıyla gezinir, Enter seçer, çıkış tuşu kapatır.
5. Birincil görev fare kullanılmadan tamamlanır.
6. Kaydırılan içerikte odaklanan öğe görünür alana kaydırılır.

## 3. Odak yönetimi

- Odak programatik olarak yalnız tanımlı durumda taşınır: katman açılış ve kapanışı, silme sonrası, hata özeti.
- Katman kapanınca odak tetikleyiciye döner; silme sonrası odak komşu öğeye veya boş duruma gider.
- Gizlenen öğe odakta bırakılmaz; devre dışı kontrol odaklanabilir kalıyorsa nedeni bildirilir.
- Odak halkası hiçbir durumda kaldırılmaz; rengi temadan gelir ve yüksek kontrastlıdır.
- Pencere yeniden boyutlandırılınca odaklanan öğe görünür alanda kalır.

## 4. Erişilebilirlik ağacı

- Her kontrol ad, rol ve değer taşır; yalnız ikonlu kontrol görünmez ad taşır.
- Dekoratif görsel ve ikon ağaçtan gizlenir.
- Başlıklar ve bölgeler ağaçta hiyerarşiyi doğru kurar; tablo başlıkları programatik tanımlıdır.
- Durum değişimi ağaçta duyurulur; yalnız renk değişimi yeterli değildir.
- Salt-okunur ve devre dışı durumlar ağaçta neden bilgisiyle birlikte görünür.

## 5. Kontrast ve DPI

- Metin ≥4,5:1; büyük metin ve bileşen kenarı ≥3:1; odak halkası ve ikon ≥3:1.
- Açık ve koyu tema ayrı ölçülür; bir temada eşiği geçmeyen çift teslim edilmez.
- DPI değişiminde ölçüler mantıksal pikselde korunur; keskinlik kaybolmaz.
- Durum renkleri tek eşleme ile kullanılır; aynı anlam için ikinci renk ailesi seçilmez.

## 6. Hareket kontrolü

- Hareket yalnız değişimi açıklar; dekoratif ve sürekli animasyon yoktur.
- Azaltılmış hareket tercihi açıkken animasyon hedef duruma sıçrar; ara değer gösterilmez.
- Süre ve eğri tema hareket token değerlerinden gelir; serbest süre yazılmaz.
- Animasyon kesintiye uğratılabilir; yeni etkileşim mevcut animasyonu hedefe yönlendirir.
- Animasyon bitince kare istemi durur; boşta kare isteyen animasyon bulunmaz.
- Animasyonsuz da durum anlaşılır; anlam animasyona bağlanmaz.
- Azaltılmış hareket ve boşta kare davranışı ölçüm aracıyla doğrulanır.

## 7. Doğrulama adımları

1. Klavye turu tamamlanır; odak kaybolmaz ve tuzak yalnız katmandadır.
2. Erişilebilirlik ağacı denetlenir: ad, rol, değer.
3. Kontrast ölçümü açık ve koyu temada yapılır.
4. Hedef boyutları ölçülür; WCAG 2.5.8 istisnaları kayda geçirilir.
5. Azaltılmış hareket açıkken animasyonlar hedef duruma sıçrar.
6. Pencere asgari boyutta ve yüksek DPI değerinde ağaç ve düzen denetlenir.
7. Kare bütçesi release ölçümünde kayda geçirilir; boşta kare isteği yoktur.

## 8. Teslim kontrol listesi

- [ ] Her ekran klavye ve ekran okuyucuyla kullanılabilir.
- [ ] Sekme sırası görsel sırayla aynıdır; odak görünür ve kaybolmaz.
- [ ] Yalnız ikonlu kontrollerin erişilebilir adı vardır.
- [ ] Metin ≥4,5:1, büyük metin ve bileşen/odak ≥3:1 kontrast sağlar.
- [ ] Hedef boyutlar ≥24x24 mantıksal pikseldir; istisnalar kayıtlıdır.
- [ ] Katman odağı yönetilir; çıkışta odak tetikleyiciye döner.
- [ ] Azaltılmış harekette animasyonlar hedef duruma sıçrar.
- [ ] Animasyon bitince kare istemi durur; boşta kare isteği yoktur.
- [ ] DPI değişiminde düzen ve keskinlik korunur.
- [ ] Tüm kullanıcı metinleri Türkçe imlâ ve yerelleşme denetiminden geçti.

## Kaynaklar

1. WCAG 2.2 (W3C Recommendation, 12 Aralık 2024) — https://www.w3.org/TR/WCAG22/
2. gpui-kit erişilebilirlik rehberi — https://gpui-kit.com/docs/accessibility
3. gpui-kit animasyon rehberi — https://gpui-kit.com/docs/animation