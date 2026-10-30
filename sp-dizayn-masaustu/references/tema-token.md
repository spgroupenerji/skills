# Tema ve Token Spesifikasyonları

> `sp-dizayn-masaustu` eki. Tema token kategorileri, renk ve durum eşlemesi, ölçü-tipografi-hareket token kullanımı, platform bileşen ve ikon kataloğu kuralları ile doğrulama adımları.
> Doğrulama: bu dosya API imzası veya sürüm iddiası taşımaz; token alanları, bileşen varyantları ve hareket token değerleri çalışma anında resmî gpui-kit belgelerinden veya context7 üzerinden doğrulanır.

## 1. Token kategorileri

| Kategori | Ne taşır | Kural |
| --- | --- | --- |
| Renk: yüzey | panel, kart, arka plan | yüzey ve yüzey-üst ayrı token; açık yüzey üstüne açık yüzey yığılmaz |
| Renk: metin | gövde, soluk, ters | soluk metin de AA ölçülür |
| Renk: sınır | 1px kenar, ayırıcı | kalınlık artışı yalnız odak halkasında |
| Renk: vurgu | primary eylem, seçili durum | tek accent; ikinci accent yok |
| Renk: durum | başarı, uyarı, hata, bilgi | eşleme sabit |
| Yarıçap | bileşen ve katman köşeleri | token değerinden; sabit piksel yok |
| Boşluk | iç ve dış boşluk | 4'ün katı |
| Tipografi | punto, ağırlık, satır yüksekliği | token değerinden; serbest punto yok |
| Hareket | süre, eğri | token değerinden; serbest süre yok |

Token alanı yoksa değer ürün temasında tanımlanır; çağrı yerine palet değeri gömülmez. Tema erişimi için platformun tema erişim katmanı kapsamda tutulur; erişim yolunun adı çalışma anında doğrulanır.

## 2. Renk ve durum eşlemesi

| Rol | Eşleme | Sunum kuralı |
| --- | --- | --- |
| Başarı | emerald/green | metin + ikon |
| Uyarı | amber/yellow | metin + ikon |
| Hata | rose/red | metin + ikon + eylem önerisi |
| Bilgi | sky/blue | metin + ikon |
| Primary eylem | vurgu token değeri | tek accent; ekranda tek primary |
| Seçili durum | vurgu token değeri | renk + işaret (ikon veya metin) |

- Aynı anlam için ikinci renk ailesi seçilmez.
- Açık ve koyu tema ayrı doğrulanır; bir temada eşiği geçmeyen çift yayınlanmaz.
- Durum metni Türkçe ve eyleme dönüktür; renk tek başına anlam taşımaz.

## 3. Boşluk ve ölçü token değerleri

| Kullanım | Aralık | Not |
| --- | --- | --- |
| Bileşen içi | 4/8/12 px | simetrik dikey dolgu |
| Grup içi | 8/12/16 px | ilişkili öğeler |
| Bölüm arası | 24/32/48 px | kavramsal ayrım |
| Pencere kenarı | 16/24/32 px | içerik kenara yapışmaz |

- Barem 4px; 4'ün katı olmayan ara değer yalnız tema token değerinde tanımlanır.
- Sabit ölçüde kırpma yok; esnek büyüme ve asgari sınır kullanılır.
- Pencere ve panel ölçüleri references/yerlesim-pencere.md dosyasındadır.

## 4. Tipografi token değerleri

| Rol | Kural |
| --- | --- |
| Başlık | token puntosu + güçlü ağırlık; hiyerarşi ağırlıkla kurulur |
| Gövde | taban punto; satır yüksekliği token değerinden |
| Etiket | gövdeden küçük; orta ağırlık |
| Yardım metni | küçük punto; kontrast AA |
| Sayısal veri | eşit genişlikli rakam; sağa hizalı |

- Metne serbest punto veya piksel boyutu verilmez.
- İki-üç ağırlık yeterlidir; fazlası hiyerarşiyi bulanıklaştırır.
- Metin büyütmesinde düzen kırılmaz; uzun metin kırpılmaz.

## 5. Hareket token değerleri

