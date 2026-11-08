"""credits.json v2: okuma, v1 göçü, yazma, kayıt ve onay işlemleri."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .hata import AracHatasi
from .model import Aday
from .ortak import atomik_yaz, metin_temizle, simdi_iso
from .sabitler import CIKIS_BULUNAMADI, CIKIS_DOGRULAMA, LISANS_SERBEST_TICARI, MANIFEST_ADI

MANIFEST_SURUM = 2
ONAY_BEKLIYOR = "manuel_dogrulama_gerekli"


def bos_manifest() -> dict[str, Any]:
    """Yeni boş v2 manifest üretir."""
    zaman = simdi_iso()
    return {"surum": MANIFEST_SURUM, "olusturma": zaman, "guncelleme": zaman, "kayitlar": []}


def _v1_goc(eski: dict[str, Any]) -> dict[str, Any]:
    kayitlar: list[dict[str, Any]] = []
    for ham in eski.get("fotograflar", []):
        if not isinstance(ham, dict):
            continue
        fotografci = ham.get("fotografci") if isinstance(ham.get("fotografci"), dict) else {}
        dosyalar = []
        for ham_dosya in ham.get("dosyalar", []):
            if not isinstance(ham_dosya, dict):
                continue
            dosyalar.append({
                "yol": str(ham_dosya.get("dosya") or ""),
                "genislik": int(ham_dosya.get("genislik") or 0),
                "bayt": 0,
                "bicim": str(ham.get("bicim") or ""),
            })
        kayitlar.append({
            "kaynak": "unsplash",
            "kimlik": str(ham.get("id") or ""),
            "ad": str(ham.get("ad") or ""),
            "baslik": metin_temizle(ham.get("aciklama"), 120),
            "lisans": str(ham.get("lisans") or "Unsplash License"),
            "lisans_sinifi": LISANS_SERBEST_TICARI,
            "sayfa_url": str(ham.get("fotograf_sayfasi") or ""),
            "fotografci": {
                "ad": str(fotografci.get("ad") or ""),
                "profil": str(fotografci.get("profil_url") or ""),
            },
            "dosyalar": dosyalar,
            "atif_html": str(ham.get("atif_html") or ""),
            "ticari_durum": str(ham.get("ticari_durum") or ONAY_BEKLIYOR),
            "ticari_onay": ham.get("ticari_onay") if isinstance(ham.get("ticari_onay"), dict) else {},
            "kayit_zamani": str(ham.get("indirme_tarihi") or simdi_iso()),
            "goc": "v1",
        })
    manifest = bos_manifest()
    manifest["kayitlar"] = kayitlar
    return manifest


def _kayit_normalize(ham: Any) -> dict[str, Any] | None:
    if not isinstance(ham, dict):
        return None
    kaynak = str(ham.get("kaynak") or "")
    kimlik = str(ham.get("kimlik") or "")
    ad = str(ham.get("ad") or "")
    if not kaynak or not kimlik or not ad:
        return None
    kayit = dict(ham)
    kayit["kaynak"] = kaynak
    kayit["kimlik"] = kimlik
    kayit["ad"] = ad
    if not isinstance(kayit.get("dosyalar"), list):
        kayit["dosyalar"] = []
    if not isinstance(kayit.get("ticari_onay"), dict):
        kayit["ticari_onay"] = {}
    return kayit


def manifest_oku(klasor: Path) -> tuple[dict[str, Any], str | None]:
    """credits.json'ı okur; bozuksa yedekler ve yeni manifest döndürür."""
    yol = klasor / MANIFEST_ADI
    if not yol.is_file():
        return bos_manifest(), None
    try:
        veri = json.loads(yol.read_text(encoding="utf-8"))
    except (OSError, ValueError) as hata:
        return _bozuk_yedekle(yol, hata)
    if not isinstance(veri, dict):
        return _bozuk_yedekle(yol, ValueError("manifest nesne değil"))
    if isinstance(veri.get("fotograflar"), list):
        return _v1_goc(veri), "credits.json v1 biçimi v2'ye göç edildi; kayıtlar korundu."
    kayitlar = [kayit for kayit in (_kayit_normalize(ham) for ham in veri.get("kayitlar", [])) if kayit]
    manifest = bos_manifest()
    manifest["olusturma"] = str(veri.get("olusturma") or manifest["olusturma"])
    manifest["kayitlar"] = kayitlar
    return manifest, None


def _bozuk_yedekle(yol: Path, hata: Exception) -> tuple[dict[str, Any], str | None]:
    yedek = yol.with_name(f"{MANIFEST_ADI}.bozuk-{simdi_iso().replace(':', '').replace('-', '')[:15]}")
    try:
        yol.replace(yedek)
    except OSError as yedek_hatasi:
        raise AracHatasi(
            CIKIS_DOGRULAMA, "Bozuk credits.json yedeklenemedi; dosyayı elle kontrol edin."
        ) from yedek_hatasi
    return bos_manifest(), f"Bozuk credits.json yedeklendi: {yedek.name} ({type(hata).__name__})."


