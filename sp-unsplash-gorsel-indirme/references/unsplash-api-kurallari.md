# Unsplash API Kuralları

Doğrulama tarihi: 2026-10-30. Bu belge uygulama aracının (`scripts/unsplash_gorsel.py`) uyum davranışının dayanağıdır. API ve kurallar değişebilir; yayın öncesi resmî kaynaktan yeniden doğrula. Hukuki danışmanlık değildir.

## Kaynaklar (doğrulandı)

- context7 kütüphanesi `/websites/unsplash` — `https://unsplash.com/documentation`
- Unsplash API Guidelines — `https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines` (27 Temmuz 2026)
- Hotlinking — `https://help.unsplash.com/api-guidelines/guideline-hotlinking-images`
- İndirme tetikleyicisi — `https://help.unsplash.com/api-guidelines/guideline-triggering-a-download`
- Atıf — `https://help.unsplash.com/api-guidelines/guideline-attribution`
- Lisans — `https://unsplash.com/license`

## Kimlik doğrulama

- API tabanı `https://api.unsplash.com`, sürüm `Accept-Version: v1`.
- Genel işlemler için `Authorization: Client-ID <ACCESS_KEY>`; alternatif olarak `client_id` sorgu parametresi.
- Access/Secret anahtarları gizlidir; istemci tarafında gerekiyorsa proxy kullanılır. Anahtar repoya, loga, komut satırına yazılmaz.

## Arama

`GET /search/photos` parametreleri:

| Parametre | Değer |
| --- | --- |
| `query` | Arama terimi (zorunlu) |
| `page`, `per_page` | Sayfa; `per_page` en fazla 30 |
| `order_by` | `relevant` (varsayılan) veya `latest` |
| `content_filter` | `low` (varsayılan) veya `high`; `high` daha katıdır ama tam garanti değildir |
| `orientation` | `landscape`, `portrait`, `squarish` |
| `color` | `black_and_white`, `black`, `white`, `yellow`, `orange`, `red`, `purple`, `magenta`, `green`, `teal`, `blue` |
| `lang` | ISO 639-1 dil kodu (varsayılan `en`) |

Yanıt: `total`, `total_pages`, `results[]`. Fotoğraf nesnesi: `id`, `width`, `height`, `color`, `alt_description`, `description`, `user`, `urls`, `links`. Bazı uçlar `urls.custom` döndürebilir.

## Görsel URL'leri

- `urls.raw` parametresiz temel URL'dir; `urls.full`, `urls.regular` (1080 px JPG), `urls.small`, `urls.thumb` hazır boyutlardır.
- URL'lerdeki `ixid` parametresi korunmalıdır; izlenme/atıf uyumu buna bağlıdır.
- Desteklenen dönüşüm parametreleri: `w`, `h`, `crop`, `fm`, `auto=format`, `q`, `fit`, `dpr`. Diğer imgix parametreleri resmî destek kapsamı dışındadır.
- Araç: `urls.raw` + `w`, `q`, `fm`, `fit=max`; `ixid` korunur. Görsel indirme istekleri `images.unsplash.com` üzerinedir ve hız limitine sayılmaz.

## İndirme tetikleyicisi

- İndirme benzeri eylemde (blog/başlık/hero için fotoğraf seçimi gibi) `photo.links.download_location` adresine istek atılmalıdır.
- `links.download` alanı kullanılmaz; doğru alan `download_location`'dır ve içindeki `ixid` gibi sorgu parametreleri korunur.
- Çağrı yetkilendirilmelidir (`client_id` veya Bearer token); aksi halde 401 döner.
- Uç nokta yalnız sayaç/analitik amaçlıdır; görseli gömmek için kullanılmaz, kullanıcıyı indirmeye yönlendirmek için kullanılmaz.
- Araç, görsel indirmeden önce tetikleyiciyi bir kez çağırır; çağrı başarısızsa görseli indirmez (çıkış kodu 7).

## Hotlink kuralı

- API kullanımının tamamında `photo.urls` altındaki URL'ler hotlink edilmelidir; bu yalnız arama sonuçları için değil, görselin kullanıldığı her yer için geçerlidir.
- Kendi görsel altyapısında barındırmak isteyen kurumlar için Unsplash API ekibiyle "photo views beacon" alternatifi görüşülmelidir.
- Sonuç: üretim sitesi için varsayılan yol hotlink + atıftır. Yerel indirme, kullanıcı açıkça isterse yapılır; API kılavuzuyla çelişebileceği kullanıcıya bildirilir ve karar kullanıcıya bırakılır.
- API kılavuzundaki "non-automated, high-quality, authentic experiences" maddesi otomatik ajan kullanımını gri alana sokar; otomatik toplu indirme yerine seçilmiş, az sayıda görsel kullan.

