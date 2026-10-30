---
name: sp-mimari-masaustu
description: "Rust ve GPUI Kit masaüstü uygulamalarının katman sınırını, bağımlılık ve sürüm pinlemesini, eşzamanlılık modelini, masaüstü davranışını, hata/gizlilik disiplinini, gömülü SQLite sözleşmesini ve derleme/sürüm artefaktı zincirini uygular. Şu durumlarda kullan: yeni uygulama kurulumu, GPUI katman veya eşzamanlılık kararı, SQLite göçü, derleme betiği ve release exe üretimi. Kullanma: görsel tasarım, web sitesi veya panel mimarisi, salt estetik dil; bu alanlarda yüklenmez."
version: "v202610300555"
---

# sp-mimari-masaustu

Rust ve GPUI Kit ile geliştirilen yerel çizimli masaüstü uygulamalarının mimari sözleşmesi. Katman, bağımlılık, eşzamanlılık, davranış, hata/gizlilik, SQLite, paketleme, derleme ve sürüm artefaktı burada tanımlanır; görsel tasarım ayrı tasarım becerisinin alanıdır.

Varsayılan mod geliştirmedir; release ve prod kapıları yalnız risk sınıfı veya açık yayın isteğiyle yüklenir. Alan ayrıntıları references dosyalarındadır ve yalnız o alan tetiklendiğinde okunur.

## 0. Ortak çalışma ilkeleri (kaynak: AGENTS-tr; bilinçli kopya)

0.1. Öncelik: kullanıcı talimatı > AGENTS-tr > bu beceri > model bilgisi.
0.2. Mod: varsayılan geliştirme; release ve prod kapıları yalnız risk sınıfı veya açık yayın isteğiyle yüklenir.
0.3. Değişmezler: güvenlik, erişilebilirlik, veri bütünlüğü, sır yönetimi ve Türkçe imlâ her modda korunur.
0.4. Bilgi: sürüm, API ve davranış varsayılmaz; çalışma anında context7 veya resmî kaynaktan doğrulanır; doğrulanamayan bilgi doğrulanmalı etiketiyle verilir.
0.5. Araç: işe göre seçilir, gerektiğinde hibrit kullanılır; erişim hatasında tanı, basit çözüm, çözülemezse işe başlamadan bildir (sp-sozlesme 1.3, 2.2, §4).
0.6. Kanıt: kanıtsız tamamlandı beyanı yoktur; kabul kapıları yalnız release veya risk tetikte yüklenir.

## 1. Katman sınırı

1.1. Uygulama `ui/`, `domain/` ve `depo/` modüllerine ayrılır; her modül yalnız kendi sorumluluğunu taşır.
1.2. `ui/` altında SQL, ağ çağrısı ve dosya yazma bulunmaz; ihlal eden değişiklik birleştirilmez.
1.3. `domain/` hiçbir arayüz paketini içe aktaramaz; alan mantığı arayüzden bağımsız ve test edilebilir.
1.4. `render` gövdesinde iş kuralı, doğrulama, veri dönüşümü ve G/Ç yoktur; render yalnız durum çizer, ucuz biçimlendirme serbesttir.
1.5. Katmanlar arası veri tipli `struct` ve `enum` ile taşınır; `static mut` ve kilitsiz global mutable durum yoktur.
1.6. Sistem sınırından giren veri tipli modele çözülüp doğrulanmadan iç katmana geçemez; genel API'de tip gizleyen kaçış yoktur.
1.7. Statik denetim ve kapı komutları: references/kabul-kapilari.md.

## 2. Bağımlılık ve sürüm pinleme

2.1. Arayüz bağımlılığı tek paketle sınırlıdır; ikinci arayüz paketi, ayrı GPUI çatalı veya farklı bir GPUI paketi eklenmez.
2.2. GPUI erişimi arayüz kitinin yeniden dışa aktarımıyla yapılır; dışa aktarımlar modül bazlıdır: kök yeniden dışa aktarım yüzeyi çekirdeği, `component` ve `assets` özellikleri bileşen ve varlık yüzeylerini verir.
2.3. Bir öğenin hangi modülden geldiği varsayılmaz; docs.rs ve sürümün resmî dokümanından doğrulanır (references/surumler-ve-bagimlilik.md).
2.4. Tüm sürümler tam numarayla sabitlenir; `Cargo.lock` depoya işlenir; joker sürüm ve kilitsiz derleme kabul edilmez.
2.5. Yeni bağımlılık yalnız MIT veya Apache-2.0 lisanslıysa, gerekçe ve lisans kaydıyla eklenir; atıf şartlı lisans yoktur.
2.6. WebView, gömülü tarayıcı motoru ve JavaScript köprüsü yoktur; arayüz yalnız yerel GPUI çizimiyle üretilir.
2.7. Doğrulanmamış API üretime girmez; sürüm, özellik ve lisans değerleri beceriye gömülmez, çalışma anında doğrulanır.

