"""Cevrimdisi test paketi: sahte HTTP API sunucusuyla CLI sozlesmesini dogrular."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

KOK = Path(__file__).resolve().parent
ARAC = KOK / "gorsel_tedarik.py"
sys.path.insert(0, str(KOK))

from tedarik import guvenlik
from tedarik.hata import AracHatasi
from tedarik.model import Aday, Varyant
from tedarik.sabitler import CIKIS_TICARI, LISANS_KOSULLU

JPEG_GOVDE = b"\xff\xd8\xff\xe0" + b"0" * 240
HTML_GOVDE = b"<html><body>gecersiz gorsel</body></html>"
KAYNAK_ADLARI = {
    "pexels", "pixabay", "unsplash", "openverse", "wikimedia",
    "smithsonian", "met", "nasa", "polyhaven", "flickr",
}
ANAHTARSIZLAR = ("openverse", "wikimedia", "met", "nasa", "polyhaven")
ANAHTARLILAR = ("pexels", "pixabay", "unsplash", "smithsonian", "flickr")
GIZLI_ORTAMLAR = (
    "PEXELS_API_KEY", "PIXABAY_API_KEY", "UNSPLASH_ACCESS_KEY", "FLICKR_API_KEY",
    "SI_OPEN_ACCESS_API_KEY", "SMITHSONIAN_API_KEY", "OPENVERSE_API_TOKEN",
)
ANAHTARLAR = {
    "PEXELS_API_KEY": "test-pexels",
    "PIXABAY_API_KEY": "test-pixabay",
    "UNSPLASH_ACCESS_KEY": "test-unsplash",
    "FLICKR_API_KEY": "test-flickr",
    "SI_OPEN_ACCESS_API_KEY": "test-smithsonian",
}


class _Isleyici(BaseHTTPRequestHandler):
    """Sahte sunucu isteklerini kaydedip kaynak yanitina yonlendirir."""

    def do_GET(self) -> None:
        parca = urlsplit(self.path)
        sorgu = {
            anahtar: (deger[0] if len(deger) == 1 else ",".join(deger))
            for anahtar, deger in parse_qs(parca.query).items()
        }
        self.server.sunucu.kayitlar.append({"yol": parca.path, "sorgu": sorgu})
        try:
            durum, govde, basliklar = self.server.sunucu.yanit(parca.path, sorgu)
        except Exception:
            durum, govde, basliklar = 500, {"hata": "test sunucusu"}, {}
        self._yaz(durum, govde, basliklar)

    def _yaz(self, durum: int, govde: Any, basliklar: dict[str, str]) -> None:
        if isinstance(govde, bytes):
            veri = govde
            tur = "image/jpeg"
        else:
            veri = json.dumps(govde, ensure_ascii=False).encode("utf-8")
            tur = "application/json"
        self.send_response(durum)
        self.send_header("Content-Type", tur)
        self.send_header("Content-Length", str(len(veri)))
        for anahtar, deger in basliklar.items():
            self.send_header(anahtar, deger)
        self.end_headers()
        self.wfile.write(veri)

    def log_message(self, *_argumanlar: Any) -> None:
        """Test ciktisini kirletmemek icin erisim kaydini susturur."""


class SahteSunucu:
    """Yerel sahte API sunucusu; her kaynak icin gercek API alan adlariyla yanit verir."""

    def __init__(self) -> None:
        self.kayitlar: list[dict[str, Any]] = []
        self.sayac: dict[str, int] = {}
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), _Isleyici)
        self.httpd.daemon_threads = True
        self.httpd.sunucu = self
        self.port = int(self.httpd.server_address[1])
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def baslat(self) -> None:
        """Sunucuyu arka planda baslatir."""
        self.thread.start()

    def durdur(self) -> None:
        """Sunucuyu kapatir ve is parcacigini bekler."""
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def gorsel(self, kaynak: str, dosya: str) -> str:
        """Ayni sunucudan sunulan gordugu yerel gorsel URL'si uretir."""
        return f"http://127.0.0.1:{self.port}/{kaynak}/img/{dosya}"

    def yanit(self, yol: str, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        """Yolu kaynak isleyicisine dagitir."""
        parcalar = [parca for parca in yol.split("/") if parca]
        kaynak = parcalar[0] if parcalar else ""
        isleyici = getattr(self, f"_{kaynak}", None)
        if isleyici is None:
            return 404, {"hata": f"bilinmeyen yol: {yol}"}, {}
        return isleyici(yol, sorgu)

    def _pexels(self, yol: str, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        if "/img/" in yol:
            return 200, JPEG_GOVDE, {}
        if "/html" in yol:
            return 200, HTML_GOVDE, {}
        if yol.rstrip("/").endswith("/v1/search"):
            return self._pexels_arama(sorgu)
        if "/v1/photos/" in yol:
            return self._pexels_detay(yol.rstrip("/").rsplit("/", 1)[-1])
        return 404, {"hata": "pexels yolu"}, {}

    def _pexels_arama(self, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        konu = sorgu.get("query", "")
        if konu == "bos":
            return 200, {"photos": []}, {}
        if konu == "hata":
            return 500, {"hata": "sunucu"}, {"Retry-After": "0"}
        if konu == "limit":
            return 429, {"hata": "limit"}, {"Retry-After": "0"}
        if konu == "deneme":
            sayi = self.sayac.get("deneme", 0)
            self.sayac["deneme"] = sayi + 1
            if sayi == 0:
                return 500, {"hata": "gecici"}, {"Retry-After": "0"}
        if konu == "businessman":
            return 200, {"photos": [self._pexels_foto(112, "businessman portrait in office")]}, {}
        return 200, {"photos": [self._pexels_foto(101, "Quail and Millet"), self._pexels_foto(102, "Calm forest")]}, {}

    def _pexels_detay(self, kimlik: str) -> tuple[int, Any, dict[str, str]]:
        basliklar = {
            "101": "Quail and Millet", "102": "Calm forest",
            "103": "Quail and Millet", "112": "businessman portrait in office",
        }
        if kimlik == "104":
            veri = self._pexels_foto(104, "imza testi")
            veri["src"] = {anahtar: f"http://127.0.0.1:{self.port}/pexels/html" for anahtar in veri["src"]}
            return 200, veri, {}
        if kimlik not in basliklar:
            return 404, {"hata": "fotograf yok"}, {}
        return 200, self._pexels_foto(int(kimlik), basliklar[kimlik]), {}

    def _pexels_foto(self, kimlik: int, alt: str) -> dict[str, Any]:
        taban = self.gorsel("pexels", str(kimlik))
        return {
            "id": kimlik, "width": 1720, "height": 1840,
            "url": f"https://www.pexels.com/photo/{kimlik}/",
            "photographer": "Ayse Yilmaz",
            "photographer_url": "https://www.pexels.com/@ayse-yilmaz",
            "alt": alt,
            "src": {
                "original": f"{taban}-original.jpg",
                "large2x": f"{taban}-large2x.jpg",
                "large": f"{taban}-large.jpg",
                "medium": f"{taban}-medium.jpg",
                "small": f"{taban}-small.jpg",
                "tiny": f"{taban}-tiny.jpg",
            },
        }

    def _pixabay(self, yol: str, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        if "/img/" in yol:
            return 200, JPEG_GOVDE, {}
        if "q" in sorgu:
            return 200, {"totalHits": 2, "hits": [self._pixabay_hit(501, "tree, nature"), self._pixabay_hit(502, "lake")]}, {}
        if "id" in sorgu:
            return 200, {"totalHits": 1, "hits": [self._pixabay_hit(int(sorgu["id"]), "tree")]}, {}
        return 404, {"hata": "pixabay yolu"}, {}

    def _pixabay_hit(self, kimlik: int, etiketler: str) -> dict[str, Any]:
        taban = self.gorsel("pixabay", str(kimlik))
        return {
            "id": kimlik, "pageURL": f"https://pixabay.com/photos/{kimlik}/",
            "previewURL": f"{taban}-preview.jpg", "webformatURL": f"{taban}-640.jpg",
            "largeImageURL": f"{taban}-1280.jpg", "fullHDURL": f"{taban}-1920.jpg",
            "imageURL": f"{taban}-image.jpg", "imageWidth": 1920, "imageHeight": 1280,
            "user": "PixabayUser", "user_id": 7, "tags": etiketler,
        }

    def _unsplash(self, yol: str, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        if "/img/" in yol:
            return 200, JPEG_GOVDE, {}
        if "/tetik/" in yol:
            return 200, {"ok": True}, {}
        if "/search/photos" in yol:
            return 200, {"total": 3, "total_pages": 1, "results": [self._unsplash_foto("u1"), self._unsplash_premium("u2"), self._unsplash_plus("u3")]}, {}
        if "/photos/" in yol:
            return 200, self._unsplash_foto(yol.rstrip("/").rsplit("/", 1)[-1]), {}
        return 404, {"hata": "unsplash yolu"}, {}

    def _unsplash_foto(self, kimlik: str, alt: str = "calm lake") -> dict[str, Any]:
        taban = self.gorsel("unsplash", kimlik)
        return {
            "id": kimlik, "width": 4000, "height": 3000, "color": "#dddddd",
            "alt_description": alt, "description": "Lake view",
            "urls": {
                "raw": f"{taban}-raw?ixid=test", "full": f"{taban}-full.jpg",
                "regular": f"{taban}-regular.jpg", "small": f"{taban}-small.jpg",
                "thumb": f"{taban}-thumb.jpg",
            },
            "links": {
                "html": f"https://unsplash.com/photos/{kimlik}",
                "download_location": f"http://127.0.0.1:{self.port}/unsplash/tetik/{kimlik}",
            },
            "user": {"name": "Ada Nur", "username": "adanur", "links": {"html": "https://unsplash.com/@adanur"}},
        }

    def _unsplash_premium(self, kimlik: str) -> dict[str, Any]:
        veri = self._unsplash_foto(kimlik, "premium manzara")
        veri["premium"] = True
        return veri

    def _unsplash_plus(self, kimlik: str) -> dict[str, Any]:
        veri = self._unsplash_foto(kimlik, "plus manzara")
        veri["urls"] = {anahtar: f"https://plus.unsplash.com/premium_{kimlik}.jpg" for anahtar in veri["urls"]}
        return veri

    def _openverse(self, yol: str, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        if "/img/" in yol:
            return 200, JPEG_GOVDE, {}
        if "/images" in yol:
            sonuclar = [self._openverse_kayit("ov-cc0", "cc0", False), self._openverse_kayit("ov-by", "by", False)]
            return 200, {"result_count": len(sonuclar), "results": sonuclar}, {}
        return 404, {"hata": "openverse yolu"}, {}

    def _openverse_kayit(self, kimlik: str, lisans: str, olgun: bool) -> dict[str, Any]:
        taban = self.gorsel("openverse", kimlik)
        return {
            "id": kimlik, "title": "Doku ornegi",
            "url": f"{taban}.jpg", "thumbnail": f"{taban}-thumb.jpg",
            "foreign_landing_url": f"https://example.org/{kimlik}", "creator": "Sanatci",
            "creator_url": "https://example.org/sanatci", "license": lisans,
            "license_version": "1.0", "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "attribution": "", "source": "flickr", "provider": "flickr",
            "width": 1600, "height": 1200, "mature": olgun,
        }

    def _wikimedia(self, yol: str, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        if "/img/" in yol:
            return 200, JPEG_GOVDE, {}
        if "titles" in sorgu:
            return 200, {"query": {"pages": [self._wikimedia_sayfa("File:Cc0.jpg", 11, "cc0", "CC0 1.0")]}}, {}
        sayfalar = [
            self._wikimedia_sayfa("File:Cc0.jpg", 11, "cc0", "CC0 1.0"),
            self._wikimedia_sayfa("File:CcBySa.jpg", 12, "cc-by-sa", "CC BY-SA 4.0"),
        ]
        return 200, {"batchcomplete": True, "query": {"pages": sayfalar}}, {}

    def _wikimedia_sayfa(self, baslik: str, pageid: int, lisans: str, kisa: str) -> dict[str, Any]:
        taban = self.gorsel("wikimedia", baslik.replace("File:", "").replace(".", "-"))
        return {
            "pageid": pageid, "title": baslik,
            "imageinfo": [{
                "url": f"{taban}-orijinal.jpg",
                "descriptionurl": f"https://commons.wikimedia.org/wiki/{baslik}",
                "thumburl": f"{taban}-thumb.jpg", "width": 1600, "height": 1200,
                "mime": "image/jpeg",
                "extmetadata": {
                    "License": {"value": lisans}, "LicenseShortName": {"value": kisa},
                    "UsageTerms": {"value": kisa},
                    "LicenseUrl": {"value": "https://creativecommons.org/licenses/publicdomain/"},
                    "Artist": {"value": "Sanatci"},
                },
            }],
        }

    def _met(self, yol: str, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        if "/img/" in yol:
            return 200, JPEG_GOVDE, {}
        if "/v1.1/search" in yol or yol.rstrip("/").endswith("/search"):
            return 200, {"total": 2, "objectIDs": [1, 2]}, {}
        if "/objects/" in yol:
            return self._met_nesne(yol.rstrip("/").rsplit("/", 1)[-1])
        return 404, {"hata": "met yolu"}, {}

    def _met_nesne(self, kimlik: str) -> tuple[int, Any, dict[str, str]]:
        if kimlik not in {"1", "2"}:
            return 404, {"hata": "nesne yok"}, {}
        taban = self.gorsel("met", kimlik)
        kamu = kimlik == "1"
        return 200, {
            "objectID": int(kimlik),
            "title": "Quail and Millet" if kamu else "Telifli Eser",
            "isPublicDomain": kamu,
            "primaryImage": f"{taban}-buyuk.jpg", "primaryImageSmall": f"{taban}-kucuk.jpg",
            "objectURL": f"https://www.metmuseum.org/art/collection/search/{kimlik}",
            "artistDisplayName": "Sanatci", "objectDate": "1900", "medium": "Yagliboya",
            "creditLine": "Hediye", "tags": [{"term": "Birds"}],
        }, {}

    def _smithsonian(self, yol: str, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        if "/img/" in yol:
            return 200, JPEG_GOVDE, {}
        if "/content/" in yol:
            return 200, {"response": {"rowCount": 1, "rows": [self._smithsonian_satir("edan-1", "CC0")]}}, {}
        if yol.rstrip("/").endswith("/search"):
            satirlar = [self._smithsonian_satir("edan-1", "CC0"), self._smithsonian_satir("edan-2", "Kisitli")]
            return 200, {"status": 200, "response": {"rowCount": len(satirlar), "rows": satirlar}}, {}
        return 404, {"hata": "smithsonian yolu"}, {}

    def _smithsonian_satir(self, kimlik: str, erisim: str) -> dict[str, Any]:
        taban = self.gorsel("smithsonian", kimlik)
        return {
            "id": kimlik, "title": "Muze nesnesi",
            "content": {
                "descriptiveNonRepeating": {
                    "online_media": {"media": [{
                        "content": f"{taban}.jpg", "thumbnail": f"{taban}-thumb.jpg",
                        "idsId": kimlik, "usage": {"access": erisim},
                        "width": 1600, "height": 1200,
                    }]},
                    "metadata_usage": {"access": erisim},
                },
                "freetext": {"name": [{"content": "Sanatci"}]},
            },
            "creditLine": "Hediye",
        }

    def _nasa(self, yol: str, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        if "/img/" in yol:
            return 200, JPEG_GOVDE, {}
        if "/asset/" in yol:
            kimlik = yol.rstrip("/").rsplit("/", 1)[-1]
            boyutlar = ("orig.tif", "large.jpg", "medium.jpg", "small.jpg", "thumb.jpg")
            return 200, [self.gorsel("nasa", f"{kimlik}~{boyut}") for boyut in boyutlar], {}
        if yol.rstrip("/").endswith("/search"):
            return self._nasa_arama()
        return 404, {"hata": "nasa yolu"}, {}

    def _nasa_arama(self) -> tuple[int, Any, dict[str, str]]:
        kimlik = "PIA123"
        linkler = [
            {"href": self.gorsel("nasa", f"{kimlik}~{boyut}"), "rel": "preview", "render": "image"}
            for boyut in ("orig.tif", "large.jpg", "medium.jpg", "small.jpg", "thumb.jpg")
        ]
        oge = {
            "href": "https://images-api.nasa.gov/search?nasa_id=PIA123",
            "data": [{
                "nasa_id": kimlik, "title": "Nebula", "description": "Derin uzay",
                "keywords": ["space"], "center": "JPL",
                "date_created": "2020-01-01T00:00:00Z", "secondary_creator": "",
            }],
            "links": linkler,
        }
        return 200, {"collection": {"items": [oge], "links": []}}, {}

    def _polyhaven(self, yol: str, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        if "/img/" in yol:
            return 200, JPEG_GOVDE, {}
        if "/files/" in yol:
            return 200, self._polyhaven_dosyalar(yol.rstrip("/").rsplit("/", 1)[-1]), {}
        if "/info/" in yol:
            return 200, {"name": "Brick Wall", "authors": {"Rob Tuytel": "CC0"}, "date": 1600000000, "categories": ["textures"], "tags": []}, {}
        return 404, {"hata": "polyhaven yolu"}, {}

    def _polyhaven_dosyalar(self, kimlik: str) -> dict[str, Any]:
        taban = self.gorsel("polyhaven", kimlik)
        dosyalar: dict[str, Any] = {"Diffuse": {}, "Nor": {}}
        for cozunurluk, _genislik in (("1k", 1024), ("2k", 2048), ("4k", 4096), ("8k", 8192), ("16k", 16384)):
            dosyalar["Diffuse"][cozunurluk] = {
                "jpg": {"url": f"{taban}-diffuse-{cozunurluk}.jpg", "md5": "a", "size": 1000},
            }
            if cozunurluk in ("1k", "2k"):
                dosyalar["Nor"][cozunurluk] = {
                    "png": {"url": f"{taban}-nor-{cozunurluk}.png", "md5": "b", "size": 1000},
                }
        return dosyalar

    def _flickr(self, yol: str, sorgu: dict[str, str]) -> tuple[int, Any, dict[str, str]]:
        if "/img/" in yol:
            return 200, JPEG_GOVDE, {}
        if "getInfo" in sorgu.get("method", ""):
            return 200, {"photo": self._flickr_foto("11", 9), "stat": "ok"}, {}
        return 200, {"photos": {"page": 1, "pages": 1, "perpage": 20, "total": 2,
                                "photo": [self._flickr_foto("11", 9), self._flickr_foto("12", 7)]}, "stat": "ok"}, {}

    def _flickr_foto(self, kimlik: str, lisans: int) -> dict[str, Any]:
        taban = self.gorsel("flickr", kimlik)
        return {
            "id": kimlik, "owner": "1@N01", "secret": "s", "server": "1", "farm": 1,
            "title": "Tarihi kopru", "license": lisans, "owner_name": "Ada Nur",
            "url_sq": f"{taban}-sq.jpg", "url_m": f"{taban}-m.jpg",
            "url_l": f"{taban}-l.jpg", "url_o": f"{taban}-o.jpg",
        }


class GorselTedarikTest(unittest.TestCase):
    """Sahte API sunucusu ve gecici klasorle calisan temel test sinifi."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.pil_klasoru = tempfile.TemporaryDirectory()
        Path(cls.pil_klasoru.name, "PIL.py").write_text("raise ImportError('test: Pillow yok')\n", encoding="utf-8")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.pil_klasoru.cleanup()

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.kok = Path(self.tmp.name)
        self.sunucu = SahteSunucu()
        self.addCleanup(self.sunucu.durdur)
        self.sunucu.baslat()

    def tabanlar(self) -> dict[str, str]:
        """Her kaynak icin sahte sunucu taban URL'si uretir."""
        taban = f"http://127.0.0.1:{self.sunucu.port}"
        return {
            "GORSEL_API_TABANI_PEXELS": f"{taban}/pexels",
            "GORSEL_API_TABANI_PIXABAY": f"{taban}/pixabay",
            "GORSEL_API_TABANI_UNSPLASH": f"{taban}/unsplash",
            "GORSEL_API_TABANI_OPENVERSE": f"{taban}/openverse/v1",
            "GORSEL_API_TABANI_WIKIMEDIA": f"{taban}/wikimedia",
            "GORSEL_API_TABANI_MET": f"{taban}/met/public/collection",
            "GORSEL_API_TABANI_SMITHSONIAN": f"{taban}/smithsonian/v1.0",
            "GORSEL_API_TABANI_NASA": f"{taban}/nasa",
            "GORSEL_API_TABANI_POLYHAVEN": f"{taban}/polyhaven",
            "GORSEL_API_TABANI_FLICKR": f"{taban}/flickr/services/rest/",
        }

    def ortam(self, anahtarlar: bool = True, ek: dict[str, str] | None = None) -> dict[str, str]:
        """Anahtarlari temizlenmis izole subprocess ortami uretir."""
        ortam = {anahtar: deger for anahtar, deger in os.environ.items() if not anahtar.upper().startswith("GORSEL_API_TABANI_")}
        for ad in GIZLI_ORTAMLAR:
            ortam.pop(ad, None)
        ortam.update(self.tabanlar())
        if anahtarlar:
            ortam.update(ANAHTARLAR)
        if ek:
            ortam.update(ek)
        yollar = [type(self).pil_klasoru.name]
        mevcut = ortam.get("PYTHONPATH")
        if mevcut:
            yollar.append(mevcut)
        ortam["PYTHONPATH"] = os.pathsep.join(yollar)
        ortam["PYTHONIOENCODING"] = "utf-8"
        return ortam

    def calistir(self, *arguman: str, anahtarlar: bool = True, ek_ortam: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        """CLI'yi izole ortamda calistirir."""
        return subprocess.run(
            [sys.executable, str(ARAC), *arguman],
            cwd=str(self.kok), env=self.ortam(anahtarlar, ek_ortam),
            capture_output=True, text=True, encoding="utf-8", timeout=60,
        )

    def basarili(self, cp: subprocess.CompletedProcess[str]) -> dict[str, Any]:
        """Basarili CLI ciktisini JSON olarak dondurur."""
        self.assertEqual(cp.returncode, 0, (cp.stdout or "") + (cp.stderr or ""))
        return json.loads(cp.stdout)

    def hatali(self, cp: subprocess.CompletedProcess[str], kod: int) -> dict[str, Any]:
        """Beklenen cikis kodlu hatayi JSON olarak dondurur."""
        self.assertEqual(cp.returncode, kod, (cp.stdout or "") + (cp.stderr or ""))
        return json.loads(cp.stderr)

    def istekler(self, onek: str = "") -> list[dict[str, Any]]:
        """Sahte sunucuya gelen istekleri dondurur."""
        return [kayit for kayit in self.sunucu.kayitlar if str(kayit["yol"]).startswith(onek)]

    def gorsel_istekleri(self) -> list[str]:
        """Gorsel indirme isteklerinin yollarini dondurur."""
        return [str(kayit["yol"]) for kayit in self.sunucu.kayitlar if "/img/" in str(kayit["yol"])]

    def manifest_oku(self, klasor: str = "assets/img") -> dict[str, Any]:
        """credits.json icerigini dondurur."""
        return json.loads((self.kok / klasor / "credits.json").read_text(encoding="utf-8"))

    def test_01_kaynaklar_on_kaynak_ve_anahtar_durumu(self) -> None:
        veri = self.basarili(self.calistir("kaynaklar", anahtarlar=False))
        self.assertEqual(veri["komut"], "kaynaklar")
        self.assertIn("pillow", veri["cevirici"])
        kaynaklar = {kayit["ad"]: kayit for kayit in veri["kaynaklar"]}
        self.assertEqual(set(kaynaklar), KAYNAK_ADLARI)
        for ad in ANAHTARSIZLAR:
            self.assertEqual(kaynaklar[ad]["anahtar"], "gerekmez", ad)
        for ad in ANAHTARLILAR:
            self.assertEqual(kaynaklar[ad]["anahtar"], "yok", ad)
        for kayit in kaynaklar.values():
            self.assertIn("lisans", kayit)
            self.assertIn("yerel_indirme", kayit)
        self.assertEqual(self.istekler(), [])

    def test_02_auto_kategori_sanat_met_ve_openverse(self) -> None:
        veri = self.basarili(self.calistir("ara", "--konu", "tablo", "--kategori", "sanat", "--adet", "2", anahtarlar=False))
        self.assertEqual(veri["kaynaklar"], ["met", "openverse"])
        self.assertEqual({sonuc["kaynak"] for sonuc in veri["sonuclar"]}, {"met", "openverse"})
        self.assertTrue(any("/v1.1/search" in str(kayit["yol"]) for kayit in self.istekler("/met")))

    def test_03_pexels_normalize_ve_atif(self) -> None:
        veri = self.basarili(self.calistir("ara", "--kaynak", "pexels", "--konu", "quail", "--adet", "5"))
        kayit = next(sonuc for sonuc in veri["sonuclar"] if sonuc["kimlik"] == "101")
        self.assertEqual(kayit["kaynak"], "pexels")
        self.assertEqual(kayit["genislik"], 1720)
        self.assertEqual(kayit["yukseklik"], 1840)
        self.assertEqual(kayit["lisans"]["sinif"], "serbest-ticari")
        self.assertTrue(kayit["lisans"]["atif"])
        self.assertTrue(kayit["sayfa"].startswith("https://www.pexels.com/photo/101"))
        self.assertTrue(kayit["gorsel"]["indir"].startswith("http://127.0.0.1"))
        self.assertIn("Ayse", kayit["atif_html"])
        self.assertIn("Pexels", kayit["atif_html"])
        self.assertEqual(kayit["yerel_indirme"], "serbest")
        sorgu = self.istekler("/pexels/v1/search")[0]["sorgu"]
        self.assertEqual(sorgu.get("query"), "quail")

    def test_04_pixabay_safesearch_ve_alanlar(self) -> None:
        veri = self.basarili(self.calistir("ara", "--kaynak", "pixabay", "--konu", "doga", "--adet", "4", "--yon", "landscape"))
        kayit = veri["sonuclar"][0]
        self.assertEqual(kayit["kimlik"], "501")
        self.assertEqual(kayit["lisans"]["sinif"], "serbest-ticari")
        self.assertIn("Pixabay", kayit["atif_html"] or "")
        sorgu = self.istekler("/pixabay/api")[0]["sorgu"]
        self.assertEqual(sorgu.get("q"), "doga")
        self.assertEqual(sorgu.get("safesearch"), "true")
        self.assertEqual(sorgu.get("image_type"), "photo")
        self.assertEqual(sorgu.get("orientation"), "horizontal")
        self.assertTrue(3 <= int(sorgu.get("per_page", "0")) <= 200)

    def test_05_unsplash_premium_plus_suzme(self) -> None:
        veri = self.basarili(self.calistir("ara", "--kaynak", "unsplash", "--konu", "lake", "--adet", "6"))
        self.assertEqual([sonuc["kimlik"] for sonuc in veri["sonuclar"]], ["u1"])
        sorgu = self.istekler("/unsplash/search/photos")[0]["sorgu"]
        self.assertEqual(sorgu.get("query"), "lake")
        self.assertLessEqual(int(sorgu.get("per_page", "99")), 30)

    def test_06_unsplash_yerel_kabul_kapisi(self) -> None:
        cp = self.calistir("indir", "--kaynak", "unsplash", "--id", "u1", "--ad", "gol", "--genislikler", "640", "--format", "jpg")
        hata = self.hatali(cp, 8)
        self.assertTrue(hata["hata"])
        self.assertFalse(any("/tetik/" in str(kayit["yol"]) for kayit in self.istekler("/unsplash")))
        self.assertFalse((self.kok / "assets").exists())

    def test_07_unsplash_yerel_kabul_ile_indirme(self) -> None:
        veri = self.basarili(self.calistir("indir", "--kaynak", "unsplash", "--id", "u1", "--ad", "gol", "--genislikler", "640", "--format", "jpg", "--yerel-kabul"))
        self.assertEqual(veri["durum"], "indirildi")
        self.assertTrue(any("/tetik/u1" in str(kayit["yol"]) for kayit in self.istekler("/unsplash")))
        self.assertTrue(veri["dosyalar"])
        self.assertEqual(veri["credits"]["surum"], 2)
        manifest = self.manifest_oku()
        self.assertEqual(manifest["kayitlar"][0]["kaynak"], "unsplash")

    def test_08_openverse_license_parametresi_ve_cc_by_suzme(self) -> None:
        veri = self.basarili(self.calistir("ara", "--kaynak", "openverse", "--konu", "texture", anahtarlar=False))
        self.assertEqual([sonuc["kimlik"] for sonuc in veri["sonuclar"]], ["ov-cc0"])
        sorgu = self.istekler("/openverse")[0]["sorgu"]
        lisanslar = {parca.strip() for parca in sorgu.get("license", "").split(",")}
        self.assertEqual(lisanslar, {"cc0", "pdm"})
        self.assertEqual(veri["sonuclar"][0]["lisans"]["sinif"], "kamu-mali")

    def test_09_wikimedia_cc_by_sa_suzme_cc0_tutma(self) -> None:
        veri = self.basarili(self.calistir("ara", "--kaynak", "wikimedia", "--konu", "texture", anahtarlar=False))
        self.assertEqual([sonuc["kimlik"] for sonuc in veri["sonuclar"]], ["File:Cc0.jpg"])
        sorgu = self.istekler("/wikimedia")[0]["sorgu"]
        self.assertIn("extmetadata", sorgu.get("iiprop", ""))
        self.assertIn("LicenseShortName", sorgu.get("iiextmetadatafilter", ""))
        self.assertEqual(sorgu.get("gsrnamespace"), "6")
        self.assertEqual(veri["sonuclar"][0]["lisans"]["sinif"], "kamu-mali")

    def test_10_met_v11_akisi_ve_ispublicdomain_suzme(self) -> None:
        veri = self.basarili(self.calistir("ara", "--kaynak", "met", "--konu", "quail", "--adet", "3", anahtarlar=False))
        self.assertEqual([sonuc["kimlik"] for sonuc in veri["sonuclar"]], ["1"])
        aramalar = self.istekler("/met")
        self.assertTrue(any("/v1.1/search" in str(kayit["yol"]) for kayit in aramalar))
        self.assertEqual(len([kayit for kayit in aramalar if "/v1/objects/" in str(kayit["yol"])]), 2)
        self.assertIn("hasImages", next(kayit["sorgu"] for kayit in aramalar if "/v1.1/search" in str(kayit["yol"])))

    def test_11_nasa_orig_tif_yerine_jpg(self) -> None:
        veri = self.basarili(self.calistir("ara", "--kaynak", "nasa", "--konu", "nebula", "--adet", "2", anahtarlar=False))
        self.assertEqual(len(veri["sonuclar"]), 1)
        sonuc = veri["sonuclar"][0]
        self.assertIn("~large", sonuc["gorsel"]["indir"])
        self.assertNotIn("~orig", json.dumps(veri, ensure_ascii=False))
        self.assertTrue(any("/nasa/asset/PIA123" in str(kayit["yol"]) for kayit in self.istekler("/nasa")))

    def test_12_flickr_license_9_10_ve_7_suzme(self) -> None:
        veri = self.basarili(self.calistir("ara", "--kaynak", "flickr", "--konu", "tarih", "--adet", "4"))
        self.assertEqual([sonuc["kimlik"] for sonuc in veri["sonuclar"]], ["11"])
        sorgu = self.istekler("/flickr")[0]["sorgu"]
        self.assertEqual(sorgu.get("license"), "9,10")
        self.assertEqual(sorgu.get("safe_search"), "1")
        self.assertEqual(sorgu.get("method"), "flickr.photos.search")
        self.assertEqual(veri["sonuclar"][0]["lisans"]["sinif"], "kamu-mali")

    def test_13_smithsonian_cc0_olmayan_medya_suzme(self) -> None:
        veri = self.basarili(self.calistir("ara", "--kaynak", "smithsonian", "--konu", "museum"))
        self.assertEqual([sonuc["kimlik"] for sonuc in veri["sonuclar"]], ["edan-1"])
        sorgu = self.istekler("/smithsonian")[0]["sorgu"]
        self.assertEqual(sorgu.get("api_key"), "test-smithsonian")
        self.assertEqual(sorgu.get("type"), "edanmdm")
        self.assertEqual(veri["sonuclar"][0]["lisans"]["sinif"], "kamu-mali")

    def test_14_polyhaven_doku_varyant_esleme(self) -> None:
        veri = self.basarili(self.calistir("indir", "--kaynak", "polyhaven", "--id", "brick_01", "--ad", "tugla-doku", "--genislikler", "1024", "--format", "jpg", anahtarlar=False))
        self.assertEqual(veri["durum"], "indirildi")
        yollar = self.gorsel_istekleri()
        self.assertTrue(yollar)
        self.assertTrue(all("diffuse" in yol.lower() for yol in yollar), yollar)
        self.assertTrue(any("/polyhaven/files/brick_01" in str(kayit["yol"]) for kayit in self.istekler("/polyhaven")))
        self.assertEqual(veri["dosyalar"][0]["bicim"], "jpg")

    def test_15_ticari_heuristik_insan_manuel_kosullu_engelli(self) -> None:
        veri = self.basarili(self.calistir("ara", "--kaynak", "pexels", "--konu", "businessman", "--adet", "3"))
        self.assertEqual(len(veri["sonuclar"]), 1)
        ticari = veri["sonuclar"][0]["ticari"]
        self.assertEqual(ticari["durum"], "manuel_dogrulama_gerekli")
        self.assertIn("insan", ticari["riskler"])
        aday = Aday(kaynak="flickr", kimlik="7", baslik="kosullu lisans", genislik=100, yukseklik=100,
                    lisans_adi="CC BY 4.0", lisans_sinifi=LISANS_KOSULLU, sayfa_url="",
                    varyantlar=(Varyant(100, "http://127.0.0.1/x.jpg"),))
        degerlendirme = guvenlik.ticari_degerlendir(aday)
        self.assertEqual(degerlendirme["durum"], "engelli")
        with self.assertRaises(AracHatasi) as baglam:
            guvenlik.kapi(degerlendirme)
        self.assertEqual(baglam.exception.kod, CIKIS_TICARI)

    def test_16_indir_iki_genislik_srcset_manifest_v2_onay(self) -> None:
        veri = self.basarili(self.calistir("indir", "--kaynak", "pexels", "--id", "101", "--ad", "gun-batimi", "--genislikler", "640,940", "--format", "jpg"))
        self.assertEqual(veri["durum"], "indirildi")
        self.assertEqual([dosya["genislik"] for dosya in veri["dosyalar"]], [640, 940])
        for dosya in veri["dosyalar"]:
            yol = self.kok / dosya["yol"]
            self.assertTrue(yol.is_file(), dosya["yol"])
            self.assertTrue(yol.read_bytes().startswith(b"\xff\xd8\xff"))
            self.assertGreater(dosya["bayt"], 0)
        self.assertIn("640w", veri["srcset"])
        self.assertIn("940w", veri["srcset"])
        self.assertEqual(veri["img"]["width"], 940)
        self.assertEqual(veri["ticari"]["durum"], "manuel_dogrulama_gerekli")
        self.assertTrue(veri["ticari"]["onay_gerekli"])
        manifest = self.manifest_oku()
        self.assertEqual(manifest["surum"], 2)
        self.assertEqual(len(manifest["kayitlar"]), 1)
        self.assertEqual(manifest["kayitlar"][0]["ticari_durum"], "manuel_dogrulama_gerekli")
        self.assertEqual(len(manifest["kayitlar"][0]["dosyalar"]), 2)

    def test_17_cift_ad_ikinci_kayit_2_ekli(self) -> None:
        ilk = self.basarili(self.calistir("indir", "--kaynak", "pexels", "--id", "101", "--ad", "kahve-fincani", "--genislikler", "640", "--format", "jpg"))
        ikinci = self.basarili(self.calistir("indir", "--kaynak", "pexels", "--id", "103", "--ad", "kahve-fincani", "--genislikler", "640", "--format", "jpg"))
        self.assertEqual(ilk["ad"], "kahve-fincani")
        self.assertEqual(ikinci["ad"], "kahve-fincani-2")
        manifest = self.manifest_oku()
        self.assertEqual([kayit["ad"] for kayit in manifest["kayitlar"]], ["kahve-fincani", "kahve-fincani-2"])

    def test_18_onayla_onaylandi_ve_denetle(self) -> None:
        self.basarili(self.calistir("indir", "--kaynak", "pexels", "--id", "101", "--ad", "onay-testi", "--genislikler", "640", "--format", "jpg"))
        onay = self.basarili(self.calistir("onayla", "--kaynak", "pexels", "--id", "101", "--karar", "uygun", "--onaylayan", "Denetci"))
        self.assertEqual(onay["durum"], "onaylandi")
        self.assertEqual(onay["ticari"]["durum"], "onaylandi")
        manifest = self.manifest_oku()
        self.assertEqual(manifest["kayitlar"][0]["ticari_durum"], "onaylandi")
        self.assertEqual(manifest["kayitlar"][0]["ticari_onay"]["karar"], "uygun")
        denetim = self.basarili(self.calistir("denetle"))
        self.assertEqual(denetim["toplam"], 1)
        self.assertEqual(denetim["onaysiz"], [])
        self.assertEqual(denetim["eksik_dosyalar"], [])

    def test_19_bozuk_credits_json_yedekleme(self) -> None:
        klasor = self.kok / "assets" / "img"
        klasor.mkdir(parents=True)
        (klasor / "credits.json").write_text("{bozuk json", encoding="utf-8")
        veri = self.basarili(self.calistir("denetle"))
        self.assertIn("yedeklendi", veri["uyari"] or "")
        yedekler = list(klasor.glob("credits.json.bozuk-*"))
        self.assertEqual(len(yedekler), 1)
        self.assertFalse((klasor / "credits.json").exists())
        self.assertEqual(veri["toplam"], 0)

    def test_20_gorsel_imza_reddi_html_govde(self) -> None:
        cp = self.calistir("indir", "--kaynak", "pexels", "--id", "104", "--ad", "imza-testi", "--genislikler", "640", "--format", "jpg")
        hata = self.hatali(cp, 6)
        self.assertIn("imza", hata["hata"])
        self.assertFalse((self.kok / "assets").exists())

    def test_21_500_sonra_200_retry(self) -> None:
        basla = time.monotonic()
        veri = self.basarili(self.calistir("ara", "--kaynak", "pexels", "--konu", "deneme", "--adet", "1"))
        gecen = time.monotonic() - basla
        self.assertEqual(len(self.istekler("/pexels/v1/search")), 2)
        self.assertIn("101", [sonuc["kimlik"] for sonuc in veri["sonuclar"]])
        self.assertLess(gecen, 15)

    def test_22_cikis_kodlari(self) -> None:
        with self.subTest("kullanim"):
            self.hatali(self.calistir("ara", "--konu", "x", "--kaynak", "yok"), 2)
        with self.subTest("anahtar"):
            self.hatali(self.calistir("indir", "--kaynak", "pexels", "--id", "101", "--ad", "x", anahtarlar=False), 3)
        with self.subTest("bulunamadi"):
            self.hatali(self.calistir("ara", "--kaynak", "pexels", "--konu", "bos", "--adet", "1"), 4)
        with self.subTest("api"):
            self.hatali(self.calistir("ara", "--kaynak", "pexels", "--konu", "hata", "--adet", "1"), 5)
        with self.subTest("ticari"):
            self.hatali(self.calistir("indir", "--kaynak", "unsplash", "--id", "u1", "--ad", "x", "--genislikler", "640", "--format", "jpg"), 8)

    def test_23_v1_manifest_gocu(self) -> None:
        klasor = self.kok / "assets" / "img"
        klasor.mkdir(parents=True)
        eski = {"fotograflar": [{
            "id": "u9", "ad": "eski-gorsel", "aciklama": "Eski kayit", "lisans": "Unsplash License",
            "fotografci": {"ad": "Ada", "profil_url": "https://unsplash.com/@ada"},
            "dosyalar": [], "fotograf_sayfasi": "https://unsplash.com/photos/u9",
            "atif_html": "<p>ada</p>", "ticari_durum": "onaylandi",
            "indirme_tarihi": "2026-01-01T00:00:00+03:00",
        }]}
        (klasor / "credits.json").write_text(json.dumps(eski), encoding="utf-8")
        denetim = self.basarili(self.calistir("denetle"))
        self.assertEqual(denetim["toplam"], 1)
        self.assertIn("v1", denetim["uyari"] or "")
        onay = self.basarili(self.calistir("onayla", "--ad", "eski-gorsel", "--karar", "uygun", "--onaylayan", "Denetci"))
        self.assertEqual(onay["durum"], "onaylandi")
        manifest = self.manifest_oku()
        self.assertEqual(manifest["surum"], 2)
        self.assertEqual(manifest["kayitlar"][0]["kaynak"], "unsplash")
        self.assertEqual(manifest["kayitlar"][0]["ticari_durum"], "onaylandi")

    def test_24_toplu_ara_plani(self) -> None:
        plan = [{"ad": "bir", "konu": "orman", "kaynak": "pexels"}, {"ad": "iki", "konu": "deniz", "kaynak": "pexels", "adet": 2}]
        (self.kok / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
        veri = self.basarili(self.calistir("toplu-ara", "--plan", "plan.json", "--adet", "2"))
        self.assertEqual(veri["komut"], "toplu-ara")
        self.assertEqual([varlik["ad"] for varlik in veri["varliklar"]], ["bir", "iki"])
        for varlik in veri["varliklar"]:
            self.assertEqual(varlik["kaynaklar"], ["pexels"])
            self.assertTrue(varlik["sonuclar"])
        sorgular = [kayit["sorgu"].get("query") for kayit in self.istekler("/pexels/v1/search")]
        self.assertEqual(sorgular, ["orman", "deniz"])

    def test_25_ayni_dosya_tekrar_indirilmemesi(self) -> None:
        komut = ("indir", "--kaynak", "pexels", "--id", "101", "--ad", "tekrar-eden", "--genislikler", "640", "--format", "jpg")
        self.basarili(self.calistir(*komut))
        ilk_sayi = len(self.gorsel_istekleri())
        self.basarili(self.calistir(*komut))
        self.assertEqual(len(self.gorsel_istekleri()), ilk_sayi)
        manifest = self.manifest_oku()
        self.assertEqual(len(manifest["kayitlar"]), 1)
        self.assertTrue((self.kok / "assets" / "img" / "tekrar-eden-640.jpg").is_file())

    def test_26_429_retry_after(self) -> None:
        cp = self.calistir("ara", "--kaynak", "pexels", "--konu", "limit", "--adet", "1")
        hata = self.hatali(cp, 5)
        self.assertEqual(hata["kod"], 5)
        self.assertEqual(len(self.istekler("/pexels/v1/search")), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
