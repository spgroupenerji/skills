"""Flickr adaptörü (yalnız CC0 / Public Domain Mark: lisans 9-10)."""

from __future__ import annotations

import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import json_istek, metin_temizle
from ..sabitler import CIKIS_ANAHTAR, CIKIS_BULUNAMADI, CIKIS_TICARI, LISANS_KAMU_MALI, YEREL_SERBEST
from ._yardimci import alan, bicim_tahmin, liste, sozluk, tam_sayi, varyantlari_uret

KABUL_EDILEN = (9, 10)
BOYUT_GENISLIK = {"url_o": 0, "url_l": 1024, "url_m": 500, "url_sq": 75}
LISANS_URL = "https://www.flickr.com/commons/usage/"


class FlickrKaynak:
    """Flickr REST adaptörü; lisans 7 ve 8 ticari için güvenilmez sayılır."""

    ad = "flickr"
    lisans_adi = "CC0 / Public Domain Mark (Flickr)"
    lisans_sinifi = LISANS_KAMU_MALI
    yerel_indirme = YEREL_SERBEST
    atif_zorunlu = False
    anahtar_ortami = "FLICKR_API_KEY"
    varsayilan_taban = "https://www.flickr.com/services/rest/"
    taban_ortami = "GORSEL_API_TABANI_FLICKR"
    gorsel_hostlari: tuple[str, ...] = ("staticflickr.com",)
    kota_basliklari: tuple[str, ...] = ()

    def _istek(self, taban: str, parametreler: dict[str, Any]) -> Any:
        veri_parametreleri = dict(parametreler)
        veri_parametreleri.update({"format": "json", "nojsoncallback": "1"})
        veri, _ = json_istek(f"{taban}?{urllib.parse.urlencode(veri_parametreleri)}")
        return veri

    def _arama_adayi(self, foto: Any) -> Aday | None:
        if tam_sayi(alan(foto, "license"), -1) not in KABUL_EDILEN:
            return None
        kimlik = str(alan(foto, "id", ""))
        sahip = str(alan(foto, "owner", ""))
        adaylar = []
        for anahtar, genislik in BOYUT_GENISLIK.items():
            url = str(alan(foto, anahtar, ""))
            if url:
                adaylar.append((genislik, url, bicim_tahmin(url)))
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if not kimlik or not varyantlar:
            return None
        bilinen = [varyant.genislik for varyant in varyantlar if varyant.genislik > 0]
        baslik = metin_temizle(alan(foto, "title", ""), 120) or f"flickr-{kimlik}"
        return Aday(
            kaynak=self.ad,
            kimlik=kimlik,
            baslik=baslik,
            genislik=max(bilinen) if bilinen else 0,
            yukseklik=0,
            lisans_adi=self.lisans_adi,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=f"https://www.flickr.com/photos/{urllib.parse.quote(sahip)}/{urllib.parse.quote(kimlik)}",
            varyantlar=varyantlar,
            fotografci=metin_temizle(alan(foto, "ownername", ""), 80),
            risk_metni=baslik,
            ek={"lisans_url": LISANS_URL},
        )

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        if not anahtar:
            raise AracHatasi(CIKIS_ANAHTAR, "Flickr anahtarı yok (FLICKR_API_KEY).")
        veri = self._istek(taban, {
            "method": "flickr.photos.search",
            "api_key": anahtar,
            "text": istek.konu,
            "license": "9,10",
            "safe_search": "1",
            "per_page": min(max(istek.adet * 2, 10), 500),
            "page": istek.sayfa,
            "extras": "license,owner_name,url_sq,url_m,url_l,url_o",
        })
        fotograflar = liste(sozluk(veri, "photos"), "photo")
        adaylar = [self._arama_adayi(foto) for foto in fotograflar]
        return [aday for aday in adaylar if aday is not None]

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        if not anahtar:
            raise AracHatasi(CIKIS_ANAHTAR, "Flickr anahtarı yok (FLICKR_API_KEY).")
        bilgi = self._istek(taban, {"method": "flickr.photos.getInfo", "api_key": anahtar, "photo_id": kimlik})
        foto = sozluk(bilgi, "photo")
        if tam_sayi(alan(foto, "license"), -1) not in KABUL_EDILEN:
            raise AracHatasi(CIKIS_TICARI, "Flickr lisansı yalnız 9 (CC0) ve 10 (PDM) kabul edilir.")
        boyut_veri = self._istek(taban, {"method": "flickr.photos.getSizes", "api_key": anahtar, "photo_id": kimlik})
        boyutlar = liste(sozluk(boyut_veri, "sizes"), "size")
        adaylar = []
        for boyut in boyutlar:
            kaynak = str(alan(boyut, "source", ""))
            genislik = tam_sayi(alan(boyut, "width"))
            if kaynak and genislik > 0:
                adaylar.append((genislik, kaynak, bicim_tahmin(kaynak)))
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if not varyantlar:
            raise AracHatasi(CIKIS_BULUNAMADI, "Flickr görseli bulunamadı.")
        baslik_veri = alan(foto, "title", {})
        baslik = metin_temizle(alan(baslik_veri, "_content", "") if isinstance(baslik_veri, dict) else baslik_veri, 120)
        sahip = sozluk(foto, "owner")
        fotografci = metin_temizle(alan(sahip, "username", "") or alan(sahip, "realname", ""), 80)
        sahip_id = str(alan(sahip, "nsid", ""))
        return Aday(
            kaynak=self.ad,
            kimlik=kimlik,
            baslik=baslik or f"flickr-{kimlik}",
            genislik=max(varyant.genislik for varyant in varyantlar),
            yukseklik=0,
            lisans_adi=self.lisans_adi,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=f"https://www.flickr.com/photos/{urllib.parse.quote(sahip_id)}/{urllib.parse.quote(kimlik)}",
            varyantlar=varyantlar,
            fotografci=fotografci,
            risk_metni=baslik,
            ek={"lisans_url": LISANS_URL},
        )


KAYNAK = FlickrKaynak()
