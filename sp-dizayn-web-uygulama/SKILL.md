---
name: sp-dizayn-web-uygulama
description: "Oturumlu panel ve uygulama arayüzlerinin YAPISAL tasarımı: kalıcı kabuk, yerleşim ve yoğunluk, tipografi ölçeği, durum renkleri, ikonlar, bileşen davranışları, yükleme/boş/hata durumları, WCAG 2.2 AA ve zero-build teslim. Şu durumlarda yükle: panel arayüzü, uygulama ekranı tasarımı, SCADA/dashboard, tutarlı uygulama hissi, bileşen/durum tasarımı. Kullanma: statik tanıtım sitesi, salt estetik dil talebi, backend ve veritabanı mimarisi; Vite SPA teslimi."
version: "v202610300420"
---

# sp-dizayn-web-uygulama

Oturumlu panel, gösterge tablosu ve uygulama ekranlarının yapısal tasarımı. Amaç dekorasyon değil **tam uygulama hissi**dir: her sayfa aynı kabuğu, aynı katalog bileşenlerini ve aynı davranışları taşır; kullanıcı yeni bir modülde hiçbir şeyi yeniden öğrenmez.

- Öncelik: kullanıcının güncel yazılı talimatı > ana anayasa > platform mimari becerisi > bu beceri > estetik dil becerisi.
- Sınır: bu beceri yapıyı ve davranışı tanımlar. Estetik dil (palet hissi, materyal, derinlik, hareket karakteri) `sp-zen-dizayn` alanıdır; statik tanıtım sitesi, backend, veritabanı ve dağıtım kapsam dışıdır; yalnız bunlar isteniyorsa yüklenmez. Vite+React SPA'nın derleme ve teslim hükümleri sp-mimari-web-spa'dadır.

## 1. Kabuk ve yerleşim

1.1. Her sayfa aynı iskeleti çizer: sidebar → üst çubuk → `<main>`. Gezinmede kabuğun sırası, konumu ve genişliği değişmez.
1.2. Kaydırma yalnız `<main>` içindedir; sidebar ve üst çubuk sabittir, gövde kaydırması yoktur.
1.3. İçerik `mx-auto max-w-7xl px-4 sm:px-6 lg:px-8` ile sınırlanır; istisna yalnız tam ekran harita, tekil topoloji şeması ve yatay kaydırmalı telemetri tablosudur, bu üç yüzey dışında `w-full` kullanılmaz.
1.4. Sayfa başına tek `h1` vardır; başlık seviyesi atlanmaz. Sayfa başlığı, eylem çubuğu ve içerik sırası tüm modüllerde aynıdır.
1.5. Menü tek katalogdan üretilir; tam bir öğe aktiftir (`bg-slate-100 font-medium text-slate-900` + `aria-current="page"` + durum ikonu).
1.6. Taşma çözülür, kırpılmaz: uzun metin `break-words`, sayısal hücre `tabular-nums text-right`, geniş tablo `overflow-x-auto` sarmalayıcıdadır.
1.7. 320 CSS px genişlikte yatay gövde kaydırması olmadan kullanılabilir; ızgara dar ekranda tek kolona iner ve hiçbir bileşen taşmaz.

## 2. Yoğunluk ve boşluk

2.1. Barem 4px'tir. Boşluklar 4/8/12/16/24/32/48/64 adımından seçilir: `gap-1`, `gap-2`, `gap-3`, `gap-4`, `gap-6`, `gap-8`, `gap-12`, `gap-16`. `p-[7px]`, `gap-[3px]`, `text-[13px]` gibi keyfi değer yoktur.
2.2. Dikey dolgu simetriktir ve 4px katıdır (`py-1` 4px, `py-2` 8px, `py-3` 12px, `py-4` 16px); `pt-2 pb-3.5` gibi asimetrik ya da 4px katı olmayan dolgu yasaktır.
2.3. Kart/kutu kalabalığı yoktur: aynı bilgi grubu tek yüzeyde toplanır; kart içinde kart ve her kutuya çerçeve+gölge+başlık yığma yoktur.
2.4. Yakınlık: ilişkili öğeler 4-8px, ayrı kavramsal gruplar 32-48px aralıkla ayrılır.
2.5. Veri yoğun yüzeylerde satır yüksekliği tokenla sabittir ve sayfa türüne göre değişmez; veri tablosu satırı 40px (`h-10`) alır.
2.6. Bölümler arası ayrım çizgi yığınıyla değil hizalama, tipografik kontrast ve zemin tonuyla kurulur; satır ayrımı tek `divide-y` çizgisinde kalır.

