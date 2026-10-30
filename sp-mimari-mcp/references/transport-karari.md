# Taşıma Kararı

> Gövde §2'nin ayrıntısı. SDK adları, sürüm ve feature'lar burada sabitlenmez; seçim ölçütleri ve doğrulama hedefleri yazılır.

## 1. Ölçütler
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

## 5. Karar kaydı ve geri dönüş
5.1. Seçilen taşıma, gerekçe, riskler, geri dönüş adımı ve test kanıtı yazılır.
5.2. Taşıma değişikliği kırıcı değişikliktir; istemci yapılandırması ve sürüm el sıkışması birlikte güncellenir.
5.3. A'dan B'ye geçiş aynı araç yüzeyini korur; araç sözleşmesi taşımadan bağımsızdır.

## 6. Kontrol listesi
- [ ] Tek örnek kuralı taşımada korunuyor.
- [ ] Sidecar sürüm el sıkışması tanımlı ve test edildi.
- [ ] HTTP seçildiyse Host/Origin/kimlik doğrulama açıkça yapılandırıldı.
- [ ] Taşıma ve feature doğrulaması resmî kaynakla yapıldı; sürüm gömülü değil.