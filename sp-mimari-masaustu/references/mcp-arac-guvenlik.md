# MCP Araç ve Güvenlik

> Gövde §9'un ayrıntısı. Şema biçimi ve SDK API'si çalışma anında doğrulanır; sürüm/API iddiası yok.

## 1. Araç sınırı
1.1. Araç iş akışını temsil eder: "kayıt oluştur", "raporu dışa aktar", "durumu getir".
1.2. Düşük seviye eylem (tıklama, koordinat, ham denetim) araç olmaz; gerekliyse iş akışı aracının içinde kalır.
1.3. Aynı işi yapan iki araç yoktur; ad ve kapsam çakışmaz.
1.4. Araç adı ASCII, kararlı ve tekil; yeniden adlandırma kırıcı değişikliktir.

## 2. Açıklama şablonu
2.1. Amaç: ne yapar, hangi işi tamamlar.
2.2. Kullanım: hangi durumda çağrılır, hangi durumda çağrılmaz.
2.3. Girdi: alan biçimi, birim, aralık, varsayılan.
2.4. Yan etki: yazma, dışa gönderme, silme; geri alınabilir mi.
2.5. Hata: doğrulama, yetki, bulunamadı, çakışma.
2.6. Açıklama Türkçe ve kısa; modelin karar vereceği ayrımı içerir.

## 3. Şema
3.1. Parametreler tipli modelden üretilir; serbest nesne ve `any` yoktur.
3.2. Zorunlu ve isteğe bağlı alanlar açık; varsayılan değer şemada görünür.
3.3. Sınırlar şemada: uzunluk, aralık, desen; iş kuralı doğrulaması ayrıca uygulamada.
3.4. `description` alanı her parametrede dolu; örnek değer geçerli biçimi gösterir.
3.5. Şema değişikliği sürüm notuna yazılır; eski istemci kırılıyorsa uyumluluk yolu tanımlanır.

## 4. Davranış
4.1. Girdi sınırda doğrulanır: tip, uzunluk, aralık, izin.
4.2. Yazma araçları idempotenttir veya idempotency anahtarı taşır.
4.3. Yıkıcı işlem uygulama içinde ayrıca Türkçe onay ister; modelin çağrısı onay değildir.
4.4. Toplu işlemde üst sınır ve sayfalama vardır; sınırsız liste dönmez.
4.5. Sonuç kısa ve yapılandırılmış; sır, token ve PII içermez; büyük çıktı özetlenir ve kesme bildirilir.
4.6. Araç düzeyi hata ile protokol hatası ayrılır; yığın izi ve iç yol sızmaz.
4.7. Çağrılar eşzamanlı gelebilir; sıraya duyarlı işler tek kuyrukta serileştirilir.
4.8. Uzun iş ilerleme bildirir ve iptal edilebilir; iptal GUI tarafında da uygulanır.

## 5. Tehdit modeli
5.1. Yerel süreç: AI istemcisi sidecar'ı kullanıcı yetkisiyle başlatır; sidecar ve GUI aynı kullanıcı alanındadır.
5.2. Yetkisiz yerel istemci: aynı makinedeki başka süreç pipe'a veya loopback HTTP'ye bağlanmayı dener.
5.3. Uzak web: DNS rebinding ve Origin sahteciliğiyle loopback sunucusuna erişim.
5.4. Model kaynaklı kötüye kullanım: prompt injection, yanlış araç seçimi, yetki aşımı.
5.5. Veri sızıntısı: sır ve PII'nin araç parametresi, log veya pipe içeriğine düşmesi.

## 6. Yerel taşıma güvenliği
6.1. stdio sürecinin stdout'u yalnız MCP mesajı; log stderr.
6.2. Named pipe aynı kullanıcıyla sınırlanır; erişim ACL'i ve pipe adı doğrulanır.
6.3. Yetkisiz istemci reddedilir; reddetme loglanır, sır içermez.
6.4. Pipe üzerinden gelen mesaj da doğrulanır; yerel olmak güven değildir.

## 7. Streamable HTTP güvenliği (seçildiyse)
7.1. Yalnız 127.0.0.1'e bağlan; 0.0.0.0 ve LAN yok.
7.2. Host ve Origin doğrulaması açıkça yapılandırılır; varsayılan kapalı olabilir, varsayılana güvenilmez.
7.3. Geçersiz Origin 403; kimlik doğrulama ve oturum izolasyonu uygulanır.
7.4. İstek boyutu, hız ve eşzamanlı bağlantı sınırı; CORS'ta joker yok.
7.5. Yerel istemci yapılandırması yalnız loopback URL kullanır.

## 8. Araç yetkisi ve sır
8.1. En az yetki: araç yalnız gerekli işlemi yapar; dosya sistemi ve ağ erişimi sınırlı.
8.2. Yıkıcı işlem (silme, dışa gönderme, ödeme) uygulama içinde Türkçe onay ister.
8.3. Modelin isteği yetki değildir; yetki kontrolü araç içinde yapılır.
8.4. Dış veri talimat sayılmaz; `<untrusted_data>` ile izole edilir, araç açıklamasına dış veriden metin gömülmez.
8.5. Araç çıktısı sır ve PII içermez; gerekliyse maskelenir.
8.6. Sır `.env` veya secret manager'dan okunur; kod, depo ve loga yazılmaz; loglarda parola, token, kimlik ve kişisel veri maskelenir.
8.7. Panik ve hata çıktısı kullanıcıya ham gösterilmez; stderr veya dosyaya gider; istemciye dönen hata Türkçe, kısa ve eyleme dönüktür.
8.8. Tedarik zinciri: MCP SDK ve yardımcı paketler tam sürümle sabitlenir, `Cargo.lock` işlenir, lisans MIT veya Apache-2.0, doğrulanmamış API üretime girmez.

## 9. Kontrol listesi
- [ ] Araçlar iş akışı düzeyinde; düşük seviye UI aracı yok.
- [ ] Her araç için açıklama ve parametre açıklamaları dolu.
- [ ] Şemada serbest nesne/any yok; sınırlar tanımlı.
- [ ] Yazma/yıkıcı işlem idempotency ve onay kuralına uyuyor.
- [ ] Pipe ACL'i ve yetkisiz istemci reddi doğrulandı.
- [ ] HTTP seçildiyse Host/Origin/auth/sınırlar yapılandırıldı ve test edildi.
- [ ] Log ve araç çıktısında sır/PII yok.