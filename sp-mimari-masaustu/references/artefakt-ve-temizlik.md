# Artefakt ve Release Temizliği

> Gövde §5, §6 ve §8'in ayrıntısı: adlandırma, kopyalama, temizlik, doğrudan çalışma ve depo hijyeni.

## 1. Adlandırma

1.1. Artefakt adı `release\<uygulama>_beta-vYYYYMMDDHHMM.exe` biçimindedir.
1.2. `<uygulama>` parametredir; `app-pdf` yalnız örnektir, ürün adı sabitlenmez.
1.3. `beta` etiketi sabittir; kanal değişikliği bu becerinin kapsamı dışındadır.
1.4. Artefakt doğrudan release klasörü kökünde durur; alt klasör ve ek dosya yoktur.
1.5. Ad içinde boşluk, Türkçe karakter ve tarih biçimi dışında ek bilgi bulunmaz.

## 2. Kopyalama

2.1. Derleme çıktısı önce hedef klasörde geçici ada kopyalanır.
2.2. Kopya boyutu kaynakla karşılaştırılır ve dosyanın çalıştırılabilir uzantıda olduğu doğrulanır.
2.3. Geçici dosya nihai damgalı ada tek işlemle taşınır; aynı ad varsa üzerine yazılır.
2.4. Kopyalama başarısızsa geçici dosya silinir ve eski artefakt korunur.
2.5. Kopyalama sonrası derleme çıktısı silinmez; artefakt yalnız release klasöründe tekilleştirilir.

## 3. Release temizliği

3.1. Kural: release klasöründe yalnız en güncel artefakt bulunur.
3.2. Silme kapsamı yalnız ürün adı, `beta` etiketi ve damga desenine uyan dosyalardır.
3.3. Yabancı dosya, elle bırakılmış not ve başka klasör silinmez.
3.4. Sıra değişmez: yeni artefakt doğrulanır, sonra önceki damgalı dosyalar silinir.
3.5. Derleme veya kopyalama başarısızsa temizlik adımı çalışmaz; hiçbir dosya silinmez.
3.6. Temizlik sonrası klasörde tek dosya olduğu doğrulanır.
3.7. Temizlik betik kapsamındadır; elle silme ve elle yeniden adlandırma yapılmaz.

## 4. Doğrudan çalışma

4.1. Artefakt kurulum gerektirmez; çift tıklama veya komutla doğrudan başlatılır.
4.2. Çalışması için yanında yardımcı dosya, klasör veya kayıt defteri değişikliği aranmaz.
4.3. İlk açılışta ana pencere açılmalı ve temel akış (örnek: bir belge açma) smoke kapsamında denenmelidir.
4.4. Doğrudan çalışma koşulu bozulursa artefakt yayınlanmaz; sapma kayda geçirilir.

## 5. Doğrulama ve smoke

5.1. Dosya doğrulaması: artefakt var, boyutu sıfırdan büyük, ad deseni doğru.
5.2. Damga doğrulaması: dosya adındaki damga biçimli ve uygulama içi sürümle aynı.
5.3. Teklik doğrulaması: release klasöründe tek dosya var.
5.4. Smoke: exe başlatılır, kurulum istenmez, ana pencere açılır ve süreç beklenen çıkış kodunu verir.
5.5. Hata sonrası: geçici dosya, yarım artefakt ve artık süreç kalmamıştır.
5.6. Smoke sonucu ve ek manuel kontrol release kaydına yazılır.

## 6. Depo hijyeni

6.1. release ve target klasörleri sürüm kontrolü dışındadır.
6.2. Artefakt, damga ve derleme çıktısı depoya işlenmez; commit içinde yer almaz.
6.3. Release klasörü yalnız yerel çıktı içindir; paylaşım ayrı bir süreçtir ve bu becerinin kapsamı dışındadır.
6.4. Betik ve yapılandırma sürüm kontrolünde kalır; release klasörü `.gitignore` ile korunur.

## 7. Hata durumları

7.1. Kopyalama hatası: geçici dosya silinir, eski artefakt korunur, çıkış kodu sıfır dışı.
7.2. Taşıma hatası: hedef ve geçici dosya denetlenir; yarım dosya bırakılmaz.
7.3. Temizlik hatası: yeni artefakt doğrulandıktan sonra oluşursa betik uyarır ve durur; eski dosya elle silinmez.
7.4. Smoke hatası: artefakt damgalı olsa da yayınlanmaz; hata nedenine göre yeni derleme gerekir.

## 8. Kontrol listesi

- [ ] Ad `release\<uygulama>_beta-vYYYYMMDDHHMM.exe` biçiminde; ürün adı parametre.
- [ ] Kopyalama geçici ad üzerinden atomik taşımayla yapıldı.
- [ ] Yeni artefakt doğrulanmadan eski dosya silinmedi.
- [ ] Release klasöründe tek dosya var.
- [ ] Exe kurulum gerektirmeden doğrudan çalıştı; smoke kayıtlı.
- [ ] Dosya adı damgası ile uygulama içi sürüm aynı.
- [ ] release ve target sürüm kontrolü dışında; artefakt commit edilmedi.
