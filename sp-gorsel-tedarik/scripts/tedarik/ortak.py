"""Ortak yardımcılar: HTTP, URL güvenliği, dosya, metin, .env ve görsel imzası."""

from __future__ import annotations

import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any

from .hata import AracHatasi
from .sabitler import (
    AZAMI_JSON_BAYT,
    CIKIS_API,
    CIKIS_ANAHTAR,
    CIKIS_BULUNAMADI,
    CIKIS_DOGRULAMA,
    CIKIS_KULLANIM,
    GERI_CEKILME,
    ISTEMCI_AJANI,
    SLUG_AZAMI,
    SLUG_YEDEK,
    UTM_UYGULAMA,
    YENIDEN_DENEME,
    YEREL_HOSTLAR,
    ZAMAN_ASIMI,
)

_TURKCE_HARITA = str.maketrans({
    "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g", "ı": "i", "İ": "i",
    "ö": "o", "Ö": "o", "ş": "s", "Ş": "s", "ü": "u", "Ü": "u",
})


class _DurumHatasi(Exception):
    """HTTP durum kodu taşıyan iç istisna (yeniden deneme kararı için)."""

    def __init__(self, kod: int, govde: bytes, basliklar: dict[str, str]) -> None:
        super().__init__(f"HTTP {kod}")
        self.kod = kod
        self.govde = govde
        self.basliklar = basliklar


class _AgHatasi(Exception):
    """Ağ/timeout kaynaklı iç istisna."""


def turkce_kucult(metin: str) -> str:
    return (metin or "").translate(_TURKCE_HARITA).lower()


def slug_uret(metin: str, yedek: str = SLUG_YEDEK) -> str:
    temel = turkce_kucult(metin)
    temel = re.sub(r"[^a-z0-9]+", "-", temel).strip("-")
    if not temel:
        temel = yedek
    return temel[:SLUG_AZAMI].strip("-") or yedek


def simdi_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def html_kacir(metin: Any) -> str:
    return escape(str(metin or ""), quote=True)


def metin_temizle(metin: Any, sinir: int = 240) -> str:
    temiz = re.sub(r"\s+", " ", str(metin or "")).strip()
    return temiz[:sinir].strip()


def utm_ekle(url: str, uygulama: str = UTM_UYGULAMA) -> str:
    parca = urllib.parse.urlsplit(url)
    sorgu = urllib.parse.parse_qsl(parca.query, keep_blank_values=True)
    anahtarlar = {anahtar.lower() for anahtar, _ in sorgu}
    if "utm_source" not in anahtarlar:
        sorgu.append(("utm_source", uygulama))
    if "utm_medium" not in anahtarlar:
        sorgu.append(("utm_medium", "referral"))
    return urllib.parse.urlunsplit(
        (parca.scheme, parca.netloc, parca.path, urllib.parse.urlencode(sorgu), parca.fragment)
    )


def host_guvenli(url: str, izinli_hostlar: tuple[str, ...] = ()) -> bool:
    try:
        parca = urllib.parse.urlsplit(url)
    except ValueError:
        return False
    if parca.scheme not in ("https", "http") or not parca.hostname:
        return False
    host = parca.hostname.lower()
    if host in YEREL_HOSTLAR:
        return True
    if parca.scheme != "https":
        return False
    if not izinli_hostlar:
        return True
    for izin in izinli_hostlar:
        temiz = izin.lower().lstrip(".")
        if host == temiz or host.endswith("." + temiz):
            return True
    return False


def gorsel_tur_belirle(govde: bytes) -> str | None:
    if govde.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if govde.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if len(govde) >= 12 and govde[:4] == b"RIFF" and govde[8:12] == b"WEBP":
        return "webp"
    if govde.startswith(b"GIF8"):
        return "gif"
    return None