## 3. Tipografi

3.1. `font-sans` sistem yığınıdır; harici font ve gömülü web font yoktur. Taban gövde 13/14px'tir (`text-sm`); yoğunluğu azaltmak için `text-base` boyutuna zorlama yoktur.
3.2. Yalnız Tailwind ölçeği kullanılır: `text-xs` 12, `text-sm` 14, `text-base` 16, `text-lg` 18, `text-xl` 20, `text-2xl` 24 px. Keyfi punto yoktur.
3.3. Hiyerarşi ağırlıkla kurulur: `h1` `text-2xl font-semibold`, panel başlığı `text-lg font-semibold`, etiket `text-sm font-medium`, gövde normal ağırlıktadır.
3.4. Satır uzunluğu en fazla 75 karakterdir (`max-w-prose`); tablo hücresi ve etiket tek satıra zorlanmaz.
3.5. Sayılar `tabular-nums` ile hizalanır ve sağa yaslanır; birim aynı satırda kalır.

## 4. Renk ve durum

4.1. Yüzeyin en az %90'ı nötrdür (`slate`/`zinc`/`neutral`); renk yalnız tek primary CTA ve semantik durum için kullanılır.
4.2. Durum renkleri sabittir: başarı `emerald`/`green`, uyarı `amber`/`yellow`, hata `rose`/`red`, bilgi `sky`/`blue`. Sayfa bazında keyfi durum rengi seçilemez.
4.3. Ham hex, RGB ve keyfi renk değeri yoktur; renk yalnız Tailwind paletinden seçilir.
4.4. Durum yalnız renkle iletilmez: renk + metin + `lucide:` ikon birlikte kullanılır.
4.5. Metin kontrastı ≥4,5:1, büyük metin ≥3:1'dir; bileşen kenarı ve odak göstergesi ≥3:1 olur. Eşiğin altındaki çift kullanılmaz.
4.6. Odak göstergesi `focus-visible` ile her zeminde görünür kalır; odak halkası kaldırılamaz.

## 5. İkonlar

5.1. Tek sağlayıcı `<iconify-icon>`, tek önek `lucide:`; yükleyici sabit sürümle ve SRI ile yüklenir; sürüm ve SRI çalışma anında resmî kaynaktan doğrulanır. Yerel SVG, sprite, ikon fontu, base64 SVG ve ikinci ikon seti yoktur.
5.2. Metni olan eylem ve menü etiketi ikonla süslenmez; ikon ya metnin yerini tutar ya da durum bildirir (aktif menü, seçili öğe, durum rozeti).
5.3. Emoji hiçbir bağlamda kullanılmaz; anlamına uygun `lucide:` ikonu seçilir, metin bağlamında (seçenek, onay iletisi) ikon da eklenmez.
5.4. İkon boyutu metin ölçeğinden türetilir (`1em`); keyfi piksel değeri yoktur.
5.5. Dekoratif ikon `aria-hidden="true"` taşır; yalnız ikon içeren buton görünmez metin veya `aria-label` ile erişilebilir ada sahiptir.
5.6. Kodla üretilen dinamik vektör (şema, topoloji, grafik) bu kuraldan muaftır.

## 6. Bileşen davranışı