| Token kategorisi | Kullanım | Kural |
| --- | --- | --- |
| Kısa süre | bası, vurgu, küçük geçiş | tema token değeri |
| Orta süre | panel ve katman açılışı | tema token değeri |
| Uzun süre | büyük düzen değişimi | nadir ve gerekçeli |
| Giriş/çıkış eğrisi | durum geçişleri | tema token değeri |
| Yay/momentum | sürükleme ve sıçrama | platform desteği doğrulanır |

- Serbest süre ve eğri yazılmaz; süre tema hareket token değerinden okunur.
- Azaltılmış harekette animasyon hedef duruma sıçrar.
- Animasyon tamamlanınca kare istemi durur; boşta kare istenmez.
- Kesin token adları ve süre değerleri için resmî belge doğrulanır; bu dosya API adı taşımaz.

## 6. Bileşen kullanım kuralları

| Bileşen | Zorunlu kural | Durumlar |
| --- | --- | --- |
| Buton | platform kataloğundan; varyant platformdan; etiket metni | varsayılan, hover, basılı, odak, devre dışı, yükleniyor |
| Girdi | görünür etiket; hata ve yardım metni alana bağlı | normal, odak, hata, devre dışı, salt-okunur |
| Tablo/liste | başlık tanımlı; sayısal kolon hizalı; yoğunluk boyut ölçeğiyle | yükleniyor, boş, hata, dolu |
| Modal/katman | yüzey-üst token değeri; odak tuzağı; çıkış yolu | açık, kapanıyor |
| Bildirim | tek kanal; durum rengi + metin + ikon | bilgi, başarı, hata |
| Menü/araç çubuğu | platform geleneği; kısayol etiketi görünür | açık, seçili, devre dışı |

- Standart kontrolü sıfırdan yazmak yasaktır; katalogda olmayan ihtiyaç önce katalog bileşeniyle çözülür.
- Bileşen rengi ve dolgusu elle geçersiz kılınmaz; varyant ve token kullanılır.
- Etkileşim hedefi en az 24x24 mantıksal pikseldir.
- Yükleme ve hata durumu metinle bildirilir; yalnız görsel gösterge yeterli değildir.

## 7. İkon kataloğu

- Tek ikon seti Lucide'dir; ikonlar yalnız platform varlık kataloğundan gelir.
- Yerel SVG, ikon fontu, sprite ve ikinci set yasaktır.
- İkon boyutu tipografi token değerinden türetilir; serbest piksel verilmez.
- Yalnız ikon taşıyan kontrol erişilebilir ad taşır; dekoratif ikon erişilebilirlik ağacından gizlenir.
- İkon yalnız anlam taşıdığında kullanılır; süs ikonu eklenmez.

## 8. Token genişletme akışı

1. Eksik rolü belirle: renk, yarıçap, boşluk, tipografi veya hareket.
2. Tema kaynağında alanın var olup olmadığını resmî belgeden doğrula.
3. Alan yoksa ürün temasında tanımla; çağrı yerine değer gömme.
4. Açık ve koyu temada değeri doğrula, kontrastı ölç.
5. Tanımı tek yerde tut; bileşenlerde tekrar tanımlama.

## 9. Doğrulama adımları

1. Sabit değer taraması: hex, rgb ve sabit süre/yarıçap aramaları boş döner.
2. Açık ve koyu tema görsel denetimi yapılır; kontrast ölçülür.
3. Bileşen envanteri çıkarılır: elle yazılmış kontrol kalmamıştır.
4. İkon denetimi yapılır: katalog dışı varlık yoktur.
5. Token, varyant ve hareket alanları resmî belge veya context7 ile doğrulanmıştır.

## Kaynaklar

1. gpui-kit stil ve tema rehberi — https://gpui-kit.com/docs/style
2. gpui-kit varlık ve ikon rehberi — https://gpui-kit.com/docs/assets
3. gpui-kit tasarım ilkeleri — https://gpui-kit.com/docs/design-guides
4. WCAG 2.2 (W3C Recommendation, 12 Aralık 2024) — https://www.w3.org/TR/WCAG22/