# Ticari Güvenlik, Lisans Sınıfları ve Onay Kapısı

Doğrulama tarihi: 2026-11-08. Kaynaklar resmî API/lisans sayfalarıdır; kurallar ve sayfa içerikleri değişebilir, yayın öncesi yeniden doğrula.
Bu belge hukuki danışmanlık değildir; ticari kampanya, reklam, marka veya tanınabilir kişi içeren kullanımlarda avukata danış.

## 1. Temel ilke

Araç yalnız iki lisans sınıfını kullanır: **`kamu-mali`** (CC0 / Public Domain) ve **`serbest-ticari`** (Pexels, Pixabay, Unsplash özel lisansları). `kosullu` sınıf (CC-BY, CC-BY-SA, GFDL, Flickr-7, ABD hükümet işi vb.) arama sonucunda **döndürülmez**; atıf/paylaşım koşulları ve belirsizlikleri yüzünden varsayılan ticari hatta girmez.

Telif lisansı temiz olsa bile **kişilik hakkı, marka hakkı ve özel mülk** ayrı risklerdir; bu yüzden her görsel `onayla --karar uygun` kaydı olmadan ticari sayfaya eklenmez.

## 2. Kaynak lisans matrisi (doğrulanmış olgular)

| Kaynak | Lisans | Ticari | Atıf | Yerel kopya | Kritik sınır |
| --- | --- | --- | --- | --- | --- |
| Pexels | Pexels License | Evet | Gerekmez; API uygulamasında belirgin Pexels bağlantısı şart | Serbest | Değiştirilmemiş kopya satışı; stok/platform yeniden dağıtımı; onay iması yasak |
| Pixabay | Pixabay Content License | Evet | Gerekmez; API uygulamasında kaynak gösterimi beklenir | Serbest; **hotlink yasak** | Tek başına satış/dağıtım yasak; marka/logo ile ticari kullanım yasak; tanınabilir kişi sınırı |
| Unsplash | Unsplash License | Evet | **API'de zorunlu** (+UTM) | **Hotlink zorunlu**; yerel için açık kullanıcı kabulü | Değiştirilmeden satış; çekirdek deneyim klonlama; Unsplash+ ayrı lisans |
| Openverse | CC0 / PDM (süzülür) | Evet | Gerekmez | Serbest | Toplayıcıdır: orijinal kaynak ve lisans her kayıtta doğrulanır |
| Wikimedia Commons | CC0 / PD (süzülür) | Evet | Gerekmez (CC0/PD) | Serbest | Karışık lisans havuzu; yalnız CC0/PD geçer; kişilik hakkı saklı |
| Smithsonian | CC0 | Evet | Gerekmez (kaynak göstermek faydalı) | Serbest | Yalnız CC0 işaretli medya; logo/marka CC0 dışı; kültürel hassasiyet |
| The Met | CC0 (kamu malı eser) | Evet | Gerekmez | Serbest | Yalnız `isPublicDomain=true` eserler; telifli eser kullanılmaz |
| NASA | ABD kamu malı | **Koşullu** | Gerekmez; kaynak gösterilir | Serbest | Amblem/logotype kamu malı değil; onay iması yasak; üçüncü taraf telif ve tanınabilir kişi istisnası |
| Poly Haven | CC0 | Evet | Gerekmez ("Powered by Poly Haven" rica) | Serbest | HTML kazıma yasak, API zorunlu; UA/Referer şart |
| Flickr | CC0 (9) / PDM (10) | Evet | Gerekmez (CC0/PDM) | Serbest | **Yalnız lisans 9-10**; 7 (Commons) CC lisansı değildir ve ticari garanti vermez; sahibi kaldırma isterse 24 saat içinde cache güncelle |

Ayrıntılı API/atıf davranışı: `kaynak-api-sozlesmesi.md`.

## 3. Kaynak bazlı kritik açıklamalar

