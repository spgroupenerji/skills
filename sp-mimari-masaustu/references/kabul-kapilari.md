# Kabul Kapıları

> Gövde §7, §8 ve §9'un ayrıntısı. Kapılar yalnız release veya risk tetikte yüklenir; dev modda hızlı kontrol yeterlidir.

## 1. Mod eşlemesi

| Mod | Ne zaman | Zorunlu kanıt |
| --- | --- | --- |
| Geliştirme (varsayılan) | her değişiklik | `cargo check`, etkilenen testler, katman grep'i |
| Release veya risk | açık yayın isteği ya da risk tetiği | tam zincir: build, test, biçim, lint, paket, ölçüm |

1.2. Risk tetikleri: yetki veya kimlik, veri kaybı, şema göçü, dağıtım ve paketleme, sır işlemleri, güvenlik düzeltmesi.
1.3. Dev modda tam zincir çalıştırılmaz; güvenlik, erişilebilirlik, veri bütünlüğü ve sır değişmezleri yine korunur.

## 2. Geliştirme kapıları

2.1. `cargo check` temiz.
2.2. Değişen davranışın testleri yeşil; kapsam dışı testler bekletilebilir.
2.3. Katman grep'i: `ui/` altında SQL, dosya yazma ve alt süreç yok; `domain/` altında arayüz paketi yok.
2.4. Değişiklik yeni sır veya loga kişisel veri eklemiyor.
2.5. Dev modda ölçüm ve paketleme kapıları çalıştırılmaz; bunlar release kapısıdır.

## 3. Release kapıları

3.1. Derleme ve test: `cargo build --release --locked` ve `cargo test --locked`.
3.2. Biçim ve lint: `cargo fmt --check` ve `cargo clippy -- -D warnings`.
3.3. Bağımlılık: arayüz kiti tek sürüm, ayrı GPUI paketi yok, lisans denetimi temiz.
3.4. Paketleme: betik iki kez çalıştırıldı; çıkış 0, tek artefakt, damga değişmedi, damga Hakkında ile aynı.
3.5. Performans: release ve tam pencere ölçümü; P95 kare süresi bütçe içinde, rapor dağılım içeriyor.
3.6. Erişilebilirlik: ağaç rol, ad ve durum doğruladı; IME ve ekran okuyucu gerçek pencere testi yapıldı.
3.7. Depo hijyeni: `release/` ve `target/` izlenmiyor; sır taraması temiz.
3.8. Platform CI: macOS ve Linux işleri yeşil; eksik sistem bağımlılığı yok.

## 4. Kanıt kaydı

4.1. Her kapı için komut ve sonuç release kaydına yazılır; kanıtsız geçti beyanı kullanılmaz.
4.2. İstisna (ör. GPU'suz CI'da yazılım Vulkan, gerekçeli tam eşzamanlama) kayda geçer; kayıtsız istisna yok.
4.3. Başarısız kapıda yayın durur; kapı atlanmaz, kapsamı daraltılmış geçici istisna yazılı onayla kaydedilir.

## 5. MCP kapıları

5.1. Geliştirme: stdout saflık testi (her stdout satırı geçerli MCP mesajı, log stderr); el sıkışma ve en az bir araç çağrısı; katman grep'i (MCP modülü UI çizim kodu ve doğrudan SQL içermez, `ui/` altında MCP taşıma kodu yok); araç açıklama ve şema gözden geçirmesi.
5.2. Release veya risk: MCP Inspector ile manuel doğrulama (resmî araç, sürümü çalışma anında doğrulanır); istemci matrisi (Claude Desktop, VS Code ve hedeflenen diğer istemcide ilk araç çağrısı); Windows E2E (iki istemci oturumu tek GUI, GUI kapalıyken sidecar hatası, süreç öldürme/yeniden bağlanma, SQLite kilidi); sürüm el sıkışması ve uyuşmazlık reddi; installer sidecar'ı doğru yolda içerir.
5.3. HTTP seçildiyse 127.0.0.1 bağlama, Host/Origin doğrulaması, kimlik doğrulama, istek boyutu ve hız sınırı doğrulanır.
5.4. MCP kapı sonuçları kanıt kaydına yazılır; kanıtsız geçti beyanı yoktur.

## 6. Kapı listesi

- [ ] `cargo build --release --locked` ve `cargo test --locked` yeşil.
- [ ] `cargo fmt --check` ve `cargo clippy -- -D warnings` temiz.
- [ ] Arayüz kiti tek sürüm; ayrı GPUI veya arayüz paketi yok.
- [ ] Lisans taraması yalnız MIT veya Apache-2.0.
- [ ] Paket betiği iki kez: çıkış 0, tek dosya, damga sabit.
- [ ] Damga artefakt adında ve Hakkında sürümünde aynı.
- [ ] FPS ve P95 ölçümü release ve tam pencerede kayıtlı.
- [ ] Erişilebilirlik ağacı ve IME, ekran okuyucu gerçek test kaydı var.
- [ ] Katman grep'i temiz; sır taraması temiz.
- [ ] Platform CI iki iş yeşil; `release/` ve `target/` izlenmiyor.
- [ ] MCP seçildiyse stdout saflık testi geçti (yalnız JSON-RPC, log stderr).
- [ ] El sıkışma/araç testi, istemci matrisi ve sürüm el sıkışması kanıtlandı.
- [ ] Windows E2E (tek GUI, GUI kapalı hata, kill/reconnect, SQLite kilidi) geçti.
