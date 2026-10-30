---
name: sp-mimari-web-spa
description: "Vite ile derlenen React SPA'nın (istemci yönlendirme) LiteSpeed üzerinde PHP REST API ile mimarisini kurar: dist teslimi, /api/* yönlendirmesi, aynı origin oturum ve CSRF, sözleşme-önce API, süreklilik ve release kapıları. Şu durumlarda kullan: React SPA + PHP API kurulumu, SPA yönlendirme/derin bağlantı sorunu, API sözleşmesi ve dağıtımı. Kullanma: SSR panel, statik/SEO site, salt estetik dil; bu alanlarda yüklenmez."
version: "v202610300515"
---

# sp-mimari-web-spa

Vite ile derlenen React SPA ve LiteSpeed üzerinde PHP REST API mimarisinin sözleşmesi: istemci yönlendirme, statik dist teslimi, aynı origin güvenlik, sözleşme-önce API ve mevcut sistemle süreklilik. Varsayılan mod geliştirmedir; güvenlik, erişilebilirlik, veri bütünlüğü ve sır yönetimi her modda değişmezdir.

## 0. Ortak çalışma ilkeleri
> Kaynak: AGENTS-tr; ortak blok, bilinçli kopya. Süreç ve araç ayrıntısı: sp-sozlesme 1.3, 2.2 ve §4.

0.1. Öncelik: kullanıcının güncel yazılı talimatı > AGENTS-tr > bu beceri > model genel bilgisi. Çelişkide üstteki kaynak kazanır.
0.2. Mod: varsayılan geliştirmedir; release/prod kapıları yalnız risk sınıfı (oturum, API sözleşmesi, env/secret, yönlendirme, dağıtım) veya açık yayın isteğiyle yüklenir.
0.3. Değişmezler: güvenlik, erişilebilirlik, veri bütünlüğü, sır yönetimi ve Türkçe imlâ her modda korunur; hız veya token için kısaltılmaz.
0.4. Bilgi: sürüm, API ve davranış varsayılmaz; çalışma anında context7 veya resmî kaynaktan doğrulanır; doğrulanamayan bilgi "doğrulanmalı" etiketiyle verilir.
0.5. Araç: işe göre seçilir, gerektiğinde hibrit kullanılır; erişim hatasında tanı (izin, kurulum, indeks, sürüm, yol), basit çözüm, çözülemezse işe başlamadan kullanıcıya bildir (sp-sozlesme 1.3, 2.2, §4).
0.6. Kanıt: kanıtsız "tamamlandı" yoktur; kabul kapıları yalnız release veya risk tetiklediğinde yüklenir (references/kabul-kapilari.md).

## 1. Kapsam ve sınır

1.1. Bu beceri Vite ile derlenen React SPA'yı ve LiteSpeed üzerindeki PHP REST API'yi bağlar: derleme, dağıtım, yönlendirme, oturum/CSRF, sözleşme ve süreklilik.
1.2. Çalışma zamanı modeli istemci yönlendirmeli SPA'dır; sunucu yalnız statik dist dosyalarını ve /api/* PHP yanıtını verir.
1.3. Kapsam dışı: SSR zero-build PHP panel (sp-mimari-web-uygulama), statik/SEO site (sp-mimari-web-site), salt estetik dil (sp-zen-dizayn), yapısal UI tasarımı (sp-dizayn-web-uygulama).
1.4. SSR panelde SPA yasaktır; SPA modeli ayrı yüzey veya proje içindir; iki teslim modeli aynı yüzeyde karıştırılmaz.
1.5. Yapısal UI ve erişilebilirlik sp-dizayn-web-uygulama alanındadır; o becerinin zero-build/htmx teslim bölümü SPA'da uygulanmaz, build ve teslim mekaniği bu beceridedir.
1.6. Çelişkide öncelik: kullanıcı talimatı > AGENTS-tr > platform mimari becerisi > tasarım becerisi > estetik dil; SPA teslim mekaniğinde bu beceri mimari katmandır.

## 2. Model ve dağıtım

