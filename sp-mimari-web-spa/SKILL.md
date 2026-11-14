---
name: sp-mimari-web-spa
description: "Vite ile derlenen React SPA'nın (istemci yönlendirme) LiteSpeed üzerinde PHP REST API ile mimarisini kurar: kök yayını (derleme çıktısı depo kökünde, kaynak spa/ altında), GitHub kancasıyla git çekme dağıtımı, /api/* yönlendirmesi, aynı origin oturum ve CSRF, sözleşme-önce API, süreklilik ve release kapıları. Şu durumlarda kullan: React SPA + PHP API kurulumu, SPA yönlendirme/derin bağlantı sorunu, API sözleşmesi ve dağıtımı. Kullanma: SSR panel, statik/SEO site, salt estetik dil; bu alanlarda yüklenmez."
version: "v202611140552"
---

# sp-mimari-web-spa

Vite ile derlenen React SPA ve LiteSpeed üzerinde PHP REST API mimarisinin sözleşmesi: istemci yönlendirme, kökten yayınlanan derlenmiş dosyalar ve git kancasıyla otomatik dağıtım, aynı origin güvenlik, sözleşme-önce API ve mevcut sistemle süreklilik. Varsayılan mod geliştirmedir; güvenlik, erişilebilirlik, veri bütünlüğü ve sır yönetimi her modda değişmezdir.

## 0. Ortak çalışma ilkeleri
> Kaynak: anayasa; ortak blok, bilinçli kopya. Süreç ve araç ayrıntısı: sp-orkestra 3.4 ve 4.

0.1. Öncelik: kullanıcının güncel yazılı talimatı > anayasa > bu beceri > model genel bilgisi. Çelişkide üstteki kaynak kazanır.
0.2. Mod: varsayılan geliştirmedir; release/prod kapıları yalnız risk sınıfı (oturum, API sözleşmesi, env/secret, yönlendirme, dağıtım) veya açık yayın isteğiyle yüklenir.
0.3. Değişmezler: güvenlik, erişilebilirlik, veri bütünlüğü, sır yönetimi ve Türkçe imlâ her modda korunur; hız veya token için kısaltılmaz.
0.4. Bilgi: sürüm, API ve davranış varsayılmaz; çalışma anında context7 veya resmî kaynaktan doğrulanır; doğrulanamayan bilgi "doğrulanmalı" etiketiyle verilir.
0.5. Araç: işe göre seçilir, gerektiğinde hibrit kullanılır; erişim hatasında tanı (izin, kurulum, indeks, sürüm, yol), basit çözüm, çözülemezse işe başlamadan kullanıcıya bildir (sp-orkestra 3.4, 4).
0.6. Kanıt: kanıtsız "tamamlandı" yoktur; kabul kapıları yalnız release veya risk tetiklediğinde yüklenir (references/kabul-kapilari.md).
0.7. Yayın anında: çıktıyı depo köküne üret, commit'le, push'la; GitHub kancası `git merge --ff-only` ile çeker; canlıyı Chrome DevTools ile kontrol et; kanca çekmiyorsa yayın kapanmaz (references/webhook-dagitim.md).
0.8. Kimlik: deploy sonrası verilen kalıcı giriş bilgisi yalnız yerel secret deposunda (.env / işletim sistemi kimlik kasası) tutulur; kalıcı bellekte yalnız referansı saklanır; depoya, kitaba, uzağa ve loga yazılmaz; sonraki oturumda tekrar sorulmaz.

## 1. Kapsam ve sınır

1.1. Bu beceri Vite ile derlenen React SPA'yı ve LiteSpeed üzerindeki PHP REST API'yi bağlar: derleme, dağıtım, yönlendirme, oturum/CSRF, sözleşme ve süreklilik.
1.2. Çalışma zamanı modeli istemci yönlendirmeli SPA'dır; sunucu yalnız kökten yayınlanan derlenmiş dosyaları (kök `index.html`, `varlik/`) ve /api/* PHP yanıtını verir.
1.3. Kapsam dışı: SSR zero-build PHP panel (sp-mimari-web-uygulama), statik/SEO site (sp-mimari-web-site), salt estetik dil (sp-zen-dizayn), yapısal UI tasarımı (sp-dizayn-web-uygulama).
1.4. SSR panelde SPA yasaktır; SPA modeli ayrı yüzey veya proje içindir; iki teslim modeli aynı yüzeyde karıştırılmaz.
1.5. Yapısal UI ve erişilebilirlik sp-dizayn-web-uygulama alanındadır; o becerinin zero-build/htmx teslim bölümü SPA'da uygulanmaz, build ve teslim mekaniği bu beceridedir.
1.6. Çelişkide öncelik: kullanıcı talimatı > anayasa > platform mimari becerisi > tasarım becerisi > estetik dil; SPA teslim mekaniğinde bu beceri mimari katmandır.

