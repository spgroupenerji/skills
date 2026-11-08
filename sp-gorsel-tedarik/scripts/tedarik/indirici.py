"""İndirme planı, görsel işleme, srcset ve atıf HTML üretimi."""

from __future__ import annotations

import io
from pathlib import Path
from typing import Any

from .hata import AracHatasi
from .model import Aday, Varyant
from .ortak import atomik_yaz, gorsel_dogrula, host_guvenli, html_kacir, ikili_istek
from .sabitler import AZAMI_GORSEL_BAYT, BICIMLER, CIKIS_DOGRULAMA, CIKIS_KULLANIM, VARSAYILAN_KALITE

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


def cevirici_var() -> bool:
    """Pillow ile yeniden boyutlandırma/biçim dönüşümü yapılabilir mi?"""
    return _pil() is not None


def varyant_sec(varyantlar: tuple[Varyant, ...], genislik: int) -> Varyant:
    """İstenen genişliği karşılayan en küçük varyantı, yoksa en büyüğü seçer."""
    uygun = [varyant for varyant in varyantlar if varyant.genislik >= genislik]
    if uygun:
        return min(uygun, key=lambda varyant: varyant.genislik)
    return max(varyantlar, key=lambda varyant: varyant.genislik)


def plan_olustur(
    aday: Aday, genislikler: tuple[int, ...], bicim: str
) -> tuple[list[dict[str, Any]], list[str]]:
    """İstenen genişlikler için indirme planı ve uyarıları üretir."""
    if bicim not in BICIMLER:
        raise AracHatasi(CIKIS_KULLANIM, "Biçim webp, jpg veya png olmalı.")
    if not aday.varyantlar:
        raise AracHatasi(CIKIS_DOGRULAMA, "Adayın indirilebilir varyantı yok.")
    cevirebilir = cevirici_var()
    uyarilar: list[str] = []
    plan: list[dict[str, Any]] = []
    gorulen: set[tuple[int, str]] = set()
    for genislik in genislikler:
        varyant = varyant_sec(aday.varyantlar, genislik)
        hedef_genislik = genislik
        if varyant.genislik and varyant.genislik < genislik:
            hedef_genislik = varyant.genislik
            uyarilar.append(f"{genislik}px kaynakta yok; {varyant.genislik}px kullanıldı.")
        hedef_bicim = bicim
        if not cevirebilir and varyant.bicim != bicim:
            hedef_bicim = varyant.bicim
            uyarilar.append("Pillow yok: biçim dönüşümü yapılamadı, kaynak biçimi kullanıldı.")
        anahtar = (hedef_genislik, hedef_bicim)
        if anahtar in gorulen:
            continue
        gorulen.add(anahtar)
        plan.append({"hedef_genislik": hedef_genislik, "hedef_bicim": hedef_bicim, "varyant": varyant})
    return plan, _tekille(uyarilar)


def _govde_indir(url: str, gorsel_hostlari: tuple[str, ...]) -> bytes:
    if not host_guvenli(url, gorsel_hostlari):
        raise AracHatasi(CIKIS_DOGRULAMA, "Görsel URL'si izinli host'larda değil.", url)
    govde, _ = ikili_istek(url, None, azami_bayt=AZAMI_GORSEL_BAYT)
    gorsel_dogrula(govde)
    return govde


def gorsel_isle(
    govde: bytes, hedef_bicim: str, hedef_genislik: int, kalite: int, varyant: Varyant
) -> tuple[bytes, str, int, int]:
    """Gerekliyse yeniden boyutlandırır/biçim dönüştürür; aksi halde baytları korur."""
    tur = gorsel_dogrula(govde)
    Image = _pil()
    gereksiz = tur == hedef_bicim and (not hedef_genislik or varyant.genislik <= hedef_genislik)
    if Image is None:
        return govde, tur, varyant.genislik, int(varyant.yukseklik or 0)
    if gereksiz:
        with Image.open(io.BytesIO(govde)) as olcu:
            return govde, tur, olcu.width, olcu.height
    with Image.open(io.BytesIO(govde)) as resim:
        resim = _yon_duzelt(resim)
        if hedef_genislik and resim.width > hedef_genislik:
            oran = hedef_genislik / resim.width
            resim = resim.resize((hedef_genislik, max(1, round(resim.height * oran))), Image.LANCZOS)
        cikti = io.BytesIO()
        if hedef_bicim == "webp":
            resim.save(cikti, format="WEBP", quality=kalite, method=6)
        elif hedef_bicim == "png":
            resim.save(cikti, format="PNG", optimize=True)
        else:
            resim.convert("RGB").save(cikti, format="JPEG", quality=kalite, optimize=True, progressive=True)
        return cikti.getvalue(), hedef_bicim, resim.width, resim.height


