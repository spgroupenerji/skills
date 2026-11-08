# Kaynak API Sözleşmesi

Doğrulama tarihi: 2026-11-08; resmî doküman + canlı API çağrıları. Kaynak sözleşmeleri değişebilir: yayın öncesi resmî belgeden yeniden doğrula, uygulamada `references/` ile `scripts/tedarik/kaynaklar/` aynı yayında güncellenir.
Araç ortak kuralları: yalnız HTTPS, açıklayıcı User-Agent (`sp-gorsel-tedarik/1.0 (SP GROUP; info@spgroupenerji.com)`), 3 deneme ve 1-2-4 sn geri çekilme, `Retry-After` desteği, JSON 2 MB / görsel 30 MB üst sınırı, görsel imza doğrulaması, atomik yazma. Test için taban URL `GORSEL_API_TABANI_<KAYNAK>` ile, kaynak CDN tabanı `GORSEL_CDN_TABANI_<KAYNAK>` ile ezilir. Kaynak bazlı indirme başlığı adaptörde `indirme_basliklari` ile tanımlanır (ör. AIC `Referer`).

## Ortam anahtarları

| Anahtar | Kaynak | Zorunlu mu |
| --- | --- | --- |
| `PEXELS_API_KEY` | Pexels | Evet |
| `PIXABAY_API_KEY` | Pixabay | Evet |
| `UNSPLASH_ACCESS_KEY` | Unsplash | Evet |
| `FLICKR_API_KEY` | Flickr | Evet |
| `SI_OPEN_ACCESS_API_KEY` (veya `SMITHSONIAN_API_KEY`) | Smithsonian | Evet |
| — | Openverse, Wikimedia, Met, NASA, Poly Haven | Anahtarsız |

Anahtarlar yalnız ortam değişkeni veya proje kökü `.env` üzerinden okunur; çıktıya/loga yazılmaz, API host'u dışına gönderilmez.

---

## Art Institute of Chicago

- Taban: `https://api.artic.edu/api/v1`; arama `GET /artworks/search`, detay `GET /artworks/{id}`; görsel IIIF `https://www.artic.edu/iiif/2/{image_id}/full/{genislik},/0/default.jpg`.
- Kimlik: anahtarsız; doküman tek iş parçacığı ve kendini sınırlama ister (sayısal limit yok).
- Arama parametreleri: `q`, **`query[term][is_public_domain]=true`** (sunucu tarafı süzgeç), `fields`, `limit` (en fazla 100), `page`.
- Yanıt `data[]`: `id`, `title`, `image_id`, `is_public_domain`, `artist_display`, `department_title`, `thumbnail.width|height`.
- Lisans: kamu malı eser görselleri CC0; metadata CC0, açıklama metinleri CC-BY 4.0. Yerel indirme serbest.
- **Kritik:** IIIF görsel ucu `Referer: https://www.artic.edu/` olmadan 403 döner; yalnız izinli genişlikler çalışır (200, 400, 600, 800, 843, 1200, 1686, 3000); araç bu genişliklerden seçip Pillow ile hedefe indirir.
- Doğrulandı: sunucu tarafı PD süzgeci, IIIF boyut allowlist'i, Referer zorunluluğu, CC0 beyanı (2026-11-08).

## Cooper Hewitt

