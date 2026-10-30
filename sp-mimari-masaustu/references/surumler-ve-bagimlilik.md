# Sürüm ve Bağımlılık Disiplini

> Gövde §2'nin ayrıntısı. Sürüm, özellik ve lisans değerleri burada sabitlenmez; çalışma anında doğrulanır.

## 1. Pinleme

1.1. Tüm doğrudan ve dolaylı sürümler tam numarayla sabitlenir; aralık, joker ve en son etiketi yoktur.
1.2. `Cargo.lock` depoya işlenir; kilit dosyasız derleme kabul edilmez; doğrulama `--locked` ile yapılır.
1.3. Arayüz kiti sürümü tek doğruluk kaynağıdır: GPUI çatalı, bileşen ve varlık paketleri kitin sabitlediği sürümlerden gelir; doğrudan bağımlılık olarak eklenmez.
1.4. Sürüm yükseltmesi ayrı değişikliktir; aynı değişiklikte özellik eklenmez veya kaldırılmaz.

## 2. Bağımlılık yüzeyi

2.1. Arayüz bağımlılığı tek paketle sınırlıdır; ikinci arayüz paketi, ayrı GPUI çatalı veya `gpui` paketi eklenmez.
2.2. Dışa aktarımlar modül bazlıdır: kök yeniden dışa aktarım yüzeyi çekirdeği verir; bileşen ve varlık (ikon) yüzeyleri `component` ve `assets` özellikleriyle ayrı modüllerden gelir.
2.3. Bir öğenin hangi modülden geldiği varsayılmaz; docs.rs ve sürümün resmî dokümanı esas alınır.
2.4. WebView, gömülü tarayıcı motoru ve JavaScript köprüsü eklenmez.
2.5. Çekirdek yüzeyde bulunmayan yardımcı katmanlar (ölçüm, izleme, tanılama) ayrı bağımlılık olarak eklenir; her biri gerekçe, lisans ve pin ile kayda geçer.
2.6. Platforma özel bağımlılık yalnız ilgili platform ve özellik arkasında eklenir; diğer platform derlemeleri bozulmaz.

## 3. Lisans

3.1. Yeni bağımlılık yalnız MIT veya Apache-2.0 lisanslıysa eklenir; atıf şartı koşan veya belirsiz lisans yoktur.
3.2. Her yeni bağımlılık için kayıt: gerekçe, lisans, sürüm, bakım durumu.
3.3. Lisans ve yasak bağımlılık denetimi otomatik araçla yapılır (ör. cargo-deny veya eşdeğeri); sonuç release kapısında kanıtlanır.
3.4. Lisans sonucu doğrulanmadan bağımlılık birleştirilmez.

## 4. Doğrulama yöntemi

4.1. Sürüm ve özellik iddiası üç kaynaktan doğrulanır: context7, sürümün resmî docs.rs sayfası, crates.io manifesti; çelişkide resmî crate kaynağı esastır.
4.2. API yolu ve imza çalışma anında doğrulanır; beceriye imza, yol veya sürüm numarası gömülmez.
4.3. Varsayılan ve opsiyonel özellikler resmî manifestten okunur; varsayılan açık kabulü yapılmaz.
4.4. Davranış iddiası kaynak gösterilmeden kullanılmaz; doğrulanamayan bilgi doğrulanmalı etiketiyle verilir.
4.5. Yerel teyit yolu: `cargo doc`, `cargo tree`, `cargo check`; araç zinciri yoksa komut ve gerekçe yazılır.

## 5. Yükseltme ve uyumluluk

5.1. Arayüz kiti yükseltmesi uyumluluk kaydıyla yapılır: kırılan API, değişen varsayılan özellik, yeni alt bağımlılıklar.
5.2. Yükseltme sonrası build, test, biçim ve lint kapıları ile ilgili davranış testleri çalıştırılır.
5.3. Uyumluluk kaydı olmadan sürüm yükseltmesi birleştirilmez.

## 6. Ölçülmüş kazanç istisnası

6.1. Hızlandırıcı veya opsiyonel özellik yalnız ölçüm ve yazılı gerekçeyle açılır; varsayılan kapalıdır.
6.2. Ölçüm temsili iş yükünde ve release profilinde yapılır; regresyon varsa özellik geri alınır.

## 7. Kontrol listesi

- [ ] Sürümler tam numaralı; `Cargo.lock` işlenmiş; `--locked` doğrulanmış.
- [ ] İkinci arayüz ve ayrı GPUI paketi yok.
- [ ] Modül bazlı dışa aktarım yolu sürüm dokümanından doğrulanmış.
- [ ] Lisans denetimi MIT veya Apache-2.0 dışında sonuç vermedi.
- [ ] Her yeni bağımlılık için gerekçe ve lisans kaydı var.
- [ ] Doğrulanmamış API kullanımı kalmadı; yerel teyit komutları yazıldı.