## 2. Model ve dağıtım

2.1. Node yalnız derleme zamanındadır; üretimde Node çalışmaz, çalışma zamanı PHP ve statik dosyalardır.
2.2. Yayın yüzeyi depo köküdür: derleme çıktısı doğrudan kök `index.html` ve kök `varlik/` dizinine yazılır. Sunucu derleme yapmaz, yalnız commit'i çeker; bu yüzden çıktı depoda olmak zorundadır.
2.3. Kaynak `spa/` altındadır ve Vite kökü orasıdır; kök `index.html` yalnız derleme çıktısıdır, kaynak girişi `spa/index.html`'dir. İki giriş aynı yola yazılmaz.
2.4. `varlik/` ayrılmış çıktı dizinidir: yalnız build yazar, elle dosya konmaz, kaynakta aynı ad kullanılmaz; yayın adımı dizini silip yeniden üretir.
2.5. `build.emptyOutDir` açıkça `false` olur; kök dizin hiçbir koşulda boşaltılmaz (Vite davranışı: kök dışı hedefte varsayılan `false`, açık değer uyarıyı da kapatır).
2.6. Kökte tek giriş `index.html`'dir; PHP giriş noktası `/api/` altındadır, kökte `index.php` ile birlikte yayınlanmaz.
2.7. Yayın tek komuttur (`npm run yayin`): `varlik/` silinir, build çalışır, kaynak ve kök çıktı birlikte stage edilir; elle dosya kopyalanmaz.
2.8. Kütüphaneler npm ile kurulur; CDN'den script, stil veya font yüklenmez.
2.9. lockfile sürüm kontrolündedir; kurulum lockfile'a göre yapılır; yeni bağımlılık gerekçelenir ve pinlenir.
2.10. Build yeniden üretilebilir: aynı lockfile ve komut aynı çıktıyı verir; yayın çıktısı (kök `index.html` + `varlik/`) depoda tutulur ve tek doğruluk kaynağıdır; git yedeği, cPanel kopyası ve rollback hedefi aynı commit'tir.
2.11. Build-time ortam değişkenleri yalnız kamuya açık değerleri taşır; sır istemci paketine gömülmez, API anahtarları PHP tarafındadır.
2.12. Node, Vite, React ve PHP sürümleri çalışma anında resmî kaynaktan doğrulanır; beceriye sürüm yazılmaz.
2.13. Ayrıntı: references/vite-derleme.md ve references/webhook-dagitim.md.
2.14. Stil kaynağı build'e girer: seçilen stil çözümü proje kaydında tanımlanır ve sürümü doğrulanır; CDN stil veya script yoktur.

## 3. Yönlendirme

