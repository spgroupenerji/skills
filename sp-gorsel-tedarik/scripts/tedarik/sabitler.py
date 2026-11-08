"""Araç sabitleri: sınırlar, lisans sınıfları, çıkış kodları, kategori ve ortam adları."""

AZAMI_JSON_BAYT = 2 * 1024 * 1024
AZAMI_GORSEL_BAYT = 30 * 1024 * 1024
ZAMAN_ASIMI = 20
YENIDEN_DENEME = 3
GERI_CEKILME = (1.0, 2.0, 4.0)
AZAMI_ADET = 30
VARSAYILAN_ADET = 6
AZAMI_SAYFA = 20
ASGARI_GENISLIK = 320
AZAMI_GENISLIK = 3840
VARSAYILAN_GENISLIKLER = "640,960,1440"
VARSAYILAN_KALITE = 82
VARSAYILAN_KLASOR = "assets/img"
MANIFEST_ADI = "credits.json"
SLUG_AZAMI = 60
SLUG_YEDEK = "gorsel"

KULLANIM_TICARI = "ticari"
KULLANIM_EDITORIAL = "editorial"
KULLANIM_TURLERI = (KULLANIM_TICARI, KULLANIM_EDITORIAL)

LISANS_KAMU_MALI = "kamu-mali"
LISANS_SERBEST_TICARI = "serbest-ticari"
LISANS_KOSULLU = "kosullu"
LISANS_SINIFLARI = (LISANS_KAMU_MALI, LISANS_SERBEST_TICARI, LISANS_KOSULLU)

TICARI_UYGUN = "uygun"
TICARI_MANUEL = "manuel_dogrulama_gerekli"
TICARI_ENGELLI = "engelli"
TICARI_DURUMLAR = (TICARI_UYGUN, TICARI_MANUEL, TICARI_ENGELLI)
TICARI_ONAY_UYGUN = "uygun"
TICARI_ONAY_UYGUN_DEGIL = "uygun-degil"

YEREL_SERBEST = "serbest"
YEREL_ONAY = "kullanici_onayi"
YEREL_HOTLINK = "hotlink"
YEREL_TURLERI = (YEREL_SERBEST, YEREL_ONAY, YEREL_HOTLINK)

YONLER = ("landscape", "portrait", "squarish")
BICIMLER = ("webp", "jpg", "png")

CIKIS_TAMAM = 0
CIKIS_KULLANIM = 2
CIKIS_ANAHTAR = 3
CIKIS_BULUNAMADI = 4
CIKIS_API = 5
CIKIS_DOGRULAMA = 6
CIKIS_UYUM = 7
CIKIS_TICARI = 8
CIKIS_KAYNAK = 9

KATEGORILER = ("genel", "kurumsal", "sanat", "bilim-uzay", "doku-3b", "tarih")

ISTEMCI_AJANI = "sp-gorsel-tedarik/1.0 (SP GROUP; info@spgroupenerji.com)"
YEREL_HOSTLAR = frozenset({"127.0.0.1", "localhost", "::1"})
UTM_UYGULAMA = "sp-gorsel-tedarik"

GORSEL_BICIM_IMZALARI = {
    "jpg": (b"\xff\xd8\xff",),
    "png": (b"\x89PNG\r\n\x1a\n",),
    "webp": (b"RIFF",),
}
