"""Wikimedia Commons adaptörü (yalnız CC0 / Public Domain)."""

from __future__ import annotations

import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import json_istek, metin_temizle
from ..sabitler import CIKIS_BULUNAMADI, LISANS_KAMU_MALI, YEREL_SERBEST
from ._yardimci import alan, liste, metin_html_temizle, tam_sayi, varyantlari_uret

IINDEKS_ALANLARI = "url|size|mime|extmetadata"
EXTMETADATA_ALANLARI = "License|LicenseShortName|UsageTerms|AttributionRequired|LicenseUrl|Artist"
THUMB_GENISLIGI = 1600
MIME_ESLEME = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}


def _lisans(extmetadata: Any) -> str | None:
    meta = extmetadata if isinstance(extmetadata, dict) else {}
    kod = metin_html_temizle(alan(alan(meta, "License", {}), "value", ""), 30).lower()
    kisa = metin_html_temizle(alan(alan(meta, "LicenseShortName", {}), "value", ""), 60)
    if kod == "cc0":
        return "CC0 1.0"
    if kod == "pd":
        return "Public domain"
    kucuk = kisa.lower()
    if kucuk.startswith("cc0"):
        return "CC0 1.0"
    if "public domain" in kucuk or kucuk.startswith("pd-"):
        return kisa or "Public domain"
    return None


class WikimediaKaynak:
    """Commons MediaWiki API adaptörü."""

    ad = "wikimedia"
    lisans_adi = "CC0 / Public domain"
    lisans_sinifi = LISANS_KAMU_MALI
    yerel_indirme = YEREL_SERBEST
    atif_zorunlu = False
    anahtar_ortami = None
    varsayilan_taban = "https://commons.wikimedia.org"
    taban_ortami = "GORSEL_API_TABANI_WIKIMEDIA"
    gorsel_hostlari: tuple[str, ...] = ("upload.wikimedia.org", "thumb.wikimedia.org")
    kota_basliklari: tuple[str, ...] = ()

    def _parametreler(self) -> dict[str, Any]:
        return {
            "action": "query",
            "prop": "imageinfo",
            "iiprop": IINDEKS_ALANLARI,
            "iiurlwidth": THUMB_GENISLIGI,
            "iiextmetadatafilter": EXTMETADATA_ALANLARI,
            "format": "json",
            "formatversion": 2,
        }

    def _aday(self, sayfa: Any) -> Aday | None:
        bilgi = liste(sayfa, "imageinfo")
        if not bilgi or not isinstance(bilgi[0], dict):
            return None
        ii = bilgi[0]
        bicim = MIME_ESLEME.get(str(alan(ii, "mime", "")).lower())
        lisans = _lisans(alan(ii, "extmetadata", {}))
        if bicim is None or lisans is None:
            return None
        genislik = tam_sayi(alan(ii, "width"))
        yukseklik = tam_sayi(alan(ii, "height"))
        thumb = str(alan(ii, "thumburl", ""))
        adaylar = [(genislik, str(alan(ii, "url", "")), bicim)]
        if thumb:
            adaylar.append((min(genislik or THUMB_GENISLIGI, THUMB_GENISLIGI), thumb, bicim))
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if not varyantlar:
            return None
        artist = metin_html_temizle(alan(alan(ii, "extmetadata", {}), "Artist", {}).get("value", "") if isinstance(alan(ii, "extmetadata", {}), dict) else "", 80)
        return Aday(
            kaynak=self.ad,
            kimlik=str(alan(sayfa, "title", "")),
            baslik=metin_temizle(str(alan(sayfa, "title", "")).replace("File:", ""), 120),
            genislik=genislik,
            yukseklik=yukseklik,
            lisans_adi=lisans,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=str(alan(ii, "descriptionurl", "")),
            varyantlar=varyantlar,
            fotografci=artist,
            risk_metni=metin_temizle(str(alan(sayfa, "title", "")), 240),
        )

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        parametreler = self._parametreler()
        parametreler.update({
            "generator": "search",
            "gsrsearch": f"{istek.konu} filetype:bitmap",
            "gsrnamespace": "6",
            "gsrlimit": min(max(istek.adet * 2, 3), 50),
        })
        veri, _ = json_istek(f"{taban}/w/api.php?{urllib.parse.urlencode(parametreler)}")
        sorgu = alan(veri, "query", {})
        adaylar = [self._aday(sayfa) for sayfa in liste(sorgu, "pages")]
        return [aday for aday in adaylar if aday is not None]

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        baslik = kimlik if kimlik.startswith("File:") else f"File:{kimlik}"
        parametreler = self._parametreler()
        parametreler["titles"] = baslik
        veri, _ = json_istek(f"{taban}/w/api.php?{urllib.parse.urlencode(parametreler)}")
        sorgu = alan(veri, "query", {})
        sayfalar = liste(sorgu, "pages")
        aday = self._aday(sayfalar[0]) if sayfalar else None
        if aday is None:
            raise AracHatasi(CIKIS_BULUNAMADI, "Wikimedia dosyası bulunamadı veya lisansı CC0/PD değil.")
        return aday


KAYNAK = WikimediaKaynak()
