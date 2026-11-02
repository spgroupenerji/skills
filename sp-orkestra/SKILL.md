---
name: sp-orkestra
description: "Şu durumlarda yükle: kullanıcı bir alanı adlandırıp 'yapılması gerekeni yap', 'en üst seviyede yap' veya 'eksiksiz yap' dediğinde; kapsamı ve kalite çıtasını kullanıcı değil ajan belirleyecekse; beceri adıyla çağrıldığında. Tek dosya düzeltmesi, sohbet, çeviri, bilgi sorusu ve acil küçük işlerde yükleme."
version: "v202611020443"
---

# sp-orkestra

Görevi alanın en üst çıtasına derinleştirir, çalışma anındaki beceri ve araç kataloğundan tek bir icra zinciri kurar ve işi kanıtlanmış biçimde bitirir. Plan üretir ama planla kapanmaz; `bitmedi` demek serbesttir, kanıtsız `bitti` yasaktır.

## 0. Amaç ve sınır

0.1. Bu beceri bir planlama değil **tamamlama sözleşmesidir**: çıktı, DoD'si kanıtla eşleşmiş iş ya da gerekçeli `bitmedi` raporudur.
0.2. Yükleme sınırı: tek dosya düzeltmesi, sohbet, çeviri, bilgi sorusu ve acil küçük işlerde kullanılmaz; kullanıcı açıkça istemedikçe basit işe seremoni bindirilmez.
0.3. Öncelik: anayasa > sp-sozlesme > bu beceri (yalnız sıra/seçim) > alan becerisi içeriği. Kural ve kanıt sp-sozlesme'de, içerik alan becerisindedir; bu beceri yalnız hangi becerinin hangi sırada çalışacağını belirler.
0.4. Adım çıktıları sohbete üç blok olarak yazılır: uzman merceği, zincir tablosu, icra direktifi. Kullanıcı sessiz mod isterse yalnız direktif içeride tutulur.
0.5. **Kök neden:** Belirtiyi kapatan yama iş sayılmaz; borç bırakan seçenek seçilmez. Kök neden çözülmeden kapanış yoktur.

## 1. Kapı ve sınıflandırma

1.1. Risk sınıfını anayasa §3'e göre belirle: basit, orta, kritik. Basit işte bu beceriyi kapat ve normal akışa dön.
1.2. brainstorming yolunu belirle: spike, bounded, architectural. Yol ve risk sınıfı, onay kapısının ve seremoni dozunun tek belirleyicisidir.
1.3. Kullanıcı "yap" dediyse bounded işte onay alınmış sayılır; mimari ve kritik işte tasarım/kapanış onayı ayrıca alınır. Onay gerektiren işlemler sp-sozlesme 3.6'dadır.

## 2. Derinleştirme (uzman merceği)

2.1. be-ambitious becerisini yükle ve dört sorusunu uygula; onun "yeniden yaz ve dur" adımını bu akışta uygulama.
2.2. Dört cevabı dört satıra indir:
- Karar: bu iş hangi karara hizmet ediyor, sonucu kim kullanacak?
- Ham malzeme: özet değil, birincil kaynak nerede? (kod, veri, ölçüm, resmî doküman)
- Yöntem: alanın adlandırılmış yöntemleri ve araçları neler?
- Dış doğrulama: model ve kullanıcı dışında neyin doğru olduğunu ne gösterir; geçme eşiği nedir?
2.3. Kimliği ilan etme; kimlik bu dört satırdır. Uzmanlık "ben uzmanım" cümlesiyle değil, karar kriteri, metrik ve kaçınılacak amatör hatayla kurulur.

## 3. Kategori tabanlı yetenek haritası

3.1. Statik araç tablosu yoktur; tablo her çalıştırmada canlı katalogdan üretilir. Katalog üç kanaldan okunur: oturum kataloğu (MCP ve beceri listesi), PATH/yerel araçlar, proje yapılandırması.
3.2. Kategoriler: süreç becerileri, kod zekâsı, doküman doğrulama, tarayıcı/UI doğrulama, hafıza, medya/3B, alan becerileri, alt ajan. Yalnız görevle ilgili kategoriler açılır; açılan kategorinin katalogdaki tüm üyeleri zincire girer, girmeyen çağrılmaz.
3.3. Yeni araç kuralı: katalogda tanımadığın araç varsa işlevini tek cümleyle yaz, kategoriye ata, ilgiliyse zincire ekle. Yeni araç gövde değişikliği istemez; yalnız yeni kategori doğarsa 3.2 listesi güncellenir.
3.4. Üç kanıt katmanı: katalogda ad, fiziksel/yapılandırma kaydı, canlı yanıt. Üçü tamamlanmadan araç "var" sayılmaz. Kapalı veya indekssiz araçta sp-sozlesme 2.2 erişim protokolü işletilir; çözülemezse yedek ve tek cümle beyan yazılır.
3.5. Zincir tablosu en fazla yedi satırdır ve şu sütunları taşır: `Aşama | Sahip | Girdi | Çıktı | Kanıt | Yedek`. Aynı iş iki sahibe verilmez; birbirini tamamlayan araçlar aynı aşamada ayrı kanıt üretir.

