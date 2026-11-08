# Ek API Envanteri ve Karar Matrisi

Doğrulama: 2026-11-08; resmî doküman + canlı uç (HTTP yanıtı/DNS). Bu dosya "public-apis" tarzı toplu listelerden gelen adayların hangisinin ticari güvenli tedarik hattına alındığını, hangisinin reddedildiğini ve nedenini kaydeder. Yeni aday eklerken aynı kanıt eşiği uygulanır: resmî doküman + canlı yanıt + lisans zinciri netliği.

## 1. Uygulanan kaynaklar

| Kaynak | Karar | Kanıt | Kapsam |
| --- | --- | --- | --- |
| Art Institute of Chicago | **EKLE (uygulandı)** | Anahtarsız; `query[term][is_public_domain]=true` sunucu tarafı süzgeç (canlı 133.165 → 62.119); IIIF `/{image_id}/full/{w},/0/default.jpg`; görseller CC0 | Sanat, doku, illüstrasyon |
| Cooper Hewitt | **EKLE (uygulandı)** | Anahtarsız GraphQL: `GET https://api.cooperhewitt.org/?raw&query=...`; medyada `cc0:true` bayrağı istemci süzgeci (canlı cc0 oranı ~%15); S3 görselleri | Tasarım, tekstil, afiş |

Ayrıntılı uç/alan sözleşmesi: `kaynak-api-sozlesmesi.md`.

## 2. İkinci faza bırakılanlar (doğrulandı, uygulanmadı)

| Kaynak | Neden şimdi değil | Hazır tarif |
| --- | --- | --- |
| Europeana | Anahtar (wskey) gerekir; medya lisansı kayıt bazında `rights` doğrulaması ister; ücretsiz kota sayısı yayımlanmıyor | `GET https://api.europeana.eu/record/v2/search.json?wskey=...&query=...&rows=...&reusability=open&media=true&qf=RIGHTS:http://creativecommons.org/publicdomain/zero/1.0/*`; yalnız `rights` CC0/PDM olanları al |
| Rijksmuseum | Anahtarsız ama iki adımlı Linked Art akışı (arama → JSON-LD detay → `subject_of[].digitally_carried_by[].access_point[].id` → `iiif.micr.io`); serbest metin arama parametreleri belirsiz | `GET https://data.rijksmuseum.nl/search/collection?objectNumber=...&imageAvailable=true`; detay `?_profile=la-framed`; görsel IIIF |
| 3DTexel | Gerçek ve CC0 ama fotoğraf değil; PBR doku/HDRI/3B model; indirme API anahtarı ister | Ayrı "3B varlık" hattı açılırsa değerlendirilir |
| Iconify | Anahtarsız, lisansı makine-okunur (set bazlı MIT/Apache-2.0/CC0) ama ikon SVG'si ayrı varlık sınıfı | İkon hattı açılırsa `https://api.iconify.design/{prefix}/{name}.svg` + `/collections` lisans kontrolü |
| Cloudmersive NSFW | Doğrulanmış tek ücretsiz kotalı NSFW sınıflandırıcı (600 çağrı/ay) ama anahtar + görselin üçüncü tarafa yüklenmesi | Opsiyonel `denetim` sağlayıcısı olarak eklenebilir; varsayılan kapalı |

## 3. Reddedilenler ve gerekçeleri

| Aday | Karar | Gerekçe (kanıt) |
| --- | --- | --- |
| Lorem Picsum | RED | Yalnız "Images from Unsplash" der; fotoğrafların lisans beyanı yok, MIT yalnız kodu kapsar; konu araması/atıf yok. Placeholder için bile üretimde kullanılmaz |
| Foodish | RED | Servis sahibi tarafından askıya alındı (canlı 503) |
| Coffee API | RED | Görsellerin kaynağı/lisansı beyan edilmemiş; MIT yalnız kodu kapsar |
| Imagga | RED | NSFW ucu ayrı markaya taşınmış ve dokümanı 404; ücretsiz kota 100/ay; ücretli |
| Irisnet | RED | Kimlik/yaş doğrulama odaklı, kredi modeli; fiyat yayımlanmıyor; tedarikle ilgisiz |
| IPS Online | RED (YOK) | DNS NXDOMAIN; yalnız dizin sayfaları var; sağlayıcı ölü |
| Hirak FaceAPI | RED (YOK) | Park alanı; birincil ürün yok |
| UpRes | RED (şimdilik) | Gerçek ama yalnız Business $49/ay; ücretsiz API katmanı yok |
| Remove.bg / PhotoRoom / ObjectCut | RED (şimdilik) | Ücretsiz katman ticari değil ("non-commercial only") veya filigranlı; ticari kullanım ücretli |
| ReSmush.it | RED | "Personal use only"; ticari kullanım için izin gerekiyor; aynı iş Pillow/WebP ile yerel ve sınırsız |
| PHP-Noise / DummyImage | YEREL-ALTERNATIF | Aynı çıktı (gürültü, yer tutucu) Pillow ile ağsız üretilir; dış SLA yok |
| The Color API / PickShade | YEREL-ALTERNATIF | Palet/kontrast/renk dönüşümü yerelde hesaplanır; bu araç `renk.py` ile yapar |

## 4. Bu turda eklenen yerel yetenek

- `renk.py`: indirilen görselden baskın renk + 5 renk paleti + WCAG kontrast önerisi üretir; `indir` çıktısında ve `credits.json` kaydında `renk` alanı olarak saklanır (Pillow varsa).
- `indirmi` başlıkları: kaynak bazlı ek HTTP başlığı (AIC IIIF `Referer` zorunluluğu) desteklenir.
- Pexels `avg_color` ve Unsplash `color` alanları `ara` çıktısında `renk` ipucu olarak verilir (indirme öncesi marka rengi elemesi).

## 5. Yerel / API ayrımı (Pillow yetenekleri)

| İş | Yerel mümkün | Karar |
| --- | --- | --- |
| Baskın renk, palet, WCAG kontrast | Evet | Yerel (`renk.py`) |
| Kayıpsız/optimize sıkıştırma, WebP | Evet | Yerel (`indirici.py`) |
| Yer tutucu, gürültü arka planı | Evet | Gerekirse yerel; şimdilik kapsam dışı |
| Yüz/NSFW algılama | Hayır | Opsiyonel API (Cloudmersive) — varsayılan kapalı, görsel onay yine zorunlu |
| Arka plan silme, AI büyütme | Hayır | Kapsam dışı; ücretli sağlayıcı gerekir |

## 6. Yeni aday kabul kuralı

1. Ticari lisans zinciri net olmalı (CC0/PD veya ücretsiz ticari özel lisans); belirsizse red.
2. Anahtarsız veya tek ücretsiz anahtarla erişilebilir olmalı; ağır OAuth/kurumsal kredi red.
3. Sunucu tarafı lisans/kamu malı süzgeci varsa tercih; yoksa istemci süzgeci kanıtlanmalı.
4. Yerel (Pillow) alternatifi varsa API eklenmez.
5. Fotoğraf/doku dışı varlık sınıfları (ikon, 3B model) ayrı hat açılmadan bu beceriye eklenmez.
