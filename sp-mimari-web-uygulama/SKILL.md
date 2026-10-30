---
name: sp-mimari-web-uygulama
description: "Oturumlu, rol tabanlı PHP panel uygulamalarının mimarisini kurar: istek yaşam döngüsü, katman sınırları, oturum/yetki/CSRF, SSR teslimi (sabit sürümlü Tailwind tarayıcı motoru, htmx), MySQL veri katmanı, servis ve dağıtım disiplini. Şu durumlarda kullan: yeni panel modülü, oturum ve yetki akışı, htmx kısmi etkileşim. Kullanma: statik tanıtım sitesi/SEO, yalnız estetik dil, yapısal UI tasarımı, Rust masaüstü, Vite+React SPA + PHP API (sp-mimari-web-spa)."
version: "v202610300440"
---

# sp-mimari-web-uygulama

Oturumlu, rol tabanlı PHP panel uygulamalarının mimari sözleşmesi. Varsayılan mod geliştirmedir: derleme yok, her mikro değişiklikte tam kapı yok; güvenlik, erişilebilirlik, veri bütünlüğü ve sır yönetimi her modda değişmezdir. Statik site mimarisi, estetik dil ve yapısal UI tasarımı kapsam dışıdır; yapısal tasarım sp-dizayn-web-uygulama, estetik dil sp-zen-dizayn alanındadır.

## 0. Ortak çalışma ilkeleri
> Kaynak: AGENTS-tr; ortak blok, bilinçli kopya. Süreç ve araç ayrıntısı: sp-sozlesme 1.3, 2.2 ve §4.

0.1. Öncelik: kullanıcının güncel yazılı talimatı > AGENTS-tr > bu beceri > model genel bilgisi. Çelişkide üstteki kaynak kazanır.
0.2. Mod: varsayılan geliştirmedir; release/prod kapıları yalnız risk sınıfı (oturum, şema, sır, dağıtım) veya açık yayın isteğiyle yüklenir.
0.3. Değişmezler: güvenlik, erişilebilirlik, veri bütünlüğü, sır yönetimi ve Türkçe imlâ her modda korunur; hız veya token için kısaltılmaz.
0.4. Bilgi: sürüm, API ve davranış varsayılmaz; çalışma anında context7 veya resmî kaynaktan doğrulanır; doğrulanamayan bilgi "doğrulanmalı" etiketiyle verilir.
0.5. Araç: işe göre seçilir, gerektiğinde hibrit kullanılır; erişim hatasında tanı (izin, kurulum, indeks, sürüm, yol), basit çözüm, çözülemezse işe başlamadan kullanıcıya bildir (sp-sozlesme 1.3, 2.2, §4).
0.6. Kanıt: kanıtsız "tamamlandı" yoktur; kabul kapıları yalnız release veya risk tetiklediğinde yüklenir (references/kabul-kapilari.md).

## 1. Kapsam ve kimlik

1.1. Bu beceri oturumlu, rol tabanlı PHP panel uygulamalarını bağlar: istek yaşam döngüsü, katman sınırları, oturum/yetki, SSR teslimi, MySQL erişimi, servis katmanı ve dağıtım.
1.2. Kapsam dışı: statik tanıtım/SEO siteleri, estetik dil ve yapısal UI tasarımı; bunlar sp-dizayn-web-uygulama ve sp-zen-dizayn alanındadır. Vite+React SPA + PHP API hedefi sp-mimari-web-spa alanındadır.
1.3. Çalışma zamanı ve bileşen sürümleri çalışma anında doğrulanıp sabitlenir; sürüm ve uzantı envanteri release kaydına geçmeden dağıtım yapılmaz.
1.4. Kimlik üçlüsü zorunludur: sunucu taraflı oturum, tek katalogdan gelen rol, fail-closed denetim kaydı.
1.5. Proje içi belgeler bu becerinin altındadır; çelişen proje belgesi düzeltilmeden release yapılmaz.

## 2. Sunucu, ini, OPcache, sır

