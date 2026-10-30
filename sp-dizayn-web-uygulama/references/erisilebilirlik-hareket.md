# Erişilebilirlik ve Hareket Kontrol Listesi

> `sp-dizayn-web-uygulama` becerisinin eki. WCAG 2.2 AA ölçütlerini, klavye/odak/duyuru desenlerini ve hareket kontrolünü ölçülebilir adımlara çevirir.
> Doğrulama: WCAG 2.2 (W3C Recommendation, 12 Aralık 2024); MDN `prefers-reduced-motion`; Chrome DevTools erişilebilirlik ve rendering panelleri.

## 1. Bağlayıcı ölçütler

| Ölçüt | Seviye | Bu arayüzdeki karşılığı | Doğrulama |
| --- | --- | --- | --- |
| 1.3.1 Bilgi ve ilişkiler | A | başlık hiyerarşisi, `th scope`, `label for` | erişilebilirlik ağacı |
| 1.4.3 Kontrast (asgari) | AA | metin ≥4,5:1, büyük metin ≥3:1 | kontrast ölçer |
| 1.4.10 Yeniden akış | AA | 320px'te yatay gövde kaydırması yok | görünüm emülasyonu |
| 1.4.11 Bileşen kontrastı | AA | kenar, ikon ve odak ≥3:1 | kontrast ölçer |
| 2.1.1 Klavye | A | tüm işlev klavyeyle erişilebilir | Tab turu |
| 2.4.3 Odak sırası | A | odak DOM sırasını izler | Tab turu |
| 2.4.7 Görünür odak | AA | `focus-visible` halkası görünür | Tab turu |
| 2.4.11 Odak gizlenmemesi | AA | yapışkan üst çubuk ve sidebar odağı örtmez | kaydırmalı klavye turu |
| 2.5.8 Hedef boyutu | AA | etkileşim hedefi ≥24x24 CSS px | DevTools ölçümü |
| 3.3.1 Hata tanımlama | A | hata alanı işaret eder, metin Türkçedir | form testi |
| 3.3.2 Etiketler | A | her alan görünür etiketlidir | form testi |
| 4.1.2 Ad, rol, değer | A | `aria-current`, `aria-sort`, `aria-busy` | erişilebilirlik ağacı |

Bu tablo asgari kümedir; eksik ölçüt WCAG 2.2 AA hedefini düşürür.

## 2. Klavye turu

1. Sayfa açılışında ilk Tab odağı "İçeriğe geç" bağlantısına gider.
2. Sidebar → üst çubuk → `<main>` sırası DOM sırasıyla ilerler; her adımda odak görünürdür.
3. Modal açıldığında odak panel içinde kalır (tuzak); ESC kapatır; odak tetikleyiciye döner.
4. Açılır menü ok tuşlarıyla gezinir, Enter seçer, ESC kapatır.
5. Tablo sıralama başlığı Enter/Space ile çalışır; satır eylemleri erişilebilir adlıdır.
6. Form hatasında odak ilk hatalı alana taşınır; hata özeti varsa odaklanabilir özet gösterilir.

## 3. Odak yönetimi

- Odak yalnız tanımlı durumlarda programatik taşınır: modal açılış/kapanışı, kısmi güncelleme, hata özeti, silme sonrası.
- htmx kısmi değişiminde odak değişen bölgeye taşınır ve bölge `role="status"` ile duyurulur.
- Silme sonrası odak silinen satırın komşusuna, liste boşsa boş durum başlığına gider.
- Kaydırmalı odaklamada öğe yapışkan çubuk altında kalmaz; gerekli öğe `scroll-mt-16` taşır.
- Odak halkası hiçbir durumda `outline-none` ile tek başına kaldırılmaz; yerine görünür `focus-visible:ring-*` konur.

## 4. Duyurular

| Durum | Rol | Politika |
| --- | --- | --- |
| Bilgi, başarı | `role="status"` | kibar duyuru; 5 sn sonra kapanır |
| Hata | `role="alert"` | acil duyuru; elle kapatılır |
| Yükleniyor | `aria-busy="true"` | bölge düzeyinde işaretlenir |
| İlerleme, sayaç | `role="status"` | metinle güncellenir |

