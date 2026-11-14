# agir-mod — sıra, rol tablosu, zincir, doküman kapısı ve devir

> Bu dosya sp-orkestra becerisinin references dosyasıdır; yalnız ağır modda yüklenir. Üyelik burada yazılmaz; roller kurulu katalogdan doldurulur.

## 1. Sıra

1.1. keşif → etki/risk → düzenleme → değişiklik analizi → bağımsız doğrulama → kapanış.
1.2. Bir aşama sahibi çağrılmadan kapanmaz; araç danışılan yan kanal değil, işin yürütüldüğü kanaldır.
1.3. Kanıtlar devredilemez; tam dosya okuma ve grep araç kanıtını tamamlar, yerine geçmez.

## 2. İş türü → zorunlu roller

| İş türü | Zorunlu roller | Geçme eşiği (örnek) |
| --- | --- | --- |
| Kod/veri/şema | keşif, etki/risk, uygulama, değişiklik analizi, bağımsız doğrulama, kapanış | sembol/risk kanıtı + test/lint |
| Doküman/API | doküman doğrulama; kod işi varsa kod rolleri eklenir | kütüphane kimliği + sürüm + snippet |
| Tarayıcı/UI | canlı doğrulama, erişilebilirlik, responsive, görsel kanıt | DOM/konsol/ağ + ekran |
| Medya/3B | üretim/dönüştürme, format doğrulama | çıktı + format/ölçü |
| Araştırma | birincil kaynak, çapraz doğrulama, hafıza | kaynak + karşılaştırma |
| Karışık | birleşim | rol başına ayrı kanıt |

## 3. Zincir tablosu

3.1. Sütunlar: `Aşama | Sahip | Girdi | Çıktı | Kanıt | Yedek`.
3.2. Aynı iş iki sahibe verilmez; birbirini tamamlayan araçlar aynı aşamada ayrı kanıt üretir.
3.3. Her aşamaya geçme eşiği ve bağlam maliyeti yazılır; tablo iç planda kalır, kullanıcıya sonuç özeti verilir.

## 4. Doküman kapısı

4.1. Sürüm, API veya parametre iddiası icradan önce doğrulanır: kurulu doküman aracı → resmî doküman → `doğrulanmalı`.
4.2. Doğrulanmamış "şöyle çalışıyor" cümlesi varsayımdır; varsayım üzerine kod yazılmaz.

## 5. Alt ajan ve kuyruk

5.1. Devir paketi: artefakt yolu, tek paragraf özet, kanıt, açık risk, sonraki adım.
5.2. Bağımsız işler paralel, bağımlı işler sıralı; aynı adım iki kez çalıştırılmaz, ikinci kuyruk kurulmaz.
5.3. Alt ajan sonucu ana bağlama özetle döner; ham çıktı taşınmaz.
