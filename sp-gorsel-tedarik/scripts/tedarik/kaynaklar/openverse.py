"""Openverse adaptörü (CC0 / Public Domain Mark)."""

from __future__ import annotations

import os
import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import json_istek, metin_temizle
from ..sabitler import CIKIS_API, CIKIS_BULUNAMADI, LISANS_KAMU_MALI, YEREL_SERBEST
from ._yardimci import alan, bicim_tahmin, liste, sozluk, tam_sayi, varyantlari_uret

YON_ESLEME = {"landscape": "wide", "portrait": "tall", "squarish": "square"}
KABUL_EDILEN = ("cc0", "pdm")
LISANS_ADLARI = {"cc0": "CC0 1.0", "pdm": "Public Domain Mark"}


def _etiketler(kayit: Any) -> str:
    parcalar = []
    for etiket in liste(kayit, "tags"):
        if isinstance(etiket, dict):
            parcalar.append(str(alan(etiket, "name", "")))
        elif isinstance(etiket, str):
            parcalar.append(etiket)
    return metin_temizle(" ".join(parcalar), 240)


class OpenverseKaynak:
    """Openverse toplayıcı API adaptörü; yalnız CC0/PDM sonuç verir."""

    ad = "openverse"
    lisans_adi = "CC0 / Public Domain Mark"
    lisans_sinifi = LISANS_KAMU_MALI
    yerel_indirme = YEREL_SERBEST
    atif_zorunlu = False
    anahtar_ortami = None
    varsayilan_taban = "https://api.openverse.org/v1"
    taban_ortami = "GORSEL_API_TABANI_OPENVERSE"
    gorsel_hostlari: tuple[str, ...] = ()
    kota_basliklari: tuple[str, ...] = ()

    def _basliklar(self) -> dict[str, str] | None:
        token = os.environ.get("OPENVERSE_API_TOKEN", "").strip()
        return {"Authorization": f"Bearer {token}"} if token else None

    def _aday(self, kayit: Any) -> Aday | None:
        lisans = str(alan(kayit, "license", "")).strip().lower()
        if lisans not in KABUL_EDILEN or alan(kayit, "mature"):
            return None
        kimlik = str(alan(kayit, "id", "")).strip()
        url = str(alan(kayit, "url", ""))
        genislik = tam_sayi(alan(kayit, "width"))
        yukseklik = tam_sayi(alan(kayit, "height"))
        varyantlar = varyantlari_uret([(genislik, url, bicim_tahmin(url))], self.gorsel_hostlari)
        if not kimlik or not varyantlar:
            return None
        return Aday(
            kaynak=self.ad,
            kimlik=kimlik,
            baslik=metin_temizle(alan(kayit, "title", ""), 120) or f"openverse-{kimlik}",
            genislik=genislik,
            yukseklik=yukseklik,
            lisans_adi=LISANS_ADLARI.get(lisans, "CC0"),
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=str(alan(kayit, "foreign_landing_url", "")),
            varyantlar=varyantlar,
            fotografci=str(alan(kayit, "creator", "")),
            profil_url=str(alan(kayit, "creator_url", "")),
            risk_metni=metin_temizle(f"{alan(kayit, 'title', '')} {alan(kayit, 'creator', '')}", 240) + " " + _etiketler(kayit),
            ek={"lisans_url": str(alan(kayit, "license_url", ""))},
        )

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        parametreler: dict[str, Any] = {
            "q": istek.konu,
            "page": istek.sayfa,
            "page_size": min(max(istek.adet * 2, 5), 50),
            "license": "cc0,pdm",
            "mature": "false",
        }
        if istek.yon in YON_ESLEME:
            parametreler["aspect_ratio"] = YON_ESLEME[istek.yon]
        url = f"{taban}/images/?{urllib.parse.urlencode(parametreler)}"
        veri, _ = json_istek(url, self._basliklar())
        adaylar = [self._aday(kayit) for kayit in liste(veri, "results")]
        return [aday for aday in adaylar if aday is not None]

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        if not kimlik:
            raise AracHatasi(CIKIS_BULUNAMADI, "Openverse kimliği boş.")
        veri, _ = json_istek(f"{taban}/images/{urllib.parse.quote(kimlik)}/", self._basliklar(), hata_kodu=CIKIS_API)
        if isinstance(veri, dict) and "id" not in veri:
            sonuclar = liste(veri, "results")
            veri = sonuclar[0] if sonuclar else {}
        aday = self._aday(veri)
        if aday is None:
            raise AracHatasi(CIKIS_BULUNAMADI, "Openverse görseli bulunamadı veya lisansı CC0/PDM değil.")
        return aday


KAYNAK = OpenverseKaynak()