- Aynı anda tek duyuru gösterilir; yığılma yoktur.
- Yalnız ikon içeren buton erişilebilir ad taşır; dekoratif ikon `aria-hidden="true"` olur.
- Başarı ve hata metni ekranda da görünür; yalnız ekran okuyucuya özel mesaj bırakılmaz.

## 5. Form hata deseni

- İşaretleme örneği: references/token-bilesenler.md §6.2; etiket + `aria-invalid` + `aria-describedby` üçlüsü zorunludur.
- Hata metni alanın altında ve Türkçedir; hangi alanın, neden hatalı olduğunu söyler.
- Doğrulama hem istemcide hem sunucuda tekrarlanır; sunucu hatası da aynı deseni kullanır.
- Zorunlu alan işareti metinle belirtilir; yıldız tek başına anlam taşımaz.

## 6. Hareket kontrolü

- Süre 150ms, `ease-out`; yalnız `transform` ve `opacity` hareket eder.
- `active:scale-95` bası tepkisi tüm tıklanabilir buton ve kartlarda bulunur.
- Animasyon kesintiye uğratılabilir; yeni etkileşim mevcut geçişi hedefe yönlendirir.
- Azaltılmış hareket: her hareketli öğe `motion-reduce:transition-none motion-reduce:transform-none motion-reduce:animate-none` taşır; JS animasyonu `matchMedia('(prefers-reduced-motion: reduce)')` ile atlanır.
- Dekoratif, sürekli, otomatik oynatılan animasyon yoktur.
- Yükleme göstergesi spinner + "Yükleniyor" metni + `aria-busy` taşır; durum yalnız spinner ile anlatılmaz.
- DevTools → Rendering → "Emulate CSS prefers-reduced-motion: reduce" seçilir; geçişlerin durduğu doğrulanır.

## 7. Doğrulama adımları

1. Lighthouse erişilebilirlik denetimi çalıştırılır; ihlal yoktur.
2. §2 klavye turu tamamlanır; odak kaybolmaz, tuzak yalnız modaldadır.
3. 320px görünümde yatay gövde kaydırması yoktur.
4. Kontrast ölçerle metin, kenar ve odak çiftleri ölçülür; eşik altı çift kalmamıştır.
5. Azaltılmış hareket emülasyonunda geçiş ve animasyon durur.
6. Ekran okuyucuyla modal, tablo ve durum duyurusu okunur; ad ve rol doğrudur.

## 8. Teslim kontrol listesi

- [ ] Sayfada tek `h1` ve atlanmamış başlık hiyerarşisi vardır.
- [ ] Tüm etkileşim klavyeyle tamamlanır; odak görünür ve DOM sırasındadır.
- [ ] Odak tuzağı yalnız modaldadır; ESC kapatır ve odak tetikleyiciye döner.
- [ ] Her form alanı görünür etiketlidir; hata `aria-describedby` ile bağlıdır.
- [ ] Her tablo `th scope` ve sıralamada `aria-sort` taşır.
- [ ] Yükleme, boş, hata ve çevrimdışı durumları tanımlıdır ve duyurulur.
- [ ] Metin ≥4,5:1, büyük metin ≥3:1, bileşen ve odak ≥3:1 kontrast sağlar.
- [ ] Etkileşim hedefleri ≥24x24 CSS px; yapışkan çubuklar odağı örtmez.
- [ ] 320px'te yatay gövde kaydırması yoktur.
- [ ] Azaltılmış harekette tüm geçişler durur; dekoratif animasyon yoktur.

## Kaynaklar

1. WCAG 2.2 (W3C Recommendation, 12 Aralık 2024) — https://www.w3.org/TR/WCAG22/
2. `prefers-reduced-motion` — https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
3. Tailwind CSS tema değişkenleri — https://tailwindcss.com/docs/theme