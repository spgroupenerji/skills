"""Adaptör yardımcıları: güvenli alan erişimi, varyant üretimi, görsel boyut okuma."""

from __future__ import annotations

import re
import struct
import urllib.parse
from typing import Any

from ..hata import AracHatasi
from ..model import Varyant
from ..ortak import host_guvenli, ikili_istek
from ..sabitler import CIKIS_API


def alan(veri: Any, anahtar: str, varsayilan: Any = None) -> Any:
    """Sözlükten güvenli alan okur."""
    if not isinstance(veri, dict):
        return varsayilan
    deger = veri.get(anahtar)
    return varsayilan if deger is None else deger


def liste(veri: Any, anahtar: str) -> list[Any]:
    """Sözlükteki listeyi, yoksa boş listeyi döndürür."""
    deger = alan(veri, anahtar)
    return deger if isinstance(deger, list) else []


def sozluk(veri: Any, anahtar: str) -> dict[str, Any]:
    """Sözlükteki iç sözlüğü, yoksa boş sözlüğü döndürür."""
    deger = alan(veri, anahtar)
    return deger if isinstance(deger, dict) else {}


def tam_sayi(deger: Any, varsayilan: int = 0) -> int:
    """Değeri güvenli biçimde tam sayıya çevirir."""
    try:
        return int(float(deger))
    except (TypeError, ValueError):
        return varsayilan


def metin_html_temizle(veri: Any, sinir: int = 240) -> str:
    """HTML etiketlerini söker, boşlukları toparlar."""
    metin = re.sub(r"<[^>]+>", " ", str(veri or ""))
    return re.sub(r"\s+", " ", metin).strip()[:sinir]


def bicim_tahmin(url: str, varsayilan: str = "jpg") -> str:
    """URL uzantısından görsel biçimini tahmin eder."""
    yol = urllib.parse.urlsplit(url).path.lower()
    for uzanti, bicim in ((".webp", "webp"), (".png", "png"), (".jpg", "jpg"), (".jpeg", "jpg"), (".jfif", "jpg")):
        if yol.endswith(uzanti):
            return bicim
    return varsayilan


def varyantlari_uret(
    adaylar: list[tuple[int, str, str | None]],
    izinli: tuple[str, ...],
    yukseklikler: dict[int, int] | None = None,
) -> tuple[Varyant, ...]:
    """URL/izin doğrulaması yapıp tekrarsız, büyükten küçüğe varyant listesi üretir."""
    gorulen: set[tuple[int, str]] = set()
    sonuc: list[Varyant] = []
    for genislik, url, bicim in adaylar:
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            continue
        if not host_guvenli(url, izinli):
            continue
        tur = bicim or bicim_tahmin(url)
        anahtar = (int(genislik), tur)
        if anahtar in gorulen:
            continue
        gorulen.add(anahtar)
        sonuc.append(Varyant(int(genislik), url, tur, (yukseklikler or {}).get(int(genislik))))
    sonuc.sort(key=lambda varyant: varyant.genislik, reverse=True)
    return tuple(sonuc)


def boyut_sniff(url: str, izinli: tuple[str, ...]) -> tuple[int, int]:
    """Görselin ilk baytlarından genişlik/yükseklik okur (en fazla 256 KB)."""
    try:
        govde, _ = ikili_istek(url, None, azami_bayt=256 * 1024, hata_kodu=CIKIS_API, kes=True)
    except AracHatasi:
        return (0, 0)
    return _boyut_ayikla(govde)


def _boyut_ayikla(govde: bytes) -> tuple[int, int]:
    if govde.startswith(b"\x89PNG\r\n\x1a\n") and len(govde) >= 24:
        return (struct.unpack(">I", govde[16:20])[0], struct.unpack(">I", govde[20:24])[0])
    if govde[:4] == b"RIFF" and govde[8:12] == b"WEBP":
        return _webp_boyut(govde)
    if govde.startswith(b"\xff\xd8"):
        return _jpeg_boyut(govde)
    return (0, 0)


def _jpeg_boyut(govde: bytes) -> tuple[int, int]:
    sira = 2
    while sira + 9 < len(govde):
        if govde[sira] != 0xFF:
            sira += 1
            continue
        isaret = govde[sira + 1]
        if isaret in (0xD8, 0xD9) or 0xD0 <= isaret <= 0xD7:
            sira += 2
            continue
        if sira + 4 > len(govde):
            return (0, 0)
        uzunluk = struct.unpack(">H", govde[sira + 2: sira + 4])[0]
        if 0xC0 <= isaret <= 0xCF and isaret not in (0xC4, 0xC8, 0xCC):
            if sira + 9 <= len(govde):
                yukseklik, genislik = struct.unpack(">HH", govde[sira + 5: sira + 9])
                return (genislik, yukseklik)
            return (0, 0)
        sira += 2 + uzunluk
    return (0, 0)


def _webp_boyut(govde: bytes) -> tuple[int, int]:
    parca = govde[12:16]
    if parca == b"VP8X" and len(govde) >= 30:
        return (1 + int.from_bytes(govde[24:27], "little"), 1 + int.from_bytes(govde[27:30], "little"))
    if parca == b"VP8 " and len(govde) >= 30:
        genislik, yukseklik = struct.unpack("<HH", govde[26:30])
        return (genislik & 0x3FFF, yukseklik & 0x3FFF)
    if parca == b"VP8L" and len(govde) >= 25:
        bitler = int.from_bytes(govde[21:25], "little")
        return ((bitler & 0x3FFF) + 1, ((bitler >> 14) & 0x3FFF) + 1)
    return (0, 0)