"""The Metropolitan Museum of Art adaptörü (yalnız kamu malı eserler)."""

from __future__ import annotations

import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import json_istek, metin_temizle
from ..sabitler import CIKIS_BULUNAMADI, LISANS_KAMU_MALI, YEREL_SERBEST
from ._yardimci import alan, bicim_tahmin, boyut_sniff, liste, sozluk, tam_sayi, varyantlari_uret

LISANS_URL = "https://creativecommons.org/publicdomain/zero/1.0/"
AZAMI_DETAY = 12


class MetKaynak:
    """Met Museum Collection API adaptörü (v1.1 arama)."""

    ad = "met"
    lisans_adi = "CC0 1.0"
    lisans_sinifi = LISANS_KAMU_MALI
    yerel_indirme = YEREL_SERBEST
    atif_zorunlu = False
    anahtar_ortami = None
    varsayilan_taban = "https://collectionapi.metmuseum.org/public/collection"
    taban_ortami = "GORSEL_API_TABANI_MET"
    gorsel_hostlari: tuple[str, ...] = ("images.metmuseum.org",)
    kota_basliklari: tuple[str, ...] = ()

    def _aday(self, nesne: Any) -> Aday | None:
        if alan(nesne, "isPublicDomain") is not True:
            return None
        birincil = str(alan(nesne, "primaryImage", ""))
        kucuk = str(alan(nesne, "primaryImageSmall", ""))
        if not birincil:
            return None
        genislik, yukseklik = boyut_sniff(birincil, self.gorsel_hostlari)
        adaylar = [(genislik, birincil, bicim_tahmin(birincil))]
        if kucuk:
            adaylar.append((0, kucuk, bicim_tahmin(kucuk)))
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if not varyantlar:
            return None
        etiketler = " ".join(str(alan(etiket, "term", "")) for etiket in liste(nesne, "tags"))
        return Aday(
            kaynak=self.ad,
            kimlik=str(alan(nesne, "objectID", "")),
            baslik=metin_temizle(alan(nesne, "title", ""), 120) or f"met-{alan(nesne, 'objectID', '')}",
            genislik=genislik,
            yukseklik=yukseklik,
            lisans_adi=self.lisans_adi,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=str(alan(nesne, "objectURL", "")),
            varyantlar=varyantlar,
            fotografci=metin_temizle(alan(nesne, "artistDisplayName", ""), 80),
            risk_metni=metin_temizle(f"{alan(nesne, 'title', '')} {alan(nesne, 'objectName', '')} {alan(nesne, 'medium', '')} {etiketler}", 240),
            ek={"lisans_url": LISANS_URL},
        )

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        limit = min(max(istek.adet * 2, 12), 60)
        parametreler = {
            "q": istek.konu,
            "hasImages": "true",
            "offset": (istek.sayfa - 1) * limit,
            "limit": limit,
        }
        veri, _ = json_istek(f"{taban}/v1.1/search?{urllib.parse.urlencode(parametreler)}")
        kimlikler = [tam_sayi(deger) for deger in liste(veri, "objectIDs")][:AZAMI_DETAY]
        adaylar: list[Aday] = []
        for kimlik in kimlikler:
            if len(adaylar) >= istek.adet:
                break
            try:
                aday = self.detay(str(kimlik), None, taban)
            except AracHatasi:
                continue
            adaylar.append(aday)
        return adaylar

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        if not kimlik.isdigit():
            raise AracHatasi(CIKIS_BULUNAMADI, "Met objectID sayısal olmalı.")
        veri, _ = json_istek(f"{taban}/v1/objects/{kimlik}")
        aday = self._aday(veri)
        if aday is None:
            raise AracHatasi(CIKIS_BULUNAMADI, "Met nesnesi bulunamadı veya kamu malı değil.")
        return aday


KAYNAK = MetKaynak()
