---
name: sp-zen-dizayn
description: "Apple'ın klasik/ilk iPhone döneminin (iPhone 5 ve öncesi) sade ama göze hoş gelen tasarım dilini estetik referans olarak tanımlar: sakin renk, cömert boşluk, sistem tipografisi, hafif derinlik ve doğal hareket. Şu durumlarda yüklenir: Apple tarzı arayüz, klasik iPhone sadeliği, sade ve göze hoş tasarım dili, zen/minimal estetik istendiğinde. Yapısal veya teknik uygulama istendiğinde kullanılmaz; bileşen, yerleşim, kod ve erişilebilirlik platform becerilerinin alanıdır."
version: "v202610300440"
---

# sp-zen-dizayn

Sade ama göze hoş gelen bir arayüzün estetik dilini tarif eder: neyin sakin, tanıdık ve ustalıklı hissettirdiğini söyler; bileşeni, yerleşimi ve kodu kurmaz. Uygulama sorusunun yanıtı platform becerilerindedir; bu becerinin yanıtı "nasıl hissettirmeli" sorusudur.

## Ne zaman / ne zaman değil

| Kullan | Kullanma |
| --- | --- |
| "Apple tarzı arayüz", "klasik iPhone sadeliği" istendiğinde | Bileşen, yerleşim, ızgara veya durum davranışı kurulacaksa |
| "Sade ve göze hoş tasarım dili", "zen/minimal estetik" tarifi istendiğinde | Kod, token altyapısı, tema mimarisi veya derleme işi varsa |
| Renk, boşluk, tipografi ve hareket karakteri seçilirken | Erişilebilirlik denetimi, performans bütçesi veya test isteniyorsa |
| Mevcut arayüzün estetik yönü tartışılırken | Platforma özgü API, sürüm veya bileşen sözleşmesi kararı verilecekse |

Estetik dil ile uygulama aynı işte gerekiyorsa ikisini birlikte yükle: platform becerisi yapıyı, bu beceri hissi belirler.

## Estetik çekirdek

Apple'ın sekiz tasarım ilkesinden süzülen beş çekirdek bu dilin omurgasıdır:

1. **Amaç:** Her öğe bir işe yarar; yaramayan öğe eklenmez.
2. **Sakinlik:** Arayüz yarışmaz; tek vurgu, sakin yüzey ve dengeli boşluk dikkat çeker.
3. **Ustalık:** Hizalama, boşluk ve tipografi keyfi değildir; her değer savunulabilir.
4. **Tanıdıklık:** Bilinen davranış ve yerleşim korunur; sürpriz yenilik yerine öngörülebilirlik.
5. **Sürtünmesizlik:** Akıllı varsayılan, kısa yol ve tek adım; kullanıcı akışı kesilmez.

Zen katmanı:

- **Kanso (sadelik):** Gereksiz olan çıkar; ayrım çizgiyle değil ton, boşluk ve tipografiyle kurulur.
- **Ma (aktif boşluk):** Boşluk süs değil gruplama aracıdır; yakınlık ilişkiyi, uzaklık ayrımı anlatır.
- **Shizen (doğal hareket):** Hareket fizikten doğar; yapay süre ve sabit eğri yerine yay ve momentum kullanılır.
- **Görünmez teknoloji:** Arayüz kendini değil kullanıcının işini gösterir; bağlamı öngörür, doğru varsayılanı sunar, boş durumda tek eylem önerir.
- **Kademeli odak:** Ekranda tek primary eylem; ayrıntı katman katman açılır.

**Sade-iyi-his:** Klasik iPhone döneminin dokulu, parlak skeuomorfizmi taklit edilmez. Alınan şey süs değil histir: net hiyerarşi, gerçek materyal hissi, yumuşak hareket ve dokununca anında yanıt veren yüzey.

## Renk

- Yüzeyin en az %90'ı nötr ton ailesindedir; sıcak-soğuk tek aile seçilir, karıştırılmaz.
- Tek vurgu rengi kullanılır; vurgu primary eylemde ve seçili durumda görünür, geri kalanı nötrdür.
- Ham hex renk kodlanmaz; token önerisi: `--yuzey`, `--yuzey-ust`, `--metin`, `--metin-soluk`, `--sinir`, `--vurgu`.
- Durum renkleri sabittir: başarı `emerald`, uyarı `amber`, hata `rose`, bilgi `sky`; ton aynı ailede kalır.
- Renk tek başına anlam taşımaz; durum her zaman metin veya ikonla birlikte verilir.
- Kontrast WCAG 2.2 AA eşiğinin altına inmez; estetik gerekçe erişilebilirliği esnetmez.

## Boşluk

- Barem 4px'tir; 8pt ritim kullanılmaz. Adımlar: 4, 8, 12, 16, 24, 32, 48, 64.
- Beyaz alan cömerttir: içerik ekran kenarına yapışmaz, bölümler arasında 32-48px nefes payı kalır.
- Yakınlık hiyerarşisi: ilişkili öğeler 4-8px, farklı gruplar 32-48px aralıkla ayrılır.
- Dikey dolgu simetriktir; asimetrik dolgu optik dengeyi bozar.
- Ayrımı önce boşluk, sonra ton, en son ince çizgi kurar.