2.1. Node yalnız derleme zamanındadır; üretimde Node çalışmaz, çalışma zamanı PHP ve statik dosyalardır.
2.2. Üretime yalnız derlenmiş dist/ gider; kaynak ağacı, bağımlılık ağacı ve dev araçları dağıtılmaz.
2.3. Kütüphaneler npm ile kurulur; CDN'den script, stil veya font yüklenmez.
2.4. lockfile sürüm kontrolündedir; kurulum lockfile'a göre yapılır; yeni bağımlılık gerekçelenir ve pinlenir.
2.5. Build yeniden üretilebilir: aynı lockfile ve komut aynı çıktıyı verir; dist depoda tutulmaz, sürümlü artefakt olarak saklanır.
2.6. Build-time ortam değişkenleri yalnız kamuya açık değerleri taşır; sır istemci paketine gömülmez, API anahtarları PHP tarafındadır.
2.7. Node, Vite, React ve PHP sürümleri çalışma anında resmî kaynaktan doğrulanır; beceriye sürüm yazılmaz.
2.8. Ayrıntı: references/vite-derleme.md.
2.9. Stil kaynağı build'e girer: seçilen stil çözümü proje kaydında tanımlanır ve sürümü doğrulanır; CDN stil veya script yoktur.

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
4.6. Sırlar dist'e girmez; istemciye gömülen değerler kamuya açıktır, sunucu sırları ortam değişkeninden gelir.
4.7. Tedarik zinciri: lockfile, pinli sürüm, lockfile'a göre kurulum, yeni bağımlılık gerekçesi ve denetim; CDN ve doğrulanmamış kaynak yoktur.
4.8. Release başlıkları: CSP script-src self, unsafe-inline ve unsafe-eval yok; HSTS, nosniff ve Referrer-Policy eksiksizdir; değerler release'de resmî kaynaktan doğrulanır.
4.9. Ayrıntı: references/guvenlik-oturum.md.

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
6.5. Dağıtım öncesi ve sonrası smoke listesi ile geri alma adımı yazılıdır; rollback önceki dist ve önceki API commit'ini hedefler.
6.6. Ayrıntı: references/sureklilik-dagitim.md.

## 7. Mod sözleşmesi

| Alan | Geliştirme (varsayılan) | Release/prod kapıları |
|---|---|---|
| İstemci | Vite dev sunucusu ve HMR; API çağrıları PHP'ye gider | npm run build temiz; dist dağıtılır |
| Doğrulama | Tip kontrolü, etkilenen testler, tarayıcı kontrolü | Tam build, bundle bütçesi, smoke, tüm kapılar |
| Yönlendirme | Dev proxy veya aynı origin | LiteSpeed kuralları ve derin bağlantı doğrulanır |
| Güvenlik | Oturum/CSRF/girdi aynı | CSP/HSTS başlıkları, secret taraması, tedarik zinciri |
| Değişmez | Oturum/CSRF, yetki, sır, erişilebilirlik, veri bütünlüğü, Türkçe imlâ | Aynı |

7.1. Geliştirmede her mikro değişiklikte prod build ve deploy yoktur; HMR ve etkilenen test yeterlidir.
7.2. Release/risk tetikleri: kırıcı API değişikliği, oturum/CSRF, env/secret, yönlendirme, dağıtım, açık yayın isteği.
7.3. Risk sınıfı belirsizse en yüksek sınıf varsayılır; kapı atlanmaz, atlanan kapı geçti sayılmaz.

## 8. Doğrulama ve kabul

8.1. npm run build temizdir: hata ve uyarı yoktur.
8.2. dist Node gerektirmez; statik sunucudan servis edilerek doğrulanır.
8.3. Bundle bütçesi tanımlıdır ve aşılmaz; JS ve CSS toplamı release kaydında ölçülür.
8.4. Derin bağlantı 200 döner; /api/* PHP'ye gider; eksik varlık 404; bilinmeyen API yolu JSON 404 döner.
8.5. CSRF'siz POST 403; oturumsuz korumalı uç 401; yetkisiz istek 403 döner.
8.6. Smoke listesi ve geri alma adımı release kaydında yazılıdır; ayrıntı references/kabul-kapilari.md.

- [ ] npm run build temiz; dist Node gerektirmeden servis ediliyor.
- [ ] Derin bağlantı 200; /api/* PHP'ye gidiyor; eksik varlık 404.
- [ ] CSRF'siz POST 403; oturumsuz korumalı uç 401.
- [ ] Bundle bütçesi ölçüldü ve aşılmadı.
- [ ] Deploy öncesi/sonrası smoke listesi ve rollback adımı kayıtlı.

## 9. Sınır ve references

9.1. Sınır: bu beceri SPA ve PHP API mimarisini bağlar; SSR panel, statik site ve salt estetik dil kapsam dışıdır.
9.2. Aynı hüküm başka beceride varsa oraya atıf verilir; süreç ve araç disiplini sp-sozlesme 1.3, 2.2 ve §4'tedir.
9.3. Yapısal UI ve erişilebilirlik sp-dizayn-web-uygulama, estetik dil sp-zen-dizayn alanındadır; teslim mekaniğinde bu beceri önceliklidir.
9.4. References:
- references/vite-derleme.md
- references/litespeed-yonlendirme.md
- references/guvenlik-oturum.md
- references/api-sozlesmesi.md
- references/sureklilik-dagitim.md
- references/kabul-kapilari.md