def gorsel_dogrula(govde: bytes) -> str:
    tur = gorsel_tur_belirle(govde)
    if tur is None:
        raise AracHatasi(CIKIS_DOGRULAMA, "Yanıt geçerli bir görsel değil (imza tanınmadı).")
    if len(govde) < 64:
        raise AracHatasi(CIKIS_DOGRULAMA, "Görsel yanıtı bozuk (çok kısa).")
    return tur


def atomik_yaz(hedef: Path, veri: bytes) -> None:
    hedef.parent.mkdir(parents=True, exist_ok=True)
    tanitici, gecici_ad = tempfile.mkstemp(prefix=".gorsel-", dir=str(hedef.parent))
    try:
        with os.fdopen(tanitici, "wb") as akis:
            akis.write(veri)
            akis.flush()
            os.fsync(akis.fileno())
        os.replace(gecici_ad, hedef)
    except BaseException:
        try:
            os.unlink(gecici_ad)
        except OSError:
            pass
        raise


def env_dosyasini_yukle(yol: str | Path | None) -> None:
    if not yol:
        return
    dosya = Path(yol)
    if not dosya.is_file():
        return
    for ham in dosya.read_text(encoding="utf-8", errors="replace").splitlines():
        satir = ham.strip()
        if not satir or satir.startswith("#") or "=" not in satir:
            continue
        anahtar, deger = satir.split("=", 1)
        anahtar = anahtar.strip()
        if anahtar.startswith("export "):
            anahtar = anahtar[len("export "):].strip()
        if not anahtar or anahtar in os.environ:
            continue
        os.environ[anahtar] = deger.strip().strip('"').strip("'")


def anahtar_ortamdan(ortam: str | None) -> str | None:
    if not ortam:
        return None
    deger = os.environ.get(ortam, "").strip()
    return deger or None


def taban_ortamdan(ortam: str, varsayilan: str) -> str:
    deger = os.environ.get(ortam, "").strip()
    return (deger or varsayilan).rstrip("/")


def kota_ayikla(basliklar: dict[str, str], adlar: tuple[str, ...]) -> dict[str, int]:
    sonuc: dict[str, int] = {}
    for ad in adlar:
        deger = basliklar.get(ad.lower(), "")
        if deger.isdigit():
            sonuc[ad] = int(deger)
    return sonuc


def _govde_ozeti(govde: bytes, sinir: int = 180) -> str | None:
    if not govde:
        return None
    metin = govde.decode("utf-8", errors="replace")
    temiz = metin_temizle(metin, sinir)
    return temiz or None


def _baslik_ayarla(ek: dict[str, str] | None, kabul: str) -> dict[str, str]:
    baslik = {"User-Agent": ISTEMCI_AJANI, "Accept": kabul}
    if ek:
        baslik.update({anahtar: deger for anahtar, deger in ek.items() if deger})
    return baslik


def _bekle(deneme: int, basliklar: dict[str, str]) -> None:
    ham = basliklar.get("retry-after", "")
    if ham.isdigit():
        time.sleep(min(int(ham), 30))
        return
    time.sleep(GERI_CEKILME[min(deneme, len(GERI_CEKILME) - 1)])


def _yeniden_denenir(kod: int) -> bool:
    return kod in (408, 429) or 500 <= kod <= 599


def _durum_hatasi(hata: _DurumHatasi, hata_kodu: int) -> AracHatasi:
    ozet = _govde_ozeti(hata.govde)
    if hata.kod == 400:
        return AracHatasi(CIKIS_KULLANIM, "İstek parametreleri geçersiz.", ozet)
    if hata.kod == 401:
        return AracHatasi(CIKIS_ANAHTAR, "API anahtarı geçersiz veya eksik.", ozet)
    if hata.kod == 403:
        return AracHatasi(CIKIS_API, "Erişim reddedildi (yetki veya hız limiti).", ozet)
    if hata.kod in (404, 410):
        return AracHatasi(CIKIS_BULUNAMADI, "Kayıt bulunamadı veya kaldırıldı.", ozet)
    if hata.kod == 429:
        return AracHatasi(CIKIS_API, "Hız limiti aşıldı; kısa süre sonra yeniden dene.", ozet)
    if 500 <= hata.kod <= 599:
        return AracHatasi(hata_kodu, f"Kaynak sunucusu hatası (HTTP {hata.kod}).", ozet)
    return AracHatasi(CIKIS_API, f"API hatası (HTTP {hata.kod}).", ozet)


