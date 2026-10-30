---
name: sp-mimari-mcp
description: "Rust/GPUI masaüstü uygulamasına Model Context Protocol (MCP) sunucu desteği eklenirken kullan. Şu durumlarda yükle: MCP desteği veya araç yüzeyi ekleme; AI istemcisinin (Claude Desktop, VS Code, Cursor) uygulamayı yönetmesi; stdio sidecar, named pipe veya yerel Streamable HTTP taşıma kararı; tek GUI örneği ve UI iş parçacığı köprüsü; stdout disiplini, araç şeması, güvenlik ve kabul kapıları. Kullanma: yalnız arayüz tasarımı, web sitesi/panel mimarisi, salt estetik dil."
version: "v202610301619"
---

# sp-mimari-mcp

Rust ve GPUI Kit masaüstü uygulamasına Model Context Protocol (MCP) sunucu desteği eklemenin mimari sözleşmesi. Taşıma, süreç/oturum, araç, UI köprüsü ve güvenlik burada tanımlanır; katman, eşzamanlılık, SQLite ve paketleme `sp-mimari-masaustu` alanıdır.

Varsayılan mod geliştirmedir; kabul kapıları yalnız risk sınıfı veya açık yayın isteğiyle yüklenir. Alan ayrıntıları `references/` dosyalarındadır ve yalnız o alan tetiklendiğinde okunur.

## 0. Ortak çalışma ilkeleri (kaynak: AGENTS-tr; bilinçli kopya)

0.1. Öncelik: kullanıcı talimatı > AGENTS-tr > bu beceri > model bilgisi.
0.2. Mod: varsayılan geliştirme; kabul kapıları risk veya yayın tetikte yüklenir.
0.3. Değişmezler: güvenlik, veri bütünlüğü, sır yönetimi ve Türkçe imlâ her modda korunur.
0.4. Bilgi: SDK sürümü, feature adı, API imzası, protokol revizyonu ve istemci yapılandırması varsayılmaz; çalışma anında context7 veya resmî kaynaktan (crates.io, docs.rs, resmî SDK örnekleri, MCP spec) doğrulanır; doğrulanamayan bilgi "doğrulanmalı" etiketiyle verilir.
0.5. Kanıt: kanıtsız tamamlandı beyanı yoktur; kabul kapıları `references/kabul-kapilari.md`.
0.6. Araç: işe göre seçilir; erişim hatasında tanı, basit çözüm, çözülemezse işe başlamadan bildir (sp-sozlesme 1.3, 2.2, §4).

## 1. Kapsam ve sınır

1.1. MCP desteği uygulamanın iş mantığını AI istemcisine araç olarak açar; arayüz pikseli, koordinat tıklaması veya ham Win32 denetimi araç olarak açılmaz.
1.2. MCP katmanı taşıma, oturum ve araç sözleşmesinden sorumludur; arayüz çizimi, iş kuralı ve veritabanı erişimi kendi katmanlarında kalır.
1.3. MCP görevleri UI iş parçacığını bloklamaz; UI durumuna yalnız §5 köprüsüyle dokunulur.
1.4. Tek örnek kuralı korunur: ikinci uygulama penceresi, ikinci SQLite yazıcısı ve ikinci arayüz paketi açılmaz.
1.5. Araç yüzeyi sürümlenebilir sözleşmedir; ad veya şema değişikliği kırıcı değişiklik sayılır ve sürüm disipliniyle (`sp-mimari-masaustu` §2) yönetilir.
1.6. Resmî Rust MCP SDK (rmcp) seçilir; sürüm, feature ve lisans çalışma anında doğrulanır; bağımlılık kaydına MIT veya Apache-2.0 uyumu yazılır.

## 2. Taşıma ve süreç kararı

