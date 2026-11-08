"""Ticari güvenlik: lisans engeli, içerik riski heuristiği ve onay kaydı."""

from __future__ import annotations

import re
from typing import Any

from .hata import AracHatasi
from .model import Aday
from .ortak import metin_temizle, turkce_kucult
from .sabitler import (
    CIKIS_KULLANIM,
    CIKIS_TICARI,
    KULLANIM_EDITORIAL,
    LISANS_KOSULLU,
    TICARI_ENGELLI,
    TICARI_MANUEL,
    TICARI_ONAY_UYGUN,
    TICARI_ONAY_UYGUN_DEGIL,
    TICARI_UYGUN,
)

RISK_TERIMLERI: dict[str, tuple[str, ...]] = {
    "insan": (
        "man", "woman", "person", "people", "child", "kid", "face", "portrait",
        "selfie", "group", "team", "businessman", "family", "hands", "insan",
        "kisi", "cocuk", "yuz", "portre", "grup", "ekip", "aile", "eller",
    ),
    "marka": (
        "logo", "brand", "trademark", "billboard", "storefront", "marka",
        "tabela", "urun", "apple", "google", "microsoft", "nike", "samsung",
        "tesla", "coca", "pepsi", "adidas", "starbucks", "ikea",
    ),
    "eser": (
        "painting", "artwork", "sculpture", "mural", "graffiti", "statue",
        "eser", "heykel", "duvar-resmi", "sanat-eseri",
    ),
    "hassas": (
        "gun", "weapon", "violence", "blood", "nude", "naked", "drug",
        "smoking", "alcohol", "gambling", "politics", "religion", "military",
        "police", "money", "medical", "silah", "siddet", "kan", "ciplak",
        "uyusturucu", "sigara", "alkol", "kumar", "siyaset", "din", "asker",
        "polis", "para", "tibbi",
    ),
}

_TICARI_ONAY_KARARLARI = (TICARI_ONAY_UYGUN, TICARI_ONAY_UYGUN_DEGIL)


def riskleri_bul(metin: str) -> list[str]:
    """Metindeki risk kategorilerini kelime eşleşmesiyle döndürür."""
    kucuk = turkce_kucult(metin)
    kelimeler = {parca for parca in re.split(r"[^a-z0-9]+", kucuk) if parca}
    bulunan: list[str] = []
    for kategori, terimler in RISK_TERIMLERI.items():
        if any(terim in kelimeler or terim in kucuk for terim in terimler):
            bulunan.append(kategori)
    return bulunan


def ticari_degerlendir(aday: Aday) -> dict[str, Any]:
    """Adayı ticari kullanım açısından sınıflandırır."""
    if aday.lisans_sinifi == LISANS_KOSULLU:
        return {"durum": TICARI_ENGELLI, "riskler": ["lisans kosullu"]}
    engel = str(aday.ek.get("engel") or "").strip()
    if engel:
        return {"durum": TICARI_ENGELLI, "riskler": [engel]}
    metin = " ".join((aday.risk_metni, aday.baslik, aday.aciklama))
    riskler = riskleri_bul(metin)
    if riskler:
        return {"durum": TICARI_MANUEL, "riskler": riskler}
    return {"durum": TICARI_UYGUN, "riskler": []}


def kapi(degerlendirme: dict[str, Any]) -> None:
    """Engelli adayı indirme aşamasında durdurur."""
    if degerlendirme.get("durum") != TICARI_ENGELLI:
        return
    riskler = ", ".join(str(risk) for risk in degerlendirme.get("riskler", []))
    raise AracHatasi(CIKIS_TICARI, f"Ticari risk: görsel indirilmedi ({riskler or 'engel'}).")


def onay_kaydi(karar: str, onaylayan: str, not_metni: str) -> dict[str, str]:
    """Görsel denetim onayını doğrular ve kayıt sözlüğü üretir."""
    if karar not in _TICARI_ONAY_KARARLARI:
        raise AracHatasi(CIKIS_KULLANIM, f"--karar {TICARI_ONAY_UYGUN} veya {TICARI_ONAY_UYGUN_DEGIL} olmalı.")
    onaylayan_temiz = metin_temizle(onaylayan, 80)
    if not onaylayan_temiz:
        raise AracHatasi(CIKIS_KULLANIM, "--onaylayan zorunlu (denetimi yapan kişi).")
    from .ortak import simdi_iso

    return {
        "karar": karar,
        "onaylayan": onaylayan_temiz,
        "tarih": simdi_iso(),
        "not": metin_temizle(not_metni, 240),
    }


def onay_durumu(karar: str) -> str:
    """Onay kararını kayıt durumuna çevirir."""
    return "onaylandi" if karar == TICARI_ONAY_UYGUN else "reddedildi"
