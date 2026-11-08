"""Pixabay adaptörü."""

from __future__ import annotations

import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import json_istek, metin_temizle
from ..sabitler import CIKIS_ANAHTAR, CIKIS_BULUNAMADI, LISANS_SERBEST_TICARI, YEREL_SERBEST
from ._yardimci import alan, liste, tam_sayi, varyantlari_uret

YON_ESLEME = {"landscape": "horizontal", "portrait": "vertical"}


class PixabayKaynak:
    """Pixabay REST API adaptörü."""

    ad = "pixabay"
    lisans_adi = "Pixabay Content License"
    lisans_sinifi = LISANS_SERBEST_TICARI
    yerel_indirme = YEREL_SERBEST
    atif_zorunlu = True
    anahtar_ortami = "PIXABAY_API_KEY"
    varsayilan_taban = "https://pixabay.com"
    taban_ortami = "GORSEL_API_TABANI_PIXABAY"
    gorsel_hostlari: tuple[str, ...] = ("cdn.pixabay.com",)
    kota_basliklari: tuple[str, ...] = ("X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset")

    def _aday(self, hit: Any) -> Aday | None:
        kimlik = tam_sayi(alan(hit, "id"))
        genislik = tam_sayi(alan(hit, "imageWidth"))
        yukseklik = tam_sayi(alan(hit, "imageHeight"))
        orijinal = str(alan(hit, "imageURL", ""))
        adaylar = [
            (genislik, orijinal, None),
            (1920, str(alan(hit, "fullHDURL", "")), None),
            (1280, str(alan(hit, "largeImageURL", "")), None),
            (640, str(alan(hit, "webformatURL", "")), None),
        ]
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if kimlik <= 0 or not varyantlar:
            return None
        return Aday(
            kaynak=self.ad,
            kimlik=str(kimlik),
            baslik=metin_temizle(alan(hit, "tags", ""), 120) or f"pixabay-{kimlik}",
            genislik=genislik,
            yukseklik=yukseklik,
            lisans_adi=self.lisans_adi,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=str(alan(hit, "pageURL", "")),
            varyantlar=varyantlar,
            fotografci=str(alan(hit, "user", "")),
            risk_metni=metin_temizle(alan(hit, "tags", ""), 240),
        )

    def _istek(self, taban: str, parametreler: dict[str, Any]) -> Any:
        url = f"{taban}/api/?{urllib.parse.urlencode(parametreler)}"
        veri, _ = json_istek(url)
        return veri

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        if not anahtar:
            raise AracHatasi(CIKIS_ANAHTAR, "Pixabay anahtarı yok (PIXABAY_API_KEY).")
        parametreler: dict[str, Any] = {
            "key": anahtar,
            "q": istek.konu,
            "image_type": "photo",
            "safesearch": "true",
            "order": "popular",
            "page": istek.sayfa,
            "per_page": min(max(istek.adet * 2, 3), 200),
        }
        if istek.min_genislik:
            parametreler["min_width"] = istek.min_genislik
        if istek.yon in YON_ESLEME:
            parametreler["orientation"] = YON_ESLEME[istek.yon]
        veri = self._istek(taban, parametreler)
        adaylar = [self._aday(hit) for hit in liste(veri, "hits")]
        return [aday for aday in adaylar if aday is not None]

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        if not anahtar:
            raise AracHatasi(CIKIS_ANAHTAR, "Pixabay anahtarı yok (PIXABAY_API_KEY).")
        if not kimlik.isdigit():
            raise AracHatasi(CIKIS_BULUNAMADI, "Pixabay kimliği sayısal olmalı.")
        veri = self._istek(taban, {"key": anahtar, "id": kimlik})
        hits = liste(veri, "hits")
        aday = self._aday(hits[0]) if hits else None
        if aday is None:
            raise AracHatasi(CIKIS_BULUNAMADI, "Pixabay görseli bulunamadı.")
        return aday


KAYNAK = PixabayKaynak()
