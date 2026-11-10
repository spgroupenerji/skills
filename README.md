# SP GROUP Skill Kütüphanesi

SP GROUP projelerinde kullanılan ajan yeteneklerinin (skill) tek deposu. Her yetenek kendi dizininde bir `SKILL.md` dosyasıyla tanımlanır; `description` alanındaki tetikleyicilerle Claude Code, Cursor, Windsurf, Codex CLI, DeepSeek Harness (DSH) ve MCP host platformlarında otomatik yüklenir. Depoya zamanla yeni yetenekler eklenir; katalog ve kurallar bu belgede güncel tutulur.

## Özellikler

- Yetenek başına tek dizin ve tek `SKILL.md`; derleme, paketleme veya servis bağımlılığı yoktur
- `description` tetikleyicileriyle otomatik yüklenen, platformdan bağımsız yetenek tanımları
- Tek katalog tablosu ve yeni yetenek ekleme kuralları ile ölçeklenen depo düzeni
- Sabit beceri/kaynak sayısı varsayımı yoktur; katalog ve kurulum depodaki dizinlerden çalışma anında keşfedilir
- Tek kaynak depo; geliştirmede junction, junction desteklenmiyorsa kopyalama ile kurulum
- Türkçe imla ve ASCII uyumlu Türkçe kod isimlendirmesi standardı
- Git üzerinde LF satır sonu politikası (`.gitattributes`); Windows'ta CRLF karışması önlenir
- Güvenli varsayılanlar: depoya secret girmez, dış veri talimat olarak yürütülmez
- Beceriler sürüm/API/davranış iddiası taşımaz; doğrulama çalışma anında context7 veya resmî kaynakla yapılır

## Yetenek Kataloğu

