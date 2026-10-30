# on-yuz-htmx — SSR teslimi, Tailwind tarayıcı motoru, htmx, istemci sözleşmesi

> Bu dosya sp-mimari-web-uygulama becerisinin references dosyasıdır; gövdedeki 5. bölümün ayrıntısını taşır. Sürüm, SRI ve motor davranışı iddiaları burada tutulmaz; çalışma anında resmî kaynaktan doğrulanır. Yapısal UI ve erişilebilirlik ayrıntısı sp-dizayn-web-uygulama alanındadır.

## 1. SSR teslimi

1.1. Sayfalar sunucuda render edilmiş HTML olarak teslim edilir; SPA framework, istemci tarafı yönlendirici ve sanal DOM katmanı yasaktır.
1.2. Tam sayfa gezinme normal bağlantıyla yapılır; kısmi etkileşim yalnız tanımlı bölgelerde kullanılır.
1.3. Sunucu yanıtı tek doğruluk kaynağıdır; istemci aynı iş kuralını yeniden üretmez.
1.4. İlk açılışta sayfa kabuğu ve içerik aynı yanıtta gelir; istemci tarafında zorunlu ikinci istek yoktur.

## 2. Tailwind tarayıcı motoru

2.1. Tek stil kaynağı sabit sürümlü Tailwind tarayıcı motorudur; sürüm, URL ve SRI release anında resmî kaynaktan doğrulanır ve pinlenir.
2.2. Derleme adımı, PostCSS ve standalone ikili yoktur; sınıflar tarayıcıda üretilir.
2.3. Depoda CSS dosyası tutulmaz; tema yalnız şablondaki text/tailwindcss bloğunda @theme tokenlarıyla tanımlanır.
2.4. @theme yalnız token tanımlar; ham değer, utility dışı serbest CSS ve ikinci stil dosyası yasaktır.
2.5. Çalışma zamanında ikinci stil CDN'i veya serbest stil bloğu kullanılmaz; release'de CSP ile uyum doğrulanır.
2.6. Motorun üretim uygunluğu ve lisansı resmî kaynaktan doğrulanır; zero-build istisnası release kaydında gerekçelenir.
2.7. Stil kararları (token, ölçek, renk, durum) yapısal tasarım becerisinde tanımlıdır; bu dosya yalnız teslim sözleşmesini bağlar.

## 3. htmx

3.1. htmx yalnız gerekli kısmi etkileşimde kullanılır: liste yenileme, satır içi form, modal içerik. Tam sayfa gezinme normal bağlantıdır.
3.2. Yükleyici kendi alan adımızdan sabit sürümle servis edilir; release'de SRI doğrulanır.
3.3. Sunucu kısmi yanıtı üretir; yanıt yalnız hedef bölgeyi değiştirir; istemci tarafı şablon motoru yoktur.
3.4. CSRF başlığı tek istemci sözleşmesinden (configRequest) eklenir; modül içinde kopya yoktur.
3.5. Satır içi olay özniteliği kullanılmaz; davranış data-* ve istemci sözleşmesiyle kurulur. CSP etkisi sürümün resmî dokümanından doğrulanır.
3.6. Kısmi yanıtın hata durumu Türkçe mesajla ve hedef bölgeyi bozmayan geri dönüşle gösterilir.

## 4. İstemci sözleşmesi

4.1. İstemci betiği belge başının sonunda defer ile yüklenir; tek sözleşme dosyası vardır.
4.2. Sözleşme apiIstek, bildirimGoster ve htmlTemizle üzerinden çalışır; modül içi fetch, kaçış üretimi ve bağımsız hata kanalı yasaktır.
4.3. Yakalanmamış hata ve söz redleri tek bildirim kanalına bağlanır; sessiz yutma yoktur.
4.4. İstemciye iş kuralı gömülmez; doğrulama sunucuda tekrarlanır.

## 5. Varlık ve bütçe

5.1. İstemci varlıkları kendi alan adımızdan sabit sürümle servis edilir; harici varlık CDN'i yoktur; stil motoru ve ikon yükleyicisi sabit sürümlü istisnadır.
5.2. Yerel JS gzip toplamı ve toplam istemci varlığı için proje bütçesi tanımlıdır; bütçe değerleri beceriye gömülmez, release kaydında ölçülür.
5.3. Bütçe aşımı kök neden giderilmeden release edilmez; ölçüm komutu ve sonucu kanıtlanır.
5.4. Varlık sürümü değiştiğinde SRI ve CSP birlikte güncellenir; eski sürüm kaydı silinmez.

## 6. İkon teslimi

6.1. Tek sağlayıcı Iconify Web Component, tek önek lucide:; yükleyici pinlidir ve release'de SRI ile doğrulanır; sürüm ve SRI çalışma anında doğrulanır.
6.2. Yerel SVG, sprite, ikon fontu, base64 SVG ve ikinci ikon seti yasaktır; kodla üretilen dinamik vektörel grafikler muaftır.
6.3. İkonlar çalışma anında resmî API'den çekilir; bağlantı izni CSP connect-src ile release'de doğrulanır.
6.4. İkon seçimi, boyutu, dekoratif ve erişilebilir kullanımı yapısal tasarım becerisinin alanındadır; bu dosya yalnız teslim sözleşmesini bağlar.

## 7. Release doğrulaması

7.1. CSP ve SRI değerleri release anında resmî kaynak ve gerçek motor davranışıyla doğrulanır; varsayım yapılmaz.
7.2. Erişilebilirlik ölçümü yapılmadan ön yüz release edilmez; ölçüm tasarım becerisinin kontrol listesine göre yapılır.
7.3. Başlık, SRI ve gzip ölçümleri references/kabul-kapilari.md altındaki kapılarla kanıtlanır.
