---
name: sp-mimari-web-spa
description: "Vite ile derlenen React SPA'nın (istemci yönlendirme) LiteSpeed üzerinde PHP REST API ve nohup Python arka plan veri servisiyle mimarisini kurar: kök yayını (çıktı depo kökünde; kök index.html ve public/ derleme çıktısı, kaynak spa/ altında, elle konan medya assets/ altında), GitHub kancasıyla git çekme dağıtımı, /api/* → api.php yönlendirmesi, PHP çalıştırma beyaz listesi, aynı origin oturum ve CSRF, sözleşme-önce API, veri servisinin dağıtımda yeniden başlatılması, süreklilik ve release kapıları. Şu durumlarda kullan: React SPA + PHP API kurulumu, SPA yönlendirme/derin bağlantı sorunu, API sözleşmesi, SPA yanında arka plan veri servisi. Kullanma: SSR panel, statik/SEO site, salt estetik dil; bu alanlarda yüklenmez."
version: "v202611240016"
---

# sp-mimari-web-spa

Vite ile derlenen React SPA, LiteSpeed üzerinde PHP REST API ve aynı sunucudaki Python arka plan veri servisinin sözleşmesi: istemci yönlendirme, kökten yayınlanan derleme çıktısı, git kancasıyla otomatik dağıtım, aynı origin güvenlik, sözleşme-önce API, servis yaşam döngüsü ve mevcut sistemle süreklilik. Varsayılan mod geliştirmedir; güvenlik, erişilebilirlik, veri bütünlüğü ve sır yönetimi her modda değişmezdir.

## 0. Ortak çalışma ilkeleri
> Kaynak: anayasa; ortak blok, bilinçli kopya. Süreç ve araç ayrıntısı: sp-orkestra 3.4 ve 4.

0.1. Öncelik: kullanıcının güncel yazılı talimatı > anayasa > bu beceri > model genel bilgisi. Çelişkide üstteki kaynak kazanır.
0.2. Mod: varsayılan geliştirmedir; release/prod kapıları yalnız risk sınıfı (oturum, API sözleşmesi, env/secret, yönlendirme, dağıtım, servis) veya açık yayın isteğiyle yüklenir.
0.3. Değişmezler: güvenlik, erişilebilirlik, veri bütünlüğü, sır yönetimi ve Türkçe imlâ her modda korunur; hız veya token için kısaltılmaz.
0.4. Bilgi: sürüm, API ve davranış varsayılmaz; çalışma anında context7 veya resmî kaynaktan doğrulanır; doğrulanamayan bilgi "doğrulanmalı" etiketiyle verilir.
0.5. Araç: işe göre seçilir, gerektiğinde hibrit kullanılır; erişim hatasında tanı (izin, kurulum, indeks, sürüm, yol), basit çözüm, çözülemezse işe başlamadan kullanıcıya bildir (sp-orkestra 3.4, 4).
0.6. Kanıt: kanıtsız "tamamlandı" yoktur; kabul kapıları yalnız release veya risk tetiklediğinde yüklenir (references/kabul-kapilari.md).
0.7. Yayın anında: çıktıyı depo köküne üret, commit'le, push'la; GitHub kancası `git merge --ff-only` ile çeker ve arka plan servisini yeniden başlatır; canlıyı Chrome DevTools ile kontrol et; kanca çekmiyorsa veya servis ayağa kalkmıyorsa yayın kapanmaz (references/webhook-dagitim.md).
0.8. Kimlik: deploy sonrası verilen kalıcı giriş bilgisi yalnız yerel secret deposunda (.env / işletim sistemi kimlik kasası) tutulur; kalıcı bellekte yalnız referansı saklanır; depoya, kitaba, uzağa ve loga yazılmaz; sonraki oturumda tekrar sorulmaz.

## 1. Kapsam ve sınır

