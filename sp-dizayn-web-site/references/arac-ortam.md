# Araç ve Ortam — keşif, eşleme, hibrit kullanım

> `sp-dizayn-web-site` eki; gövdedeki 7. bölümün ayrıntısıdır. Araç adı geçen her yerde çağrılabilirlik çalışma anında kanıtlanır; bu dosya envanter değil, keşif ve karar protokolüdür. Sürüm, API ve araç mekaniği iddiası taşımaz.

## 1. Araç keşif protokolü

1.1. Üç kanıt katmanı aranır: oturum kataloğunda ad, fiziksel dizinde SKILL.md, canlı çağrıda yanıt. Üçü tamamlanmadan araç var sayılmaz.
1.2. Keşif sırası: beceri kataloğu, beceri dizinleri ve SKILL.md, MCP sunucu listesi ve tek canlı çağrı, PATH'teki yerel komutlar, proje araç zinciri. Sıra atlanmaz.
1.3. MCP aracı için bağlantı canlı çağrıyla sınanır; envantere bağlı yazmak için yanıt şarttır. Sunucu tanımlı ama hedef uygulama kapalıysa araç kullanılamaz sayılır.
1.4. Yerel araç için --help, sürüm veya zararsız bir örnek komut çalıştırılır; çıktı yoksa araç yok sayılır.
1.5. Keşif sonucu envanter satırına yazılır: ihtiyaç, aday, çağrı yolu, kanıt türü, yedek ve tarih. Kanıtsız satır doğrulanmalı etiketi taşır.
1.6. Envanter iş başında ve yeni yetenek gerektiğinde tazelenir; eski tarihli kayıt güncel karar dayanağı değildir.

## 2. İhtiyaç → araç matrisi

Tablodaki adaylar yön gösterir; her satırın kanıt durumu kullanımdan önce yeniden sınanır. Kanıtsız araç işe bağlanmaz.