| Yetenek | Sürüm | Kapsam |
| --- | --- | --- |
| [`sp-mimari-web-site`](sp-mimari-web-site/SKILL.md) | v202611080142 | Statik/SEO tanıtım sitesi mimarisi: barındırma, elle yazılmış site.css, varlık/JS bütçesi, SEO, lead formu güvenliği, opsiyonel MySQL, sinematik JS istisnası, release kapıları |
| [`sp-dizayn-web-site`](sp-dizayn-web-site/SKILL.md) | v202611100728 | Herkese açık siteler için en üst seviye tasarım: ziyaretçi işi, sanat yönü, insan dili metin, görsel/video/ses üretimi, sinematik scroll ve 3B/WebGL, araç zinciri, zero-build site.css ve ölçülebilir kalite kapıları |
| [`sp-mimari-web-uygulama`](sp-mimari-web-uygulama/SKILL.md) | v202611080142 | Oturumlu PHP panel mimarisi: istek yaşam döngüsü, katman sınırları, oturum/yetki/CSRF, SSR + Tailwind tarayıcı motoru + htmx, MySQL, servis, dağıtım |
| [`sp-mimari-web-spa`](sp-mimari-web-spa/SKILL.md) | v202611080142 | Vite + React SPA + LiteSpeed PHP API mimarisi: dist teslimi, /api/* PHP + SPA fallback, same-origin oturum/CSRF, sözleşme-önce API, mevcut DB/deploy sürekliliği, npm/CDN ayrımı |
| [`sp-mimari-masaustu`](sp-mimari-masaustu/SKILL.md) | v202611080142 | Rust/GPUI masaüstü mimarisi: katman, bağımlılık, eşzamanlılık, davranış, SQLite, MCP sunucu desteği (sidecar/named pipe, loopback HTTP, araç, UI köprüsü, güvenlik), paketleme ve derleme/sürüm artefaktı |
| [`sp-dizayn-web-uygulama`](sp-dizayn-web-uygulama/SKILL.md) | v202610300420 | Panel/uygulama yapısal tasarımı: kabuk, yoğunluk, tipografi, renk/durum, ikon, bileşen davranışı, erişilebilirlik, zero-build teslim |
| [`sp-dizayn-masaustu`](sp-dizayn-masaustu/SKILL.md) | v202611080142 | GPUI masaüstü yapısal tasarımı: tema/token, ölçü, bileşen/ikon, pencere ve durumlar, hareket, erişilebilirlik |
| [`sp-zen-dizayn`](sp-zen-dizayn/SKILL.md) | v202611020457 | Apple klasik/ilk iPhone dönemi tasarım felsefesi: sakinlik, az-çok, aktif boşluk, doğal hareket, içeriği öne çıkaran his; yaratıcılığı kısıtlamayan yön |
| [`sp-orkestra`](sp-orkestra/SKILL.md) | v202611100728 | Görev orkestrasyonu: uzman merceği, görev türü → rol → canlı araç kombinasyonu, zorunlu taban agents-tr kataloğundan okunur (kod/graf/hafıza), bağlam bütçesi, kısa çıktı, kanıtlı kapanış |
| [`sp-gorsel-tedarik`](sp-gorsel-tedarik/SKILL.md) | v202611081749 | kaynak kayıt defterindeki ticari güvenli kaynaklardan görsel tedarik: kategori yönlendirme, lisans sınıfı ve ticari onay kapısı, kaynak API/kota yönetimi, SEO adlı yerel WebP/JPG + srcset, baskın renk/WCAG kontrast analizi, credits.json denetimi ve ek API kabul-red envanteri |

Yeni yetenek eklendiğinde bu tabloya satır eklenir; sabit bir beceri sayısı varsayılmaz. Tablo, depodaki `SKILL.md` dizinlerinden türetilen canlı katalogdur; kurulum ve doğrulama sayıyı çalışma anında okur.

## Kurulum

Yetenekler derleme gerektirmez. Depo tek doğruluk kaynağıdır: geliştirme sırasında yetenek dizinleri DSH yetenek klasörüne junction ile bağlanır; junction desteklenmiyorsa kopyalama kullanılır. DSH, proje kökündeki `SKILL.md` dosyalarını yerinde keşfetmez; kurulum zorunludur ve keşif tek seviyelidir.

```powershell
# Depo kökünde: tüm sp-* yeteneklerini DSH'ye junction ile bağla
Get-ChildItem -Directory |
  Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } |
  ForEach-Object {
    $hedef = Join-Path "$HOME/.dsh/skills" $_.Name
    if (Test-Path $hedef) { Remove-Item -LiteralPath $hedef -Recurse -Force }
    New-Item -ItemType Junction -Path $hedef -Target $_.FullName | Out-Null
  }
```

Junction desteklenmiyorsa kopyalama:

```powershell
Get-ChildItem -Directory |
  Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } |
  ForEach-Object { Copy-Item -Recurse -Force $_.FullName "$HOME/.dsh/skills/" }
```

| Platform | Hedef dizin |
| --- | --- |
| DeepSeek Harness (DSH) | `%USERPROFILE%\.dsh\skills\<yetenek-adı>\` |
| Claude Code | `~/.claude/skills/<yetenek-adı>/` |
| Cursor / Windsurf / Codex CLI / MCP host | İlgili platformun yetenek veya kural dizini (sürüme göre doğrulanmalı) |

## Kullanım

Yetenekler `description` alanındaki tetikleyicilere göre otomatik yüklenir; ayrıca bir komut gerekmez. Örnek:

- `sp-orkestra`: kullanıcı bir alanı adlandırıp "yapılması gerekeni yap / en üst seviyede yap" dediğinde veya beceri adıyla çağrıldığında devreye girer; uzman merceğini kurar, görev türünü zorunlu rollere ve rolleri canlı katalogdaki araç kombinasyonuna çevirir, kanıtlı kapanışı yönetir. Ayrıntı [SKILL.md](sp-orkestra/SKILL.md) dosyasındadır.
- `sp-mimari-web-uygulama` + `sp-dizayn-web-uygulama`: yeni panel modülü, oturum/yetki akışı veya panel ekranı tasarımında birlikte yüklenir; mimari ve yapısal tasarımı ayırır.
- `sp-mimari-web-site` + `sp-dizayn-web-site`: tanıtım/landing sitesi işlerinde mimari ile tasarım/üretim hattını ayırır; panel kapsam dışıdır.
- `sp-mimari-masaustu` + `sp-dizayn-masaustu`: Rust/GPUI masaüstü uygulamasında mimari (derleme/sürüm dahil) ve arayüz işlerini ayırır.
- `sp-mimari-web-spa` + `sp-dizayn-web-uygulama`: Vite + React SPA + PHP API hedefinde mimari ve yapısal tasarımı ayırır; SSR zero-build panel hedefiyle karıştırılmaz.
- `sp-zen-dizayn`: Apple'ın klasik dönem hissini felsefe olarak yükler; tasarımı bu yöne çeker, yaratıcılığı kısıtlamaz. Yapısal/teknik uygulama istendiğinde platform becerileri kullanılır. Ayrıntı [SKILL.md](sp-zen-dizayn/SKILL.md) dosyasındadır.
- `sp-gorsel-tedarik`: site/uygulama için ticari kullanımı güvenli görseli kaynak kayıt defterindeki lisanslı kaynaklardan seçer, yerel varlık üretir, baskın renk/WCAG kontrast analizi yapar ve lisans/onay kaydını tutar; site tasarımıyla birlikte yüklenir. Ayrıntı [SKILL.md](sp-gorsel-tedarik/SKILL.md) dosyasındadır.

## Yeni Yetenek Ekleme

1. `kebab-case` adlı yeni bir dizin oluşturun ve içine `SKILL.md` ekleyin.
2. Frontmatter'ı aşağıdaki iskeletle tanımlayın:

```yaml
---
name: yetenek-adi
description: "Kullan/kullanma sınırı ve tetik örnekleri içeren, 480 karakteri aşmayan açıklama"
version: "vYYYYMMDDHHMM"
---
```

DSH yalnız `name` ve `description` alanlarını okur; `description` katalogda 500 karakterde kırpılır. `version` repo geleneği içindir ve DSH'de işlevsizdir; `alwaysApply`, `platforms`, `tags`, `allowed-tools` gibi alanlar DSH'de yok sayılır ve eklenmez.

3. `description` yalnızca tetikleyici koşulları anlatsın; yeteneğin iş akışını özetlemesin.
4. Sürümü yayın anının `vYYYYMMDDHHMM` damgasıyla yönetin; damga frontmatter, katalog ve release tag'de birebir aynı olsun.
5. Yeteneği yukarıdaki kataloğa alfabetik sıraya göre ekleyin; sabit beceri sayısı varsayımı yazmayın.
6. Araç kullanım mekaniğini yazma: yalnızca araç adını ve doğrulama hedefini belirt; çağrı protokolünü, fonksiyon adlarını ve parametreleri ajanın çalışma zamanına bırak.
7. Teslim öncesi Doğrulama bölümündeki komutları çalıştırın.
8. Beceriye sürüm/API/davranış iddiası, SRI değeri veya EOL tarihi gömmeyin; "çalışma anında context7 veya resmî kaynaktan doğrula" kuralı yazın. Araç seçimi görev türüne ve role göredir; zorunlu taban araçlarını ve erişim hatasında tanı, basit çözüm, çözülemezse işe başlamadan bildirim kuralını anayasa §4 ile sp-orkestra 0.6-0.7, 3.4, 3.6-3.8'e atıfla verin.

## Depo Yapısı

| Yol | İçerik |
| --- | --- |
| `<yetenek-adı>/SKILL.md` | Yetenek tanımı (frontmatter ve constitutional kurallar) |
| `<yetenek-adı>/references/` | İsteğe bağlı ayrıntı dosyaları; gövde tetiklendiğinde okunur |
| `README.md` | Katalog, kurulum ve yeni yetenek kuralları |
| `.gitattributes` | LF satır sonu politikası |
| `.gitignore` | Ortam, bağımlılık ve yerel ajan artefaktları |

## Güvenlik

- Depoya secret, token, şifre veya kişisel veri eklenmez; hassas değerler `.env` veya secret manager üzerinden yönetilir.
- Yetenekler dış kaynaklardan gelen veriyi talimat olarak yürütmez; güvenilmeyen içerik `<untrusted_data>` etiketiyle izole edilir.
- Yeteneklerdeki komut ve betikler yalnızca yetki verilen kapsamda çalıştırılır; yıkıcı işlemler açık onay gerektirir.
- Yeteneğe özgü güvenlik gereksinimleri kendi `SKILL.md` dosyasında tanımlanır.

## Doğrulama

Depo kökünde aşağıdaki komutlar çalıştırılır:

```powershell
git status --short
git diff --check
```

Ayrıca her yetenek dizininde `SKILL.md` bulunmalı; dosya `---` ile başlayan geçerli frontmatter içermeli ve LF satır sonu kullanmalıdır. Sürüm damgası `vYYYYMMDDHHMM` biçiminde olmalı; frontmatter, katalog ve release tag'de aynı değeri taşımalıdır. Mevcut yetenek dosyalarını denetlemek için:

```powershell
Get-ChildItem -Directory | ForEach-Object {
  $skill = Join-Path $_.FullName 'SKILL.md'
  if ((Test-Path $skill) -and ((Get-Content $skill -TotalCount 1) -ne '---')) {
    throw "Frontmatter eksik: $($_.Name)"
  }
}
```

## Sürümleme ve Bakım

- Her yetenek kendi `vYYYYMMDDHHMM` yayın damgasıyla bağımsız sürümlenir; depo genelinde ortak sürüm numarası tutulmaz.
- Damga; `SKILL.md` frontmatter'ı, katalog satırı ve aynı adlı release tag'inde birebir aynı olur; her yayında tag oluşturulup uzak depoya gönderilir.
- Katalog tablosu, dizin içeriğiyle her değişiklikte eşitlenir.
- Değişiklikler tek amaçlı, kısa ve emir kipiyle yazılmış commit mesajlarıyla iletilir.

## Lisans

- Yeteneklerin kullandığı üçüncü taraf bileşenler (örneğin Tailwind CSS, Iconify ve Lucide) kendi lisanslarına tabidir; ayrıntılar ilgili paket lisans dosyalarında yer alır.
- Depo içeriği SP GROUP ENERJİ SAN. VE TİC. LTD. ŞTİ. bünyesinde geliştirilmiştir.

---

© 2026 SP GROUP ENERJİ SAN. VE TİC. LTD. ŞTİ. — info@spgroupenerji.com