6.1. Her etkileşimli bileşen yedi durumu tanımlar: varsayılan, hover, focus-visible, active, disabled, loading, hata. Aynı bileşen her sayfada aynı sınıf ve davranışla kullanılır.
6.2. Buton: tek satır metin; `h-9` varsayılan (`h-8` yoğun tablo, `h-10` form), `transition-transform duration-150 ease-out active:scale-95`; hover bir ton koyulaşır; disabled `opacity-50 pointer-events-none`; loading `aria-busy="true"` + spinner + "Kaydediliyor" metni taşır.
6.3. Form: her alanın görünür `label` bağlantısı vardır; hata metni `aria-describedby` ve `aria-invalid` ile alana bağlanır; doğrulama sunucuda da tekrarlanır; hata Türkçe ve alanın yanındadır.
6.4. Tablo: `th` + `scope`, sıralama `aria-sort`, satır eylemi görünür veya menülüdür; yatay taşma `overflow-x-auto` ile çözülür.
6.5. Modal: `role="dialog" aria-modal="true"`, odak tuzağı, ESC ile kapanır ve odak tetikleyiciye döner; yıkıcı eylem onay ister ve geri alınamaz sonucu Türkçe yazar.
6.6. Panel: başlık + eylem satırı + içerik sırası tüm panellerde aynıdır; panel içinde ikinci kaydırma alanı açılmaz ve kart içine kart konmaz.
6.7. Her liste, tablo ve panel dört durumu tanımlar: yükleniyor (iskelet), boş (açıklama + tek CTA), hata (Türkçe mesaj + yeniden dene), dolu. Bağlantı kesilirse çevrimdışı durumu ayrıca gösterilir.
6.8. Arama yalnız envanter >100 kayıt veya arama birincil görevse eklenir; varsa gerçek indeksten sonuç döner ve boş durumda öneri sunar.
6.9. Bildirim tek kanaldan gelir: bilgi/başarı `role="status"`, hata `role="alert"`; aynı anda tek bildirim gösterilir.
6.10. Bileşen sınıf spec'leri ve token tabloları references/token-bilesenler.md dosyasındadır; §1-§6 uygulanırken oradan okunur.

## 7. Tutarlılık ve tam uygulama hissi

7.1. Üç farklı modül aynı kabuk sırasını, aynı boşluk ritmini ve aynı bileşen sınıflarını taşır; sayfalar arası geçişte konum sıçraması olmaz.
7.2. Her ekranda tek primary CTA vardır; diğer eylemler ikincil veya üçüncüldür. Primary CTA dışında vurgu rengi kullanılmaz.
7.3. Aynı veri türü aynı biçimde gösterilir: tarih, para, yüzde, kimlik ve durum rozeti biçimi katalogda tektir.
7.4. Kabul ölçütü: kullanıcı hiç görmediği bir modülde menüyü, başlığı, eylem çubuğunu ve durum bileşenlerini yeniden öğrenmez; iki modülün aynı bileşeni arasında sınıf farkı yoktur.

## 8. Hareket

8.1. Geçiş 150ms `ease-out` olur; yalnız `transform` ve `opacity` hareket eder. Tıklanabilir buton ve kartta `active:scale-95` bası tepkisi vardır.
8.2. Animasyon kesintiye uğratılabilir: yeni etkileşim mevcut geçişi hedefe yönlendirir, sıfırlamaz.
8.3. Dekoratif, sürekli veya nabız gibi dikkat çeken animasyon yoktur; hareket yalnız durum değişimini açıklar.
8.4. `prefers-reduced-motion: reduce` altında geçiş ve dönüşüm kapanır: `motion-reduce:transition-none motion-reduce:transform-none motion-reduce:animate-none`; JS hareketi `matchMedia` kontrolüyle atlanır.
8.5. Kontrol listesi: references/erisilebilirlik-hareket.md.

## 9. Erişilebilirlik