2.1. Web kökü tektir; destek, api, sayfa, sidebar, docs, log ve vendor yolları HTTP isteğine kapalıdır ve sunucu yapılandırması bu yollar için 403 döndürür.
2.2. HTTPS release koşuludur; geliştirmede localhost http kabul edilir; TLS sonlandırma dışında HTTP dinlenmez.
2.3. Yapılandırma tek noktadan yönetilir; ortam değişkeni yükleyicisi mevcut değerleri ezmez ve ortam dosyası sürüm dışıdır.
2.4. Sırlar yalnız ortam değişkeni veya secret manager'da tutulur; kod, depo, log ve hata mesajında düz metin sır bulunmaz.
2.5. Üretimde hata gösterimi kapalı, hata loglaması açık ve OPcache etkindir; dağıtım sonrası OPcache temizlenir.
2.6. Loglarda parola, token ve kişisel veri maskelenir; zaman dilimi ve ini farkları tek noktadan yönetilir.
2.7. Ayrıntı: references/php-panel.md, references/kimlik-guvenlik.md.

## 3. İstek yaşam döngüsü ve katman sınırları

3.1. HTTP girişi tek çift giriş noktasından yapılır: sayfa istekleri ve headless API istekleri; başka giriş dosyası yoktur.
3.2. Modül çözümlemesi desen, işleyici dosyası ve sayfa varlığı koşullarıyla yapılır; elle tutulan izinli liste yasaktır; sayfasız modül tek açık listede tanımlanır, listede olmayan istek 400 döner.
3.3. Zincir sırası sabittir: gövde çözümü, desen, dosya kuralı, CSRF, oturum ve zaman aşımı, rol denetimi, denetim kaydı; sıra atlanmaz.
3.4. SQL yalnız DAO/veri katmanında yaşar; controller, sunum kabuğu ve istemci kodunda SQL metni veya PDO çağrısı bulunmaz.
3.5. Sayfa, menü ve rol tanımları tek katalogdan okunur; giriş, API ve sidebar aynı kaynağı kullanır; ikinci kaynak yasaktır.
3.6. Sayfa dosyası ince sunum kabuğudur; iş mantığı destek katmanındadır; yeni modül kabuk, işleyici, katalog kaydı ve istemci sözleşmesi birlikte tamamlanmadan açılmaz.
3.7. Modüle özel mantık çağıran dosyada kalır; iki veya daha fazla modülün paylaştığı yan etkisiz mantık destek altında toplanır; bağımlılık yönü tek yönlüdür.
3.8. Birinci taraf iş mantığında strict_types ve parametre/dönüş tip bildirimleri zorunludur; gerekçesiz mixed reddedilir; adlandırma amacı doğrudan açıklar.
3.9. Boş catch ve hatayı yutan blok yoktur; istisna sınıf, mesaj ve yığın iziyle loglanır; kullanıcıya Türkçe eyleme dönük mesaj gösterilir, iç ayrıntı sızmaz.
3.10. Alan hataları ile sistem hataları ayrı yönetilir; yarım işaret, yoruma alınmış kod ve ölü uç release engelidir; yorum yalnız zorunlu gerekçeyle yazılır.
3.11. Ayrıntı: references/php-panel.md, references/veri-tabani.md.

## 4. Oturum, yetki, CSRF, yükleme

4.1. Oturum sertleştirmesi zorunludur: strict mode, yalnız çerez, httponly, samesite Lax ve HTTPS'te secure; çerez adı proje öneklidir.
4.2. Girişte oturum kimliği yenilenir; hareketsizlik ve mutlak süre tanımlıdır; süre aşımında oturum sunucuda sonlandırılır.
4.3. Parolalar bcrypt (cost en az 12) veya argon2id ile hashlenir; düz metin parola hiçbir katmanda bulunmaz.
4.4. Durum değiştiren her istekte CSRF zorunludur; belirteç hash_equals ile sabit zamanlı doğrulanır; GET, HEAD ve OPTIONS muaftır; eksik veya geçersiz istek 403 döner.
4.5. Yetki rol tabanlıdır ve tek katalogdan gelir; yetkisiz istek 403 döner ve denetim kaydına yazılır.
4.6. Giriş ve parola sıfırlama uçlarında ayrı hız sınırı vardır; eşik aşımı 429 döner.
4.7. Denetim kaydı fail-closed çalışır; denetim yazımı başarısızsa işlem tamamlanmaz.
4.8. Yükleme boyut, MIME ve dosya imzası doğrulanmadan kabul edilmez; istemci dosya adına güvenilmez; yükleme dizini sürüm dışı, script çalıştırmaya kapalı ve yalnız doğrulanmış dosya olarak sunulur.
4.9. Ayrıntı: references/kimlik-guvenlik.md.