1.1. Bu beceri Vite ile derlenen React SPA'yı, LiteSpeed üzerindeki PHP REST API'yi ve aynı sunucudaki Python arka plan veri servisini bağlar: derleme, dağıtım, yönlendirme, oturum/CSRF, sözleşme, servis yaşam döngüsü ve süreklilik.
1.2. Çalışma zamanı modeli istemci yönlendirmeli SPA'dır; sunucu kök `index.html` ile `public/` altındaki derlenmiş dosyaları, `assets/` altındaki elle konan medyayı ve beyaz listedeki PHP girişlerini verir.
1.3. PHP yönetim paneli (`merkez.php`) ayrı bir yüzeydir: SPA ile aynı sayfada karışmaz, kendi oturum ve CSRF bağlamını korur.
1.4. Python arka plan servisi HTTP isteği karşılamaz; veriyi aynı sunucudaki depoya yazar, PHP oradan okur.
1.5. Kapsam dışı: SSR zero-build PHP panel (sp-mimari-web-uygulama), statik/SEO site (sp-mimari-web-site), salt estetik dil (sp-zen-dizayn), yapısal UI tasarımı (sp-dizayn-web-uygulama).
1.6. İki teslim modeli aynı yüzeyde karışmaz: SSR panel rotaları SPA fallback'ine, SPA rotaları panele düşmez.
1.7. Yapısal UI ve erişilebilirlik sp-dizayn-web-uygulama alanındadır; o becerinin zero-build/htmx teslim bölümü SPA'da uygulanmaz, build ve teslim mekaniği bu beceridedir.
1.8. Çelişkide öncelik: kullanıcı talimatı > anayasa > platform mimari becerisi > tasarım becerisi > estetik dil; SPA teslim mekaniğinde bu beceri mimari katmandır.

## 2. Model ve dağıtım

2.1. Node yalnız derleme zamanındadır; üretimde Node çalışmaz. Çalışma zamanı üç parçadır: statik dosyalar, PHP ve Python arka plan servisi.
2.2. Yayın yüzeyi depo köküdür: derleme çıktısı doğrudan kök `index.html` ve kök `public/` dizinine yazılır. Sunucu derleme yapmaz, yalnız commit'i çeker; bu yüzden çıktı depoda olmak zorundadır.
2.3. Kaynak `spa/` altındadır ve Vite kökü orasıdır; kaynak düzdür: `spa/index.html` giriş kabuğu, `spa/main.tsx`, `spa/App.tsx`, `spa/ortak.tsx`, `spa/stil.css`, `spa/sayfa/`. `src/` katmanı yoktur; kök `index.html` yalnız derleme çıktısıdır ve iki giriş aynı yola yazılmaz.
2.4. `public/` ayrılmış çıktı dizinidir (`build.assetsDir`): yalnız build yazar, elle dosya konmaz, kaynakta aynı ad kullanılmaz.
2.5. `assets/` elle konan medya dizinidir (görsel, video): build buraya yazmaz ve buradan silmez; içerik git'te izlenir. Vite'ın `publicDir` kavramı `spa/public/` ile temsil edilir, kök `public/` ile karıştırılmaz.
2.6. `build.emptyOutDir` açıkça `false` olur; kök dizin hiçbir koşulda boşaltılmaz (Vite davranışı: kök dışı hedefte varsayılan `false`, açık değer uyarıyı da kapatır). Bayat hash'li dosyalar `npm run yayin` adımının silme işiyle temizlenir.
2.7. Yayın tek komuttur (`npm run yayin`): `public/` silinir, build çalışır, kaynak ve kök çıktı birlikte stage edilir; elle dosya kopyalanmaz.
2.8. Kökte tek HTML girişi `index.html` ve tek istemci yapılandırma kümesi vardır (`package.json`, `tsconfig.json`, `vite.config.ts`); PHP girişleri beyaz listededir (4.10).
2.9. Kütüphaneler npm ile kurulur; CDN'den script, stil veya font yüklenmez.
2.10. lockfile sürüm kontrolündedir; kurulum lockfile'a göre yapılır; yeni bağımlılık gerekçelenir ve pinlenir.
2.11. Build yeniden üretilebilir: aynı lockfile ve komut aynı çıktıyı verir; yayın çıktısı (kök `index.html` + `public/`) depoda tutulur ve tek doğruluk kaynağıdır; git yedeği, cPanel kopyası ve rollback hedefi aynı commit'tir.
2.12. Build-time ortam değişkenleri yalnız kamuya açık değerleri taşır; sır istemci paketine gömülmez, API anahtarları PHP tarafındadır.
2.13. Node, Vite, React ve PHP sürümleri çalışma anında resmî kaynaktan doğrulanır; beceriye sürüm yazılmaz.
2.14. Stil kaynağı build'e girer: seçilen stil çözümü proje kaydında tanımlanır ve sürümü doğrulanır; CDN stil veya script yoktur.
2.15. Python servisi `python_daq/` altındadır; ayrı süreçtir, PHP veya LiteSpeed içinde çalışmaz.
2.16. Servis Passenger/WSGI ile çalışmaz; `passenger_wsgi.py` kullanılmaz. Barındırıcının süreç başlatma izniyle daemon olarak çalışır.
2.17. Servis kendi sanal ortamını ve `requirements.txt` pinlerini kullanır; bağımlılık kurulumu yayın hattında değil, sunucuda bilinçli adımdır.
2.18. `python_daq/data/` sürüm dışıdır: SQLite (wal/shm), parquet ve cache git'e girmez, yayında korunur.
2.19. Dağıtım sırası: servis durdurulur, birleştirme yapılır, OPcache temizlenir, servis başlatılır; sıra bozulursa veri kilidi veya eski kod çalışma riski doğar.
2.20. Servisin yeniden başlatma yolu ve log konumu tanımlıdır; log web'den erişilemez.
2.21. Ayrıntı: references/vite-derleme.md, references/python-daq.md ve references/webhook-dagitim.md.

