# Orkestrasyon — beş akış, ekip, sıra ve kapılar

> `sp-dizayn-web-site` eki; gövdedeki 8. bölümün ayrıntısıdır. Lead ve subagent iş bölümünü, bağımlılık sırasını, handoff biçimini ve anti-desenleri tanımlar. Kapı ölçütleri kabul-kapilari.md dosyasındadır; bu dosya onları tekrar etmez.

## 1. İşi beş akışa bölme

1.1. Akışlar: sanat yönü ve keşif, metin, medya, build, QA ve yayın. Her akışın tek sahibi, tanımlı girdisi, dosya artefaktı ve kapısı vardır.
1.2. Akış sınırı: bir akış diğerinin dosyasına yazmaz; girdi dosya ve kısa notla taşınır.
1.3. Akış tablosu:

| Akış | Girdi | Çıktı artefaktı | Kapı |
|---|---|---|---|
| Sanat yönü ve keşif | Brief, gerçek malzeme, referans | design/design-package.md | Yön ve erken treatment onayı |
| Metin | Onaylı brief ve araştırma | copy/copy.md, birebir metinler | Kopya ve insan dili kapısı |
| Medya | Onaylı paket ve izinli bütçe | assets/media/, master ve teslim | Görsel doğrulama ve hareket pilotu |
| Build | Onaylı paket, metin, medya | site/, tek site.css | Çalışan önizleme |
| QA ve yayın | Çalışan önizleme | review/ rapor ve görseller | Kabul kapıları, smoke, geri alma |

1.4. Zero-build sınırı: build akışı Node veya CDN üretmez; medya offline üretilip statik varlığa dönüşür. Yayın ayrı alt adımdır; yayın kabulü canlı doğrulamayla kapanır.
1.5. Akış atlanmaz; küçük işte akışlar birleşse bile artefakt ve kapı ayrımı korunur.

## 2. Subagent tablosu

| Rol | Görev | Artefakt | Yazma kapsamı | Kabul |
|---|---|---|---|---|
| Lead | Kapsam, onay, entegrasyon, kapılar, yayın | plan.md, release kaydı | plan.md ve yayın | Kapılar kanıtlı |
| Sanat yönü | Keşif, konsept, treatment, token ve tipografi | design/design-package.md | design/ | Yön onayı ve treatment |
| Metin | Bölüm metinleri, CTA, SSS, dürüst durumlar | copy/copy.md | copy/ | İnsan dili ve imlâ kapısı |
| Medya (koşullu) | Görsel, video, ses üretimi ve encode | assets/media/ | assets/media/ | Pilot ve görsel doğrulama |
| Build | Site iskeleti, CSS/JS, hareket, responsive | site/ | site/ | Önizleme ve teknik taban |
| QA | Ekran, a11y, performans, SEO, metin taraması | review/ rapor ve görseller | review/, kaynak salt-okunur | Kabul kapıları |

2.1. Her üye tek kapsam, net girdi, net çıktı, yazma kapsamı ve ölçülebilir kabul alır.
2.2. Aynı dosyaya iki üye yazmaz; QA kaynak siteye yazmaz, bulguyu görev kaydıyla iade eder.
2.3. Medya üyesi yalnız açık video veya ses isteği ve onaylı araç ya da bütçe varsa açılır; yoksa akış atlanır ve fallback yazılır.
2.4. Ekip iş hacmine göre ölçeklenir; küçük işte tek ajan yeterlidir, aşırı bölünme iletişim maliyeti üretir.

## 3. Bağımlılık ve sıra

3.1. Sanat yönü ve design package onayı olmadan build yazmaya başlamaz; görev blocked_by ile işaretlenir.
3.2. Erken görsel treatment onayı olmadan geniş medya üretimine geçilmez.
3.3. Metin onayı build öncesidir; build metni yeniden yazmaz, paketteki satırları birebir bağlar.
3.4. Build çalışan önizleme vermeden tam QA başlamaz; QA build sonrası ve bağımsızdır.
3.5. Medya bağımlı işler pilot onayından sonra açılır; film ve tipografi eşlemesi doğrulanmadan tamam denmez.
3.6. Onaylar taşınır; yön veya kapsam maddi olarak değişirse yeni onay alınır.
3.7. Bağımlı görev onaysız başlatılmaz; atlanan kapı geçti sayılmaz.