## 3. Eşzamanlılık ve yürütme modeli

3.1. UI iş parçacığında veritabanı, ağ ve senkron dosya G/Ç yapılmaz; bu işler GPUI arka plan yürütücüsünde çalışır.
3.2. UI ile arka plan arasındaki veri yalnız sınırlı kapasiteli kanallarla taşınır; sınırsız kuyruk ve tampon yoktur.
3.3. Kuyruk dolduğunda üretici bekletilir ve geri basınç uygulanır; sessiz veri kaybı kabul edilmez.
3.4. UI durumunu yalnız UI tarafı günceller; arka plan sonucu mesajla iletilir, UI durumuna doğrudan yazılmaz.
3.5. Her arka plan görevi pencere kapanışında iptal edilir; sahipsiz görev ve kapanmış pencereye güncelleme yoktur.
3.6. Eşzamanlı görev sayısı adlandırılmış sabit bir üst sınırla sınırlanır; sınırsız görev üretimi yoktur.
3.7. Dış çağrılar (ağ, dosya, alt süreç) katı zaman aşımıyla sınırlanır; zaman aşımı olmayan çağrı üretim kodunda yer alamaz.
3.8. Yeniden deneme yalnız üst sınır, üstel geri çekilme ve rastgele sapma ile yapılır; sürekli başarısız bağımlılık devre kesiciyle kapatılır.
3.9. Uzun işlem ilerleme ve iptal kontrolü sunar; kilit yalnız en küçük kritik kesitte tutulur.

## 4. Masaüstü davranışı

4.1. Pencere boyutu, konumu ve bölünme oranları oturumlar arasında saklanır, açılışta geri yüklenir.
4.2. Her birincil komutun klavye kısayolu vardır ve menüde veya araç ipucunda görünür; yalnız fareyle erişilen komut yoktur.
4.3. Platform kısayol farkı platform bilgisiyle çözülür; her platforma `ctrl` varsayılmaz.
4.4. Her etkileşimli bölgenin görünür odak halkası vardır; modal veya pencere kapanınca odak mantıklı öğeye döner.
4.5. Metin düzenlenen her alanda geri al ve ileri al çalışır; platform kısayollarıyla uyumsuz eşleme yoktur.
4.6. Dosya seçimi ve kaydetme yerel platform diyaloglarıyla yapılır; özel dosya tarayıcısı yazılmaz.
4.7. Kaydedilmemiş değişiklikte kapatma isteği Türkçe onay sorar; sessiz veri kaybı yoktur.
4.8. Ağ yokken uygulama yerel işlevlerini sürdürür; ağa bağımlı özellik pasifleşir, çökme olmaz.

## 5. Hata, gizlilik ve loglama

5.1. Hata `Result` ile taşınır; boş hata dalı ve hatayı yutan blok yoktur.
5.2. `unwrap()` üretim yolunda yoktur; `expect()` yalnız başlangıçta değişmez kabul edilen ve Türkçe gerekçe taşıyan çağrılarda kullanılır.
5.3. Alan hataları ile sistem hataları ayrı `enum` tipleriyle modellenir; ikisi de maskelenmez, uygun katmanda ele alınır.
5.4. Kullanıcıya gösterilen hata Türkçe ve eyleme dönüktür; stack trace, dosya yolu, SQL veya sürücü ayrıntısı gösterilmez.
5.5. Sırlar yalnız `.env` veya secret manager'dan okunur; kod, depo ve derleme çıktısına gömülmez.
5.6. Loglarda parola, token ve kişisel veri maskelenir; ham değer yazılmaz. Log yapısal üretilir; metin birleştirmeyle log yazılmaz.
5.7. Sır taraması ve log denetimi release kapısında kanıtlanır (references/kabul-kapilari.md).

## 6. SQLite sözleşmesi

6.1. SQLite tek gömülü motordur; istemci-sunucu, harici veya bulut veritabanı yoktur.
6.2. Veritabanı erişimi yalnız `depo/` katmanındadır; `ui/` ve `domain/` SQLite paketini içe aktaramaz. Paket gömülü derleme özelliğiyle gelir, sistem kütüphanesine bağlanmaz.
6.3. Açılışta WAL, yabancı anahtar zorlaması ve adlandırılmış tek bekleme süresi uygulanır; seçilen değerler testte doğrulanır.
6.4. Tek yazıcı ilkesi geçerlidir: tüm yazmalar tek arka plan yürütücüsünden sırayla geçer; ikinci yazıcı açılmaz.
6.5. Veritabanı yalnız yerel diskte tutulur; WAL dosyaları ağ paylaşımında veya eşzamanlanan klasörde açılmaz. Yol platform veri dizininden çözülür, mutlak yol gömülmez.
6.6. Göçler kod içinde tanımlanır, açılışta atomik uygulanır ve testte doğrulanır; her göç tek mantıksal değişiklik taşır. Yıkıcı göç öncesi doğrulanmış dosya yedeği alınır; veri kaybı riskinde Türkçe uyarı ve açık onay transaction öncesi alınır.
6.7. Sorgular hazırlanmış ifadeyle çalışır; `SELECT *` yoktur; her listeleme adlandırılmış sabit bir `LIMIT` taşır; N+1 yoktur; toplu yazma tek transaction'dadır.
6.8. Filtre ve sıralama sorguları indekslidir; plan `EXPLAIN QUERY PLAN` ile doğrulanır; indeksi devre dışı bırakan sarmal ve baştan jokerli `LIKE` yoktur; sayfalama keyset ile yapılır.
6.9. Açılışta bütünlük kontrolü yapılır; hatalı sonuçla çalışılmaz; hata transaction'ı geri alır ve yarım durum bırakmaz. Ayrıntı: references/veri-tabani-sqlite.md.

