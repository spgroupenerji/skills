"""Araç veri modeli: arama isteği, aday, varyant ve kaynak sözleşmesi."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from .sabitler import VARSAYILAN_ADET


@dataclass(frozen=True)
class Varyant:
    """Bir adayın indirilebilir genişlik varyantı."""

    genislik: int
    url: str
    bicim: str = "jpg"
    yukseklik: int | None = None


@dataclass(frozen=True)
class Aday:
    """Kaynaklardan bağımsız, ticari değerlendirmeye hazır görsel adayı."""

    kaynak: str
    kimlik: str
    baslik: str
    genislik: int
    yukseklik: int
    lisans_adi: str
    lisans_sinifi: str
    sayfa_url: str
    varyantlar: tuple[Varyant, ...]
    fotografci: str = ""
    profil_url: str = ""
    aciklama: str = ""
    risk_metni: str = ""
    ek: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AramaIstegi:
    """Kaynak adaptörlerine geçen normalize arama isteği."""

    konu: str
    adet: int = VARSAYILAN_ADET
    yon: str | None = None
    min_genislik: int = 0
    sayfa: int = 1
    kategori: str = "genel"


class Kaynak(Protocol):
    """Her görsel kaynağının uyduğu adaptör sözleşmesi."""

    ad: str
    lisans_adi: str
    yerel_indirme: str
    atif_zorunlu: bool
    anahtar_ortami: str | None
    varsayilan_taban: str
    taban_ortami: str
    gorsel_hostlari: tuple[str, ...]
    kota_basliklari: tuple[str, ...]

    def ara(self, istek: AramaIstegi, anahtar: str | None, taban: str) -> list[Aday]:
        """Arama yapar; ağ ve doğrulama hatalarını AracHatasi olarak yükseltir."""

    def detay(self, kimlik: str, anahtar: str | None, taban: str) -> Aday:
        """Tek kaydı yeniden getirir; indirme ve onay akışının girdisidir."""