## Tipografi

- Varsayılan sistem fontudur; marka fontu zorunlu değil, tek aile yeterlidir.
- Optical sizing açık tutulur; yazı boyutla birlikte şekil değiştirir.
- Tracking boyuta göre değişir: büyük başlıkta negatif (yaklaşık -0.02em), gövdede sıfıra yakın, küçük etikette hafif pozitif.
- Leading boyutla ters çalışır: büyük başlık 1.05-1.15, gövde yaklaşık 1.5.
- Hiyerarşi ağırlık, boyut ve leading birlikte kurulur; iki-üç ağırlık yeterlidir.
- Satır uzunluğu 60-75 karakter aralığında tutulur; metin büyütmesinde düzen kırılmaz.

## Derinlik ve materyal

- Tek ışık ve tek yükseklik dili kullanılır; gölge yumuşak, düşük opaklıkta ve az sayıdadır.
- Yarı saydam katman yalnız platform destekliyorsa ve işlev taşıyorsa kullanılır; desteklenmiyorsa düz yüzey ve ton farkı yeterlidir.
- Gereksiz çerçeve, kutu ve ayırıcı çizgi yoktur; hiyerarşi boşluk ve tipografiyle kurulur.
- Materyal ağırlığı hiyerarşi taşır: yapısal yüzey daha ağır, etkileşimli yüzey daha hafif; açık yüzey üstüne açık yüzey konmaz.
- Gölge yığını ve dekoratif parlama yoktur; derinlik işlevi açıklar.

## Hareket

| Bağlam | Damping | Response |
| --- | --- | --- |
| Varsayılan geçiş | 1.0 | 0.3-0.4 |
| Momentumlu sürükleme/fırlatma | ~0.8 | 0.3-0.4 |
| Panel/katman açılışı | 0.8-1.0 | 0.3-0.4 |

- Hareket yay fiziğiyle kurulur; sabit süre ve sabit eğri yerine hedef değişince yay yeniden hesaplanır.
- Animasyon kesintiye uğratılabilir: canlı ekran değerinden başlar, kullanıcı yön değiştirince sıçramaz.
- Momentum projeksiyonu: hedef, bırakılan noktaya göre değil, hareketin gideceği yere göre seçilir.
- Giriş ve çıkış aynı yolu izler; aynı yönden giren aynı yöne çıkar.
- `prefers-reduced-motion: reduce` tercihinde kayma, yay ve paralaks yerine kısa cross-fade kullanılır.
- Animasyon zorunlu değildir; statik hâl de doğru kabul edilir. Sürekli veya nabız gibi atan animasyon yoktur.

## Geri bildirim

- Görsel tepki pointer-down anında başlar; bırakıldıktan sonra değil.
- Basılı hâl hafif ölçek küçülmesiyle (yaklaşık 0.97) ve kısa geçişle verilir.
- Sürükleme, kaydırma ve çekme sırasında geri bildirim kesintisiz sürer; yalnız sonuçta gösterilmez.
- Haptik yalnız destekleyen platformda kullanılır; desteklenmeyen yerde titreşim taklidi yapılmaz.
- Görsel, ses ve haptik aynı anda tetiklenir; nedeni belli olmayan ve sık tekrarlanan geri bildirim kullanılmaz.

## Yap / Yapma

| Yap | Yapma |
| --- | --- |
| Tek vurgu, nötr zemin | İkon enflasyonu; metin yeterliyken ikon |
| Cömert boşluk, az çizgi | Border ve ayırıcı çizgi kalabalığı |
| Sistem fontu ve ağırlık hiyerarşisi | Ölçek dışı punto, keyfi piksel |
| Ton farkıyla ayırma | Mor-mavi AI gradyanı, neon parlama |
| Tek yönlü, kesintisiz hareket | Sürekli, nabız gibi atan animasyon |
| Sakin durum geçişleri | Skeuomorfik doku ve gölge taklidi |
| Ham hex yerine token | Emoji ve süs ikonları |

## Sınırlar

- Öncelik: kullanıcı talimatı > AGENTS-tr > platform mimari becerisi > platform tasarım becerisi > bu estetik dil.
- Yapısal uygulama bu becerinin dışındadır: bileşen, yerleşim, tema altyapısı ve kod platform becerilerinindir.
- Somut token, sınıf ve ölçü değerleri platform tasarım becerisinde tutulur; buradaki değerler estetik referanstır.
- Sürüm, API ve araç davranışı gömülmez; platform becerisi ilgili bilgiyi çalışma anında resmî kaynakla doğrular.
- 4px barem ve durum renkleri değişmezdir; bu beceri onları esnetmez.
- WCAG 2.2 AA erişilebilirlik hedefi platform becerisinde denetlenir; estetik karar bu hedefi bozamaz.
- UI metinleri tam Türkçe imlâ ile yazılır (ğ, ü, ş, ı, ö, ç).
- Bu beceri kod, token dosyası veya derleme adımı üretmez.
- Platformun translucency, haptik gibi yetenekleri doğrulanmadan varsayılmaz; destek durumu "doğrulanmalı" etiketiyle ele alınır.
- Web sitesi tasarımı ve üretimi sp-dizayn-web-site alanındadır; bu beceri yalnız estetik dil referansıdır.