## 5. Ön yüz teslimi

5.1. Sayfalar sunucuda render edilmiş HTML olarak teslim edilir; SPA framework, istemci yönlendirici ve sanal DOM yasaktır; tam sayfa gezinme normal bağlantıyla yapılır.
5.2. Stil yalnız sabit sürümlü Tailwind tarayıcı motorundan ve şablondaki text/tailwindcss bloğundaki @theme tokenlarından gelir; derleme, PostCSS, ikinci CSS dosyası ve serbest stil bloğu yoktur.
5.3. htmx yalnız gerekli kısmi etkileşimde kullanılır: liste yenileme, satır içi form, modal içerik; sürüm pinlenir, release'de SRI doğrulanır; kısmi yanıt sunucuda üretilir ve yalnız hedef bölgeyi değiştirir.
5.4. htmx isteklerinin CSRF başlığı tek istemci sözleşmesinden eklenir; modül içinde ikinci başlık kopyası yoktur.
5.5. İstemci sözleşmesi apiIstek, bildirimGoster ve htmlTemizle üzerinden çalışır; modül içi fetch veya kaçış üretimi yasaktır; yakalanmamış hata ve red tek bildirim kanalına bağlanır.
5.6. İstemci varlıkları kendi alan adımızdan sabit sürümle servis edilir; yerel JS ve toplam istemci varlığı için proje bütçesi vardır ve release'de ölçülür.
5.7. İkonlar tek sağlayıcı ve tek önekle Iconify Web Component üzerinden gelir; yükleyici pinlidir ve release'de SRI ile doğrulanır; yerel SVG, sprite, ikon fontu, base64 SVG ve ikinci set yoktur.
5.8. Ayrıntı: references/on-yuz-htmx.md; yapısal UI ve erişilebilirlik ayrıntısı sp-dizayn-web-uygulama alanındadır.

## 6. Servis ve telemetri (koşullu)

6.1. Servis katmanı yalnız panel dışı, uzun süreli veya eşzamanlı iş yükü gerektiğinde kullanılır; asenkron Python ile yazılır; parametre ve dönüş tipleri eksiksizdir, gerekçesiz Any reddedilir.
6.2. Olay döngüsünde bloklayan senkron G/Ç yürütülmez; dosya, soket ve veritabanı erişimi asenkron sürücü veya thread havuzuyla yapılır.
6.3. CPU-yoğun rutinler to_thread veya ProcessPoolExecutor'a devredilir; her dış çağrı katı timeout ile sınırlıdır.
6.4. Her görev için güçlü referans tutulur; iptal yakalanır; soket, kilit ve dosya tanıtıcıları deterministik bırakılır.
6.5. Paylaşılan mutasyon kilitlidir; kilit altında ağ, disk veya uzun hesap yapılmaz; kuyruk ve önbellekler maxsize ile sınırlıdır; doygunlukta deterministik yük atılır ve sayaçla kaydedilir.
6.6. Yeniden deneme tavan sayı, üstel geri çekilme ve rastgele sapma içerir; kalıcı arızada devre kesici devreye girer; loglar JSON yapısal ve trace kimliklidir; sınır verisi katı şemayla doğrulanır.
6.7. Ayrıntı: references/servis-telemetri.md.

## 7. Performans, dağıtım, geri dönüş

7.1. Performans bütçeleri proje kaydında tanımlıdır; release öncesi ölçülür ve kayda geçer; eşik aşımı kök neden giderilmeden kapatılmaz.
7.2. Dağıtım yalnız ff-only merge ile yapılır; force push, geçmiş yeniden yazımı ve ff dışı birleştirme yasaktır.
7.3. Depo kancası HMAC-SHA256 imzası doğrulanmadan çalışmaz; panelden tetiklenen dağıtım yönetici oturumu, POST ve CSRF ister.
7.4. Her dağıtım öncesi geri dönüş commit'i kaydedilir; şema değişikliği göç disiplinine tabidir; dağıtım sırasında elle SQL çalıştırılmaz.
7.5. Dağıtım sonrası OPcache temizlenir ve sağlık kontrolü yapılır; başarısız sağlıkta geri dönüş zorunludur; ortam dosyası ve yükleme dizini üzerine yazılmaz.
7.6. Log ve denetim tek kanaldadır; kanal başına budama tavanı tanımlıdır ve log dizini web'den erişilemez.
7.7. Ayrıntı: references/dagitim.md, references/kabul-kapilari.md.

