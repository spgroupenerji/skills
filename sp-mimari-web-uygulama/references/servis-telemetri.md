# servis-telemetri — asenkron servis katmanı ve yapısal telemetri

> Bu dosya sp-mimari-web-uygulama becerisinin references dosyasıdır; gövdedeki 6. bölümün ayrıntısını taşır. Koşulludur: yalnız servis katmanı gerektiğinde yüklenir.

## 1. Kapsam ve tipler

1.1. Servis katmanı yalnız panel dışı, uzun süreli veya eşzamanlı iş yükü gerektiğinde kullanılır; basit istekler PHP içinde çözülür.
1.2. Servis asenkron Python ile yazılır; parametre ve dönüş tipleri eksiksizdir; gerekçesiz Any reddedilir.
1.3. Servis sözleşmesi katı şemayla tanımlanır; sürüm ve API davranışı çalışma anında resmî kaynaktan doğrulanır.

## 2. Olay döngüsü

2.1. Olay döngüsünde bloklayan senkron G/Ç yürütülmez.
2.2. Dosya, soket ve veritabanı erişimi asenkron sürücü veya thread havuzuyla yapılır.
2.3. CPU-yoğun rutinler to_thread veya ProcessPoolExecutor'a devredilir; döngü tick süresi uzatılmaz.
2.4. Her dış çağrı katı timeout ile sınırlıdır; timeoutsuz çağrı üretim kodunda yer almaz.

## 3. Görev ve eşzamanlılık

3.1. Başlatılan her görev için güçlü referans tutulur; görev kaybolmaz.
3.2. İptal yakalanır; soket, kilit ve dosya tanıtıcıları deterministik bırakılır.
3.3. Coroutine ile thread arasındaki veri takası tek yönlü ve atomiktir (kuyruk veya run_coroutine_threadsafe).
3.4. Paylaşılan mutasyon kilitlidir; kilit altında ağ, disk veya uzun hesap yapılmaz; kilitleme sırası deterministiktir.

## 4. Sınırlar ve yük

4.1. Sınırsız kuyruk, arabellek ve önbellek yoktur; maxsize tanımlıdır, doygunlukta üretici bekletilir.
4.2. Doygunlukta deterministik yük atılır (429 veya 503 ya da en eskiyi düşürme); atılan veri yapısal sayaçla kaydedilir.
4.3. Yeniden deneme tavan sayı, üstel geri çekilme ve rastgele sapma içerir; kontrolsüz sonsuz döngü yasaktır.
4.4. Sürekli başarısız bağımlılıkta devre kesici uygulanır; açık devrede istek hızla reddedilir ve metrikle raporlanır.

## 5. Telemetri

5.1. Loglar JSON yapısal formattadır; zaman, seviye, trace kimliği ve modül alanları zorunludur.
5.2. String biçimlendirmeyle log yazılmaz; alanlar ayrı taşınır.
5.3. Parola, token ve kişisel veri loglanmaz; zorunluysa maskelenir.
5.4. Sistem sınırından gelen veri katı şemayla doğrulanmadan iç katmana aktarılmaz.

## 6. Sağlık ve kapanış

6.1. Servis sağlık uçları bağımlılık durumunu ve kuyruk doygunluğunu raporlar; iç ayrıntı istemciye sızmaz.
6.2. Kapanışta görevler iptal edilir, kuyruklar boşaltılır ve kaynaklar deterministik serbest bırakılır.
6.3. Release'de servis davranışı sürüm dokümanından doğrulanır; varsayım yapılmaz.