def manifest_yaz(klasor: Path, manifest: dict[str, Any]) -> None:
    """Manifesti atomik olarak yazar."""
    veri = {
        "surum": MANIFEST_SURUM,
        "olusturma": str(manifest.get("olusturma") or simdi_iso()),
        "guncelleme": simdi_iso(),
        "kayitlar": [kayit for kayit in manifest.get("kayitlar", []) if isinstance(kayit, dict)],
    }
    gorunum = (json.dumps(veri, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    atomik_yaz(klasor / MANIFEST_ADI, gorunum)


def kayit_bul(
    manifest: dict[str, Any],
    kaynak: str | None = None,
    kimlik: str | None = None,
    ad: str | None = None,
) -> dict[str, Any] | None:
    """Kaydı kaynak+kimlik veya ad ile bulur."""
    for kayit in manifest.get("kayitlar", []):
        if not isinstance(kayit, dict):
            continue
        if kimlik is not None and kaynak is not None:
            if kayit.get("kaynak") == kaynak and str(kayit.get("kimlik")) == str(kimlik):
                return kayit
        elif ad is not None and kayit.get("ad") == ad:
            return kayit
    return None


def kayit_ekle(manifest: dict[str, Any], kayit: dict[str, Any]) -> dict[str, Any]:
    """Aynı kaynak+kimlik kaydını günceller, yoksa sona ekler."""
    mevcut = kayit_bul(manifest, kayit.get("kaynak"), kayit.get("kimlik"))
    if mevcut is not None:
        mevcut.clear()
        mevcut.update(kayit)
        return mevcut
    manifest.setdefault("kayitlar", []).append(kayit)
    return kayit


def ad_benzersiz(manifest: dict[str, Any], istenen: str, kaynak: str, kimlik: str) -> str:
    """Aynı adı başka görsel kullanıyorsa sonuna sayı ekler."""
    sahip = kayit_bul(manifest, ad=istenen)
    if sahip is None or (sahip.get("kaynak") == kaynak and str(sahip.get("kimlik")) == str(kimlik)):
        return istenen
    sira = 2
    while True:
        aday = f"{istenen}-{sira}"
        sahip = kayit_bul(manifest, ad=aday)
        if sahip is None or (sahip.get("kaynak") == kaynak and str(sahip.get("kimlik")) == str(kimlik)):
            return aday
        sira += 1


def onay_yaz(
    manifest: dict[str, Any],
    karar: dict[str, str],
    durum: str,
    kaynak: str | None = None,
    kimlik: str | None = None,
    ad: str | None = None,
) -> dict[str, Any]:
    """Ticari onay kararını kayda işler."""
    kayit = kayit_bul(manifest, kaynak, kimlik, ad)
    if kayit is None:
        raise AracHatasi(CIKIS_BULUNAMADI, "Kayıt bulunamadı; önce indir veya --ad ile mevcut kaydı seç.")
    kayit["ticari_durum"] = durum
    kayit["ticari_onay"] = karar
    return kayit


def kayit_uret(
    aday: Aday,
    ad: str,
    dosyalar: list[dict[str, Any]],
    atif_html: str | None,
    ticari: dict[str, Any],
    lisans_url: str = "",
) -> dict[str, Any]:
    """İndirme sonucundan v2 kayıt sözlüğü üretir."""
    return {
        "kaynak": aday.kaynak,
        "kimlik": str(aday.kimlik),
        "ad": ad,
        "baslik": metin_temizle(aday.baslik, 120),
        "lisans": aday.lisans_adi,
        "lisans_sinifi": aday.lisans_sinifi,
        "lisans_url": lisans_url,
        "sayfa_url": aday.sayfa_url,
        "fotografci": {"ad": aday.fotografci, "profil": aday.profil_url},
        "dosyalar": dosyalar,
        "atif_html": atif_html or "",
        "ticari_degerlendirme": ticari,
        "ticari_durum": ONAY_BEKLIYOR,
        "ticari_onay": {},
        "kayit_zamani": simdi_iso(),
    }


def onaysiz_kayitlar(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Ticari onayı tamamlanmamış kayıtları döndürür."""
    return [
        kayit for kayit in manifest.get("kayitlar", [])
        if isinstance(kayit, dict) and kayit.get("ticari_durum") not in ("onaylandi", "reddedildi")
    ]


def eksik_dosyalar(manifest: dict[str, Any]) -> list[str]:
    """Manifestte kayıtlı olup diskte bulunmayan dosya yollarını döndürür."""
    eksik = []
    for kayit in manifest.get("kayitlar", []):
        if not isinstance(kayit, dict):
            continue
        for dosya in kayit.get("dosyalar", []):
            if not isinstance(dosya, dict):
                continue
            yol = str(dosya.get("yol") or "")
            if not yol:
                continue
            hedef = Path(yol)
            if not hedef.is_absolute():
                hedef = Path.cwd() / hedef
            if not hedef.is_file():
                eksik.append(yol)
    return eksik