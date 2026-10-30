# MCP Kabul Kapıları

> Gövde §7'nin ayrıntısı. Kapılar yalnız release veya risk tetikte yüklenir; dev modda hızlı kontrol yeterlidir.

## 1. Mod eşlemesi

| Mod | Ne zaman | Zorunlu kanıt |
| --- | --- | --- |
| Geliştirme (varsayılan) | her değişiklik | `cargo check`, etkilenen testler, stdout saflık testi |
| Release veya risk | açık yayın isteği ya da risk tetiği | tam zincir: build, test, biçim, lint, Inspector, istemci matrisi, E2E |

1.2. Risk tetikleri: yetki/kimlik, veri kaybı, silme, dışa gönderme, sır işlemleri, dağıtım, güvenlik düzeltmesi.
1.3. Dev modda tam zincir çalıştırılmaz; güvenlik ve veri bütünlüğü değişmezleri korunur.

## 2. Geliştirme kapıları
2.1. `cargo check` temiz.
2.2. Değişen araç ve köprü davranışının testleri yeşil.
2.3. stdout saflık testi: her stdout satırı geçerli MCP mesajı; loglar stderr'de.
2.4. Katman grep'i: MCP modülü UI çizim kodu ve doğrudan SQL içermez; `ui/` altında MCP taşıma kodu yok.
2.5. Araç açıklamaları ve parametre şemaları gözden geçirildi.
2.6. Değişiklik yeni sır veya loga PII eklemiyor.

## 3. Release ve risk kapıları
3.1. Derleme ve test: `cargo build --release --locked` ve `cargo test --locked`.
3.2. Biçim ve lint: `cargo fmt --check` ve `cargo clippy -- -D warnings`.
3.3. El sıkışma testi: başlatma, araç listeleme, en az bir araç çağrısı, hata yolu.
3.4. MCP Inspector ile manuel doğrulama (resmî araç, sürümü çalışma anında doğrulanır).
3.5. İstemci matrisi: Claude Desktop, VS Code ve hedeflenen diğer istemcide ilk araç çağrısı kanıtlandı.
3.6. Windows E2E: iki istemci oturumu aynı anda tek GUI; GUI kapalıyken sidecar hatası; süreç öldürme ve yeniden bağlanma; SQLite kilit testi.
3.7. Sürüm el sıkışması: uygulama ve sidecar aynı damgada; uyuşmazlık reddi test edildi.
3.8. Paketleme: installer sidecar'ı ve doğru yolu içeriyor; tek artefakt zinciri.
3.9. Sır taraması ve log denetimi temiz.

## 4. Kanıt kaydı
4.1. Her kapı için komut ve sonuç release kaydına yazılır; kanıtsız geçti beyanı yoktur.
4.2. İstisna yazılı gerekçeyle kaydedilir; kayıtsız istisna yoktur.
4.3. Başarısız kapıda yayın durur; kapı atlanmaz.

## 5. Kapı listesi
- [ ] `cargo check` temiz; etkilenen testler yeşil.
- [ ] stdout saflık testi geçti (yalnız JSON-RPC, log stderr).
- [ ] `cargo build --release --locked`, `cargo test --locked`, `cargo fmt --check`, `cargo clippy -- -D warnings` yeşil.
- [ ] El sıkışma ve araç testi uçtan uca geçti.
- [ ] Inspector ve istemci matrisi kanıtlandı.
- [ ] Windows E2E (tek örnek, çok oturum, kill/reconnect, DB kilidi) geçti.
- [ ] Sürüm el sıkışması ve paketleme doğrulandı.
- [ ] Sır ve PII taraması temiz.