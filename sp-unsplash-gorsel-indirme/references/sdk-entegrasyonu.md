# SDK Entegrasyonu: unsplash-php ve unsplash-js

Doğrulama tarihi: 2026-10-31. Kaynaklar: context7 `/unsplash/unsplash-php` ve `/unsplash/unsplash-js`; resmî README dosyaları (`github.com/unsplash/unsplash-php`, `github.com/unsplash/unsplash-js`) ve Unsplash API kılavuzu. Depolar: https://github.com/unsplash/unsplash-php.git ve https://github.com/unsplash/unsplash-js.git. Sürümler değişebilir; kodu yazmadan önce context7 veya resmî README ile doğrula. Bu belge hukuki danışmanlık değildir.

## Yol seçimi

| Proje ortamı | Önerilen yol |
| --- | --- |
| Python, CLI, herhangi bir dil | Bu skill'deki `scripts/unsplash_gorsel.py` |
| PHP / WordPress arka ucu | `unsplash-php` (aşağıdaki bölüm) |
| Node.js / Next.js sunucu tarafı | `unsplash-js` (aşağıdaki bölüm) |
| Tarayıcıda çalışan React/Vue | İstemcide anahtar tutma; kendi sunucunda proxy + `unsplash-js` |
| API anahtarı yok | `references/tarayici-yedegi.md` (düşük hacim, kullanıcı onayı) |

Hangi yolu seçersen seç: **hotlink**, **atıf + UTM** ve **indirme benzeri eylemde `download_location` tetikleyicisi** zorunludur. Anahtar yalnız sunucuda/ortam değişkeninde tutulur.

## PHP: unsplash-php

Kurulum (Composer gerekir; kurulu değilse önce Composer kurulmalı, kurulum **doğrulanmalı**):

```bash
composer require unsplash/unsplash
```

Yapılandırma ve arama:

```php
<?php
require __DIR__ . '/vendor/autoload.php';

Unsplash\HttpClient::init([
    'applicationId' => getenv('UNSPLASH_ACCESS_KEY'),
    'secret' => getenv('UNSPLASH_SECRET_KEY') ?: null,
    'callbackUrl' => null,
    'utmSource' => 'kayitli-uygulama-adi',
]);

$sonuclar = Unsplash\Search::photos('modern office', 1, 12, 'landscape', null, 'relevant', 'high');
foreach ($sonuclar->getResults() as $foto) {
    $hotlink = $foto->urls['regular'];
    $fotografci = $foto->user['name'];
    $profil = $foto->user['links']['html'];
    $fotoSayfasi = $foto->links['html'];
    $foto->download();
}
```

- Yalnız genel (public) işlemler için `applicationId` yeterlidir; `secret` yalnız kullanıcı yetkilendirmesi gereken akışlarda gerekir.
- `utmSource` verilmezse kütüphane uyarı üretir; kayıtlı uygulama adını kullan ve "Unsplash" adını uygulama adına koyma.
- Tek fotoğraf: `Unsplash\Photo::find($id)`; indirme tetikleyicisi: `$photo->download()`.
- Hata yönetimi: `Unsplash\Exception`; `getCode()`, `getMessage()`, `getArray()`. 401 anahtar, 403/429 hız limiti/yetki, 404 bulunamadı.
- Hız limiti: demo 50 JSON isteği/saat, production onayında 1000; yanıt nesnesinde `rateLimitRemaining()` ile izle.
- Görsel URL'lerini `images.unsplash.com` üzerinden hotlink et; yerel kopya üretiyorsan `download_location` tetikleyicisini atlama ve `credits.json`/atıf kaydını koru.

## Node.js: unsplash-js

Kurulum:

```bash
npm i --save unsplash-js
```

Sunucu tarafı kullanım:

```ts
import { createApi } from "unsplash-js";

const unsplash = createApi({ accessKey: process.env.UNSPLASH_ACCESS_KEY! });

const sonuc = await unsplash.GET("/search/photos", {
  params: {
    query: {
      query: "modern office",
      per_page: 12,
      orientation: "landscape",
      content_filter: "high",
    },
  },
});

if (sonuc.error) throw new Error("Unsplash: " + JSON.stringify(sonuc.error));
const foto = sonuc.data.results[0];

await fetch(foto.links.download_location, {
  headers: { Authorization: "Client-ID " + process.env.UNSPLASH_ACCESS_KEY },
});
```

- `createApi({ accessKey })` yalnız sunucuda kullanılır. Resmî README: tarayıcıda kullanılacaksa istekler `baseUrl` ile kendi sunucundan proxy'lenmeli ve istemcide anahtar bulunmamalıdır.
- Güncel README genel `.GET("/search/photos", { params: { query: ... } })` biçimini gösterir; eski sürümlerdeki `search.getPhotos` kullanımı sürüme göre **doğrulanmalı**.
- İndirme tetikleyicisi için kütüphanenin `.GET("/photos/{id}/download", { params: { path: { id } } })` çağrısı da vardır; ancak `links.download_location` içindeki `ixid` parametresini korumak için sunucuda doğrudan bu adrese istek atmak daha güvenlidir.
- Hatalar `{ data, error }` döner; 401 anahtar, 403/429 hız limiti, 404 bulunamadı. Demo 50/saat, production 1000/saat.

## Ticari güvenlik kapısı (SDK uygulamaları)

SDK kullanan uygulamada da aynı politika zorunludur; ayrıntı: `references/ticari-guvenlik.md`.

- Unsplash+ / premium / Getty içeriğini filtrele; standart Unsplash License bu görselleri kapsamaz.
- Alt/açıklama üzerinde kişi, marka/logo, sanat eseri, hassas içerik ve özel mülk taraması yap; engelli içeriği indirme veya kullanıcıya gösterme.
- Ticari sayfaya eklemeden önce görseli **gözle** denetle; denetim kaydına `ticari_durum=onaylandi`, onaylayan, tarih ve not yaz (`credits.json` benzeri).
- Kişi/özel mülk için release veya izin gerekebilir; Unsplash lisansı release sağlamaz.
- Editoryal kullanım ayrıdır; ticari reklamda kullanma. Anahtar kelime taraması hukuki garanti değildir.

## Ortak uyum kontrolü

- [ ] Görüntüleme için API'nin verdiği `photo.urls.*` adresleri hotlink edildi.
- [ ] Fotoğrafçı adı + Unsplash + profil bağlantısı görünür; bağlantılarda `utm_source` ve `utm_medium=referral` var.
- [ ] İndirme/ekleme eyleminde `download_location` çağrıldı; başarısızsa görsel işlenmedi.
- [ ] Anahtar istemciye sızmıyor; log/commit/sohbet temiz.
- [ ] Demo/production limiti biliniyor; toplu istek yapılmıyor.
- [ ] Yerel kopya üretildiyse API hotlink kuralıyla çelişki kullanıcıya bildirildi ve sorumluluk kabul edildi.
- [ ] Ticari modda kişi/logo/marka/eser/özel mülk/hassas içerik filtrelendi ve görsel gözle onaylandı.
- [ ] Unsplash+ / premium / Getty içeriği kullanılmadı; onay kaydı (onaylayan/tarih/not) tutuldu.