| İhtiyaç | Aday (envanterdeki durum) | Yedek ve kural |
|---|---|---|
| Sanat yönü | design-taste-frontend, frontend-design, hallmark, impeccable, brand, ui-ux-pro-max (katalogda tanımlı; canlı kullanım sınanır) | Kullanıcı brief'i ve yerel referans arşivi; kompozisyon kopyalanmaz |
| Metin | brand ve tasarım paketi akışı (tanımlı) | Gerçek malzeme ile insan editör; uydurma iddia yasak |
| Görsel | Üretken görsel yalnız bağlıysa; kullanıcı fotoğrafı ve açık lisans arşiv adaydır | Araçsız tasarlanmış statik kompozisyon, CSS/SVG |
| Video ve hareket | hyperframes, remotion, gsap-* (envanterde yanıt veya global kayıt var; kullanımdan önce sınanır) | CSS/WAAPI ve poster; üretken video yoksa statik sahne |
| Ses | sound-effects, sound-design (dizin ve SKILL.md var) | Varsayılan sessiz; açık istekte CC0 kit |
| 3B | blender MCP (envanterde eklenti bağlantısı başarısızdı; açılmadan kullanılamaz), img2threejs | Kod tabanlı Three.js, CSS/SVG; 3B gerekmiyorsa kullanılmaz |
| Tarayıcı ve QA | chrome-devtools MCP (canlı çağrı doğrulandı) | MCP yoksa manuel tarayıcı ve Lighthouse |
| Performans | chrome-devtools trace ve debug-optimize-lcp; trace ilk çalıştırmada sınanır | Laboratuvar ölçümü; alan verisi yoksa doğrulanmalı |
| Erişilebilirlik | a11y-debugging, chrome-devtools snapshot ve lighthouse | Elle klavye, kontrast ve odak ölçümü |
| SEO | Site mimarisi becerisi ve lighthouse SEO denetimi | Elle meta/JSON-LD ve canlı yanıt kontrolü |
| Varlık iyileştirme | ffmpeg ve Pillow (PATH'te; biçim desteği sınanır) | Pillow ve ffmpeg; eksik araç varsayılmaz |
| Prototip | Statik önizleme ve chrome-devtools | Tek HTML dosya, yerel sunucu ve tarayıcı |

Envanterde adı geçmeyen üretken üretim veya barındırma connector'ı yok sayılır; onun yerine yalnız yöntem ve manuel adım kullanılır.

## 3. Hibrit kullanım örnekleri

3.1. Görsel hattı: yön becerisiyle kompozisyon kararı, varlığın kullanıcıdan veya açık lisans arşivinden temini, ffmpeg/Pillow ile optimize, chrome-devtools ile sayfada doğrulama. Her adım kendi kanıtını üretir.
3.2. Hareket hattı: kod tabanlı üretim veya kullanıcı videosu, ffmpeg ile encode ve poster, tarayıcıda oynatma, seek ve reduced-motion kontrolü. Poster ve mobil statik alternatif ayrı doğrulanır.
3.3. QA hattı: chrome-devtools ile ekran, konsol ve ağ; Lighthouse veya a11y denetimi; metin ve imlâ taraması; ölçüm kaydı. Tek araç tam kabul üretmez.
3.4. Hibrit kuralı: bir aracın çıktısı diğerinin kanıtı yerine geçmez; araç yoksa tasarım statik ve dürüst fallback'e düşer, kalite iddiası da buna göre düşürülür.
3.5. Zero-build sınırı: hiçbir araç siteye Node bağımlılığı, CDN kütüphanesi veya ikinci stil dosyası sokamaz; araç çıktısı assets/ altında statik varlığa dönüşür.

## 4. Erişim hatasında tanı ve çözüm

4.1. Tanı sırası: hedef uygulama veya sunucu kapalı mı, bağımlılık eksik mi, ağ mı, yetki veya hesap mı, yol ya da sürüm uyumsuz mu. Şıklar tek tek ayrılır.
4.2. Basit çözüm: uygulamayı aç, yalnız gerekli bağımlılığı kur, gerekirse yerel veya offline alternatife geç. Ücretli hesap ve yeni abonelik zorlanmaz.
4.3. Tarayıcı MCP'si bağlanmıyorsa tarayıcı açılır; 3B MCP'si için uygulama ve eklenti açılır. Açılmıyorsa manuel doğrulama yapılır ve sonuç doğrulanmalı işaretlenir.
4.4. Dış connector yoksa ilke ve yöntem uygulanır; üretken medya, otomatik yayın ve sağlayıcıya bağlı adımlar atlanır; manuel adımlar açıkça yazılır.
4.5. Çözülemeyen erişimde işe başlamadan kullanıcıya bildirilir; sessiz vazgeçme ve sahte tamam yoktur.
4.6. Her tanı ve çözüm komut ya da yanıt çıktısıyla kayda geçer; çalıştı beyanı kanıtsızdır.

## 5. Ücretli araç, ağ ve lisans politikası

5.1. Ücretli araç, API anahtarı, kredi ve harici hesap varsayılmaz; onay olmadan harcama yapılmaz, fiyat veya indirim taahhüdü verilmez.
5.2. OpenArt, Hostinger ve HeyGen gibi ücretli sağlayıcılar bu ortamda varsayılmaz; connector yoksa yalnız yöntem kullanılır, üretim ve yayın adımı manuel ve doğrulanmalı olur.
5.3. Ağ yoksa yerel arşivler, ffmpeg ve Pillow, kod tabanlı görsel ve hareket kullanılır; ağ isteyen script çalıştırılmaz.
5.4. Lisans: yalnız kendi varlığı veya açık lisanslı malzeme kullanılır; credit zorunludur; marka referans dosyası kopyalanmaz.
5.5. Gerçek fotoğraf yalnız sahibinin izniyle işlenir; kişisel veri üretim aracına gönderilmez.
5.6. Ücretsiz araç da kanıt ister; kurulum ağ veya izin gerektiriyorsa plana yazılır, sessizce atlanmaz.

## 6. Güncellik ve doğrulama

6.1. Sürüm, API ve araç davranışı bu dosyaya gömülmez; context7 veya resmî kaynak çalışma anında doğrulanır.
6.2. Örnek komut, URL, model adı ve sağlayıcı adı kopyalanmaz; her kullanımda yeniden doğrulanır.
6.3. Doğrulanamayan bilgi doğrulanmalı etiketiyle teslim edilir.
6.4. Envanter tarih ve kanıtla tazelenir; süresi geçmiş envanter karar dayanağı olmaz.
