"""Art Institute of Chicago adaptörü (yalnız kamu malı eserler, IIIF)."""

from __future__ import annotations

import os
import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import json_istek, metin_temizle
from ..sabitler import CIKIS_BULUNAMADI, CIKIS_TICARI, LISANS_KAMU_MALI, YEREL_SERBEST
from ._yardimci import alan, liste, metin_html_temizle, sozluk, tam_sayi, varyantlari_uret

LISANS_URL = "https://www.artic.edu/open-access/public-domain-images"
ALANLAR = "id,title,image_id,is_public_domain,artist_display,date_display,thumbnail,department_title"
GENISLIKLER = (3000, 1686, 1200, 800, 600, 400)


class ArticKaynak:
    """Art Institute of Chicago API adaptörü; IIIF görselleri Referer ister."""

    ad = "artic"
    lisans_adi = "CC0 1.0"
    lisans_sinifi = LISANS_KAMU_MALI
    yerel_indirme = YEREL_SERBEST
    atif_zorunlu = False
    anahtar_ortami = None
    varsayilan_taban = "https://api.artic.edu/api/v1"
    taban_ortami = "GORSEL_API_TABANI_ARTIC"
    varsayilan_cdn = "https://www.artic.edu/iiif/2"
    cdn_ortami = "GORSEL_CDN_TABANI_ARTIC"
    gorsel_hostlari: tuple[str, ...] = ("www.artic.edu",)
    indirme_basliklari = {"Referer": "https://www.artic.edu/"}
    kota_basliklari: tuple[str, ...] = ()

    def _cdn(self) -> str:
        return os.environ.get(self.cdn_ortami, self.varsayilan_cdn).rstrip("/")

    def _aday(self, eser: Any) -> Aday | None:
        if alan(eser, "is_public_domain") is not True:
            return None
        image_id = str(alan(eser, "image_id", "") or "").strip()
        if not image_id:
            return None
        thumb = sozluk(eser, "thumbnail")
        genislik = tam_sayi(alan(thumb, "width"))
        yukseklik = tam_sayi(alan(thumb, "height"))
        cdn = self._cdn()
        adaylar = [
            (boyut, f"{cdn}/{image_id}/full/{boyut},/0/default.jpg", "jpg")
            for boyut in GENISLIKLER
            if not genislik or boyut <= genislik
        ]
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if not varyantlar:
            return None
        kimlik = str(alan(eser, "id", ""))
        baslik = metin_temizle(alan(eser, "title", ""), 120) or f"artic-{kimlik}"
        sanatci = metin_html_temizle(alan(eser, "artist_display", ""), 80)
        return Aday(
            kaynak=self.ad,
            kimlik=kimlik,
            baslik=baslik,
            genislik=genislik,
            yukseklik=yukseklik,
            lisans_adi=self.lisans_adi,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=f"https://www.artic.edu/artworks/{urllib.parse.quote(kimlik)}",
            varyantlar=varyantlar,
            fotografci=sanatci,
            risk_metni=metin_temizle(f"{alan(eser, 'title', '')} {alan(eser, 'department_title', '')} {alan(eser, 'date_display', '')}", 240),
            ek={"lisans_url": LISANS_URL},
        )

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        parametreler = [
            ("q", istek.konu),
            ("query[term][is_public_domain]", "true"),
            ("fields", ALANLAR),
            ("limit", min(max(istek.adet * 2, 3), 100)),
            ("page", istek.sayfa),
        ]
        url = f"{taban}/artworks/search?{urllib.parse.urlencode(parametreler)}"
        veri, _ = json_istek(url)
        adaylar = [self._aday(eser) for eser in liste(veri, "data")]
        return [aday for aday in adaylar if aday is not None]

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        if not kimlik.isdigit():
            raise AracHatasi(CIKIS_BULUNAMADI, "Art Institute kimliği sayısal olmalı.")
        veri, _ = json_istek(f"{taban}/artworks/{kimlik}?{urllib.parse.urlencode({'fields': ALANLAR})}")
        eser = alan(veri, "data", {})
        aday = self._aday(eser) if isinstance(eser, dict) else None
        if aday is None:
            raise AracHatasi(CIKIS_TICARI, "Art Institute eseri kamu malı değil veya görseli yok.")
        return aday


KAYNAK = ArticKaynak()