## Atıf

- Zorunlu: Unsplash, fotoğrafçı ve fotoğrafçının Unsplash profiline bağlantı; bağlantılarda `utm_source=<uygulama_adı>&utm_medium=referral` parametreleri.
- Önerilen biçim: `Fotoğraf: <a href="profil?utm...">Fotoğrafçı</a> / <a href="https://unsplash.com/?utm...">Unsplash</a>`. Araç `atif_html` alanını bu biçimde üretir.
- Unsplash License atıf zorunluluğu getirmez; ancak API Guidelines API kullanan uygulamalarda atıf ister. API kullanan her yerde atıf yapılır.
- Uygulama adı ve UTM kaynağı "Unsplash" adını içeremez.

## Hız limitleri

- Demo modu: saatte 50 JSON isteği. Production onayı: saatte 1000 istek. Daha yüksek limit için başvuru gerekir.
- Yalnız `api.unsplash.com` JSON istekleri sayılır; `images.unsplash.com` görsel istekleri sayılmaz.
- Yanıt başlıkları: `X-Ratelimit-Limit`, `X-Ratelimit-Remaining`.
- 403/429 durumunda istek tekrarlanmaz; bekleme ve production onayı gerekir. Araç 429 ve 5xx için 1-2-4 saniye geri çekilmeyle 3 deneme yapar, `Retry-After` başlığına uyar.
- 410 Gone: sorgu spam olarak işaretlenmiş olabilir; terimi değiştir.

## Kullanım kuralları (özet)

- Uygulama adında "Unsplash" adı kullanılamaz; Unsplash logosu uygulama simgesi olamaz.
- Değiştirilmemiş Unsplash fotoğrafları doğrudan veya dolaylı satılamaz (baskı, ürün vb.).
- Unsplash'ın çekirdek kullanıcı deneyimi klonlanamaz (resmî olmayan istemci, duvar kağıdı uygulaması vb.).
- API, otomatik olmayan, yüksek kaliteli ve özgün deneyimler için kullanılır; aşırı istek erişimi kapatabilir.
- Kullanıcıdan Unsplash geliştirici hesabı açması istenmez; proxy veya OAuth çözümü kullanılır.

## Lisans ile API koşulları farkı

- Unsplash License: fotoğraflar ücretsiz indirilip kullanılabilir (ticari kullanım dahil), atıf zorunlu değildir.
- API Terms ve API Guidelines: API üzerinden kullanımda hotlink, indirme tetikleyicisi, atıf ve UTM zorunludur.
- Yerel indirme kararı bu iki rejim arasındaki farkı doğurur; kritik/hukuki kararlar `doğrulanmalı` etiketiyle kullanıcıya bırakılır.

## Ticari kullanım sınırı

Unsplash License ticari kullanıma izin verir; ancak Terms & Conditions marka/logo, tanınabilir kişi ve sanat eseri/telifli iş haklarını kapsamaz. Unsplash+ ayrı abonelik lisansıdır. Araç varsayılan ticari modda riskli metadata ve premium kaynakları bloklar (çıkış 8); indirilen görsel gözle denetlenip `onayla` ile kayda geçmeden ticari sayfaya eklenmemelidir. Ayrıntı: `references/ticari-guvenlik.md`. Hukuki değerlendirme kullanıcıya aittir.

## Hata eşlemesi

| HTTP / durum | Araç çıkış kodu | Not |
| --- | --- | --- |
| 400 | 2 | İstek parametreleri geçersiz |
| 401 | 3 | Anahtar geçersiz/yetkisiz |
| 403 | 5 | İzin yok veya hız limiti; production onayı gerekebilir |
| 404 | 4 | Fotoğraf/kaynak bulunamadı |
| 410 | 5 | Sorgu spam olarak işaretlendi; terimi değiştir |
| 429 | 5 | Hız limiti; geri çekilme ve bekleme |
| 5xx | 5 | Sunucu hatası; sınırlı yeniden deneme |
| Geçersiz görsel yanıtı | 6 | MIME/imza doğrulaması başarısız |
| Tetikleyici başarısız | 7 | Görsel indirilmedi; API kuralı gereği atlanmaz |
| Ticari risk | 8 | Unsplash+/kişi/marka/eser/hassas içerik; görsel indirilmedi |