## 4. Kod işlerinde zorunlu icra

4.1. Kod, veri veya şema işlerinde kod zekâsı kategorisinin tamamı zorunludur: bugün codegraph, trail, graphify, gitnexus; katalogda aynı işlevi gören yeni araç da aynı zorunluluğa girer.
4.2. Sıra: keşif → etki/risk → düzenleme → değişiklik analizi → doğrulama. Araçlar yalnız danışılan yan kanal değil, işin yürütüldüğü kanaldır.
4.3. Kanıtlar devredilemez: bir aracın kanıtı diğerinin yerine geçmez (sp-sozlesme 2.6). Araçların yetmediği yerde manuel tarama yapılabilir; manuel tarama yalnız ek kanıttır.

## 5. Doküman kapısı

5.1. API, parametre, sürüm veya framework davranışı iddiası varsa icradan önce context7'den ilgili yapı ve bölüm öğrenilir; context7 yoksa resmî doküman; ikisi de yoksa iddia `doğrulanmalı` olur ve icra ona dayanamaz.
5.2. Doküman doğrulaması yapılmadan "şöyle çalışıyor" diye yazılan her cümle varsayımdır; varsayım üzerine kod yazılmaz.

## 6. İcra direktifi

6.1. Direktif tek bloktur ve şunları taşır: kapsam, kalite çıtası (kriter + metrik + kaçınılacak hata), zincir tablosu, DoD ve kanıt eşiği, onay noktaları, durma koşulu.
6.2. Direktif her aşama sonunda tazelenir; kapsam, kanıt veya kullanıcı düzeltmesi değiştiyse eski direktif geçersizdir.
6.3. Direktif alt ajana devredilecekse artefakt yolu, tek paragraf özet, kanıt, açık risk ve sonraki adım birlikte verilir.

## 7. Yürütme

7.1. using-superpowers zaten oturum kuralıdır; bu beceri onu son adımda yeniden çağırmaz. Süreç becerisi önce gelir: yaratıcı veya belirsiz işte brainstorming, hata işinde systematic-debugging, çok adımlı işte writing-plans, kapanışta verification-before-completion.
7.2. Her araç çağrısından önce tek satır beyan yaz: tetik → araç → soracağım soru. Kapanışta her beyan için tek satır kanıt yaz: araç → sorgu → sonuç (sp-sozlesme 2.5-2.6).
7.3. "İyi görünüyor" kanıt değildir. Ekran, ölçüm, komut çıktısı, dosya:satır veya test sonucu kanıttır.
7.4. Engel çıkarsa gizleme: engel, denenen yol, kanıtı ve seçenekleri tek blokta yaz; kullanıcı kararı gerekiyorsa dur.

## 8. Kapanış

8.1. DoD'nin her maddesini kanıtla eşle. Kanıtsız madde varsa iş `bitmedi`dir; gerekçe, engel ve sonraki adım yazılır.
8.2. Dış doğrulamayı çalıştır: test, ölçüm, komut veya uzman denetimi; sonucu tek satırda yaz. Kritik işte anayasa §3.3 ek kanıtları ayrıca aranır.
8.3. Kalan riskleri ve `doğrulanmalı` listesini açık bırak; kullanıcıya "bitti" derken bu listeyi de ver.
8.4. Kalıcı kararı ve kanıt üreten araç-kullanım desenini claude-mem'e yaz; değişen indeksleri ve araç durumunu senkronize et.
8.5. İş ancak kullanıcı "en üst seviyede yapılmıştır" diyebiliyorsa kapanır; aksi halde kapanmaz.
8.6. Geçici yama, ertelenmiş borç veya "sonra düzeltilir" notu bırakılmışsa iş `bitmedi`dir; borç kaydı ve kök neden çözümü yoksa kapanış yoktur.

## 9. Anti-desenler

| Anti-desen | Neden kötü | Doğrusu |
| --- | --- | --- |
| Statik araç tablosu | Katalog değişince ölür | Kategori + canlı keşif |
| Envanteri ezberden yazmak | Varsayım üretir | Üç kanaldan doğrula |
| Her aracı çağırmak | Bağlam şişer, çelişki doğar | Yalnız ilgili kategori üyeleri |
| Tek araç kanıtıyla yetinmek | Kanıt devredilemez | Her araç ayrı kanıt |
| Kimlik ilan etmek | Davranış değiştirmez | Kriter + metrik + dış doğrulama |
| Planı bitmiş saymak | İş yapılmamış olur | Kanıtlı kapanış |
| Kanıtsız "bitti" | Güven kaybı | `bitmedi` + engel |
| Manuel taramayı araç yerine koymak | Denetlenemez kanıt | Araç kanıtı + ek manuel kanıt |
