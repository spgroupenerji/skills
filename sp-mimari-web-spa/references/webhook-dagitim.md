# webhook-dagitim — GitHub kancası, git çekme dağıtımı, hata çözümü

> Bu dosya sp-mimari-web-spa becerisinin references dosyasıdır; gövdedeki 2., 6. ve 8. bölümlerin dağıtım ayrıntısını taşır. Mekanizma çalışma anında mevcut `deploy/deploy.php` üzerinden doğrulanır; beceriye sabit yol veya değişken değeri yazılmaz.

## 1. Mekanizma

1.1. Canlı belge kökü depo klonunun kendisidir; ayrı bir yayın dizinine kopyalama yapılmaz.
1.2. Güncelleme `git fetch` + `git merge --ff-only origin/<dal>` ile yapılır; sunucuda derleme, npm veya Node adımı yoktur.
1.3. Kanca ucu `…/deploy/deploy.php?kanca=github` biçimindedir; yalnız POST kabul eder ve istek gövdesi boyutla sınırlıdır.
1.4. Kimlik doğrulama HMAC-SHA256 imzasıyladır: `X-Hub-Signature-256` başlığı `DEPLOY_WEBHOOK_SECRET` ile karşılaştırılır; imza yoksa veya yanlışsa 403.
1.5. Sır tanımlı değilse kanca kapalıdır ve 503 döner; imzasız istekle açık kalmaz.
1.6. `X-GitHub-Event: ping` olayı son dağıtım özetiyle 200 döner; imza doğrulaması ping üzerinde de çalışır.
1.7. Yalnız push olayı ve yalnız canlı klonun bağlı olduğu dal işlenir; diğer dallar ve dal silme olayları 202 ile yok sayılır.
1.8. Kabul edilen push 202 döner, iş isteğin dışında sürer ve sonuç `log/deploy.log` dosyasına yazılır.
1.9. Birleştirme öncesi `uploads/` dizini web kökü dışında `_yedek` arşivine alınır; eski arşivler saklama sınırına göre temizlenir.
1.10. Birleştirme sonrası OPcache temizlenir; kanca yanıtı sır, yol veya yığın izi sızdırmaz.

## 2. Kurulum kapıları

2.1. `DEPLOY_WEBHOOK_SECRET` sunucuda `deploy/.env` veya proje `.env` dosyasındadır; git'e girmez; her ortamın kendi sırrı vardır.
2.2. GitHub deposunda kanca: yalnız `push` olayı, JSON içerik türü, aynı sır, canlı dal.
2.3. İlk doğrulama ping'dir; ping yanıtı alınmadan push denenmez.
2.4. Sunucu klonu canlı dala bağlıdır ve uzak depo okunabilir; uzakta o dal yoksa kanca güncelleme yapamaz.
2.5. Sunucuda `git` çalıştırılabilir olmalıdır (süreç başlatma açık); kapalıysa dağıtım çalışmaz ve barındırıcı politikası düzeltilir.
2.6. `.git` dizini yazılabilir olmalıdır; salt okunur klonda birleştirme başarısız olur.
2.7. cPanel `.cpanel.yml` yalnız "dağıtım tanımı var" kontrolünü sağlar; kopyalama yapmaz ve ikinci hat kurmaz.

## 3. Yayın akışı

3.1. Sıra: `npm run yayin` → kök çıktı diff'i gözden geçir → commit (kaynak + çıktı) → push → kanca → birleştirme → smoke.
3.2. Commit atomiktir: kaynak ve yayın çıktısı aynı commit'te gider; sunucu ikisini tek birleştirmeyle alır.
3.3. Canlı doğrulama: sayfa yüklenir, Console hatasızdır, derin bağlantı 200 döner, `/api/*` PHP yanıtı verir.
3.4. Kapanış kanıtı: `log/deploy.log` içindeki son satır başarılıdır ve canlı commit push edilen commit'tir.

## 4. Hata çözümü

| Belirti | Neden | Çözüm |
|---|---|---|
| 403 imza doğrulanamadı | sır uyuşmuyor veya gövde değişmiş | sırrı iki tarafta eşitle, ping ile doğrula |
| 503 kanca kapalı | sır tanımlı değil | sunucuda sırrı tanımla, tekrar ping at |
| 202 ama güncelleme yok | push başka dala gitti veya canlı klon başka dalda | canlı klonun dalı ile push dalını eşitle |
| birleştirme uygulanamıyor | canlıda yayımlanmamış yerel fark | sunucudaki elle değişikliği geri al; tek doğruluk kaynağı git |
| uzakta dal yok | klon başka dala bağlı | `git fetch` + `git switch -c <dal> --track origin/<dal>` |
| süreç başlatma kapalı | barındırıcı kısıtı | politikayı düzelt; kancayı imzasız açma |
| .git yazılamıyor | izinler | klon sahibinin izinlerini düzelt |

## 5. Sınırlar

5.1. Sunucuda derleme yoktur; Node yalnız geliştirici makinesinde çalışır.
5.2. Yayın çıktısı commit'e girdiği için `varlik/` her yayında tümüyle yeniden üretilir; eski hash'li dosyalar aynı commit'te silinir, elle düzenlenmez.
5.3. Yayınlanmış geçmiş yeniden yazılmaz; force-push ve rebase dağıtımı kırar.
5.4. Geri alma `git revert` + push ile yapılır; sunucuda dosya kopyalama veya elle geri alma yapılmaz.
5.5. Sır, kanca ucu ve log içeriği istemciye veya depoya yazılmaz.

## 6. Doğrulama

6.1. Ping yanıtı, kabul edilen push yanıtı ve `log/deploy.log` satırı release kaydına eklenir.
6.2. Canlı derin bağlantı ve `/api/*` yanıtı gerçek istekle doğrulanır; sözlü beyan kanıt sayılmaz.
