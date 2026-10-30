# dagitim — dağıtım, kanca, rollback

> Bu dosya sp-mimari-web-uygulama becerisinin references dosyasıdır; gövdedeki 7. bölümün ayrıntısını taşır. Yalnız release tetiklendiğinde yüklenir.

## 1. Önkoşullar

1.1. Sürüm ve uzantı envanteri, şema durumu, yedek ve rollback hedefi dağıtımdan önce kayda geçer.
1.2. Ortam değişkenleri ve yükleme dizini dağıtım kapsamı dışındadır; üzerine yazılmaz.
1.3. Şema değişikliği göç disiplinine tabidir; dağıtım sırasında elle SQL çalıştırılmaz.
1.4. Release kapıları geçmeden dağıtım başlatılmaz; atlanan kapı geçti sayılmaz.

## 2. Birleştirme

2.1. Dağıtım yalnız ff-only merge ile yapılır; force push, geçmiş yeniden yazımı ve ff dışı birleştirme yasaktır.
2.2. Birleştirilecek commit ve önceki rollback commit'i kaydedilir; kayıtsız dağıtım reddedilir.
2.3. Dağıtım dalı korumalıdır; doğrudan commit yasaktır.

## 3. Tetikleme

3.1. Depo kancası HMAC-SHA256 imzası doğrulanmadan çalışmaz; imzasız veya geçersiz imzalı istek 403 döner.
3.2. Panelden tetiklenen dağıtım yönetici oturumu, POST ve CSRF olmadan yürütülemez.
3.3. Dağıtım betiği yalnız kendi hattından ve kayıtlı sürümle çalışır; elle tetikleme kayda geçer.

## 4. Sonrası ve rollback

4.1. Dağıtım sonrası OPcache temizlenir ve sağlık kontrolü yapılır.
4.2. Başarısız sağlık kontrolünde önceki commit'e geri dönülür; geri dönüş de kayda geçer.
4.3. Veri göçü varsa down blokları doğrulanmıştır; geri dönüş veri kaybı riski taşıyorsa yedekten dönülür.
4.4. Log ve denetim tek kanaldadır; kanal başına budama tavanı vardır ve log dizini web'den erişilemez.

## 5. Kanıt

5.1. Her dağıtımda birleştirme yöntemi, commit kimlikleri, sağlık sonucu ve rollback hedefi kayıt altındadır.
5.2. Kapı sonuçları references/kabul-kapilari.md biçimine göre raporlanır.
5.3. Başarısız kapıda dağıtım durdurulur; sonra düzeltilir istisnası yoktur.
