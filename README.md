# SP GROUP Skill Kütüphanesi

SP GROUP projelerinde kullanılan ajan yeteneklerinin (skill) tek deposu. Her yetenek kendi dizininde bir `SKILL.md` dosyasıyla tanımlanır; `description` alanındaki tetikleyicilerle Claude Code, Cursor, Windsurf, Codex CLI, DeepSeek Harness (DSH) ve MCP host platformlarında otomatik yüklenir. Depoya zamanla yeni yetenekler eklenir; katalog ve kurallar bu belgede güncel tutulur.

## Özellikler

- Yetenek başına tek dizin ve tek `SKILL.md`; derleme, paketleme veya servis bağımlılığı yoktur
- `description` tetikleyicileriyle otomatik yüklenen, platformdan bağımsız yetenek tanımları
- Tek katalog tablosu ve yeni yetenek ekleme kuralları ile ölçeklenen depo düzeni
- Kopyala-çalıştır kurulum; yetenek dizinleri platformun yetenek klasörüne kopyalanır
- Türkçe imla ve ASCII uyumlu Türkçe kod isimlendirmesi standardı
- Git üzerinde LF satır sonu politikası (`.gitattributes`); Windows'ta CRLF karışması önlenir
- Güvenli varsayılanlar: depoya secret girmez, dış veri talimat olarak yürütülmez

## Yetenek Kataloğu

| Yetenek | Sürüm | Kapsam |
| --- | --- | --- |
| [`kural-hatirlatici`](kural-hatirlatici/SKILL.md) | v202610282031 | Kullanıcının kalıcı çalışma direktiflerini ve tek kuyruk iş akışını her görevde hatırlatan başlangıç skili; araç disiplini, kanıt, Chrome DevTools doğrulaması, push/deploy/webhook ve kapanış senkronu |
| [`zen-mimari-anayasa`](zen-mimari-anayasa/SKILL.md) | v202610281847 | Kıdemli yazılım mimarı anayasası; zero-build Tailwind/Iconify arayüzleri, Zen Katmanı ilkeleri, MCP yetenek mühendisliği ve 10 maddelik QA matrisi |

Yeni yetenek eklendiğinde bu tabloya satır eklenir. Tablo, depodaki yeteneklerin tek doğruluk kaynağıdır.

## Kurulum

Yetenekler derleme gerektirmez; ilgili dizin platformun yetenek klasörüne kopyalanır. Depo kökünden tek yetenek kurulumu:

```powershell
Copy-Item -Recurse -Force zen-mimari-anayasa "$HOME/.dsh/skills/"
```

Tüm yetenekleri tek seferde kurmak için:

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

- `kural-hatirlatici`: görev başında, kodlama/refaktör/hata ayıklama öncesinde ve "kuralları hatırlat" dendiğinde devreye girer; kullanıcının kalıcı direktiflerini ve araç kuyruğunu hatırlatır. Ayrıntı [SKILL.md](kural-hatirlatici/SKILL.md) dosyasındadır.
- `zen-mimari-anayasa`: SCADA paneli, zero-build Tailwind arayüzü, MCP yeteneği veya refaktör isteğinde devreye girer. Ayrıntılı anayasa [SKILL.md](zen-mimari-anayasa/SKILL.md) dosyasındadır.

## Yeni Yetenek Ekleme

1. `kebab-case` adlı yeni bir dizin oluşturun ve içine `SKILL.md` ekleyin.
2. Frontmatter'ı aşağıdaki iskeletle tanımlayın:

```yaml
---
name: yetenek-adi
description: "Tetikleyici koşulları anlatan kısa açıklama"
version: "vYYYYMMDDHHMM"
alwaysApply: false
platforms:
  - CLAUDE_CODE
  - CURSOR
  - WINDSURF
  - CODEX_CLI
  - MCP_HOST
tags:
  - kategori
allowed-tools:
  - context7
---
```

3. `description` yalnızca tetikleyici koşulları anlatsın; yeteneğin iş akışını özetlemesin.
4. Sürümü yayın anının `vYYYYMMDDHHMM` damgasıyla yönetin; damga frontmatter, katalog ve release tag'de birebir aynı olsun.
5. Yeteneği yukarıdaki kataloğa alfabetik sıraya göre ekleyin.
6. Araç kullanım mekaniğini yazma: yalnızca araç adını ve doğrulama hedefini belirt; çağrı protokolünü, fonksiyon adlarını ve parametreleri ajanın çalışma zamanına bırak.
7. Teslim öncesi Doğrulama bölümündeki komutları çalıştırın.

## Depo Yapısı

| Yol | İçerik |
| --- | --- |
| `<yetenek-adı>/SKILL.md` | Yetenek tanımı (frontmatter ve yönerge) |
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