def _yon_duzelt(resim: Any) -> Any:
    try:
        from PIL import ImageOps
        return ImageOps.exif_transpose(resim)
    except Exception:
        return resim


def indir(
    plan: list[dict[str, Any]],
    klasor: Path,
    ad: str,
    kalite: int,
    uzerine_yaz: bool,
    gorsel_hostlari: tuple[str, ...],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Planı indirir, dönüştürür ve dosya bilgilerini döndürür."""
    uyarilar: list[str] = []
    onbellek: dict[str, bytes] = {}
    dosyalar: list[dict[str, Any]] = []
    for adim in plan:
        varyant: Varyant = adim["varyant"]
        hedef_genislik = int(adim["hedef_genislik"])
        hedef_bicim = str(adim["hedef_bicim"])
        dosya = klasor / f"{ad}-{hedef_genislik}.{_uzanti(hedef_bicim)}"
        if dosya.is_file() and not uzerine_yaz:
            dosyalar.append(_dosya_bilgisi(dosya, hedef_genislik, hedef_bicim))
            continue
        govde = onbellek.get(varyant.url)
        if govde is None:
            govde = _govde_indir(varyant.url, gorsel_hostlari)
            onbellek[varyant.url] = govde
        ham, bicim, genislik, yukseklik = gorsel_isle(govde, hedef_bicim, hedef_genislik, kalite, varyant)
        if bicim != _uzanti(hedef_bicim):
            dosya = dosya.with_suffix(f".{_uzanti(bicim)}")
            uyarilar.append(f"{hedef_bicim} yazılamadı; {bicim} kaydedildi.")
        atomik_yaz(dosya, ham)
        dosyalar.append({
            "yol": _goreli(dosya),
            "genislik": genislik,
            "yukseklik": yukseklik,
            "bayt": len(ham),
            "bicim": bicim,
        })
    return dosyalar, _tekille(uyarilar)


def _dosya_bilgisi(dosya: Path, genislik: int, bicim: str) -> dict[str, Any]:
    return {
        "yol": _goreli(dosya),
        "genislik": genislik,
        "yukseklik": 0,
        "bayt": dosya.stat().st_size,
        "bicim": _uzanti(bicim),
    }


def _uzanti(bicim: str) -> str:
    return "jpg" if bicim in ("jpg", "jpeg") else bicim


def _goreli(dosya: Path) -> str:
    try:
        return dosya.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return dosya.as_posix()


def _tekille(degerler: list[str]) -> list[str]:
    return list(dict.fromkeys(degerler))


def srcset_uret(dosyalar: list[dict[str, Any]]) -> str:
    """srcset niteliği üretir."""
    return ", ".join(f"{dosya['yol']} {dosya['genislik']}w" for dosya in dosyalar)


def img_etiketleri(dosyalar: list[dict[str, Any]], alt: str, aday: Aday) -> dict[str, Any]:
    """HTML img niteliklerini üretir; LCP görselinde çağıran eager/fetchpriority ekler."""
    if not dosyalar:
        raise AracHatasi(CIKIS_DOGRULAMA, "İndirilmiş dosya yok.")
    buyuk = max(dosyalar, key=lambda dosya: int(dosya["genislik"]))
    genislik = int(buyuk["genislik"])
    yukseklik = int(buyuk.get("yukseklik") or 0)
    if not yukseklik and aday.genislik:
        yukseklik = round(genislik * aday.yukseklik / aday.genislik)
    return {
        "src": buyuk["yol"],
        "srcset": srcset_uret(dosyalar),
        "width": genislik,
        "height": yukseklik,
        "alt": alt,
        "loading": "lazy",
        "decoding": "async",
    }


def atif_html_uret(aday: Aday, kaynak_adi: str, atif_zorunlu: bool) -> str | None:
    """Kaynağa uygun görünür atıf paragrafı üretir."""
    ozel = aday.ek.get("atif_html")
    if isinstance(ozel, str) and ozel.strip():
        return ozel.strip()
    parcalar = []
    if aday.fotografci and aday.profil_url:
        parcalar.append(f'<a href="{html_kacir(aday.profil_url)}">{html_kacir(aday.fotografci)}</a>')
    if aday.sayfa_url:
        parcalar.append(f'<a href="{html_kacir(aday.sayfa_url)}">{html_kacir(kaynak_adi)}</a>')
    if not parcalar:
        return None
    if not atif_zorunlu and not aday.fotografci:
        return None
    return f'<p class="fotograf-atif">Fotoğraf: {" / ".join(parcalar)}</p>'