- **Pexels:** "Attribution is not required" ders; ancak API uygulamalarında belirgin bir Pexels bağlantısı beklenir. "Don't sell unaltered copies" ve "don't redistribute on stock/wallpaper platforms" yasakları; marka/logo ve tanınabilir kişi için izin gerekebilir.
- **Pixabay:** İçerik lisansı ticari kullanıma izin verir; "You cannot sell or distribute the Content on a Standalone basis" (baskı, poster, ürün, NFT). Marka/logo ile ticari kullanım açıkça yasak. Hotlink yasak: görsel indirilip barındırılmalı.
- **Unsplash:** Lisans atıf istemez; **API Guidelines** ise hotlink, görünür atıf + UTM ve indirme benzeri eylemde `links.download_location` tetikleyicisi ister. API kullanımında yerel kopya bu kural ile çelişebilir; araç varsayılan olarak hotlink önerir, yerel indirmeyi yalnız `--yerel-kabul` ile yapar. Unsplash+ / premium görseller standart lisans kapsamında değildir ve araç tarafından dışlanır.
- **Openverse:** CC0/PDM filtresi `license=cc0,pdm` ile istenir; her kayıtta `license` alanı yeniden doğrulanır. Kayıt `source`/`provider` alanı orijinal kaynağı gösterir; orijinal kaynağın ticari sınırları ayrıca geçerlidir.
- **Wikimedia Commons:** Yalnız CC0/PD lisanslı dosyalar kullanılır (`extmetadata.License` = cc0/pd; yedek `LicenseShortName`). Commons'ta CC-BY/CC-BY-SA dosyalar da bulunur; bunlar araç tarafından elenir. Kişi fotoğraflarında kişilik hakkı saklıdır.
- **Smithsonian:** Yalnız `usage.access == "CC0"` işaretli medya kullanılır; metadata'da CC0 olsa bile nesneye bağlı kültürel hassasiyet/donör kısıtı olabilir. Smithsonian adı/logo ve diğer markalar CC0 kapsamı dışıdır.
- **The Met:** Yalnız `isPublicDomain=true` nesneler kullanılır (arama parametresi yok sayıldığı için filtre istemci tarafında yapılır). Eserin kendisi kamu malı olsa da fotoğrafın çekildiği bağlam veya üçüncü taraf hakları istisna olabilir.
- **NASA:** İçerik genelde ABD'de telifsizdir; fakat **NASA amblemi, logosu ve kimlik işaretleri kamu malı değildir**, onay ima eden kullanım yasaktır, üçüncü taraf telifli görseller ve tanınabilir kişiler istisnadır. Araç NASA'yı `kamu-mali` sayar ama onay kapısında bu riskleri ayrıca denetletir.
- **Poly Haven:** CC0; API üzerinden indirme serbest, HTML kazıma yasak. Son kullanıcıya gösterimde "Powered by Poly Haven" atfı rica edilir (zorunlu değil).
- **Flickr:** API ToS ticari kullanımda Creative Commons lisansı şartı koyar; **lisans 7 (No known copyright restrictions) CC lisansı değildir** ve Commons açıkça garanti vermez. Bu yüzden araç yalnız 9 (CC0) ve 10 (PDM) kullanır.

## 4. İçerik riski heuristiği

Araç başlık, açıklama ve etiket metninde şu kategorileri arar ve `ticari.durum` üretir:

- `insan`: man, woman, person, people, child, face, portrait, group, team, hands, Türkçe karşılıkları.
- `marka`: logo, brand, trademark, billboard, storefront, bilinen marka adları, tabela, ürün.
- `eser`: painting, artwork, sculpture, mural, graffiti, statue, eser, heykel.
- `hassas`: silah, şiddet, kan, çıplaklık, uyuşturucu, sigara, alkol, kumar, siyaset, din, asker/polis, para, tıbbi.
- `engel`: kaynak adaptörünün işaretlediği kesin engel (ör. premium/plus kaynak, lisans koşullu).

Durumlar: `uygun` (metadata temiz), `manuel_dogrulama_gerekli` (risk terimi bulundu; hâlâ indirilebilir ama görsel denetim şart), `engelli` (indirilmez, çıkış 8).

Bu tarama **heuristiktir**: kişiyi/logoyu tam yakalamaz, yanlış pozitif üretebilir. Nihai karar görsel denetimi ve kullanıcı sorumluluğudur.

## 5. Onay kapısı ve `credits.json`

Her indirme `credits.json` içine `ticari_durum: manuel_dogrulama_gerekli` ile yazılır. Ticari sayfaya eklemeden önce:

1. Görseli `read_image` ile aç; tanınabilir kişi/yüz, logo/marka, sanat eseri, özel mülk, hassas içerik, yanıltıcı bağlam yok mu?
2. Uygunsa: `onayla --kaynak <k> --id <id> --karar uygun --onaylayan "<ad>" --not "<denetim notu>"`.
3. Değilse: `--karar uygun-degil`; görsel kullanılmaz, yeni aday aranır.
4. Yalnız `ticari_durum: onaylandi` olan kayıt ticari sayfaya girer. `ticari_onay` alanı karar, onaylayan, tarih ve notu saklar.

`denetle` komutu onaysız kayıtları ve diskte eksik dosyaları listeler; yayın öncesi çalıştırılır.

## 6. Denetim listesi

- [ ] Lisans sınıfı `kamu-mali` veya `serbest-ticari`; `kosullu` değil.
- [ ] Kaynakta premium/plus/editorial-only işaret yok.
- [ ] Tanınabilir kişi/yüz yok; varsa ticari kullanım için izin durumu net.
- [ ] Logo, marka, tabela, ürün kimliği yok.
- [ ] Sanat eseri, heykel, mural, telifli tasarım yok.
- [ ] Özel mülk/ikonik yapı riski yok veya izin var.
- [ ] Hassas/uygunsuz bağlam yok; görsel sayfa bağlamına uygun.
- [ ] `credits.json`: lisans, kaynak sayfası, fotoğrafçı, dosyalar, `ticari_durum: onaylandi`, `ticari_onay` dolu.
- [ ] Görünür atıf/UTM (zorunlu kaynaklarda) ve hotlink/yerel kopya kararı bilinçli.
- [ ] `alt` metni yazıldı; `width`/`height` gerçek oran; LCP görseli eager.
- [ ] Ticari sınırlar: değiştirilmemiş satış yok, stok platformunda yeniden dağıtım yok, onay iması yok.

## 7. Sınırlar

- Anahtar kelime taraması ve görsel denetim hukuki garanti değildir; kişilik/marka hakkı ve özel mülk için izin kullanıcıya aittir.
- Lisanslar ve API koşulları değişebilir; kritik kararlar `doğrulanmalı` etiketiyle kullanıcıya bırakılır.
- ABD dışı yargı alanlarında kamu malı statüsü farklılaşabilir; uluslararası kampanyalarda hukuki görüş alın.
