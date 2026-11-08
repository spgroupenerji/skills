"""Cooper Hewitt Smithsonian Design Museum adaptörü (CC0 medya, GraphQL)."""

from __future__ import annotations

import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import json_istek, metin_temizle
from ..sabitler import CIKIS_BULUNAMADI, LISANS_KAMU_MALI, YEREL_SERBEST
from ._yardimci import alan, liste, metin_html_temizle, sozluk, tam_sayi, varyantlari_uret

LISANS_URL = "https://creativecommons.org/publicdomain/zero/1.0/"
ALANLAR = "id summary multimedia"


def _graphql_url(taban: str, sorgu: str) -> str:
    return f"{taban}/?raw&query={urllib.parse.quote(sorgu)}"


def _metin_kacir(deger: str) -> str:
    return deger.replace("\\", "").replace('"', "'").strip()


class CooperHewittKaynak:
    """Cooper Hewitt GraphQL API adaptörü; yalnız cc0 işaretli görseller."""

    ad = "cooperhewitt"
    lisans_adi = "CC0 1.0"
    lisans_sinifi = LISANS_KAMU_MALI
    yerel_indirme = YEREL_SERBEST
    atif_zorunlu = False
    anahtar_ortami = None
    varsayilan_taban = "https://api.cooperhewitt.org"
    taban_ortami = "GORSEL_API_TABANI_COOPERHEWITT"
    gorsel_hostlari: tuple[str, ...] = ("ciim-static-media.s3.us-east-1.amazonaws.com",)
    kota_basliklari: tuple[str, ...] = ()

    def _olcu(self, medya: dict[str, Any], anahtar: str) -> tuple[int, int]:
        olcum = sozluk(sozluk(medya, anahtar), "measurements")
        for boyut in liste(olcum, "dimensions"):
            if not isinstance(boyut, dict) or str(alan(boyut, "dimension", "")) != "width":
                continue
            genislik = tam_sayi(alan(boyut, "value"))
            for digeri in liste(olcum, "dimensions"):
                if isinstance(digeri, dict) and str(alan(digeri, "dimension", "")) == "height":
                    return genislik, tam_sayi(alan(digeri, "value"))
            return genislik, 0
        return 0, 0

    def _aday(self, nesne: Any) -> Aday | None:
        medya_listesi = liste(nesne, "multimedia")
        secilen = None
        for medya in medya_listesi:
            if not isinstance(medya, dict):
                continue
            if alan(medya, "cc0") is not True or str(alan(medya, "type", "")) != "image":
                continue
            if str(alan(sozluk(medya, "original"), "url", "")) or str(alan(sozluk(medya, "large"), "url", "")):
                secilen = medya
                break
        if secilen is None:
            return None
        adaylar = []
        for anahtar in ("original", "large"):
            url = str(alan(sozluk(secilen, anahtar), "url", ""))
            if not url:
                continue
            genislik, yukseklik = self._olcu(secilen, anahtar)
            bicim = str(alan(sozluk(secilen, anahtar), "format", "jpg")).lower()
            adaylar.append((genislik, url, "jpg" if bicim == "jpeg" else bicim))
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if not varyantlar:
            return None
        kimlik = str(alan(nesne, "id", ""))
        if not kimlik:
            return None
        baslik = metin_temizle(alan(sozluk(nesne, "summary"), "title", ""), 120) or f"cooperhewitt-{kimlik}"
        numara = kimlik.rsplit("-", 1)[-1]
        genislik = max(varyant.genislik for varyant in varyantlar)
        return Aday(
            kaynak=self.ad,
            kimlik=kimlik,
            baslik=baslik,
            genislik=genislik,
            yukseklik=0,
            lisans_adi=self.lisans_adi,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=f"https://collection.cooperhewitt.org/objects/{urllib.parse.quote(numara)}/",
            varyantlar=varyantlar,
            risk_metni=baslik,
            ek={"lisans_url": LISANS_URL},
        )

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        adet = min(max(istek.adet * 10, 20), 100)
        sorgu = (
            '{ object(general:"' + _metin_kacir(istek.konu) + '", hasImages:true, size:' + str(adet) + ") "
            "{ " + ALANLAR + " } }"
        )
        veri, _ = json_istek(_graphql_url(taban, sorgu))
        adaylar = [self._aday(nesne) for nesne in liste(alan(veri, "data", {}), "object")]
        return [aday for aday in adaylar if aday is not None]

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        kimlik = kimlik.strip()
        if not kimlik:
            raise AracHatasi(CIKIS_BULUNAMADI, "Cooper Hewitt kimliği boş.")
        sorgu = '{ object(id:"' + _metin_kacir(kimlik) + '") { ' + ALANLAR + " } }"
        veri, _ = json_istek(_graphql_url(taban, sorgu))
        adaylar = [self._aday(nesne) for nesne in liste(alan(veri, "data", {}), "object")]
        aday = next((aday for aday in adaylar if aday is not None), None)
        if aday is None:
            raise AracHatasi(CIKIS_BULUNAMADI, "Cooper Hewitt nesnesi bulunamadı veya medyası CC0 değil.")
        return aday


KAYNAK = CooperHewittKaynak()