- Taban: `https://api.cooperhewitt.org`; tek uç GraphQL GET `/?raw&query=<url-encoded GraphQL>`.
- Kimlik: anahtarsız (kayıt gerekmez; isteğe bağlı erişim anahtarı rate limit'i kaldırır). Varsayılan rate limit sayısı yayımlanmıyor; art arda isteklerde 429 görülebilir.
- Arama sorgusu: `{ object(general:"<terim>", hasImages:true, size:<n>) { id summary multimedia } }`; detay: `{ object(id:"object-123") { ... } }`.
- Yanıt `data.object[]`: `id`, `summary.title`, `multimedia[]` → `cc0` (bool), `type` ("image"), `original.url|measurements.dimensions`, `large.url`.
- Lisans: yalnız `multimedia[].cc0 == true` görseller CC0 kabul edilir; istemci süzgeci. Yerel indirme serbest. Host: `ciim-static-media.s3.us-east-1.amazonaws.com`.
- CC0 oranı ilk sonuçlarda ~%15'tir; araç istek boyutunu büyütüp süzgeç uygular.
- Doğrulandı: GraphQL arama/detay, cc0 bayrağı, S3 görselleri, canlı indirme (2026-11-08).

## Pexels

- Taban: `https://api.pexels.com`; arama `GET /v1/search`, ayrıntı `GET /v1/photos/{id}`.
- Kimlik: `Authorization: <PEXELS_API_KEY>` başlığı.
- Arama parametreleri: `query` (zorunlu), `orientation=landscape|portrait|square`, `size=large|medium|small`, `color`, `locale`, `page`, `per_page` (varsayılan 15, en fazla 80). Lisans/güvenli arama parametresi yok.
- Yanıt `photos[]`: `id`, `width`, `height`, `url`, `photographer`, `photographer_url`, `alt`, `src.original|large2x(1880)|large(940)|medium(640)|small(340)`.
- Hız: 200 istek/saat, 20.000 istek/ay; `X-Ratelimit-Limit/Remaining/Reset` başlıkları.
- Lisans/atıf: Pexels License; atıf gerekmez **ama API uygulamasında belirgin Pexels bağlantısı beklenir**; araç `atif_html` üretir.
- Yerel indirme: serbest. Görsel host: `images.pexels.com`.
- Doğrulandı: uçlar, parametreler, hız limiti, atıf metni (2026-11-08).

## Pixabay

- Taban: `https://pixabay.com`; arama `GET /api/`, ayrıntı `GET /api/?key=...&id={id}`.
- Kimlik: `key` sorgu parametresi.
- Arama parametreleri: `q`, `lang`, `image_type=photo`, `orientation=horizontal|vertical`, `min_width`, `min_height`, `safesearch=true` (varsayılan false — araç true gönderir), `order=popular|latest`, `page`, `per_page` 3-200.
- Yanıt `hits[]`: `id`, `pageURL`, `previewURL`, `webformatURL(640)`, `largeImageURL(1280)`, `fullHDURL(1920)`, `imageURL`, `imageWidth`, `imageHeight`, `user`, `tags`.
- Hız: 100 istek/60 sn; `X-RateLimit-*`. API yanıtlarının 24 saat önbelleklenmesi istenir; araç tek seferlik çalışır, toplu kazıma yapmaz.
- Lisans/atıf: Pixabay Content License; atıf gerekmez, API uygulamasında kaynak gösterimi beklenir; araç `pageURL` atfı üretir.
- Yerel indirme: serbest; **hotlink yasak** ("download them to your server first").
- Görsel host: `cdn.pixabay.com`.
- Doğrulandı: parametreler, hız limiti, hotlink yasağı, lisans sınırları.

## Unsplash

- Taban: `https://api.unsplash.com`; arama `GET /search/photos`, ayrıntı `GET /photos/{id}`, tetikleyici `links.download_location`.
- Kimlik: `Authorization: Client-ID <UNSPLASH_ACCESS_KEY>`.
- Arama parametreleri: `query`, `page`, `per_page` (varsayılan 10, en fazla 30), `order_by=relevant|latest`, `content_filter=low|high`, `orientation`, `color`, `lang`.
- Yanıt `results[]`: `id`, `width`, `height`, `color`, `alt_description`, `description`, `urls.raw|full|regular|small|thumb`, `links.html`, `links.download_location`, `user.name`, `user.username`, `user.links.html`.
- Dönüşüm: `urls.raw` + `w`, `q`, `fm=webp`, `fit=max`; `ixid` parametresi korunur.
- Hız: demo 50/saat, production 1.000/saat; `X-Ratelimit-*`.
- Lisans/atıf: Unsplash License ticari kullanıma izin verir, atıf istemez; **API Guidelines** hotlink + görünür atıf + UTM + indirme benzeri eylemde tetikleyici ister.
- Yerel indirme: API kuralı gereği varsayılan hotlink; yerel indirme yalnız `--yerel-kabul` ile. Tetikleyici çağrılmadan görsel indirilmez (çıkış 7).
- Premium/Unsplash+: standart lisans kapsamı dışı; `plus.unsplash.com` host'lu ve `premium`/`plus` işaretli adaylar dışlanır (alan adı resmî dokümanda belgeli değil; canlı yanıtla teyit edilmeli — **doğrulanmalı**).
- Görsel host: `images.unsplash.com`.
- Doğrulandı: arama parametreleri, per_page 30, hız limiti, API atıf/hotlink kuralı; premium bayrağı doğrulanmalı.

## Openverse

- Taban: `https://api.openverse.org/v1`; arama `GET /images/`, ayrıntı `GET /images/{id}/`.
- Kimlik: anahtarsız; `OPENVERSE_API_TOKEN` varsa `Authorization: Bearer`.
- Arama parametreleri: `q`, `page`, `page_size`, **`license=cc0,pdm`**, `aspect_ratio=wide|tall|square` (yönlendirme bu parametreyle yapılır; `orientation` kullanılmaz), `size`, `mature=false`, `extension`, `category`, `source`, `tags`. `license_type=commercial` şemada var ama canlı filtre etkisi doğrulanamadı; birincil filtre `license` parametresidir.
- Yanıt `results[]`: `id`, `title`, `url` (doğrudan dosya), `thumbnail`, `foreign_landing_url`, `creator`, `creator_url`, `license`, `license_version`, `license_url`, `attribution`, `source`, `provider`, `width`, `height`, `mature`.
- Hız: anonim varsayılan 5 istek/saat burst + 100 istek/gün (resmî repo varsayılanı); kayıtlı 100/dk + 10.000/gün — üretimde teyit **doğrulanmalı**.
- Lisans: her kayıtta `license` ∈ {cc0, pdm} ve `mature=false` doğrulanır; aksi aday atılır. CC0/PDM → atıf gerekmez.
- Yerel indirme: serbest. Görsel host: kayıt bazlı (https yeterli).
- Doğrulandı: uç, alanlar, license parametresi; kota ve license_type etkisi doğrulanmalı.

## Wikimedia Commons

- Taban: `https://commons.wikimedia.org`; uç `GET /w/api.php`.
- Arama: `action=query&generator=search&gsrsearch={q} filetype:bitmap&gsrnamespace=6&gsrlimit=N&prop=imageinfo&iiprop=url|size|mime|extmetadata&iiurlwidth=W&iiextmetadatafilter=License|LicenseShortName|UsageTerms|AttributionRequired|LicenseUrl|Artist&format=json&formatversion=2`.
- Ayrıntı: `action=query&titles=File:{ad}&prop=imageinfo` (aynı `iiprop`).
- Kimlik: anahtarsız; **açıklayıcı User-Agent zorunlu**, istekler seri yapılır, paralel istek yok. Okuma için sert hız limiti yok ("be considerate").
- Yanıt `query.pages[]`: `pageid`, `title`, `imageinfo[0].url|descriptionurl|thumburl|width|height|mime`, `extmetadata`.
- Lisans tespiti: `extmetadata.License.value` ∈ {cc0, pd} (öncelikli); yedek `LicenseShortName` "CC0"/"Public domain". `Copyrighted` alanına güvenilmez. Aksi lisanslı dosya atılır.
- Yerel indirme: serbest (CC0/PD). Görsel host: `upload.wikimedia.org` (thumb CDN host'u dahil).
- Doğrulandı: alan adları, lisans kuralı, UA politikası; hız limiti yok.

## Smithsonian Open Access

- Taban: `https://api.si.edu/openaccess/api/v1.0`; arama `GET /search?q=...&api_key=...&rows=...&start=...&type=edanmdm`, ayrıntı `GET /content/{id}`.
- Kimlik: `api_key` (SI_OPEN_ACCESS_API_KEY; yoksa SMITHSONIAN_API_KEY). Anahtar kaynağı apidoc (edan signup) ile FAQ (api.data.gov) arasında çelişkili; iki yol da resmî.
- Yanıt `response.rows[]`: `id`, `title`, `content.descriptiveNonRepeating.online_media.media[]` (`content`, `thumbnail`, `idsId`, `usage.access`, `width`, `height`), `content.descriptiveNonRepeating.metadata_usage.access`, `content.freetext.name[].content` (sanatçı), `creditLine`.
- Lisans filtresi: **parametre yok**; `media[].usage.access == "CC0"` (ve metadata CC0) istemci tarafında doğrulanır. Medya URL: `ids.si.edu/ids/deliveryService?id=<idsId>&max=<genişlik>`.
- Hız: resmî sayı yayımlanmıyor — **doğrulanmalı** (eski 1.000/saat iddiası teyit edilemedi).
- Yerel indirme: serbest. Host: `ids.si.edu`. Logo/marka CC0 dışı.
- Doğrulandı: uç, alanlar, CC0 kuralı, anahtar adı; hız limiti doğrulanmalı.

## The Met

- Taban: `https://collectionapi.metmuseum.org/public/collection`; arama `GET /v1.1/search?q=...&hasImages=true&offset=...&limit=...`, ayrıntı `GET /v1/objects/{id}`.
- **Kritik:** `/v1/search` 2026-10-01'de emekliye ayrıldı (HTTP 410); v1.1 Elastic tabanlı ve `offset`/`limit` ile sayfalanır (limit varsayılan 100, en fazla 500). Arama parametrelerinde `isPublicDomain` **yok**; gönderilse de yok sayılır (canlı test: aynı sonuç kümesi).
- Kimlik: anahtarsız; hız 80 istek/sn (resmî doküman).
- Arama yanıtı: `{total, objectIDs[]}`; araç ilk `adet*2` kimlik için `/objects/{id}` çağırır (en fazla 12 istek) ve `isPublicDomain` doğrulamasını istemci tarafında yapar.
- Nesne alanları: `isPublicDomain`, `primaryImage`, `primaryImageSmall`, `objectURL`, `artistDisplayName`, `title`, `objectDate`, `medium`, `creditLine`, `tags[]`. Nesne kaydında görsel piksel boyutu yoktur; araç `primaryImage` başlığından boyut okur (aday başına 1 ek istek).
- Lisans: kamu malı eserler CC0; yalnız `isPublicDomain=true` kullanılır. Yerel indirme: serbest. Host: `images.metmuseum.org`.
- Doğrulandı: v1 emekliliği, v1.1 sayfalama, nesne alanları; görsel hakları sayfası 429 verdi, kredi ricası **doğrulanmalı**.

## NASA Image Library

- Taban: `https://images-api.nasa.gov`; arama `GET /search?q=...&media_type=image&page=...`, varlık `GET /asset/{nasa_id}`.
- Kimlik: anahtarsız; yayımlanmış hız limiti yok — **doğrulanmalı**.
- Arama yanıtı: `collection.items[].data[]` (`nasa_id`, `title`, `description`, `keywords[]`, `center`, `date_created`, `secondary_creator`), `items[].links[]` (önizleme/thumbnail). Sayfalama `page` + `collection.links[rel=next]`.
- Varlık yanıtı: JSON dizi — `~orig.tif`, `~large.jpg`, `~medium.jpg`, `~small.jpg`, `~thumb.jpg`. **`~orig.tif` asla seçilmez**; büyük JPG varyantları kullanılır.
- Lisans: ABD kamu malı; **amblem/logotype kamu malı değil**, onay iması yasak, üçüncü taraf telif ve tanınabilir kişi istisnası var. Araç `kamu-mali` sayar, onay kapısı zorunlu.
- Yerel indirme: serbest. Host: `images-assets.nasa.gov`. Resmî REST dokümanı zayıf — **doğrulanmalı**.

## Poly Haven

- Taban: `https://api.polyhaven.com`; arama `GET /search?q={terim}&t=textures`, dosyalar `GET /files/{id}`, bilgi `GET /info/{id}`.
- Kimlik: anahtarsız; **User-Agent veya Referer zorunlu** ("Our API terms require this"); HTML kazıma yasak, API zorunlu. Hız limiti yayımlanmıyor — **doğrulanmalı**.
- `/files/{id}` doku yanıtı: doku slotları (ör. `Diffuse`, `Nor`, `Rough`) → çözünürlük (1k/2k/4k) → biçim (jpg/png) → `{url, md5, size}`. Web varlığı için Diffuse + 1k/2k/4k seçilir; 8k/16k istenmez.
- Lisans: CC0; atıf gerekmez ("Powered by Poly Haven" rica). Yerel indirme: serbest. Host: `dl.polyhaven.org`.
- Doğrulandı: CC0, UA şartı, uçlar, dosya şeması.

## Flickr

- Taban: `https://www.flickr.com/services/rest/`; arama `?method=flickr.photos.search`, ayrıntı `?method=flickr.photos.getInfo`.
- Kimlik: `api_key` (FLICKR_API_KEY); 3.600 sorgu/saat (anahtar başına).
- Arama parametreleri: `text`, **`license=9,10`**, `safe_search=1`, `per_page` (en fazla 500), `page`, `extras=license,owner_name,url_sq,url_m,url_l,url_o`, `format=json&nojsoncallback=1`.
- Yanıt `photos.photo[]`: `id`, `owner`, `secret`, `server`, `title`, `license`, `url_sq|url_m|url_l|url_o`, `owner_name`.
- Lisans: 9 = CC0, 10 = Public Domain Mark → kamu-mali. **7 (No known copyright restrictions) CC lisansı değildir ve ticari kullanım için güvenilmez; 8 (ABD hükümet işi) de CC değildir** — ikisi de kullanılmaz.
- Yerel indirme: serbest; sahibi kaldırma isterse 24 saat içinde cache güncellenmelidir. Host: `live.staticflickr.com`.
- Doğrulandı: lisans kimlikleri, 9-10 kararı, hız limiti, API ToS ticari şartı.

---

## Adaptör sözleşmesi (bakım için)

Her kaynak `scripts/tedarik/kaynaklar/<ad>.py` içinde `class XKaynak` ve `KAYNAK = XKaynak()` tanımlar; `Kaynak` protokolü `model.py`'dedir: `ara(istek, anahtar, taban)`, `detay(kimlik, anahtar, taban)` ve sınıf değişkenleri (`ad`, `lisans_adi`, `yerel_indirme`, `atif_zorunlu`, `anahtar_ortami`, `varsayilan_taban`, `taban_ortami`, `gorsel_hostlari`, `kota_basliklari`). Adaptör lisans süzgecini kendi içinde yapar ve `kosullu` aday döndürmez; görsel URL'lerini `host_guvenli` ile doğrular. Yeni kaynak eklemek: yeni modül + `kaynaklar/__init__.py` registry satırı + `references/` güncellemesi + test.