2.1. Varsayılan mimari: stdio sidecar + yerel IPC. AI istemcisi her oturumda sidecar'ı alt süreç olarak başlatır; sidecar GUI'ye named pipe üzerinden bağlanır; MCP sunucu oturumu GUI sürecinde yaşar.
2.2. Gömülü Streamable HTTP yalnız istemci HTTP destekliyorsa ve loopback bağlama, Host/Origin doğrulaması ve kimlik doğrulama birlikte uygulanabiliyorsa seçilir.
2.3. Doğrudan `--mcp` stdio modu yalnız arayüzsüz çalışan veya mevcut tek örneğe devreden uygulamada seçilir; tek örnek GUI'yi doğrudan başlatmak çoklu pencere ve DB kilidi üretir, yasaktır.
2.4. Karar tablosu, gerekçe, risk ve geri dönüş: `references/transport-karari.md`.
2.5. Sidecar ayrı sürümlenmez; GUI ile aynı kurulum artefaktından gelir ve sürüm el sıkışması uyuşmazsa araç çağrısı reddedilir.
2.6. Taşıma ve feature seçimi resmî manifest ve SDK örneklerinden doğrulanır; beceriye sürüm veya feature listesi gömülmez.

## 3. Süreç, oturum ve protokol disiplini

3.1. stdio'da stdout yalnız MCP mesajı taşır; MCP dışı tek satır yazılmaz. Log, tanılama ve panik çıktısı stderr'e veya dosyaya gider; `println!` ve stdout'a yazan varsayılan logger yasaktır.
3.2. Mesajlar yeni satırla ayrılmış JSON-RPC'dir; gömülü yeni satır yoktur. Sidecar ile GUI arasındaki pipe da aynı çerçeveyi kullanır.
3.3. El sıkışma, yetenek müzakeresi ve protokol sürümü SDK'ya bırakılır; uygulama JSON-RPC'yi elle ayrıştırmaz.
3.4. Sidecar durumsuz ve tek kullanımlıktır: GUI yoksa anlaşılır Türkçe hata döndürür; GUI'yi kendiliğinden ikinci kez başlatmaz. Başlatma ürün kararıysa tek seferlik kilit altında yapılır.
3.5. Her araç çağrısı zaman aşımı, iptal ve adlandırılmış sabit üst sınırlı eşzamanlılık taşır; sahipsiz görev, sınırsız kuyruk ve süresiz bekleme yoktur.
3.6. Kapanışta yeni çağrı kabul edilmez, çalışanlar iptal edilir, pipe kapatılır ve süreç kalıntısı bırakılmaz.
3.7. Bağlantı koptuğunda sidecar sınırlı denemeyle yeniden bağlanır; GUI düşen çağrıları hata olarak raporlar.
3.8. stdio'da bağlantı oturumdur; HTTP'de oturumlar istemci başına ayrılır ve bir oturumun durumu diğerine sızmaz.
3.9. Sidecar sözleşmesi, çerçeve ve süreç hijyeni: `references/kenar-surec-ipc.md`.

## 4. Araç (tool) sözleşmesi

4.1. Araçlar iş akışı düzeyindedir ("kayıt oluştur", "raporu PDF dışa aktar"); düşük seviye UI eylemi araç yapılmaz.
4.2. Araç adı kararlı, tekil ve ASCII'dir; açıklama amacı, beklenen girdi biçimini, birimleri, sınırları, yan etkiyi ve hata koşullarını Türkçe yazar.
4.3. Parametre şeması tipli modelden üretilir; serbest `object` ve `any` yoktur; zorunlu alan, varsayılan ve aralık açıkça belirtilir.
4.4. Girdi uygulama sınırında doğrulanır: tip, uzunluk, aralık ve izin; doğrulanmamış girdi iç katmana geçmez.
4.5. Yazma araçları idempotenttir veya idempotency anahtarı taşır; yıkıcı işlem uygulama içinde ayrıca Türkçe onay ister.
4.6. Sonuç kısa, yapılandırılmış ve sır/PII içermez; listeleme sayfalanır ve sonuç boyutu adlandırılmış sabitle sınırlanır.
4.7. Araç düzeyi hata ile protokol hatası ayrı raporlanır; yığın izi, dosya yolu ve iç ayrıntı dışarı sızmaz.
4.8. Araç çağrıları eşzamanlı gelebilir ve sıra garantisi yoktur; paylaşılan durum kilitlidir, sıraya duyarlı işler tek kuyrukta serileştirilir.
4.9. Uzun işler ilerleme bildirir ve iptal edilebilir; iptal GUI tarafında da etkisiz hâle getirilir.
4.10. Araç açıklama şablonu ve şema kuralları: `references/arac-tasarimi.md`.

