# Token ve Bileşen Spesifikasyonları

> `sp-dizayn-web-uygulama` becerisinin eki. Boşluk, tipografi, renk ve yoğunluk tokenlarını; buton, form, tablo, modal, panel ve durum bileşenlerinin sınıf spec'lerini taşır. Çelişkide beceri gövdesi kazanır.
> Doğrulama: biçim ve `@theme` sözdizimi çalışma anında resmî dokümandan doğrulanır; beceriye gömülü sürüm, SRI veya tarih taşınmaz.

## 1. Teslim bloğu

Stil iki kaynaktan gelir: Tailwind tarayıcı motoru ve `@theme` tokenları. Depoda, şablonda veya ikinci bir bağlantıda başka stil dosyası bulunmaz.

```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser/@{dogrulanmis-surum}/dist/index.global.js"></script>
<script src="https://code.iconify.design/iconify-icon/@{dogrulanmis-surum}/iconify-icon.min.js"></script>
<!-- @{dogrulanmis-surum}: çalışma anında resmî kaynaktan doğrulanan sabit sürüm; değer gömülmez. -->
<style type="text/tailwindcss">
  @theme {
    --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    --radius-kutu: 0.5rem;
    --radius-panel: 0.75rem;
  }
</style>
```

- `@theme` yalnızca token tanımlar; token dışı serbest CSS ve ham değer yoktur.
- Renk `--color-*` altında yeniden tanımlanmaz; renk doğrudan Tailwind paletinden kullanılır.
- `--radius-kutu` `rounded-kutu`, `--radius-panel` `rounded-panel` utility'sini üretir (ad alanı: `--radius-*`).
- Sürümler sabittir; release kapısında iki script de `integrity` (SRI) ve `crossorigin="anonymous"` taşır.
- SRI değeri gömülmez: sabit sürümün resmî kaynağından her release'te üretilip doğrulanır.
- Tarayıcı motorunun üretim uygunluğu resmî dokümandan doğrulanır; zero-build istisnası release kaydında yazılır. Satır içi olay özniteliği kullanılmaz.

## 2. Boşluk tokenları

| Sınıf | Değer | Kullanım |
| --- | --- | --- |
| `p-1`, `gap-1` | 4px | ikon-metin arası, rozet içi |
| `p-2`, `gap-2` | 8px | buton içi, form içi |
| `p-4`, `gap-4` | 16px | kart içi, hücre dikey dolgusu |
| `p-6`, `gap-6` | 24px | panel içi |
| `p-8`, `gap-8` | 32px | bölüm arası |
| `p-12`, `gap-12` | 48px | sayfa bölümleri |
| `gap-16` | 64px | ana bölüm ayrımı |

- Barem 4px'tir; bu adımlar dışında boşluk değeri üretilmez.
- Dikey dolgu simetriktir; asimetrik dolgu yoktur.
- Çerçeve kalınlığı `border` (1px); kalın kenar ve halka yalnız odak göstergesinde kullanılır.

## 3. Tipografi tokenları

| Sınıf | Punto / satır | Kullanım |
| --- | --- | --- |
| `text-xs` | 12 / 16 px | rozet, yardım metni |
| `text-sm` | 14 / 20 px | taban: gövde, tablo, form, buton |
| `text-base` | 16 / 24 px | uzun okuma metni |
| `text-lg` | 18 / 28 px | panel başlığı |
| `text-xl` | 20 / 28 px | bölüm başlığı |
| `text-2xl` | 24 / 32 px | sayfa başlığı (`h1`) |

- Ağırlık: `font-semibold` başlık, `font-medium` etiket ve buton, `font-normal` gövde.
- Sayısal içerik `tabular-nums`; sayı sağa yaslı, birim aynı satırda.
- Satır uzunluğu en fazla 75 karakter (`max-w-prose`); keyfi punto yok.

## 4. Renk ve durum tokenları

| Rol | Sınıf | Kullanım |
| --- | --- | --- |
| Sayfa zemini | `bg-slate-50` | `<main>` |
| Yüzey | `bg-white` | panel, tablo, form |
| Kenar | `border-slate-200` | panel ve ayırıcı |
| Ana metin | `text-slate-900` | gövde |
| İkincil metin | `text-slate-600` | AA; `slate-400/500` yalnız dekoratif |
| Primary CTA | `bg-slate-900 text-white hover:bg-slate-800` | tek vurgu yüzeyi |
| Başarı | `bg-emerald-50 text-emerald-800 border-emerald-200` | rozet |
| Uyarı | `bg-amber-50 text-amber-800 border-amber-200` | rozet |
| Hata | `bg-rose-50 text-rose-800 border-rose-200` | rozet |
| Bilgi | `bg-sky-50 text-sky-800 border-sky-200` | rozet |

