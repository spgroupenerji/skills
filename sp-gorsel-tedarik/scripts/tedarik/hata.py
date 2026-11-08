"""Araç hataları: çıkış kodu taşıyan tek istisna türü."""

from __future__ import annotations


class AracHatasi(Exception):
    """Kullanıcıya tek satır mesajla bildirilen, çıkış kodu taşıyan hata."""

    def __init__(self, kod: int, mesaj: str, ayrinti: str | None = None) -> None:
        super().__init__(mesaj)
        self.kod = kod
        self.mesaj = mesaj
        self.ayrinti = ayrinti
