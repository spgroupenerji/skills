"""Kaynak adaptör kayıt defteri."""

from __future__ import annotations

from typing import Any

from .flickr import FlickrKaynak
from .met import MetKaynak
from .nasa import NasaKaynak
from .openverse import OpenverseKaynak
from .pexels import PexelsKaynak
from .pixabay import PixabayKaynak
from .polyhaven import PolyHavenKaynak
from .smithsonian import SmithsonianKaynak
from .unsplash import UnsplashKaynak
from .wikimedia import WikimediaKaynak

KAYNAKLAR: dict[str, Any] = {
    kaynak.ad: kaynak
    for kaynak in (
        PexelsKaynak(),
        PixabayKaynak(),
        UnsplashKaynak(),
        OpenverseKaynak(),
        WikimediaKaynak(),
        SmithsonianKaynak(),
        MetKaynak(),
        NasaKaynak(),
        PolyHavenKaynak(),
        FlickrKaynak(),
    )
}
KAYNAK_ADLARI: tuple[str, ...] = tuple(KAYNAKLAR)