- Tablo başlangıç noktasıdır; her çift ölçülür: metin ≥4,5:1, büyük metin ≥3:1, bileşen kenarı ve odak ≥3:1.
- Eşiği geçmeyen çift bir koyu adıma taşınır (`text-*-700` → `text-*-800`).
- Yüzeyin en az %90'ı nötrdür; durum rengi sayfa bazında değişmez.

## 5. Hareket ve yoğunluk tokenları

| Öğe | Değer | Sınıf |
| --- | --- | --- |
| Süre / eğri | 150ms / ease-out | `duration-150 ease-out` |
| Bası | 0.95 ölçek | `active:scale-95` |
| Geçiş özelliği | transform, opacity | `transition-transform` |
| Azaltılmış hareket | geçiş yok | `motion-reduce:transition-none motion-reduce:transform-none` |
| Üst çubuk / sidebar | 56px / 256px (daraltılmış 64px) | `h-14`, `w-64`, `w-16` |
| Veri tablosu / liste / form satırı | 40 / 48 / 40 px | `h-10`, `h-12`, `h-10` |
| Yoğun telemetri satırı (muaf yüzey) | 32px | `h-8` |

Bu değerler sayfa türüne göre değişmez; yalnız tanımlı muaf yüzey 32px satır kullanır. Dekoratif animasyon yoktur; hareket yalnız durum değişimini açıklar.

## 6. Bileşen spec'leri

### 6.1 Buton

```html
<button type="button" class="inline-flex h-9 items-center justify-center gap-2 rounded-kutu bg-slate-900 px-3 text-sm font-medium text-white transition-transform duration-150 ease-out hover:bg-slate-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95 disabled:pointer-events-none disabled:opacity-50">Kaydet</button>
```

- Boy: `h-8` yoğun tablo eylemi, `h-9` varsayılan, `h-10` form gönderimi.
- Varyant: birincil `bg-slate-900 text-white`; ikincil `bg-slate-100 text-slate-700 hover:bg-slate-200`; hayalet `text-slate-600 hover:bg-slate-100`; yıkıcı `bg-rose-600 text-white hover:bg-rose-700`.
- Durumlar: hover bir koyu ton; focus-visible halka; active `scale-95`; disabled `opacity-50 pointer-events-none`; loading `aria-busy="true"` + spinner + "Kaydediliyor" metni.

### 6.2 Form alanı

```html
<label for="eposta" class="block text-sm font-medium text-slate-700">E-posta</label>
<input id="eposta" name="eposta" type="email" aria-invalid="true" aria-describedby="eposta-hata"
       class="mt-1 block h-10 w-full rounded-kutu border border-rose-400 bg-white px-3 text-sm text-slate-900 focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/30">
<p id="eposta-hata" class="mt-1 text-sm text-rose-600">Geçerli bir e-posta adresi girin.</p>
```

- Normal alan: `border-slate-300` ve odakta `focus:ring-slate-500/30`; hata alanı yukarıdaki gibi `rose` olur.
- Her alan görünür etiketlidir; `placeholder` etiket yerine geçmez.
- Yardım metni `mt-1 text-xs text-slate-600`; zorunlu alan `required` + görünür "Zorunlu" işareti taşır.

### 6.3 Tablo

```html
<div class="overflow-x-auto rounded-panel border border-slate-200">
  <table class="w-full border-collapse text-sm">
    <caption class="sr-only">Kullanıcı listesi</caption>
    <thead class="bg-slate-50 text-xs font-semibold text-slate-600">
      <tr>
        <th scope="col" class="h-10 px-3 text-left">Ad</th>
        <th scope="col" class="h-10 px-3 text-right" aria-sort="descending"><button type="button">Kayıt</button></th>
      </tr>
    </thead>
    <tbody>
      <tr class="h-10 border-t border-slate-100 hover:bg-slate-50">
        <td class="px-3">Ayşe Yılmaz</td>
        <td class="px-3 text-right tabular-nums">1.204</td>
      </tr>
    </tbody>
  </table>
</div>
```

- Yükleniyor: iskelet satırları + `aria-busy="true"`; boş: `colspan` hücresinde boş durum; hata: `colspan` hücresinde Türkçe mesaj + "Yeniden dene"; dolu: veri satırları.
- Sayısal kolon `text-right tabular-nums`; eylem kolonu son sütundadır ve `w-10` genişliğindedir.

### 6.4 Modal

```html
<div class="fixed inset-0 z-50 flex items-start justify-center bg-slate-900/50 p-4">
  <div role="dialog" aria-modal="true" aria-labelledby="silme-baslik" class="mt-16 w-full max-w-lg rounded-panel bg-white p-6 shadow-lg">
    <h2 id="silme-baslik" class="text-lg font-semibold text-slate-900">Kaydı sil</h2>
    <p class="mt-2 text-sm text-slate-600">Bu işlem geri alınamaz; kayıt ve bağlı hareketler kalıcı silinir.</p>
    <div class="mt-6 flex justify-end gap-2">
      <button type="button">Vazgeç</button>
      <button type="button">Kalıcı sil</button>
    </div>
  </div>
</div>
```