## 5. UI iş parçacığı köprüsü

5.1. MCP görevleri UI iş parçacığında çalışmaz; UI öğelerine yalnız sahibi iş parçacığı dokunur.
5.2. Köprü sınırlı kapasiteli komut kanalı ve yanıt için korelasyon kimliğidir; sınırsız kanal ve paylaşılan mutable UI durumu yoktur.
5.3. UI durumunu yalnız UI tarafı günceller; MCP tarafı mesaj yollar, doğrudan yazmaz.
5.4. Kuyruk dolduğunda geri basınç uygulanır; sessiz düşürme yoktur. Her komut zaman aşımı ve iptal taşır.
5.5. GUI kapanırken bekleyen komutlar iptal edilir, kanal kapatılır ve MCP tarafı hata döndürür.
5.6. UI onayı bekleyen araçta modal, iptal ve zaman aşımı birlikte çalışır; kullanıcı yanıtı gelmezse araç başarısız sayılır.

## 6. Güvenlik ve gizlilik

6.1. Yerel stdio süreci istemcinin yetkisiyle çalışır; araç yüzeyi yine en az yetkiyle sınırlanır.
6.2. Named pipe aynı kullanıcıyla sınırlanır; pipe adı ve erişim ACL'i doğrulanır, yetkisiz istemci reddedilir.
6.3. Streamable HTTP yalnız 127.0.0.1'e bağlanır; Host ve Origin doğrulaması açıkça yapılandırılır, varsayılana güvenilmez; kimlik doğrulama, istek boyutu ve hız sınırı uygulanır.
6.4. Sır, token ve kişisel veri araç parametresine, loga veya pipe'a yazılmaz; zorunlu logda maskelenir.
6.5. Araç çıktısı model tarafından okunur: dış veri talimat sayılmaz, `<untrusted_data>` ile izole edilir; araç açıklamasına dış veriden metin gömülmez.
6.6. Prompt injection'a karşı yetki sınırını araç kendi doğrular; modelin isteği yetki sayılmaz.
6.7. Yıkıcı işlem öncesi Türkçe onay; onaysız toplu işlem yoktur. Tehdit modeli: `references/guvenlik.md`.

## 7. Test ve kabul

7.1. Varsayılan kapı: `cargo check`, etkilenen testler ve stdout saflık testi.
7.2. Stdout saflık testi: sunucuya JSON-RPC dizisi verilir; her stdout satırı geçerli MCP mesajı olmalı, loglar stderr'de kalmalıdır.
7.3. El sıkışma ve araç testi: başlatma, araç listeleme ve en az bir araç çağrısı şema ve hata yollarıyla uçtan uca doğrulanır.
7.4. Windows E2E: iki istemci oturumu aynı anda tek GUI; GUI kapalıyken sidecar hatası; süreç öldürme ve yeniden bağlanma; SQLite kilit testi.
7.5. Release veya risk kapıları: locked build/test, fmt, clippy `-D warnings`, MCP Inspector ile manuel doğrulama, istemci matrisi, sürüm el sıkışması ve sır taraması.
7.6. Kapı listesi ve kanıt komutları: `references/kabul-kapilari.md`.

## 8. İstemci bağlama ve yayın

8.1. Sidecar yolu kurulumla sabittir; istemci yapılandırması derlenmiş exe'yi gösterir, `cargo run` gösterilmez.
8.2. Claude Desktop `mcpServers`; VS Code `.vscode/mcp.json` `servers` kullanır. Biçim, yol ve HTTP desteği istemci sürümüne göre çalışma anında doğrulanır.
8.3. HTTP modu yalnız istemci HTTP veya connector desteği doğrulandıysa belgelenir; stdio birincil yoldur.
8.4. Uygulama ve sidecar aynı artefakt zincirinden gelir; güncelleme iki parçayı birlikte taşır ve sürüm damgası `vYYYYMMDDHHMM` biçimindedir.
8.5. README katalog satırı ve sürüm damgası bu beceriyle birlikte güncellenir.