## 3. Yönlendirme

3.1. LiteSpeed'de `/api/*` kök `api.php` dosyasına, diğer tüm GET ve HEAD yolları kök `index.html` dosyasına yönlenir (SPA fallback).
3.2. `api.php` yalnız `/api/*` üzerinden çalışır; doğrudan `/api.php` isteği işlenmez ve 403 döner.
3.3. Derin bağlantılar 200 döner; fallback yalnız GET ve HEAD ile var olmayan yollar için çalışır; durum değiştiren metotlar fallback'e düşmez.
3.4. Gerçek statik varlık isteği fallback'e düşmez; eksik varlık 404 döner ve HTML ile karşılanmaz.
3.5. Bilinmeyen `/api/*` yolu PHP tarafında JSON 404 döner; HTML fallback'e düşmez.
3.6. İstemci yönlendirici geçmiş tabanlıdır; yollar tek kaynaktan tanımlanır ve sunucu fallback kuralı bu listeyle uyumludur.
3.7. Önbellek: `index.html` önbelleklenmez; `public/` altındaki hash'li dosyalar uzun ömürlü ve immutable sunulur; `assets/` altındaki hash'siz medya sürümlü ad veya kısa ömürle sunulur.
3.8. Ayrıntı: references/litespeed-yonlendirme.md.

## 4. Güvenlik

4.1. React ve API aynı alan adındadır (dijital.<alanadi>); CORS yapılandırılmaz, same-origin dışı istemci kabul edilmez.
4.2. Oturum çerezi HttpOnly, Secure ve SameSite ile ayarlanır; girişte oturum kimliği yenilenir; her korumalı API isteği oturumu sunucuda doğrular.
4.3. CSRF: durum değiştiren her istekte belirteç zorunludur; belirteç oturuma bağlıdır, başlıkla taşınır ve sabit zamanlı doğrulanır; eksik veya geçersiz belirteç 403 döner.
4.4. Girdi doğrulama sunucuda zorunludur; istemci doğrulaması yalnız deneyim içindir; şema dışı gövde 400 veya 422 döner.
4.5. Hata kodları ayrışır: oturum yok 401, yetki yok 403, doğrulama 422, bulunamadı 404; gövde iç ayrıntı sızdırmaz.
4.6. Sırlar yayın çıktısına girmez; istemciye gömülen değerler kamuya açıktır, sunucu sırları ortam değişkeninden gelir.
4.7. Tedarik zinciri: lockfile, pinli sürüm, lockfile'a göre kurulum, yeni bağımlılık gerekçesi ve denetim; CDN ve doğrulanmamış kaynak yoktur.
4.8. Release başlıkları: CSP script-src self, unsafe-inline ve unsafe-eval yok; HSTS, nosniff ve Referrer-Policy eksiksizdir; değerler release'de resmî kaynaktan doğrulanır.
4.9. Web'den erişilemez yollar: `spa/`, `python_daq/`, `log/`, `deploy/.env`, `.env`, `config.php`, `package.json`, `tsconfig*.json`, `vite.config.*`, `requirements.txt`, `*.sqlite*`, `*.parquet`. Kökte yalnız yayın çıktısı ve beyaz listedeki PHP girişleri servis edilir.
4.10. PHP çalıştırma beyaz listesi: yalnız `api.php`, `merkez.php`, `deploy/deploy.php`, `seo/sitemap-generator.php` HTTP'den çalışır; `config.php` dahil diğer PHP dosyaları çalışmaz, yalnız include edilir.
4.11. Panel ayrı yüzeydir: `merkez.php` kendi oturum ve CSRF bağlamını korur; SPA belirteci panele, panel belirteci SPA'ya geçmez.
4.12. Ayrıntı: references/guvenlik-oturum.md.