def _tek_istek(url: str, basliklar: dict[str, str], azami_bayt: int, kes: bool = False) -> tuple[bytes, dict[str, str]]:
    istek = urllib.request.Request(url, headers=basliklar)
    try:
        with urllib.request.urlopen(istek, timeout=ZAMAN_ASIMI) as yanit:
            veri = yanit.read(azami_bayt + 1)
            baslik = {anahtar.lower(): deger for anahtar, deger in yanit.headers.items()}
    except urllib.error.HTTPError as hata:
        govde = hata.read(4096) if hata.fp else b""
        baslik = {anahtar.lower(): deger for anahtar, deger in (hata.headers or {}).items()}
        raise _DurumHatasi(hata.code, govde, baslik) from hata
    except (urllib.error.URLError, TimeoutError, OSError) as hata:
        raise _AgHatasi(str(hata)) from hata
    if len(veri) > azami_bayt:
        if not kes:
            raise AracHatasi(CIKIS_DOGRULAMA, f"Yanıt boyutu sınırı aştı ({azami_bayt} bayt).")
        veri = veri[:azami_bayt]
    return veri, baslik


def _istek(url: str, basliklar: dict[str, str], azami_bayt: int, hata_kodu: int, kes: bool = False) -> tuple[bytes, dict[str, str]]:
    if not host_guvenli(url):
        raise AracHatasi(CIKIS_DOGRULAMA, "Güvensiz veya desteklenmeyen URL.", url)
    son_hata = ""
    for deneme in range(YENIDEN_DENEME):
        try:
            return _tek_istek(url, basliklar, azami_bayt, kes)
        except _DurumHatasi as hata:
            son_hata = f"HTTP {hata.kod}"
            if not _yeniden_denenir(hata.kod) or deneme == YENIDEN_DENEME - 1:
                raise _durum_hatasi(hata, hata_kodu) from hata
            _bekle(deneme, hata.basliklar)
        except _AgHatasi as hata:
            son_hata = str(hata)
            if deneme == YENIDEN_DENEME - 1:
                raise AracHatasi(CIKIS_API, "Ağ hatası: istek tamamlanamadı.", son_hata[:180]) from hata
            time.sleep(GERI_CEKILME[min(deneme, len(GERI_CEKILME) - 1)])
    raise AracHatasi(CIKIS_API, "İstek tamamlanamadı.", son_hata[:180])


def json_istek(
    url: str,
    ek_basliklar: dict[str, str] | None = None,
    hata_kodu: int = CIKIS_API,
    azami_bayt: int = AZAMI_JSON_BAYT,
) -> tuple[Any, dict[str, str]]:
    govde, basliklar = _istek(url, _baslik_ayarla(ek_basliklar, "application/json"), azami_bayt, hata_kodu)
    try:
        veri = json.loads(govde.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as hata:
        raise AracHatasi(CIKIS_DOGRULAMA, "API yanıtı geçerli JSON değil.", str(hata)) from hata
    return veri, basliklar


def ikili_istek(
    url: str,
    ek_basliklar: dict[str, str] | None = None,
    *,
    azami_bayt: int,
    hata_kodu: int = CIKIS_API,
    kes: bool = False,
) -> tuple[bytes, dict[str, str]]:
    return _istek(url, _baslik_ayarla(ek_basliklar, "*/*"), azami_bayt, hata_kodu, kes)