## 4. Paralel ve bağımsız işler

4.1. Paralel işler: araştırma ile ilk metin, medya üretimi ile alt bölüm build'i, QA test planı ile build devamı.
4.2. Sıralı işler: paket sonrası build, treatment sonrası geniş medya, build sonrası QA, QA sonrası yayın.
4.3. Bağımsız dizinler ayrı sahipte: design/, copy/, assets/media/, site/, review/.
4.4. Aynı dizin veya dosya üzerinde eşzamanlı yazma yapılmaz; çakışma riski varsa iş sıralanır.
4.5. Paralel işler ortak planı değiştirmez; plan değişikliği Lead onayındadır.

## 5. Handoff ve kabul

5.1. Her handoff dört parçadır: artefakt yolu, tek paragraf özet, kanıt (ekran, ölçüm veya komut çıktısı), açık risk ve sonraki adım.
5.2. Kabul ölçütü ölçülebilirdir; iyi görünüyor kabul değildir.
5.3. Subagent raporu kanıt yerine geçmez; Lead kanıtı kendi görür veya çalıştırır.
5.4. Kabul edilmeyen teslim gerekçeyle iade edilir; düzeltme sahibinde kalır.
5.5. Devirde bağlam plan dosyasından okunur; sözlü aktarım ve varsayım kabul edilmez.
5.6. Kanıtsız teslim tamamlandı sayılmaz; eksik kanıt doğrulanmalı etiketiyle listelenir.

## 6. Lead entegrasyon ve kapılar

6.1. Lead plan.md, karar kaydı ve onay durumlarını tek yerde tutar; her aşamada onaylı sürüm bellidir.
6.2. Entegrasyon sırası: design package, build, QA, yayın. Lead dosya bütünlüğünü ve son diff'i görür.
6.3. Kapı anları: yön onayı, erken treatment, çalışan önizleme, kabul kapıları, yayın smoke'u. Ölçütler kabul-kapilari.md dosyasındadır.
6.4. Yayın kararı Lead'de; yayın kabulü canlı doğrulamayla ayrı kanıttır: HTTPS, URL durumu, canonical/OG, form ve robots.
6.5. Çelişkide öncelik zinciri gövde 0. bölümdedir; estetik tercih ölçülebilir tabanı esnetmez.
6.6. Kapanış: kabul edilen iş, açık riskler ve doğrulanmalı listesi tek raporda teslim edilir.

## 7. Anti-desenler

| Anti-desen | Neden kötü | Doğrusu |
|---|---|---|
| Her şeyi tek başına yapmak | Bağlam şişer, öz-denetim yanlılığı doğar | Akışlara böl, bağımsız QA kullan |
| Raporu kanıt saymak | Doğrulanmamış teslim | Ekran, ölçüm veya komut çıktısı |
| Onaysız kapsam veya harcama | Geri dönüş zor, güven kaybı | Yeni onay ve yazılı gerekçe |
| Aynı dosyaya çok yazıcı | Çakışma ve kayıp | Tek sahip, yazma kapsamı ayrımı |
| QA'yı build sahibine vermek | Kendi hatasını görmez | Bağımsız QA üyesi |
| Kapı atlamak veya sonra düzeltilir demek | Yön kayması ve borç | blocked_by; kapı kapanmadan ilerleme yok |
| Aşırı subagent | İletişim maliyeti ve gecikme | İş hacmine göre ölçekle |
| Emülasyonu gerçek cihaz saymak | Yanlış kanıt | Doğrulanmalı ve fiziksel kontrol notu |
| Teknik skoru yaratıcı kanıt saymak | Yanlış kalite kararı | Tasarım puanı ve teknik skor ayrı |
| Paket dışına metin yazmak | Onaysız içerik | Build birebir bağlar; değişiklik pakette |
| Hazır motor veya araç paketini koşulsuz kopyalamak | Lisans ve bakım bağı, zero-build sınırı | Mekanizmayı kendi CSS/JS'inde yeniden kur |
| Ücretli aracı varsaymak | Onaysız harcama ve hayal kırıklığı | Ortamı runtime keşfet, onay al |
