# Sinematik Katman — scroll, 3B ve zaman çizelgesi

> sp-dizayn-web-site gövde 1.6 ve 6.5'in ayrıntısı. Sınır: JS/GPU bütçesi, barındırma ve release kapıları sp-mimari-web-site alanındadır; bu dosya deneyimin mimarisini ve kanıtını tanımlar.
> Kural: sürüm, API ve kütüphane davranışı gömülmez; çağrı biçimi ve parametreler çalışma anında context7, resmî doküman veya ilgili gsap-* becerisinden doğrulanır.

## 1. Karar kapısı

1.1. Üç soru: anlatı gerçekten kamera, derinlik veya zaman içinde değişim istiyor mu; bu hareket olmadan içerik anlaşılmıyor mu; ekip, cihaz ve bütçe 60 fps ile üç durumlu fallback'i kaldırıyor mu? Üçü evet değilse sinematik katman açılmaz.
1.2. Dört mod: A. editoryal/statik (sinematik yok); B. kare dizisi veya video scrub; C. gerçek zamanlı WebGL/3B; D. sayfa geçişi. D tek başına sinematik hero yerine geçmez.
1.3. Reddetme: imza "kamera uçuşu" değil de içerikteyse 3B pahalı bir süstür; önce tipografi, kompozisyon, görsel ve ses ile çözülür.
1.4. Karar design package'a yazılır: mod, sayfa uzunluğu (vh), varlık listesi, JS/GPU bütçesi, fallback, mobil koreografi, lisans ve onay. Mod değişikliği yeni onay ister.

## 2. Scroll orkestrasyonu

2.1. Tek kaydırma otoritesi: bir smooth-scroll/ticker katmanı; smooth-scroll sağlayıcısı varsa tek ticker'a bağlanır, ikinci rAF açılmaz ve iki kütüphane birbirinin kaydırmasını ezmez.
2.2. Zaman çizelgesi: kaydırma ilerlemesi tek zaman çizelgesine bağlanır; sahne sabitlenir (pin) ve ilerleme animasyona yumuşak bağlanır (scrub). Yumuşatma değeri proje testiyle seçilir; kontrolsüz gecikme eklenmez.
2.3. Sayfa uzunluğu içerikten türetilir: her sahne yaklaşık 1-1,5 ekran; toplam tipik 300-500vh. Boş 500vh yasaktır; her ekranın bir işi vardır.
2.4. Duruşlar: sahne başında ve sonunda okunabilir hold; hızlı flick, ters kaydırma ve yenileme ortasında aynı kareye dönüş test edilir.
2.5. Girdi: tekerlek, tuş, dokunma ve erişilebilirlik aynı ilerlemeyi sürer; scroll-jacking, tekerlek hızını ezme ve klavye kilidi yoktur. Bağlantılar ve odak normal çalışır.
2.6. Reduced motion hareketi atlar, içerik ve eylem final durumda görünür; gizli içerik değildir. Gizli sekmede ve görünür olmayan sahnede döngü durur.

## 3. Kare dizisi ve video scrub

3.1. Ne zaman: gerçek çekim veya AI video ile sinematik kamera hareketi; etkileşim düşük, anlatı doğrusal.
3.2. Varlık: sıralı kareler (WebP/AVIF) veya kısa sessiz video; poster, mobil dikey kaynak ve her karenin okunabilir olması gerekir.
3.3. Eşleme: kaydırma yüzdesi kare indeksine bağlanır; ileri, geri ve rastgele seek aynı kareyi vermelidir. Ön yükleme penceresi ve bellek sınırı ölçülür.
3.4. Video yerine kare dizisi: ileri-geri sarma gerekiyorsa tarayıcının video seek davranışına güvenilmez; kare dizisi daha öngörülebilirdir.
3.5. Eşik: kare sayısı × boyut bütçeyi aşıyorsa çözünürlük veya kare aralığı düşürülür; kalite sessizce düşürülmez, kompozisyon sadeleşir ve kullanıcı bilgilendirilir.
3.6. Video kullanılıyorsa poster LCP'yi taşır, preload yok, otomatik ses yok, mobilde ayrı kaynak veya doğrulanmış kırpma; oynatma kontrolü ve fallback poster ile çalışır.

## 4. WebGL ve 3B sahne

4.1. Ne zaman: gerçek kamera rayı, ışık, malzeme veya model etkileşimi anlatının parçasıysa. Değilse 2B derinlik, paralaks, kare dizisi veya statik sahne tercih edilir.
4.2. Mimari: tek canvas, tek render döngüsü; sahne görünürken çalışır. DOM metni canvas üstünde kalır; metin canvas içine gömülmez.
4.3. Kamera rayı kaydırmaya bağlanır; her bölümün bir kamera duruşu vardır; geçişler easing ile yapılır, ani kesme yoktur.
4.4. Bütçe: düşük poligon, sınırlı doku, cihaz piksel oranı üst sınırı, sınırlı çizim çağrısı ve shader maliyeti ölçülür; post-process ağırlığı gerekçelenir ve mobilde kapanır.
4.5. GLSL/shader: efekt anlatıya hizmet eder; derleme hatası, bağlam kaybı ve düşük GPU için fallback vardır; kaynak ve lisans kayda geçer.
4.6. Yaşam döngüsü: geometri, materyal, doku ve hedefler bırakılır; olay dinleyicileri sökülür; resize ve görünürlük yönetilir; bellek sızıntısı yoktur.
4.7. Varlık: GLB/glTF ve dokular hedef tarayıcıda doğrulanır; sıkıştırma desteklenmiyorsa fallback; model kaynağı ve lisans kaydı tutulur.

