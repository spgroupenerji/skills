# MCP Taşıma ve IPC

> Gövde §9'un ayrıntısı. SDK adları, sürüm ve feature'lar burada sabitlenmez; seçim ölçütleri ve doğrulama hedefleri yazılır.

## 1. Taşıma ölçütleri
1.1. Tek örnek: uygulama aynı anda tek pencere ve tek SQLite yazıcısı olmalı.
1.2. İstemci desteği: hedef istemcilerde stdio varsayılan; HTTP veya connector desteği istemci ve sürüme göre değişir.
1.3. Dağıtım: ek sidecar binary kabul edilebilir mi; tek exe şartı var mı.
1.4. Güvenlik: yerel yetki, pipe ACL, Host/Origin doğrulaması, kimlik doğrulama.
1.5. Gecikme ve yük: UI bloklama, kuyruk, eşzamanlılık sınırı.
1.6. Bakım: sürüm eşleşmesi, test yüzeyi, geri dönüş maliyeti.
1.7. Ölçüt ağırlığı ürün kararıdır; karar kaydı gerekçeyle yazılır.

## 2. A. stdio sidecar + named pipe (varsayılan)
2.1. Akış: AI istemcisi → sidecar (stdio, satır bazlı JSON-RPC) → named pipe → GUI (MCP sunucu).
2.2. Sidecar yalnız taşır; araç yüzeyi, iş mantığı ve yetki GUI'dedir.
2.3. Kazanç: istemci oturumu başına yeni GUI açılmaz; UI iş parçacığı bloklanmaz; stdio destekleyen tüm istemciler çalışır; ağ yüzeyi oluşmaz.
2.4. Bedel: ikinci binary, sürüm el sıkışması, pipe erişim denetimi, süreç temizliği.
2.5. Reddetme: iş mantığını sidecar'a kopyalamak; pipe'ı kimlik doğrulamasız bırakmak; sidecar'ın GUI'yi sahiplenmesi.
2.6. Doğrulama hedefi: SDK'nın async bayt akışı taşıması ve resmî named-pipe örneği; Windows'ta tek örnek davranışı.

## 3. B. Gömülü Streamable HTTP (loopback)
3.1. Tek süreç ve tek exe; GUI çalışırken istemci URL ile bağlanır.
3.2. Zorunlu: yalnız 127.0.0.1 bağlama; Host ve Origin doğrulaması açıkça; kimlik doğrulama; istek boyutu ve hız sınırı; oturum izolasyonu.
3.3. Risk: istemci matrisi (Claude Desktop connector arayüzü, VS Code HTTP, Cursor sürümü), port çakışması, yanlış yapılandırmada uzaktan erişim.
3.4. Seçim: istemci HTTP destekliyorsa ve tek exe şartı varsa.
3.5. Doğrulama hedefi: SDK streamable HTTP sunucu feature'ı, Host/Origin yapılandırma alanları ve spec güvenlik zorunlulukları.

## 4. C. Doğrudan `--mcp` stdio (GUI exe)
4.1. Yalnız arayüzsüz veya tek oturum; GUI açan süreç istemci oturumu başına çoğalır.
4.2. GUI tek örnek şartsa bu mod ancak ikinci süreç mevcut örneğe devrediyorsa geçerlidir; aksi hâlde A'ya dönülür.
4.3. Doğrulama: ikinci başlatmada pencere ve DB çoğalmıyor mu; çıkış kodu ve stderr anlaşılır mı.

## 5. Sidecar ve IPC sözleşmesi
5.1. Sorumluluk: sidecar stdio MCP yüzeyi, pipe istemcisi, sınırlı yeniden bağlanma ve anlaşılır hata taşır; iş mantığı taşımaz. GUI pipe sunucusu, MCP oturumu, araç yürütme, UI köprüsü ve yetkiyi taşır.
5.2. Sidecar stdout'a yalnız MCP mesajı yazar; kendi logu stderr'dedir; GUI sürecini sahiplenmez.
5.3. Başlatma: argüman doğrula; pipe'a sınırlı denemeyle bağlan (deneme, bekleme, geri çekilme adlandırılmış sabit); uygulama sürümü, IPC protokol sürümü ve araç manifest özetiyle el sıkış.
5.4. Uyuşmazlıkta yazma araçları reddedilir; okuma veya teşhis aracı varsa yalnız o açılır; hata Türkçe ve eyleme dönüktür.
5.5. GUI yoksa anlaşılır hata döndürülür; GUI başlatma ürün kararıysa tek seferlik kilit altında yapılır ve bağlanma sınırlı denenir; hazır olmadan başarı yanıtı verilmez.
5.6. Çerçeve: pipe üzerinde stdio çerçevesi (UTF-8, satır başına tek JSON-RPC, gömülü satır yok); satır boyutu üst sınırı; aşan mesaj bağlantı hatası.
5.7. Yön: istemci → GUI istek/bildirim; GUI → istemci yanıt/bildirim; ters yön yok. İki yön ayrı görevlerde pompalanır; bir yönün hatası diğerini sessizce bırakmaz.
5.8. Pipe yazımı bloklandığında okuma bekletilir; sınırsız tampon yoktur; istek kimliği SDK'da kalır, sidecar yeniden yazmaz.
5.9. Hata/kapanış: pipe kopunca sınırlı yeniden bağlanma, başarısızsa stderr log ve sıfır olmayan çıkış; GUI araç hatası JSON-RPC hata yanıtı olarak iletilir; stdin EOF'ta pipe kapanır ve temiz çıkılır; GUI kapanınca bekleyen çağrılar iptal edilir.
5.10. Süreç öldürme testinde iki tarafta da kalıntı ve asılı çağrı kalmamalıdır.
5.11. Windows hijyeni: konsol penceresi açılmaz; panik çıktısı stderr'e; çıkış kodu anlamlı; pipe sunucusu ilk örnek bayrağıyla tek örnek niyetini bildirir; GUI tek örnek kilidi pipe'tan bağımsız korunur.
5.12. İstemci yapılandırması sidecar'ın derlenmiş exe yolunu gösterir.
5.13. Gözlemlenebilirlik: stderr yapısal log, seviye ortam değişkeniyle; log dosyasında boyut/döndürme sınırı ve sır/PII maskesi; istemciye kısa Türkçe teşhis.

## 6. Kontrol listesi
- [ ] Tek örnek kuralı taşımada korunuyor.
- [ ] Sidecar sürüm el sıkışması tanımlı ve test edildi.
- [ ] stdout saflık testi geçti (yalnız MCP mesajı, log stderr).
- [ ] HTTP seçildiyse Host/Origin/kimlik doğrulama açıkça yapılandırıldı.
- [ ] GUI kapalı, süreç öldürme ve yeniden bağlanma testleri yeşil.
- [ ] Taşıma ve feature doğrulaması resmî kaynakla yapıldı; sürüm gömülü değil.