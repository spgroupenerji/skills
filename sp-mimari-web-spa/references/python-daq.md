# python-daq — arka plan veri servisi, daemon, veri deposu, dağıtım

> Bu dosya sp-mimari-web-spa becerisinin references dosyasıdır; gövdedeki 1.4 ve 2.15–2.20 maddelerinin ayrıntısını taşır. Sürüm ve kütüphane davranışı çalışma anında resmî kaynaktan doğrulanır.

## 1. Yer ve sınır

1.1. Servis `python_daq/` altındadır; web kökünün içinde durur ama HTTP'ye kapalıdır (deny: references/guvenlik-oturum.md 5.7).
1.2. Servis HTTP isteği karşılamaz ve uç sunmaz; tüketen PHP aynı sunucudaki veri deposundan okur.
1.3. Servis PHP süreci içinde, LiteSpeed worker'ında veya istek yaşam döngüsünde çalışmaz.
1.4. Passenger/WSGI kullanılmaz; `passenger_wsgi.py` artık kullanılmaz ve kaldırılabilir.

## 2. Süreç modeli

2.1. Servis daemon olarak çalışır; başlatma, durdurma ve yeniden başlatma yolu proje kaydında tanımlıdır.
2.2. Tek örnek kuralı vardır: aynı anda iki kopya çalışmaz; kilit dosyası veya pid denetimi bunu zorlar.
2.3. Kanca yalnız dağıtım sırasında durdurup başlatır; sürekli gözetim barındırıcının izin verdiği mekanizmayla yapılır, kancaya yayılmaz.
2.4. Log dosyası `log/` altındadır, döndürme sınırı vardır ve web'den erişilemez; log satırı sır ve kişisel veri taşımaz.

## 3. Bağımlılık ve yapılandırma

3.1. Bağımlılıklar `requirements.txt` ile pinlenir; sanal ortam sunucuda ayrı dizindedir ve git'e girmez.
3.2. Sırlar ve bağlantı bilgileri ortam dosyasından okunur; koda, depoya ve loga yazılmaz.
3.3. Kurulum yayın hattının parçası değildir; `requirements.txt` değişikliği ayrı ve kayıtlı adımdır (references/webhook-dagitim.md 1.12).
3.4. Python sürümü ve kütüphane davranışı çalışma anında resmî kaynaktan doğrulanır; beceriye sürüm yazılmaz.

## 4. Veri deposu

4.1. `python_daq/data/` sürüm dışıdır: SQLite (wal/shm), parquet ve cache git'e girmez.
4.2. Depo web'den erişilemez; dışa açılan veri yalnız API üzerinden ve yetki denetimiyle sunulur.
4.3. Dağıtım depoyu silmez; birleştirme sırasında servis durdurulduğu için dosya kilidi oluşmaz.
4.4. Şema değişikliği eklemeli ve geri alınabilir olur; yıkıcı değişiklik yedek ve açık onay ister.
4.5. Yazma atomiktir: kısmi yazılmış dosya veya yarım kayıt okuyucuya görünmez.

## 5. Modül sınırı

5.1. `index.py` tek orkestratördür; bağlantı, işleme ve depolama ayrı dizinlerde kalır.
5.2. `istemci/` dış sistem oturumlarını yönetir; protokol ayrıntısı işleme katmanına sızmaz.
5.3. `isleme/` eşleştirme ve akış mantığını taşır, kalıcı yazma yapmaz.
5.4. `depo/` tek yazma sahibidir; okuyucular aynı arayüzü kullanır.
5.5. `destek/` yardımcı işleri taşır (zamanlama, hava durumu, rapor); çekirdek akışa bağımlılık oluşturmaz.

## 6. Doğrulama

6.1. Dağıtım sonrası servis süreci ayaktadır ve pid veya kilit dosyası tutarlıdır.
6.2. Log son satırı hata içermez; veri deposuna son yazma zamanı ilerler.
6.3. API, servis kapalıyken veri deposundaki son geçerli durumu döner; veri yoksa bunu hata olarak bildirir, uydurma değer üretmez.
6.4. Kanıt release kaydına yazılır; sözlü beyan kanıt yerine geçmez.
