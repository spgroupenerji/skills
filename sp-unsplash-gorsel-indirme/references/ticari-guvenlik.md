# Ticari Güvenlik ve Onay Kapısı

Doğrulama tarihi: 2026-10-31. Kaynaklar (resmî):

- Unsplash License — https://unsplash.com/license
- Terms & Conditions — https://unsplash.com/terms
- Unsplash+ License — https://unsplash.com/plus/license
- API Guidelines — https://help.unsplash.com/en/articles/2511245-unsplash-api-guidelines

Bu belge hukuki danışmanlık değildir; ticari kampanya, reklam veya marka kullanımı için şüphede avukata danış.

## Doğrulanan temel kurallar

- **Unsplash License:** Görseller ücretsiz indirilip kullanılabilir; ticari ve ticari olmayan kullanım serbesttir; izin veya atıf zorunlu değildir (atıf takdir edilir). Yasaklar: görseli önemli ölçüde değiştirmeden satmak; Unsplash görsellerini rakip/benzer bir hizmet oluşturacak şekilde derlemek.
- **Terms & Conditions:** Unsplash License; görsellerde yer alan **marka, logo ve işaretlerin**, **tanınabilir kişilerin görüntülerinin** ve **sanat eseri/telifli işlerin** kullanım hakkını kapsamaz. Kullanım biçimine göre marka sahibinden, kişiden veya hak sahibinden izin gerekebilir.
- **Unsplash+:** Ayrı lisans ve abonelik gerektirir. Ticari kullanım mümkündür; ancak satış, dijital şablon, makine öğrenmesi/AI/biyometri ve hassas konular gibi kısıtlar vardır; Unsplash+ kapsamında sınırlı garanti sunulur. **Standart Unsplash License bu görselleri kapsamaz.**
- **Model/property release:** Unsplash lisansı model veya mülk izni sağlamaz. Tanınabilir kişi, özel mülk veya marka içeren görselde kullanım amacına göre ayrı izin gerekebilir (**doğrulanmalı**).
- **API Guidelines:** API kullanımında hotlink, atıf + UTM ve indirme benzeri eylemde `download_location` tetikleyicisi ayrıca zorunludur.

## Varsayılan politika: ticari mod

`indir` ve `baglantidan-indir` varsayılan olarak `--kullanim-turu ticari` çalışır.

**Sert blok (indirme yapılmaz, çıkış kodu 8):**

- Unsplash+ / premium: `plus.unsplash.com`, `premium_photo`, Getty/Unsplash+ kaynaklı görseller.
- Kişi/insan: `man`, `woman`, `person`, `people`, `child`, `face`, `portrait`, `selfie`, `group`, `team`, `businessman`, `family`, `hands` ve Türkçe karşılıkları.
- Marka/logo: `logo`, `brand`, `trademark`, `billboard`, `storefront` ve bilinen marka adları.
- Sanat eseri/telifli iş: `painting`, `artwork`, `sculpture`, `mural`, `graffiti`, `statue`.
- Hassas içerik: silah, şiddet, kan, çıplaklık, uyuşturucu, sigara, alkol, kumar, siyaset, din, asker/polis, para, tıbbi görüntü.
- İkonik/özel mülk: örn. Eyfel Kulesi, `private property`.

**Manuel doğrulama (engel yok, yine de zorunlu):** Metadata kişi/logo/mülk riskini tam yakalayamaz. İndirilen her görsel gözle incelenir; kişi, logo, marka, sanat eseri, özel mülk veya hassas içerik varsa kullanılmaz.

**Onay kaydı:** Ticari sayfaya eklemeden önce:

```powershell
python scripts/unsplash_gorsel.py onayla --id "<FOTO_ID>" --ad "<seo-ad>" --karar uygun --onaylayan "<ad>" --not "<görsel denetim notu>"
```

`credits.json` içinde `ticari_durum` `onaylandi` veya `reddedildi` olur; `ticari_onay` alanı karar, onaylayan, tarih ve notu saklar. **`onaylandi` olmayan kayıt ticari sayfaya eklenmez.** Reddedilen görsel kullanılmaz; yeni aday aranır.

**Editoryal mod:** `--kullanim-turu editorial` yalnız editoryal bağlam içindir; kişi/hassas içerik serbestleşir, ancak ticari reklam/tanıtımda kullanılamaz; Unsplash+ yine bloktur.

## Akış

1. `ara` çıktısındaki `ticari_degerlendirme.durum` alanını oku; `engelli` adayı hiç seçme.
2. `indir` (varsayılan ticari) çalıştır; `8` dönerse görsel indirilmemiştir; farklı aday seç.
3. İndirilen görseli `read_image` veya Chrome ile **gözle** denetle: tanınabilir kişi/yüz, logo/marka, sanat eseri, özel mülk, hassas içerik, yanıltıcı bağlam.
4. Uygunsa `onayla --karar uygun`; değilse `onayla --karar uygun-degil` ve kullanma.
5. HTML'e ekle; görünür atıf + UTM; `credits.json` repoda kalsın.
6. Şüphe varsa görseli kullanma veya hukuki görüş al (`doğrulanmalı`).

## Denetim listesi

- [ ] Görsel Unsplash+ / premium değil (standart `images.unsplash.com` + Unsplash License).
- [ ] Tanınabilir kişi/yüz yok; varsa ticari kullanım için release/izin durumu net.
- [ ] Logo, marka, tabela, ürün kimliği yok.
- [ ] Sanat eseri, heykel, mural, telifli tasarım yok.
- [ ] Özel mülk/ikonik yapı riski yok veya izin var.
- [ ] Hassas/uygunsuz bağlam yok.
- [ ] `credits.json` kaydı `ticari_durum: onaylandi` ve `ticari_onay` dolu.
- [ ] Görünür atıf + UTM; API kullanımıysa hotlink/trigger kuralları ayrıca karşılandı.
- [ ] Ticari sınırlar: değiştirilmeden satış yok, rakip hizmet derlemesi yok, Unsplash adı/logo uygulama kimliğinde yok.

## Sınırlar

- Anahtar kelime taraması bir **heuristiktir**; görseldeki kişi/logo/mülkü tam garanti etmez. Nihai sorumluluk kullanıcıda ve hukuki değerlendirmededir.
- Unsplash+ aboneliği varsa bile bu araç Unsplash+ görsellerini bilinçli olarak indirmez; ayrı bir iş akışı ve lisans doğrulaması gerekir.
- Lisans ve Terms değişebilir; yayın öncesi resmî sayfalardan yeniden doğrula.
