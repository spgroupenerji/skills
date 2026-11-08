"""Yerel renk analizi: baskın renk, palet ve WCAG kontrastı (Pillow opsiyonel)."""

from __future__ import annotations

import io
import re
from typing import Any

from .sabitler import WCAG_AA_ESIGI

_PIL: Any = None


def _pil() -> Any | None:
    global _PIL
    if _PIL is None:
        try:
            from PIL import Image
            _PIL = Image
        except ImportError:
            _PIL = False
    return _PIL or None


def hex_coz(deger: str) -> tuple[int, int, int] | None:
    """#rrggbb veya #rgb değerini RGB'ye çevirir."""
    temiz = (deger or "").strip().lstrip("#")
    if re.fullmatch(r"[0-9a-fA-F]{3}", temiz):
        temiz = "".join(harf * 2 for harf in temiz)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", temiz):
        return None
    return (int(temiz[0:2], 16), int(temiz[2:4], 16), int(temiz[4:6], 16))


def parlaklik(rgb: tuple[int, int, int]) -> float:
    """WCAG bağıl parlaklığı (0-1)."""
    kanallar = []
    for deger in rgb:
        oran = deger / 255
        kanallar.append(oran / 12.92 if oran <= 0.03928 else ((oran + 0.055) / 1.055) ** 2.4)
    return 0.2126 * kanallar[0] + 0.7152 * kanallar[1] + 0.0722 * kanallar[2]


def kontrast_orani(bir: str, iki: str) -> float:
    """İki renk arasındaki WCAG kontrast oranını döndürür."""
    rgb_bir = hex_coz(bir)
    rgb_iki = hex_coz(iki)
    if rgb_bir is None or rgb_iki is None:
        return 0.0
    acik, koyu = sorted((parlaklik(rgb_bir), parlaklik(rgb_iki)), reverse=True)
    return round((acik + 0.05) / (koyu + 0.05), 2)


def metin_onerisi(baskin: str) -> dict[str, Any]:
    """Baskın renk üzerine okunabilir metin rengi ve WCAG durumu önerir."""
    adaylar = {"#ffffff": kontrast_orani(baskin, "#ffffff"), "#111111": kontrast_orani(baskin, "#111111")}
    secilen = max(adaylar, key=lambda renk: adaylar[renk])
    return {
        "renk": secilen,
        "kontrast": adaylar[secilen],
        "wcag_aa": adaylar[secilen] >= WCAG_AA_ESIGI,
    }


def renk_analizi(govde: bytes) -> dict[str, Any]:
    """Görsel baytlarından baskın renk, palet ve metin önerisi üretir."""
    Image = _pil()
    if Image is None:
        return {"durum": "atlandi", "neden": "Pillow yok"}
    try:
        with Image.open(io.BytesIO(govde)) as resim:
            kucuk = resim.convert("RGB")
            kucuk.thumbnail((192, 192))
            palet = _palet(kucuk)
    except (OSError, ValueError) as hata:
        return {"durum": "atlandi", "neden": str(hata)[:120]}
    if not palet:
        return {"durum": "atlandi", "neden": "renk çıkarılamadı"}
    return {"durum": "ok", "baskin": palet[0], "palet": palet, "metin": metin_onerisi(palet[0])}


def _palet(resim: Any) -> list[str]:
    kuantal = resim.quantize(colors=5)
    palet_veri = list(kuantal.getpalette() or [])
    adetler = kuantal.getcolors(192 * 192) or []
    if not palet_veri:
        return []
    sonuc = []
    for _adet, indeks in sorted(adetler, reverse=True)[:5]:
        baslangic = indeks * 3
        if baslangic + 2 >= len(palet_veri):
            continue
        kirmizi, yesil, mavi = palet_veri[baslangic:baslangic + 3]
        sonuc.append(f"#{kirmizi:02x}{yesil:02x}{mavi:02x}")
    return sonuc