3.1. LiteSpeed'de /api/* PHP API girişine, diğer tüm yollar index.html'e yönlenir (SPA fallback).
3.2. Derin bağlantılar 200 döner; fallback yalnız GET ve HEAD ile var olmayan yollar için çalışır; durum değiştiren metotlar fallback'e düşmez.
3.3. Gerçek statik varlık isteği fallback'e düşmez; eksik varlık 404 döner ve HTML ile karşılanmaz.
3.4. Bilinmeyen /api/* yolu PHP tarafında JSON 404 döner; HTML fallback'e düşmez.
3.5. İstemci yönlendirici geçmiş tabanlıdır; sunucu fallback kuralı istemci yol listesiyle uyumludur; yollar tek kaynaktan tanımlanır.
3.6. index.html önbelleklenmez; hash'li varlıklar uzun ömürlü önbellekle sunulur; fallback yanıtı kullanıcıya özel veri taşımaz.
3.7. Ayrıntı: references/litespeed-yonlendirme.md.

## 4. Güvenlik

4.1. React ve API aynı alan adındadır (dijital.<alanadi>); CORS yapılandırılmaz, same-origin dışı istemci kabul edilmez.
4.2. Oturum çerezi HttpOnly, Secure ve SameSite ile ayarlanır; girişte oturum kimliği yenilenir; her korumalı API isteği oturumu sunucuda doğrular.
4.3. CSRF: durum değiştiren her istekte belirteç zorunludur; belirteç oturuma bağlıdır, başlıkla taşınır ve sabit zamanlı doğrulanır; eksik veya geçersiz belirteç 403 döner.
4.4. Girdi doğrulama sunucuda zorunludur; istemci doğrulaması yalnız deneyim içindir; şema dışı gövde 400 veya 422 döner.
4.5. Hata kodları ayrışır: oturum yok 401, yetki yok 403, doğrulama 422, bulunamadı 404; gövde iç ayrıntı sızdırmaz.
4.6. Sırlar yayın çıktısına girmez; istemciye gömülen değerler kamuya açıktır, sunucu sırları ortam değişkeninden gelir.
4.7. Tedarik zinciri: lockfile, pinli sürüm, lockfile'a göre kurulum, yeni bağımlılık gerekçesi ve denetim; CDN ve doğrulanmamış kaynak yoktur.
4.8. Release başlıkları: CSP script-src self, unsafe-inline ve unsafe-eval yok; HSTS, nosniff ve Referrer-Policy eksiksizdir; değerler release'de resmî kaynaktan doğrulanır.
4.9. Kaynak dizini `spa/` ve `deploy/.env` gibi çalışma dosyaları web'den erişilemez (.htaccess deny); kökte yalnız yayın çıktısı servis edilir.
4.10. Ayrıntı: references/guvenlik-oturum.md.

## 5. API sözleşmesi

5.1. Her uç için metot, yol, girdi şeması, çıktı şeması ve hata kodları önce yazılır; istemci ve sunucu bu sözleşmeden üretilir.
5.2. Tek zarf biçimi kullanılır: başarı verisi; hata kodu, mesaj ve alan listesi; HTTP durumu ile uygulama kodu uyumludur.
5.3. İstemci sözleşmeden tiplenir; any yoktur; cevaplar çalışma anında doğrulanır; iş kuralı istemcide tekrarlanmaz.
5.4. Sürümleme açıktır (yol veya başlık); kırıcı değişiklik yeni sürümle gelir; eski sürümün kaldırılması kayda geçer.
5.5. Sözleşme testleri her uç için başarı ve hata durumlarını kapsar; şema doğrulaması testin parçasıdır.
5.6. Sayfalama, filtre ve idempotency anahtarı ortak sözleşmede tek kez tanımlanır.
5.7. Ayrıntı: references/api-sozlesmesi.md.

## 6. Süreklilik

6.1. Mevcut MySQL şeması ve mevcut deploy/ mekanizması korunur; yerine ikinci hat kurulmaz.
6.2. Şema değişiklikleri yalnız eklemeli göçle yapılır; yıkıcı değişiklik yedek ve açık onay ister.
6.3. SPA aynı oturum ve veri modelini kullanır; ikinci kimlik sistemi veya ikinci API katmanı kurulmaz.
6.4. Yapılandırma mevcut düzende kalır; yeni ortam anahtarları belgelenir; sırlar ortam dosyasında tutulur.
6.5. Yayın hattı: `npm run yayin` → commit → push → GitHub kancası → `git merge --ff-only` → canlı. Sunucuda build, npm veya Node adımı yoktur.
6.6. Yayınlanmış geçmiş yeniden yazılmaz: force-push ve rebase yasaktır; sunucu yalnız ileri sarımlı birleştirir, aksi halde dağıtım durur.
6.7. Canlı dizin elle düzenlenmez; çalışma zamanı üretimi (uploads, log, veri) gitignore'dadır ve birleştirme öncesi dizin temiz olmalıdır.
6.8. Dağıtım öncesi ve sonrası smoke listesi ile geri alma adımı yazılıdır; rollback önceki yayın commit'idir (`git revert` + push), sunucuda elle dosya geri alınmaz.
6.9. Ayrıntı: references/sureklilik-dagitim.md ve references/webhook-dagitim.md.
6.10. Sürüm damgası `vYYYYMMDDHHMM` biçimindedir: küçük v öneki ve on iki haneli yıl-ay-gün-saat-dakika; nokta, tire, alt çizgi, iki nokta ve boşluk kullanılmaz. Damga build başlamadan üretim betiğinde bir kez üretilir ve build ortam değişkeniyle bilgi/hakkında sayfasına aktarılır; çalışma anında hesaplanmaz, elle yazılmaz, koda gömülü ikinci sürüm sabiti bulunmaz. Bilgi sayfası, release kaydı ve aynı adlı tag birebir aynı değeri taşır; farklıysa dağıtım kabul edilmez. Bu damga §5'teki API sürümlemesinden ayrıdır.

## 7. Mod sözleşmesi

| Alan | Geliştirme (varsayılan) | Release/prod kapıları |
|---|---|---|
| İstemci | `spa/` kökünde Vite dev sunucusu ve HMR; API çağrıları PHP'ye gider | `npm run yayin` temiz; kök çıktı commit edilip push'lanır; kanca çeker |
| Doğrulama | Tip kontrolü, etkilenen testler, tarayıcı kontrolü | Tam build, bundle bütçesi, smoke, tüm kapılar |
| Yönlendirme | Dev proxy veya aynı origin | LiteSpeed kuralları ve derin bağlantı doğrulanır |
| Güvenlik | Oturum/CSRF/girdi aynı | CSP/HSTS başlıkları, secret taraması, tedarik zinciri |
| Değişmez | Oturum/CSRF, yetki, sır, erişilebilirlik, veri bütünlüğü, Türkçe imlâ | Aynı |

7.1. Geliştirmede her mikro değişiklikte prod build ve deploy yoktur; HMR ve etkilenen test yeterlidir.
7.2. Release/risk tetikleri: kırıcı API değişikliği, oturum/CSRF, env/secret, yönlendirme, dağıtım, açık yayın isteği.
7.3. Risk sınıfı belirsizse en yüksek sınıf varsayılır; kapı atlanmaz, atlanan kapı geçti sayılmaz.

## 8. Doğrulama ve kabul

8.1. `npm run yayin` temizdir: hata ve uyarı yoktur; ikinci çalıştırma çalışma ağacında fark bırakmaz.
8.2. Kök çıktı Node gerektirmez; statik sunucudan servis edilerek doğrulanır ve commit'te bulunur.
8.3. Bundle bütçesi tanımlıdır ve aşılmaz; JS ve CSS toplamı release kaydında ölçülür.
8.4. Derin bağlantı 200 döner; /api/* PHP'ye gider; eksik varlık 404; bilinmeyen API yolu JSON 404 döner.
8.5. CSRF'siz POST 403; oturumsuz korumalı uç 401; yetkisiz istek 403 döner.
8.6. Kanca doğrulanır: ping `pong` döner, push 202 alır, `log/deploy.log` kaydı düşer ve canlı commit push edilen commit'tir.
8.7. Smoke listesi ve geri alma adımı release kaydında yazılıdır; ayrıntı references/kabul-kapilari.md.

- [ ] `npm run yayin` temiz; kök çıktı commit'te ve Node gerektirmeden servis ediliyor.
- [ ] Derin bağlantı 200; /api/* PHP'ye gidiyor; eksik varlık 404.
- [ ] CSRF'siz POST 403; oturumsuz korumalı uç 401.
- [ ] Bundle bütçesi ölçüldü ve aşılmadı.
- [ ] Kanca ping/push ile doğrulandı; canlı commit güncel.
- [ ] Deploy öncesi/sonrası smoke listesi ve rollback adımı kayıtlı.

## 9. Sınır ve references

9.1. Sınır: bu beceri SPA ve PHP API mimarisini bağlar; SSR panel, statik site ve salt estetik dil kapsam dışıdır.
9.2. Aynı hüküm başka beceride varsa oraya atıf verilir; süreç ve araç disiplini sp-orkestra 3.4 ve 4'tedir.
9.3. Yapısal UI ve erişilebilirlik sp-dizayn-web-uygulama, estetik dil sp-zen-dizayn alanındadır; teslim mekaniğinde bu beceri önceliklidir.
9.4. References:
- references/vite-derleme.md
- references/litespeed-yonlendirme.md
- references/guvenlik-oturum.md
- references/api-sozlesmesi.md
- references/sureklilik-dagitim.md
- references/webhook-dagitim.md
- references/kabul-kapilari.md
