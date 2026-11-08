"""Pexels adaptörü."""

from __future__ import annotations

import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import json_istek, metin_temizle
from ..sabitler import CIKIS_ANAHTAR, CIKIS_BULUNAMADI, CIKIS_KULLANIM, LISANS_SERBEST_TICARI, YEREL_SERBEST
from ._yardimci import alan, liste, tam_sayi, varyantlari_uret

YON_ESLEME = {"landscape": "landscape", "portrait": "portrait", "squarish": "square"}


class PexelsKaynak:
    """Pexels REST API adaptörü."""

    ad = "pexels"
    lisans_adi = "Pexels License"
    lisans_sinifi = LISANS_SERBEST_TICARI
    yerel_indirme = YEREL_SERBEST
    atif_zorunlu = True
    anahtar_ortami = "PEXELS_API_KEY"
    varsayilan_taban = "https://api.pexels.com"
    taban_ortami = "GORSEL_API_TABANI_PEXELS"
    gorsel_hostlari: tuple[str, ...] = ("images.pexels.com",)
    kota_basliklari: tuple[str, ...] = ("X-Ratelimit-Limit", "X-Ratelimit-Remaining", "X-Ratelimit-Reset")

    def _aday(self, foto: Any) -> Aday | None:
        kimlik = tam_sayi(alan(foto, "id"))
        genislik = tam_sayi(alan(foto, "width"))
        yukseklik = tam_sayi(alan(foto, "height"))
        kaynaklar = alan(foto, "src", {})
        adaylar = [
            (genislik, str(alan(kaynaklar, "original", "")), "jpg"),
            (1880, str(alan(kaynaklar, "large2x", "")), "jpg"),
            (940, str(alan(kaynaklar, "large", "")), "jpg"),
            (640, str(alan(kaynaklar, "medium", "")), "jpg"),
            (340, str(alan(kaynaklar, "small", "")), "jpg"),
        ]
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if kimlik <= 0 or not varyantlar:
            return None
        return Aday(
            kaynak=self.ad,
            kimlik=str(kimlik),
            baslik=metin_temizle(alan(foto, "alt", "") or alan(foto, "url", ""), 120),
            genislik=genislik,
            yukseklik=yukseklik,
            lisans_adi=self.lisans_adi,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=str(alan(foto, "url", "")),
            varyantlar=varyantlar,
            fotografci=str(alan(foto, "photographer", "")),
            profil_url=str(alan(foto, "photographer_url", "")),
            risk_metni=metin_temizle(alan(foto, "alt", ""), 240),
        )

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        if not anahtar:
            raise AracHatasi(CIKIS_ANAHTAR, "Pexels anahtarı yok (PEXELS_API_KEY).")
        parametreler = {
            "query": istek.konu,
            "page": istek.sayfa,
            "per_page": min(max(istek.adet * 2, 3), 80),
        }
        if istek.yon in YON_ESLEME:
            parametreler["orientation"] = YON_ESLEME[istek.yon]
        url = f"{taban}/v1/search?{urllib.parse.urlencode(parametreler)}"
        veri, _ = json_istek(url, {"Authorization": anahtar})
        adaylar = [self._aday(foto) for foto in liste(veri, "photos")]
        return [aday for aday in adaylar if aday is not None]

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        if not anahtar:
            raise AracHatasi(CIKIS_ANAHTAR, "Pexels anahtarı yok (PEXELS_API_KEY).")
        if not kimlik.isdigit():
            raise AracHatasi(CIKIS_KULLANIM, "Pexels kimliği sayısal olmalı.")
        veri, _ = json_istek(f"{taban}/v1/photos/{kimlik}", {"Authorization": anahtar})
        aday = self._aday(veri)
        if aday is None:
            raise AracHatasi(CIKIS_BULUNAMADI, "Pexels fotoğrafı bulunamadı.")
        return aday


KAYNAK = PexelsKaynak()