- Buton sınıfları §6.1'den gelir; onay eylemi yıkıcı varyanttır.
- Açılışta odak panele veya ilk eyleme taşınır; odak tuzağı kurulur; ESC kapatır ve odak tetikleyiciye döner.
- Geri alınamaz eylemde onay modalı zorunludur ve sonuç metni açık yazılır.

### 6.5 Panel yüzeyi

```html
<section class="rounded-panel border border-slate-200 bg-white p-4">
  <div class="flex items-center justify-between gap-4">
    <h2 class="text-lg font-semibold text-slate-900">Son hareketler</h2>
    <button type="button">Tümünü gör</button>
  </div>
  <ul class="mt-4 divide-y divide-slate-100 text-sm text-slate-700">
    <li class="py-2">Pompa 3 çalıştı</li>
    <li class="py-2">Seviye sensörü kalibre edildi</li>
  </ul>
</section>
```

- Kart içinde kart yoktur; gölge yalnız modal ve açılır katmanda kullanılır.
- Panel başlığı + eylem satırı tüm panellerde aynıdır; panel içi dikey ritim 16px'tir.

### 6.6 Durum rozeti

```html
<span class="inline-flex items-center gap-1 rounded-full border border-emerald-200 bg-emerald-50 px-2 py-0.5 text-xs font-medium text-emerald-800">
  <iconify-icon icon="lucide:circle-check" aria-hidden="true" class="text-xs"></iconify-icon>
  Başarılı
</span>
```

- Dört durum aynı ölçüde üretilir: başarı `emerald`, uyarı `amber`, hata `rose`, bilgi `sky`.
- Renk tek başına anlam taşımaz; metin ve durum ikonu zorunludur.

### 6.7 Boş, iskelet, hata ve çevrimdışı

```html
<div class="flex flex-col items-center gap-3 py-12 text-center">
  <p class="text-sm font-medium text-slate-900">Henüz kayıt yok</p>
  <p class="max-w-prose text-sm text-slate-600">İlk kaydı ekleyerek listeyi başlatın.</p>
  <button type="button">Yeni kayıt</button>
</div>
```

- İskelet: `animate-pulse rounded bg-slate-200` bloklar; sarmalayıcı `aria-busy="true"` taşır.
- Hata: `role="alert"` + Türkçe mesaj + "Yeniden dene" butonu.
- Çevrimdışı: `<main>` üstünde kalıcı `role="status"` şerit; veri son geçerli hâliyle gösterilir.

### 6.8 Sayfa iskeleti (tek kabuk)

```html
<body class="min-h-screen bg-slate-50">
  <a href="#ana-icerik" class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-kutu focus:bg-white focus:px-3 focus:py-2 focus:text-sm">İçeriğe geç</a>
  <aside class="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white md:block">
    <nav aria-label="Ana menü" class="flex flex-col gap-1 p-2">
      <a href="/panel" aria-current="page" class="flex h-9 items-center justify-between rounded-kutu bg-slate-100 px-2 text-sm font-medium text-slate-900"><span>Panel</span><iconify-icon icon="lucide:check" aria-hidden="true" class="text-base"></iconify-icon></a>
      <a href="/kayitlar" class="flex h-9 items-center rounded-kutu px-2 text-sm text-slate-600 hover:bg-slate-100">Kayıtlar</a>
    </nav>
  </aside>
  <div class="md:pl-64">
    <header class="sticky top-0 z-30 flex h-14 items-center justify-between border-b border-slate-200 bg-white px-4 text-sm">
      <span class="font-medium text-slate-900">SCADA Paneli</span>
      <span class="text-slate-600">Ayşe Yılmaz</span>
    </header>
    <main id="ana-icerik" class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between gap-4">
        <h1 class="text-2xl font-semibold text-slate-900">Kayıtlar</h1>
        <button type="button" class="inline-flex h-9 items-center rounded-kutu bg-slate-900 px-3 text-sm font-medium text-white hover:bg-slate-800 active:scale-95">Yeni kayıt</button>
      </div>
    </main>
  </div>
</body>
```

- Aktif menü üç kanaldan bildirilir: zemin tonu ve ağırlık, durum ikonu, `aria-current="page"`. Menü etiketi metindir; etikete dekoratif ikon eklenmez.
- İçerik başlık satırının altında panel, tablo veya form bölümleriyle devam eder; her bölüm §6.1-§6.7 bileşenlerinden kurulur.
- Sidebar ve üst çubuk `<main>` dışındadır; kaydırma yalnız `<main>` alanında gerçekleşir.

## Kaynaklar

1. Tailwind CSS tema değişkenleri ve `@theme` — https://tailwindcss.com/docs/theme
2. Tailwind tarayıcı motoru — https://www.npmjs.com/package/@tailwindcss/browser
3. Iconify Web Component — https://iconify.design/docs/iconify-icon/
4. Iconify Web Component — https://www.npmjs.com/package/iconify-icon