## 5. API sözleşmesi

5.1. Her uç için metot, yol, girdi şeması, çıktı şeması ve hata kodları önce yazılır; istemci ve sunucu bu sözleşmeden üretilir.
5.2. Tek zarf biçimi kullanılır: başarı verisi; hata kodu, mesaj ve alan listesi; HTTP durumu ile uygulama kodu uyumludur.
5.3. İstemci sözleşmeden tiplenir; any yoktur; cevaplar çalışma anında doğrulanır; iş kuralı istemcide tekrarlanmaz.
5.4. Sürümleme açıktır (yol veya başlık); kırıcı değişiklik yeni sürümle gelir; eski sürümün kaldırılması kayda geçer.
5.5. Sözleşme testleri her uç için başarı ve hata durumlarını kapsar; şema doğrulaması testin parçasıdır.
5.6. Sayfalama, filtre ve idempotency anahtarı ortak sözleşmede tek kez tanımlanır.
5.7. Ayrıntı: references/api-sozlesmesi.md.

## 6. Süreklilik

6.1. Mevcut MySQL şeması ve mevcut dağıtım mekanizması korunur; yerine ikinci hat kurulmaz.
6.2. Şema değişiklikleri yalnız eklemeli göçle yapılır; yıkıcı değişiklik yedek ve açık onay ister.
6.3. SPA aynı oturum ve veri modelini kullanır; ikinci kimlik sistemi veya ikinci API katmanı kurulmaz.
6.4. Yapılandırma mevcut düzende kalır; yeni ortam anahtarları belgelenir; sırlar ortam dosyasında tutulur.
6.5. Yayın hattı: `npm run yayin` → commit → push → GitHub kancası → `git merge --ff-only` → servis yeniden başlatma (sıra: 2.19) → canlı. Sunucuda build, npm veya Node adımı yoktur.
6.6. Yayınlanmış geçmiş yeniden yazılmaz: force-push ve rebase yasaktır; sunucu yalnız ileri sarımlı birleştirir, aksi halde dağıtım durur.
6.7. Canlı dizin elle düzenlenmez; çalışma zamanı üretimi (uploads, log, `python_daq/data/`) gitignore'dadır ve birleştirme öncesi dizin temiz olmalıdır.
6.8. Dağıtım öncesi ve sonrası smoke listesi ile geri alma adımı yazılıdır; rollback önceki yayın commit'idir (`git revert` + push), sunucuda elle dosya geri alınmaz.
6.9. Ayrıntı: references/sureklilik-dagitim.md ve references/webhook-dagitim.md.
6.10. Sürüm damgası `vYYYYMMDDHHMM` biçimindedir: küçük v öneki ve on iki haneli yıl-ay-gün-saat-dakika; nokta, tire, alt çizgi, iki nokta ve boşluk kullanılmaz. Damga build başlamadan üretim betiğinde bir kez üretilir ve build ortam değişkeniyle bilgi/hakkında sayfasına aktarılır; çalışma anında hesaplanmaz, elle yazılmaz, koda gömülü ikinci sürüm sabiti bulunmaz. Bilgi sayfası, release kaydı ve aynı adlı tag birebir aynı değeri taşır; farklıysa dağıtım kabul edilmez. Bu damga §5'teki API sürümlemesinden ayrıdır.

## 7. Mod sözleşmesi

