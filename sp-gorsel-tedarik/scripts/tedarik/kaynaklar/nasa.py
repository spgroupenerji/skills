"""NASA Image Library adaptörü."""

from __future__ import annotations

import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import json_istek, metin_temizle
from ..sabitler import CIKIS_BULUNAMADI, LISANS_KAMU_MALI, YEREL_SERBEST
from ._yardimci import alan, boyut_sniff, liste, sozluk, tam_sayi, varyantlari_uret

LISANS_URL = "https://www.nasa.gov/nasa-brand-center/images-and-media/"
BILINEN_BOYUTLAR = ("~large", "~medium", "~small", "~thumb")


class NasaKaynak:
    """NASA images-api adaptörü; ~orig.tif hiçbir zaman seçilmez."""

    ad = "nasa"
    lisans_adi = "NASA Public Domain"
    lisans_sinifi = LISANS_KAMU_MALI
    yerel_indirme = YEREL_SERBEST
    atif_zorunlu = False
    anahtar_ortami = None
    varsayilan_taban = "https://images-api.nasa.gov"
    taban_ortami = "GORSEL_API_TABANI_NASA"
    gorsel_hostlari: tuple[str, ...] = ("images-assets.nasa.gov", "images-api.nasa.gov")
    kota_basliklari: tuple[str, ...] = ()

    def _varliklar(self, taban: str, nasa_id: str) -> list[str]:
        veri, _ = json_istek(f"{taban}/asset/{urllib.parse.quote(nasa_id)}")
        if isinstance(veri, list):
            return [oge for oge in veri if isinstance(oge, str)]
        ogeler = liste(sozluk(veri, "collection"), "items")
        return [str(alan(oge, "href", "")) for oge in ogeler if isinstance(oge, dict)]

    def _boyut_tablosu(self, oge: Any) -> dict[str, tuple[int, int]]:
        tablo: dict[str, tuple[int, int]] = {}
        for link in liste(oge, "links"):
            href = str(alan(link, "href", "")).replace("http://", "https://")
            if href:
                tablo[href] = (tam_sayi(alan(link, "width")), tam_sayi(alan(link, "height")))
        return tablo

    def _jpg_sec(self, varliklar: list[str]) -> dict[str, str]:
        secim: dict[str, str] = {}
        for ham in varliklar:
            url = ham.replace("http://", "https://")
            kucuk = url.lower()
            if not kucuk.endswith(".jpg"):
                continue
            for etiket in BILINEN_BOYUTLAR:
                if etiket in kucuk and etiket not in secim:
                    secim[etiket] = url
        return secim

    def _ogeden(self, oge: Any, taban: str) -> Aday | None:
        veriler = liste(oge, "data")
        if not veriler or not isinstance(veriler[0], dict):
            return None
        veri = veriler[0]
        nasa_id = str(alan(veri, "nasa_id", ""))
        if not nasa_id:
            return None
        boyutlar = self._boyut_tablosu(oge)
        secim = self._jpg_sec(self._varliklar(taban, nasa_id))
        buyuk = secim.get("~large") or secim.get("~medium")
        if not buyuk:
            return None
        genislik, yukseklik = boyutlar.get(buyuk, (0, 0))
        if genislik <= 0:
            genislik, yukseklik = boyut_sniff(buyuk, self.gorsel_hostlari)
        adaylar = [(genislik, buyuk, "jpg")]
        for etiket in ("~medium", "~small", "~thumb"):
            url = secim.get(etiket)
            if url and url != buyuk:
                boyut = boyutlar.get(url, (0, 0))
                adaylar.append((boyut[0], url, "jpg"))
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if not varyantlar:
            return None
        etiketler = " ".join(str(etiket) for etiket in liste(veri, "keywords"))
        return Aday(
            kaynak=self.ad,
            kimlik=nasa_id,
            baslik=metin_temizle(alan(veri, "title", ""), 120) or f"nasa-{nasa_id}",
            genislik=genislik,
            yukseklik=yukseklik,
            lisans_adi=self.lisans_adi,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=f"https://images.nasa.gov/details/{urllib.parse.quote(nasa_id)}",
            varyantlar=varyantlar,
            fotografci=metin_temizle(alan(veri, "photographer", "") or alan(veri, "secondary_creator", ""), 80),
            risk_metni=metin_temizle(f"{alan(veri, 'title', '')} {alan(veri, 'description', '')} {etiketler}", 240),
            ek={"lisans_url": LISANS_URL},
        )

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        parametreler = {"q": istek.konu, "media_type": "image", "page": istek.sayfa}
        veri, _ = json_istek(f"{taban}/search?{urllib.parse.urlencode(parametreler)}")
        ogeler = liste(sozluk(veri, "collection"), "items")
        adaylar: list[Aday] = []
        for oge in ogeler[: istek.adet * 2]:
            if len(adaylar) >= istek.adet:
                break
            try:
                aday = self._ogeden(oge, taban)
            except AracHatasi:
                continue
            if aday is not None:
                adaylar.append(aday)
        return adaylar

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        parametreler = {"nasa_id": kimlik, "media_type": "image"}
        veri, _ = json_istek(f"{taban}/search?{urllib.parse.urlencode(parametreler)}")
        ogeler = liste(sozluk(veri, "collection"), "items")
        aday = self._ogeden(ogeler[0], taban) if ogeler else None
        if aday is None:
            raise AracHatasi(CIKIS_BULUNAMADI, "NASA görseli bulunamadı.")
        return aday


KAYNAK = NasaKaynak()