## 5. Kütüphane ve teslim politikası

5.1. Üç yol: (a) vanilya + kopyalanabilir statik motor (ör. 10k-websites engine; motor CSS'i tek site.css'e birleştirilir, aksi halde kullanılmaz); (b) self-host GSAP + ScrollTrigger + Lenis; (c) Three.js. Seçim moda, bütçeye ve lisans doğrulamasına göredir.
5.2. CDN yoktur; tüm betikler self-host edilir, ikinci stil dosyası teslim edilmez. Kütüphane sürümü/lisansı çalışma anında resmî kaynaktan doğrulanır; kopyalanan motorun kaynağı ve lisansı kayda geçer.
5.3. JS bütçesi istisnası proje kaydında onaylanır; varsayılan bütçe aşılıyorsa gerekçe, ölçüm, fallback ve geri alma yazılır. İstisna sayfa bazlıdır.
5.4. Aynı sayfada iki scroll otoritesi, iki animation loop veya iki 3B bağlamı olmaz. "Sinematik" iddiası araç adıyla değil; trace, frame süresi, ekran ve cihaz testiyle kanıtlanır.

## 6. Sayfa geçişleri

6.1. Çok sayfalı sitede geçiş aynı dünyayı sürdürür; beyaz flash, düzen sıçraması ve odak kaybı yoktur.
6.2. View Transitions veya Barba benzeri çözüm seçilirse erişilebilirlik, odak ve reduced-motion doğrulanır; desteklemeyen tarayıcıda normal yükleme fallback'i vardır.
6.3. Geçiş kısadır; içerik geçiş bitmeden okunabilir; hızlı tıklamada birikme ve yarım kalan geçiş yoktur. Geri/ileri, kaydırma konumu ve başlık korunur.

## 7. Tipografi ve içerik filmle

7.1. Film varsa metin sahne koreografisine bağlanır; her başlık için duruş, giriş/çıkış ve okunabilir plato yazılır.
7.2. Statik hero metni ayrı yazılır: video yoksa veya reduced motion açıksa poster üstünde başlık, alt satır ve CTA okunur kalır.
7.3. Metin DOM'da kalır; kontrast en kötü kareye göre ölçülür; yerel scrim/gölge gerekçelenir. Telefon koreografisi ayrı yazılır; masaüstü değerleri kopyalanmaz.

## 8. Fallback, erişilebilirlik ve kanıt

8.1. Her sinematik öğe için üç durum tasarlanır: tam deneyim, reduced motion final durumu, WebGL/video yokluğu. Üçü de içerik ve eylem açısından eksiksizdir.
8.2. İçerik JavaScript veya animasyon olmadan okunur; klavye ve ekran okuyucu akışı bozulmaz; otomatik ses ve odak tuzağı yoktur.
8.3. Ölçüm: uzun görev, frame süresi, CLS, LCP ve transfer boyutu; chrome-devtools trace'i ve gerçek cihaz kontrolü. Emülasyon gerçek cihaz sayılmaz; konsol sıfır hata, bağlam kaybı ve ağ hatası test edilir.
8.4. Kanıt kabul kapılarına yazılır; kanıtsız "akıcı" beyanı yoktur.

## 9. Kaçınılacaklar

9.1. Scroll-jacking, tekerlek hızını ezme, klavye ve erişilebilirlik kilidi.
9.2. Her bölümde parallax, sürekli döngü, otomatik ses, ağır shader ve post-process; içerik olmadan 500vh boşluk.
9.3. Masaüstü sahnesini telefona kırpmak; reduced motion'ı görmezden gelmek.
9.4. CDN'den kütüphane, sürüm/lisans doğrulamadan kopya motor, lisanssız model/doku; aynı sayfada iki smooth-scroll, çift rAF.

## 10. Araç yönlendirmesi

10.1. Karar ve his: design-taste-frontend veya impeccable; motion-design-principles, apple-design, animate. Scroll/GSAP: gsap-core, gsap-scrolltrigger, gsap-timeline, gsap-plugins, gsap-performance, gsap-utils; çağrı biçimi resmî beceriden veya context7'den doğrulanır.
10.2. 3B: title-sequence-3d, img2threejs, web-sims, blender MCP (bağlıysa), threejs-devtools-mcp (harici). Kare dizisi/video: 10k-websites motoru, ffmpeg/Pillow; site dışı medya için hyperframes veya remotion.
10.3. Doğrulama: chrome-devtools, a11y-debugging, animation-performance, debug-optimize-lcp. Ayrıntılı eşleme ve harici MCP durumu references/arac-ortam.md dosyasındadır.
