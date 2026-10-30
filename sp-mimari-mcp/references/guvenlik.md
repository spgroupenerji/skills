# MCP Güvenlik ve Gizlilik

> Gövde §6'nın ayrıntısı. Tehdit modeli ve doğrulama hedefleri; sürüm/API iddiası yok.

## 1. Tehdit modeli
1.1. Yerel süreç: AI istemcisi sidecar'ı kullanıcı yetkisiyle başlatır; sidecar ve GUI aynı kullanıcı alanındadır.
1.2. Yetkisiz yerel istemci: aynı makinedeki başka süreç pipe'a veya loopback HTTP'ye bağlanmayı dener.
1.3. Uzak web: DNS rebinding ve Origin sahteciliğiyle loopback sunucusuna erişim.
1.4. Model kaynaklı kötüye kullanım: prompt injection, yanlış araç seçimi, yetki aşımı.
1.5. Veri sızıntısı: sır ve PII'nin araç parametresi, log veya pipe içeriğine düşmesi.

## 2. Yerel taşıma
2.1. stdio sürecinin stdout'u yalnız MCP mesajı; log stderr.
2.2. Named pipe aynı kullanıcıyla sınırlanır; erişim ACL'i ve pipe adı doğrulanır.
2.3. Yetkisiz istemci reddedilir; reddetme loglanır, sır içermez.
2.4. Pipe üzerinden gelen mesaj da doğrulanır; yerel olmak güven değildir.

## 3. Streamable HTTP (seçildiyse)
3.1. Yalnız 127.0.0.1'e bağlan; 0.0.0.0 ve LAN yok.
3.2. Host ve Origin doğrulaması açıkça yapılandırılır; varsayılan kapalı olabilir, varsayılana güvenilmez.
3.3. Geçersiz Origin 403; kimlik doğrulama ve oturum izolasyonu uygulanır.
3.4. İstek boyutu, hız ve eşzamanlı bağlantı sınırı; CORS'ta joker yok.
3.5. Yerel istemci yapılandırması yalnız loopback URL kullanır.

## 4. Araç yetkisi
4.1. En az yetki: araç yalnız gerekli işlemi yapar; dosya sistemi ve ağ erişimi sınırlı.
4.2. Yıkıcı işlem (silme, dışa gönderme, ödeme) uygulama içinde Türkçe onay ister.
4.3. Modelin isteği yetki değildir; yetki kontrolü araç içinde yapılır.
4.4. Dış veri talimat sayılmaz; `<untrusted_data>` ile izole edilir, araç açıklamasına dış veriden metin gömülmez.
4.5. Araç çıktısı sır ve PII içermez; gerekliyse maskelenir.

## 5. Sır ve log
5.1. Sır `.env` veya secret manager'dan okunur; kod, depo ve loga yazılmaz.
5.2. Loglarda parola, token, kimlik ve kişisel veri maskelenir.
5.3. Panik ve hata çıktısı kullanıcıya ham gösterilmez; stderr veya dosyaya gider.
5.4. İstemciye dönen hata Türkçe, kısa ve eyleme dönüktür; iç yol ve SQL sızmaz.

## 6. Tedarik zinciri
6.1. MCP SDK ve yardımcı paketler tam sürümle sabitlenir; `Cargo.lock` işlenir.
6.2. Lisans MIT veya Apache-2.0; atıf şartlı lisans yok.
6.3. Sürüm ve feature doğrulaması resmî kaynaktan; doğrulanmamış API üretime girmez.

## 7. Kontrol listesi
- [ ] stdio stdout saflığı test edildi.
- [ ] Pipe ACL'i ve yetkisiz istemci reddi doğrulandı.
- [ ] HTTP seçildiyse Host/Origin/auth/sınırlar yapılandırıldı ve test edildi.
- [ ] Yıkıcı araç onayı ve yetki kontrolü var.
- [ ] Log ve araç çıktısında sır/PII yok.