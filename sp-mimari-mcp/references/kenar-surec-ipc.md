# Sidecar ve IPC Sözleşmesi

> Gövde §3'ün ayrıntısı. Çerçeve ve süreç kuralları; SDK API'si çalışma anında doğrulanır.

## 1. Sorumluluklar
1.1. Sidecar: stdio MCP yüzeyi, pipe istemcisi, sınırlı yeniden bağlanma, anlaşılır hata. İş mantığı taşımaz.
1.2. GUI: pipe sunucusu, MCP oturumu, araç yürütme, UI köprüsü ve yetki.
1.3. Sidecar stdout'a yalnız MCP mesajı yazar; kendi logu stderr'dedir.
1.4. Sidecar GUI sürecini sahiplenmez; GUI kendi yaşam döngüsünü yönetir.

## 2. Başlatma sırası
2.1. Argümanlar doğrulanır; bilinmeyen argümanda stderr'e Türkçe hata ve sıfır olmayan çıkış.
2.2. Pipe'a sınırlı denemeyle bağlanılır; deneme sayısı, bekleme ve geri çekilme adlandırılmış sabittir.
2.3. El sıkışma: uygulama sürümü, IPC protokol sürümü ve araç manifest özeti.
2.4. Uyuşmazlıkta yazma araçları reddedilir; okuma veya teşhis aracı varsa yalnız o açılır; hata Türkçe ve eyleme dönüktür.
2.5. GUI yoksa anlaşılır hata döndürülür; GUI başlatma ürün kararıysa tek seferlik kilit altında yapılır ve bağlanma sınırlı denenir.
2.6. Hazır olmadan istemciye başarı yanıtı verilmez.

## 3. Çerçeve ve akış
3.1. Pipe üzerinde stdio çerçevesi kullanılır: UTF-8, satır başına tek JSON-RPC mesajı, gömülü yeni satır yok.
3.2. Satır boyutu üst sınırı vardır; aşan mesaj bağlantı hatasıdır, sessiz kesme yoktur.
3.3. Yön: istemci → GUI istek ve bildirimleri; GUI → istemci yanıt ve bildirimleri. Ters yön yoktur.
3.4. İki yön ayrı görevlerde pompalanır; bir yönün hatası diğerini sessizce bırakmaz.
3.5. Pipe yazımı bloklandığında okuma bekletilir; sınırsız tampon yoktur.
3.6. İstek kimliği ve eşleştirme SDK'da kalır; sidecar kimlik üretmez veya yeniden yazmaz.

## 4. Hata ve kapanış
4.1. Pipe koptuğunda sınırlı yeniden bağlanma; başarısızsa stderr log ve sıfır olmayan çıkış.
4.2. GUI araç hatası JSON-RPC hata yanıtı olarak iletilir; sidecar mesajı değiştirmez.
4.3. İstemci stdin'i kapatırsa sidecar pipe'ı kapatır ve temiz çıkar.
4.4. GUI kapanırsa bekleyen çağrılar iptal edilir, istemciye hata döner, sidecar çıkar.
4.5. Süreç öldürme testinde iki tarafta da kalıntı ve asılı çağrı kalmamalıdır.

## 5. Windows süreç hijyeni
5.1. Konsol penceresi açılmaz; GUI ve sidecar pencere göstermez.
5.2. Panik çıktısı stderr'e gider; sessiz çökme yoktur; çıkış kodu anlamlıdır.
5.3. Pipe sunucusu ilk örnek bayrağıyla tek örnek niyetini bildirir; ikinci örnek reddedilir.
5.5. GUI tek örnek kilidi (mutex veya named event) pipe'tan bağımsız korunur; pipe yeniden başlasa da ikinci GUI açılmaz.
5.4. İstemci yapılandırması sidecar'ın derlenmiş exe yolunu gösterir.

## 6. Gözlemlenebilirlik
6.1. stderr yapısal log; seviye ortam değişkeniyle yönetilir.
6.2. Log dosyası kullanılıyorsa boyut ve döndürme sınırı; sır ve PII maskeli.
6.3. Teşhis: bağlantı durumu, son el sıkışma, son hata kodu; istemciye kısa Türkçe özet.

## 7. Kontrol listesi
- [ ] Sidecar stdout'u yalnız MCP mesajı içeriyor (saflık testi).
- [ ] Sürüm el sıkışması ve uyuşmazlık yolu test edildi.
- [ ] Pipe ACL'i aynı kullanıcıyla sınırlı.
- [ ] GUI kapalı, süreç öldürme ve yeniden bağlanma testleri yeşil.