## 7. Mod sözleşmesi

7.1. Varsayılan mod geliştirmedir: değişiklik başına `cargo check` ve etkilenen testler yeterlidir; tam release zinciri çalıştırılmaz.
7.2. Release ve prod kapıları yalnız risk sınıfı (yetki, veri kaybı, şema göçü, dağıtım) veya açık yayın isteğiyle yüklenir.
7.3. Release zinciri: `cargo build --release --locked`, `cargo test --locked`, `cargo fmt --check`, `cargo clippy -- -D warnings`, paket ve damga, FPS/P95 ve erişilebilirlik ölçümü (references/platform-ci.md, references/artefakt-ve-temizlik.md, references/performans.md).
7.4. Kapı listesi ve kanıt komutları: references/kabul-kapilari.md.
7.5. Güvenlik, erişilebilirlik, veri bütünlüğü ve sır kuralları moddan bağımsız değişmezdir.

## 8. Derleme, sürüm ve release artefaktı

8.1. Tek giriş noktası: damga, derleme, kopyalama, temizlik ve doğrulama aynı üretim betiğinden yürür; ikinci betik, kopya betik ve elle yapılan zorunlu adım yoktur.
8.2. Sürüm damgası `vYYYYMMDDHHMM` biçimindedir; yalnız betikte, derleme başlamadan bir kez üretilir; saat dilimi politikası tek yerde tanımlanır, çakışmada UTC tercih edilir.
8.3. Aynı damga dört tüketicide birebir taşınır: dosya adı, uygulama içi sürüm, Hakkında ekranı ve release kaydı. Elle damga düzeltmesi ve koda gömülü ikinci sürüm sabiti yoktur.
8.4. Derleme: release profili; GPUI ve MuPDF C çekirdeği ilk derlemede sıfırdan derlenir (uzun), sonraki derlemeler artımlıdır; önbellek korunur. Temiz derleme yalnız ayrı bayrak ve yazılı gerekçeyle yapılır.
8.5. Artefakt: `release/<uygulama>_beta-vYYYYMMDDHHMM.exe`; ürün adı parametredir. Geçici ada kopyala, boyut ve çalıştırılabilir uzantıyı doğrula, sonra nihai ada atomik taşı; aynı ad varsa üzerine yazılır.
8.6. Release temizliği: her başarılı derlemeden sonra yalnız en güncel artefakt kalır; silme yalnız tanınan ürün/beta/damga deseninde yapılır. Yeni artefakt doğrulanmadan eski dosya silinmez; başarısız derleme veya kopyalamada hiçbir dosya silinmez.
8.7. Doğrulama: dosya var, ad ve damga biçimi doğru, damga uygulama içi sürümle eşit, release klasöründe tek dosya var ve exe kurulum istemeden doğrudan çalışıyor; sonuç release kaydına yazılır.
8.8. Ayrıntı: references/uretim-betigi.md, references/surum-damgasi.md, references/artefakt-ve-temizlik.md.

## 9. Sınır ve kabul kapısı

9.1. Bu beceri yapı, davranış, bağımlılık, paketleme, SQLite ve derleme/sürüm artefaktı sözleşmesini yönetir; görsel tasarım (tema, ölçü, bileşen görünümü, hareket) ayrı tasarım becerisinin alanıdır ve burada tanımlanmaz.
9.2. Kullanma: web sitesi veya panel mimarisi, salt estetik dil, yalnız görsel düzenleme; bu işlerde yüklenmez.
9.3. References, tetiklenince okunur: references/surumler-ve-bagimlilik.md, references/platform-ci.md, references/performans.md, references/veri-tabani-sqlite.md, references/uretim-betigi.md, references/surum-damgasi.md, references/artefakt-ve-temizlik.md, references/kabul-kapilari.md.
9.4. Bitiş koşulu: değişiklik dev modda `cargo check` ile, release modda kapı listesiyle ve release exe doğrulamasıyla kanıtlanmıştır; kanıtsız tamamlandı beyanı yoktur.
