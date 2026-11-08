"""Smithsonian Open Access adaptörü (yalnız CC0)."""

from __future__ import annotations

import os
import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import json_istek, metin_temizle
from ..sabitler import CIKIS_ANAHTAR, CIKIS_BULUNAMADI, LISANS_KAMU_MALI, YEREL_SERBEST
from ._yardimci import alan, liste, metin_html_temizle, sozluk, tam_sayi, varyantlari_uret

CC0 = "CC0"
GENISLIKLER = (2048, 1440, 960, 640)
LISANS_URL = "https://creativecommons.org/publicdomain/zero/1.0/"


class SmithsonianKaynak:
    """Smithsonian EDAN Open Access API adaptörü."""

    ad = "smithsonian"
    lisans_adi = "CC0 1.0"
    lisans_sinifi = LISANS_KAMU_MALI
    yerel_indirme = YEREL_SERBEST
    atif_zorunlu = False
    anahtar_ortami = "SI_OPEN_ACCESS_API_KEY"
    yedek_anahtar_ortami = "SMITHSONIAN_API_KEY"
    varsayilan_taban = "https://api.si.edu/openaccess/api/v1.0"
    taban_ortami = "GORSEL_API_TABANI_SMITHSONIAN"
    gorsel_hostlari: tuple[str, ...] = ("ids.si.edu",)
    kota_basliklari: tuple[str, ...] = ()

    def _anahtar(self, anahtar: str | None) -> str | None:
        return anahtar or os.environ.get("SMITHSONIAN_API_KEY", "").strip() or None

    def _medya_sec(self, dnr: dict[str, Any]) -> dict[str, Any] | None:
        medya = liste(sozluk(dnr, "online_media"), "media")
        for aday in medya:
            if not isinstance(aday, dict):
                continue
            if str(alan(sozluk(aday, "usage"), "access", "")).upper() != CC0:
                continue
            if str(alan(aday, "content", "")).startswith("http"):
                return aday
        return None

    def _aday(self, satir: Any) -> Aday | None:
        icerik = sozluk(satir, "content")
        dnr = sozluk(icerik, "descriptiveNonRepeating")
        meta_erisim = str(alan(sozluk(dnr, "metadata_usage"), "access", ""))
        if meta_erisim and meta_erisim.upper() != CC0:
            return None
        medya = self._medya_sec(dnr)
        if medya is None:
            return None
        kimlik = str(alan(satir, "id", "") or alan(dnr, "record_ID", ""))
        ids_id = str(alan(medya, "idsId", ""))
        genislik = tam_sayi(alan(medya, "width"))
        yukseklik = tam_sayi(alan(medya, "height"))
        adaylar = []
        if ids_id:
            for boyut in GENISLIKLER:
                adaylar.append((boyut, f"https://ids.si.edu/ids/deliveryService?id={urllib.parse.quote(ids_id)}&max={boyut}", "jpg"))
        adaylar.append((genislik, str(alan(medya, "content", "")), None))
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if not kimlik or not varyantlar:
            return None
        sanatcilar = list()
        for isim in liste(sozluk(icerik, "freetext"), "name"):
            if isinstance(isim, dict):
                sanatcilar.append(str(alan(isim, "content", "")))
        return Aday(
            kaynak=self.ad,
            kimlik=kimlik,
            baslik=metin_temizle(alan(satir, "title", ""), 120) or f"smithsonian-{kimlik}",
            genislik=genislik,
            yukseklik=yukseklik,
            lisans_adi=self.lisans_adi,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=str(alan(dnr, "record_link", "") or alan(satir, "url", "")),
            varyantlar=varyantlar,
            fotografci=metin_html_temizle(sanatcilar[0], 80) if sanatcilar else "",
            risk_metni=metin_temizle(alan(satir, "title", ""), 240),
            ek={"lisans_url": LISANS_URL},
        )

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        anahtar = self._anahtar(anahtar)
        if not anahtar:
            raise AracHatasi(CIKIS_ANAHTAR, "Smithsonian anahtarı yok (SI_OPEN_ACCESS_API_KEY).")
        rows = min(max(istek.adet * 2, 3), 100)
        parametreler = {
            "q": istek.konu,
            "api_key": anahtar,
            "rows": str(rows),
            "start": str((istek.sayfa - 1) * rows),
            "type": "edanmdm",
        }
        veri, _ = json_istek(f"{taban}/search?{urllib.parse.urlencode(parametreler)}")
        satirlar = liste(sozluk(veri, "response"), "rows")
        adaylar = [self._aday(satir) for satir in satirlar]
        return [aday for aday in adaylar if aday is not None]

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        anahtar = self._anahtar(anahtar)
        if not anahtar:
            raise AracHatasi(CIKIS_ANAHTAR, "Smithsonian anahtarı yok (SI_OPEN_ACCESS_API_KEY).")
        veri, _ = json_istek(f"{taban}/content/{urllib.parse.quote(kimlik)}?{urllib.parse.urlencode({'api_key': anahtar})}")
        kayit = alan(veri, "response", {})
        aday = self._aday(kayit) if isinstance(kayit, dict) else None
        if aday is None:
            raise AracHatasi(CIKIS_BULUNAMADI, "Smithsonian kaydı bulunamadı veya medya CC0 değil.")
        return aday


KAYNAK = SmithsonianKaynak()