## 8. Mod sözleşmesi

| Alan | Geliştirme (varsayılan) | Release/prod kapıları |
|---|---|---|
| Ön yüz | Sabit sürümlü Tailwind tarayıcı motoru CDN; derleme yok; localhost'ta SRI/başlık kapısı yok | CSP/HSTS, SRI, gzip bütçesi, Lighthouse |
| Doğrulama | php -l, grep seti, Chrome DevTools | Tüm kabul kapıları ve ölçüm kayıtları |
| Veri | Yerel şema, ölçeklenmiş EXPLAIN | Göç disiplini, yedek/onay, yetki ayrımı |
| Dağıtım | Yok | ff-only, HMAC, rollback kaydı, sağlık kontrolü |
| Değişmez | Oturum/CSRF, yetki, sır, erişilebilirlik, veri bütünlüğü, Türkçe imlâ | Aynı |

8.1. Geliştirmede build ve test zorunlu değildir; her mikro değişiklikte release kapısı çalıştırılmaz.
8.2. Release/risk tetikleyicileri: oturum, CSRF, yetki, şema ve göç, sır, CSP/başlık, dağıtım, silme, açık yayın isteği.
8.3. Risk sınıfı belirsizse en yüksek sınıf varsayılır; kapı atlanmaz, atlanan kapı geçti sayılmaz.

## 9. Sınır ve kabul kapısı

9.1. Sınır: bu beceri panel mimarisini bağlar; statik site mimarisi, estetik dil ve yapısal UI tasarımı kapsam dışıdır.
9.2. Aynı hüküm başka beceride varsa oraya atıf verilir; kopya hüküm üretilmez; süreç ve araç disiplini sp-sozlesme 1.3, 2.2 ve §4'tedir.
9.3. Release kapıları references/kabul-kapilari.md içindedir; her kapı komut veya araç, beklenen sonuç ve tarihle kayda geçer.
9.4. Geliştirme hızlı kontrolü: değişen PHP dosyalarında php -l, statik grep seti, Chrome DevTools Console/Network/Accessibility; bu kontrol tam ölçüm değildir.

- [ ] Etkilenen PHP dosyaları php -l ile hatasız.
- [ ] SQL yalnız DAO katmanında; controller ve istemci kodunda SQL metni veya PDO çağrısı yok.
- [ ] Durum değiştiren isteklerde CSRF var; yetkisiz istek 403 döner ve denetim kaydına yazılır.
- [ ] Release'de CSP/HSTS/SRI ve gzip bütçesi ölçülüp kaydedildi.
- [ ] Release'de göç numaraları boşluksuz, up/down blokları tam; elle ALTER yok.
- [ ] Release'de rollback commit'i, OPcache temizliği ve sağlık kontrolü kayıtlı.

## 10. References

- references/php-panel.md: istek döngüsü, modül çözümlemesi, katman sınırları, tip/adlandırma, hata yönetimi.
- references/kimlik-guvenlik.md: oturum, parola, CSRF, yetki, hız sınırı, denetim, yükleme, sırlar, release başlıkları.
- references/on-yuz-htmx.md: SSR, Tailwind tarayıcı motoru, htmx, istemci sözleşmesi, varlık bütçesi, ikon teslimi.
- references/servis-telemetri.md: asenkron servis, eşzamanlılık, sınırlar, dayanıklılık, yapısal log.
- references/dagitim.md: dağıtım, kanca, panel tetikleme, rollback, dağıtım sonrası kontroller.
- references/veri-tabani.md: PDO, kodlama, şema/indeks, sorgu, transaction, göç, erişim/yedek.
- references/kabul-kapilari.md: geliştirme hızlı kontrolü, release kapıları, kanıt biçimi.