| Alan | Geliştirme (varsayılan) | Release/prod kapıları |
|---|---|---|
| İstemci | `spa/` kökünde Vite dev sunucusu ve HMR; API çağrıları PHP'ye gider | `npm run yayin` temiz; kök çıktı commit edilip push'lanır; kanca çeker |
| Servis | Python servisi gerekliyse yerelde ayrı süreç olarak çalışır | Sunucuda daemon ayakta, log güncel ve veri deposu yazılabilir |
| Doğrulama | Tip kontrolü, etkilenen testler, tarayıcı kontrolü | Tam build, bundle bütçesi, smoke, tüm kapılar |
| Yönlendirme | Dev proxy veya aynı origin | LiteSpeed kuralları ve derin bağlantı doğrulanır |
| Güvenlik | Oturum/CSRF/girdi aynı; beyaz liste ve deny kuralları kurulu | CSP/HSTS başlıkları, secret taraması, tedarik zinciri, deny probu |
| Değişmez | Oturum/CSRF, yetki, sır, erişilebilirlik, veri bütünlüğü, Türkçe imlâ | Aynı |

7.1. Geliştirmede her mikro değişiklikte prod build ve deploy yoktur; HMR ve etkilenen test yeterlidir.
7.2. Release/risk tetikleri: kırıcı API değişikliği, oturum/CSRF, env/secret, yönlendirme, dağıtım, servis davranışı, açık yayın isteği.
7.3. Risk sınıfı belirsizse en yüksek sınıf varsayılır; kapı atlanmaz, atlanan kapı geçti sayılmaz.

## 8. Doğrulama ve kabul

8.1. `npm run yayin` temizdir: hata ve uyarı yoktur; ikinci çalıştırma çalışma ağacında fark bırakmaz.
8.2. Kök çıktı Node gerektirmez; statik sunucudan servis edilerek doğrulanır ve commit'te bulunur.
8.3. Bundle bütçesi tanımlıdır ve aşılmaz; JS ve CSS toplamı release kaydında ölçülür.
8.4. Derin bağlantı 200 döner; /api/* PHP'ye gider; eksik varlık 404; bilinmeyen API yolu JSON 404 döner.
8.5. CSRF'siz POST 403; oturumsuz korumalı uç 401; yetkisiz istek 403 döner.
8.6. Deny probu geçer: `spa/main.tsx`, `package.json`, `config.php`, `log/deploy.log` ve `python_daq/index.py` HTTP'den 403 döner.
8.7. Beyaz liste probu geçer: `api.php` doğrudan çağrıldığında 403, `merkez.php` oturum akışına girer; diğer PHP dosyaları çalışmaz.
8.8. Kanca doğrulanır: ping `pong` döner, push 202 alır, `log/deploy.log` kaydı düşer, canlı commit push edilen commit'tir ve servis ayaktadır.
8.9. Smoke listesi ve geri alma adımı release kaydında yazılıdır; ayrıntı references/kabul-kapilari.md.

- [ ] `npm run yayin` temiz; kök çıktı commit'te ve Node gerektirmeden servis ediliyor.
- [ ] Derin bağlantı 200; /api/* PHP'ye gidiyor; eksik varlık 404.
- [ ] CSRF'siz POST 403; oturumsuz korumalı uç 401.
- [ ] Deny ve PHP beyaz liste probları geçti.
- [ ] Bundle bütçesi ölçüldü ve aşılmadı.
- [ ] Kanca ping/push ile doğrulandı; canlı commit güncel, servis ayakta.
- [ ] Deploy öncesi/sonrası smoke listesi ve rollback adımı kayıtlı.

## 9. Sınır ve references

9.1. Sınır: bu beceri SPA, PHP API ve arka plan veri servisinin mimarisini bağlar; SSR panel, statik site ve salt estetik dil kapsam dışıdır.
9.2. Aynı hüküm başka beceride varsa oraya atıf verilir; süreç ve araç disiplini sp-orkestra 3.4 ve 4'tedir.
9.3. Yapısal UI ve erişilebilirlik sp-dizayn-web-uygulama, estetik dil sp-zen-dizayn alanındadır; teslim mekaniğinde bu beceri önceliklidir.
9.4. References:
- references/vite-derleme.md
- references/litespeed-yonlendirme.md
- references/guvenlik-oturum.md
- references/api-sozlesmesi.md
- references/sureklilik-dagitim.md
- references/webhook-dagitim.md
- references/python-daq.md
- references/kabul-kapilari.md
