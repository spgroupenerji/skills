"""Unsplash adaptörü."""

from __future__ import annotations

import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Aday, AramaIstegi
from ..ortak import html_kacir, json_istek, metin_temizle, utm_ekle
from ..sabitler import (
    CIKIS_ANAHTAR,
    CIKIS_BULUNAMADI,
    LISANS_SERBEST_TICARI,
    UTM_UYGULAMA,
    YEREL_ONAY,
)
from ._yardimci import alan, liste, sozluk, tam_sayi, varyantlari_uret

YON_ESLEME = {"landscape": "landscape", "portrait": "portrait", "squarish": "squarish"}
GENISLIKLER = (2400, 1880, 1440, 1200, 960, 640)


def _genislik_url(ham: str, genislik: int) -> str:
    parca = urllib.parse.urlsplit(ham)
    sorgu = urllib.parse.parse_qsl(parca.query, keep_blank_values=True)
    sorgu.extend([("w", str(genislik)), ("q", "82"), ("fm", "webp"), ("fit", "max")])
    return urllib.parse.urlunsplit((parca.scheme, parca.netloc, parca.path, urllib.parse.urlencode(sorgu), ""))


def _tetik_url(tetik: str, anahtar: str) -> str:
    if not tetik:
        return ""
    parca = urllib.parse.urlsplit(tetik)
    sorgu = urllib.parse.parse_qsl(parca.query, keep_blank_values=True)
    if not any(anahtar == "client_id" for anahtar, _ in sorgu):
        sorgu.append(("client_id", anahtar))
    return urllib.parse.urlunsplit((parca.scheme, parca.netloc, parca.path, urllib.parse.urlencode(sorgu), ""))


def _atif_html(fotografci: str, profil: str) -> str:
    unsplash = utm_ekle("https://unsplash.com/", UTM_UYGULAMA)
    if fotografci and profil:
        return (
            f'<p class="fotograf-atif">Fotoğraf: <a href="{html_kacir(profil)}">{html_kacir(fotografci)}</a> / '
            f'<a href="{html_kacir(unsplash)}">Unsplash</a></p>'
        )
    return f'<p class="fotograf-atif">Fotoğraf: <a href="{html_kacir(unsplash)}">Unsplash</a></p>'


class UnsplashKaynak:
    """Unsplash API adaptörü (hotlink + indirme tetikleyicisi)."""

    ad = "unsplash"
    lisans_adi = "Unsplash License"
    lisans_sinifi = LISANS_SERBEST_TICARI
    yerel_indirme = YEREL_ONAY
    atif_zorunlu = True
    anahtar_ortami = "UNSPLASH_ACCESS_KEY"
    varsayilan_taban = "https://api.unsplash.com"
    taban_ortami = "GORSEL_API_TABANI_UNSPLASH"
    gorsel_hostlari: tuple[str, ...] = ("images.unsplash.com",)
    kota_basliklari: tuple[str, ...] = ("X-Ratelimit-Limit", "X-Ratelimit-Remaining")

    def _basliklar(self, anahtar: str) -> dict[str, str]:
        return {"Authorization": f"Client-ID {anahtar}", "Accept-Version": "v1"}

    def _aday(self, foto: Any, anahtar: str) -> Aday | None:
        urls = sozluk(foto, "urls")
        ham = str(alan(urls, "raw", ""))
        if not ham or "plus.unsplash.com" in ham:
            return None
        if alan(foto, "premium") or alan(foto, "plus"):
            return None
        kullanici = sozluk(foto, "user")
        baglantilar = sozluk(foto, "links")
        fotografci = metin_temizle(alan(kullanici, "name", "") or alan(kullanici, "username", ""), 80)
        profil = utm_ekle(str(alan(sozluk(kullanici, "links"), "html", "")), UTM_UYGULAMA)
        genislik = tam_sayi(alan(foto, "width"))
        yukseklik = tam_sayi(alan(foto, "height"))
        adaylar = [(genislik, _genislik_url(ham, genislik), "webp")] if genislik else []
        for boyut in GENISLIKLER:
            if genislik and boyut > genislik:
                continue
            adaylar.append((boyut, _genislik_url(ham, boyut), "webp"))
        adaylar.append((1080, str(alan(urls, "regular", "")), "jpg"))
        adaylar.append((400, str(alan(urls, "small", "")), "jpg"))
        varyantlar = varyantlari_uret(adaylar, self.gorsel_hostlari)
        if not varyantlar:
            return None
        ek = {
            "atif_html": _atif_html(fotografci, profil),
            "tetik_url": _tetik_url(str(alan(baglantilar, "download_location", "")), anahtar),
            "renk": str(alan(foto, "color", "")).strip() or None,
        }
        return Aday(
            kaynak=self.ad,
            kimlik=str(alan(foto, "id", "")),
            baslik=metin_temizle(alan(foto, "alt_description", "") or alan(foto, "description", ""), 120) or "unsplash",
            genislik=genislik,
            yukseklik=yukseklik,
            lisans_adi=self.lisans_adi,
            lisans_sinifi=self.lisans_sinifi,
            sayfa_url=str(alan(baglantilar, "html", "")),
            varyantlar=varyantlar,
            fotografci=fotografci,
            profil_url=profil,
            risk_metni=metin_temizle(alan(foto, "alt_description", ""), 240),
            ek=ek,
        )

    def _istek(self, yol: str, anahtar: str | None) -> Any:
        if not anahtar:
            raise AracHatasi(CIKIS_ANAHTAR, "Unsplash anahtarı yok (UNSPLASH_ACCESS_KEY).")
        veri, _ = json_istek(f"{yol}", self._basliklar(anahtar))
        return veri

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        if not anahtar:
            raise AracHatasi(CIKIS_ANAHTAR, "Unsplash anahtarı yok (UNSPLASH_ACCESS_KEY).")
        parametreler: dict[str, Any] = {
            "query": istek.konu,
            "page": istek.sayfa,
            "per_page": min(max(istek.adet * 2, 6), 30),
            "order_by": "relevant",
            "content_filter": "high",
        }
        if istek.yon in YON_ESLEME:
            parametreler["orientation"] = YON_ESLEME[istek.yon]
        url = f"{taban}/search/photos?{urllib.parse.urlencode(parametreler)}"
        veri = self._istek(url, anahtar)
        adaylar = [self._aday(foto, anahtar) for foto in liste(veri, "results")]
        return [aday for aday in adaylar if aday is not None]

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        if not anahtar:
            raise AracHatasi(CIKIS_ANAHTAR, "Unsplash anahtarı yok (UNSPLASH_ACCESS_KEY).")
        veri = self._istek(f"{taban}/photos/{urllib.parse.quote(kimlik)}", anahtar)
        aday = self._aday(veri, anahtar)
        if aday is None:
            raise AracHatasi(CIKIS_BULUNAMADI, "Unsplash fotoğrafı bulunamadı.")
        return aday


KAYNAK = UnsplashKaynak()