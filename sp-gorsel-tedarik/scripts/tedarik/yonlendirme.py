"""Kategoriye göre kaynak yönlendirmesi ve otomatik kaynak seçimi."""

from __future__ import annotations

KATEGORI_KAYNAKLARI: dict[str, tuple[str, ...]] = {
    "genel": ("pexels", "pixabay", "openverse", "unsplash", "wikimedia"),
    "kurumsal": ("pexels", "pixabay", "unsplash", "openverse"),
    "sanat": ("met", "artic", "smithsonian", "cooperhewitt", "openverse", "wikimedia"),
    "bilim-uzay": ("nasa", "smithsonian", "openverse"),
    "doku-3b": ("polyhaven", "openverse"),
    "tarih": ("wikimedia", "flickr", "openverse", "smithsonian"),
}

AZAMI_OTOMATIK_KAYNAK = 2


def kaynak_sirasi(kategori: str) -> tuple[str, ...]:
    """Kategori için öncelik sırasını döndürür; bilinmeyen kategoride genel sıra."""
    return KATEGORI_KAYNAKLARI.get(kategori, KATEGORI_KAYNAKLARI["genel"])


def otomatik_sec(kategori: str, kullanilabilir: set[str]) -> tuple[str, ...]:
    """Sıradan, kullanılabilir ilk en fazla iki kaynağı seçer."""
    secilen = [ad for ad in kaynak_sirasi(kategori) if ad in kullanilabilir]
    return tuple(secilen[:AZAMI_OTOMATIK_KAYNAK])