9.1. Hedef WCAG 2.2 AA'dır; ihlal eden sürüm teslim edilmez.
9.2. Klavye: her işlev Tab, Shift+Tab, Enter, Space ve Escape ile tamamlanır; odak sırası DOM sırasını izler; görünür odak kaldırılamaz.
9.3. Etiket: her form alanı görünür etiketlidir; ikon-only buton erişilebilir adlıdır; tablo başlıkları programatik tanımlıdır; dekoratif görsel `alt=""` taşır.
9.4. Hedef boyut ≥24x24 CSS px'tir; yapışkan çubuk ve sidebar klavye odağını örtmez; içerik 320px'te yeniden akar.
9.5. Durum değişimi canlı bölgeyle duyurulur; kısmi güncellemede odak değişen bölgeye taşınır ve sonuç duyurulur.
9.6. Kontrol listesi: references/erisilebilirlik-hareket.md.

## 10. Teslim

10.1. Stil kaynağı, sabit sürümlü Tailwind tarayıcı motoru (sürüm resmî kaynaktan doğrulanıp pinlenir) ve şablondaki `<style type="text/tailwindcss">` bloğundaki `@theme` tokenlarıdır; derleme adımı, PostCSS, ikinci CSS dosyası ve serbest `<style>` bloğu yoktur.
10.2. Stil Tailwind utility sınıflarıyla verilir; satır içi `style` yalnız JS'in hesapladığı dinamik koordinat ve ölçüde kullanılır; `innerHTML` ile stil enjekte edilmez.
10.3. htmx (sürüm resmî kaynaktan doğrulanıp pinlenir) yalnız kısmi etkileşimde (liste yenileme, satır içi form, modal içerik) kullanılır; tam sayfa gezinme normal bağlantıyla yapılır, kısmi yanıt yalnız hedef bölgeyi değiştirir ve istemci tarafı şablon motoru yoktur.
10.4. Sayfa iskeleti ve `@theme` bloğu: references/token-bilesenler.md.
10.5. Satır içi olay özniteliği (`hx-on`) kullanılmaz; CSP etkisi ve alternatif desen sürümün resmî dokümanından doğrulanır. Davranış `data-*` ve `js/app.js` sözleşmesiyle kurulur.
10.6. CSP, seçilen motorların gerçek davranışına göre resmî dokümanla belirlenir; stil katmanının gerektirdiği izin gerekçelenir, `script-src` içinde `unsafe-eval` bulunmaz.
10.7. Tarayıcı motorunun üretim uygunluğu ve lisansı resmî dokümandan doğrulanır; zero-build politikası gereği üretimde kullanılıyorsa gerekçe release kaydında yazılır.
10.8. Vite+React SPA hedefinde derleme ve stil kaynağı sp-mimari-web-spa hükmüne tabidir; bu bölümdeki zero-build teslim kuralları uygulanmaz.

## Kabul kapısı

- [ ] Üç modül çıktısında sidebar, üst çubuk ve `<main>` aynı sıradadır; sayfada tek `h1` vardır.
- [ ] Statik tarama `(bg|text|border)-\[#`, `text-\[[0-9]`, `(p|px|py|gap)-\[[0-9]` kalıplarında eşleşme üretmez.
- [ ] `aria-current="page"` yalnız bir menü öğesindedir; arama yalnız >100 kayıt veya birincil görev sayfasında vardır.
- [ ] Her liste ve tablo yükleniyor, boş, hata ve dolu durumlarını içerir.
- [ ] Klavye turunda odak tuzağı yalnız modaldadır; ESC kapatır ve odak tetikleyiciye döner.
- [ ] 320px genişlikte yatay gövde kaydırması yoktur.
- [ ] reduced-motion emülasyonunda geçiş ve animasyon durur.
- [ ] Kontrast ölçümünde 4,5:1 altında metin, 3:1 altında bileşen ve odak çifti yoktur.
- [ ] `style=` taraması yalnız dinamik ölçü satırlarını döner; ikonlar yalnız `lucide:` önekiyle basılır.