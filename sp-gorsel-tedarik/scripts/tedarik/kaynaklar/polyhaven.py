"""Poly Haven adaptörü (CC0 dokular)."""

from __future__ import annotations

import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import json_istek, metin_temizle
from ..sabitler import CIKIS_BULUNAMADI, LISANS_KAMU_MALI, YEREL_SERBEST
from ._yardimci import alan, sozluk, varyantlari_uret

LISANS_URL = "https://polyhaven.com/license"
COZUNURLUKLER = (("4k", 4096), ("2k", 2048), ("1k", 1024))


class PolyHavenKaynak:
    """Poly Haven API adaptörü; yalnız doku (Diffuse) varlıkları."""

    ad = "polyhaven"
    lisans_adi = "CC0 1.0"
    lisans_sinifi = LISANS_KAMU_MALI
    yerel_indirme = YEREL_SERBEST
    atif_zorunlu = False
    anahtar_ortami = None
    varsayilan_taban = "https://api.polyhaven.com"
    taban_ortami = "GORSEL_API_TABANI_POLYHAVEN"
    gorsel_hostlari: tuple[str, ...] = ("dl.polyhaven.org",)
    kota_basliklari: tuple[str, ...] = ()

    def _aday(self, slug: str, dosyalar: Any) -> Aday | None:
        slot = sozluk(dosyalar, "Diffuse")
        if not slot:
            return None
        adaylar = []
        for anahtar, genislik in COZUNURLUKLER:
            for bicim in ("jpg", "png"):
                veri = sozluk(sozluk(slot, anahtar), bicim)
                url = str(alan(veri, "url", ""))
                if url:
                    adaylar.append((genislik, url, bicim))
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if not varyantlar:
            return None
        baslik = metin_temizle(slug.replace("_", " "), 120)
        return Aday(
            kaynak=self.ad,
            kimlik=slug,
            baslik=baslik,
            genislik=max(varyant.genislik for varyant in varyantlar),
            yukseklik=0,
            lisans_adi=self.lisans_adi,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=f"https://polyhaven.com/a/{urllib.parse.quote(slug)}",
            varyantlar=varyantlar,
            risk_metni=baslik,
            ek={"lisans_url": LISANS_URL},
        )

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        parametreler = {"q": istek.konu, "t": "textures"}
        veri, _ = json_istek(f"{taban}/search?{urllib.parse.urlencode(parametreler)}")
        sonuclar = veri.get("results") if isinstance(veri, dict) else None
        adaylar: list[Aday] = []
        for sonuc in (sonuclar or [])[: istek.adet * 2]:
            slug = str(alan(sonuc, "slug", ""))
            if not slug:
                continue
            try:
                aday = self.detay(slug, None, taban)
            except AracHatasi:
                continue
            adaylar.append(aday)
            if len(adaylar) >= istek.adet:
                break
        return adaylar

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        slug = kimlik.strip()
        if not slug:
            raise AracHatasi(CIKIS_BULUNAMADI, "Poly Haven kimliği boş.")
        dosyalar, _ = json_istek(f"{taban}/files/{urllib.parse.quote(slug)}")
        aday = self._aday(slug, dosyalar)
        if aday is None:
            raise AracHatasi(CIKIS_BULUNAMADI, "Poly Haven dokusu bulunamadı.")
        return aday


KAYNAK = PolyHavenKaynak()
