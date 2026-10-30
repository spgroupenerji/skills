#!/usr/bin/env python3
"""Unsplash aracının çevrimdışı testleri (ağ yok, API anahtarı gerekmez)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

ARAC = Path(__file__).with_name("unsplash_gorsel.py")
SUNUCU: dict = {}


def _sunucu_sifirla() -> None:
    SUNUCU.clear()
    SUNUCU.update({
        "kayitlar": [],
        "arama_zorla": [],
        "fotograf_zorla": [],
        "tetik_zorla": [],
        "gorsel_zorla": [],
        "bozuk_gorsel": False,
        "guvensiz_gorsel": False,
    })


def _sahte_webp() -> bytes:
    govde = b"VP8 " + b"\x00" * 92
    return b"RIFF" + len(govde).to_bytes(4, "little") + b"WEBP" + govde


def _foto_json(foto_id: str, genislik: int, yukseklik: int, port: int) -> dict:
    ham = f"http://127.0.0.1:{port}/img/{foto_id}?ixid=test-ixid-{foto_id}"
    return {
        "id": foto_id,
        "width": genislik,
        "height": yukseklik,
        "color": "#336699",
        "alt_description": ("portrait of a woman in an office" if foto_id == "foto3" else "modern ofis calisma alani"),
        "description": "Modern ofis",
        "user": {
            "name": "Test Fotografci",
            "username": "testfotografci",
            "links": {"html": "https://unsplash.com/@testfotografci"},
        },
        "urls": {
            "raw": ham,
            "full": ham + "&q=85&fm=jpg",
            "regular": ham + "&w=1080&q=80&fm=jpg&fit=max",
            "small": ham + "&w=400&q=80&fm=jpg&fit=max",
            "thumb": ham + "&w=200&q=80&fm=jpg&fit=max",
        },
        "links": {
            "self": f"https://api.unsplash.com/photos/{foto_id}",
            "html": f"https://unsplash.com/photos/{foto_id}",
            "download": f"https://unsplash.com/photos/{foto_id}/download",
            "download_location": f"http://127.0.0.1:{port}/photos/{foto_id}/download?ixid=test-ixid-{foto_id}",
        },
    }


class SahteUnsplash(BaseHTTPRequestHandler):
    def log_message(self, *_args) -> None:
        pass

    def _gonder(self, durum: int, govde: bytes, icerik_turu: str) -> None:
        self.send_response(durum)
        self.send_header("Content-Type", icerik_turu)
        self.send_header("Content-Length", str(len(govde)))
        self.end_headers()
        self.wfile.write(govde)

    def _json(self, govde: dict, durum: int = 200) -> None:
        self._gonder(durum, json.dumps(govde).encode("utf-8"), "application/json")

    def do_GET(self) -> None:
        parca = urlsplit(self.path)
        yol = parca.path
        SUNUCU["kayitlar"].append({
            "yol": yol,
            "sorgu": parca.query,
            "basliklar": {k.lower(): v for k, v in self.headers.items()},
        })
        if yol == "/search/photos":
            self._arama(parca)
        elif yol.startswith("/photos/") and yol.endswith("/download"):
            self._tetik(yol)
        elif yol.startswith("/photos/"):
            self._fotograf(yol.rsplit("/", 1)[-1])
        elif yol.startswith("/img/"):
            self._gorsel(parca)
        else:
            self._json({"errors": ["bilinmeyen yol"]}, 404)

    def _arama(self, parca) -> None:
        if SUNUCU["arama_zorla"]:
            durum = SUNUCU["arama_zorla"].pop(0)
            if durum != 200:
                self._json({"errors": ["test hatasi"]}, durum)
                return
        port = self.server.server_port
        filtre = parse_qs(parca.query).get("orientation", [""])[0]
        sonuclar = [
            _foto_json("foto1", 4000, 3000, port),
            _foto_json("foto2", 1200, 800, port),
            _foto_json("foto3", 3000, 4000, port),
        ]
        if filtre == "landscape":
            sonuclar = [s for s in sonuclar if s["width"] > s["height"]]
        elif filtre == "portrait":
            sonuclar = [s for s in sonuclar if s["height"] > s["width"]]
        govde = json.dumps({"total": 3, "total_pages": 1, "results": sonuclar}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(govde)))
        self.send_header("X-Ratelimit-Limit", "50")
        self.send_header("X-Ratelimit-Remaining", "49")
        self.end_headers()
        self.wfile.write(govde)

    def _fotograf(self, foto_id: str) -> None:
        if SUNUCU["fotograf_zorla"]:
            durum = SUNUCU["fotograf_zorla"].pop(0)
            if durum != 200:
                self._json({"errors": ["test hatasi"]}, durum)
                return
        port = self.server.server_port
        if foto_id == "premium1":
            veri = _foto_json(foto_id, 4000, 3000, port)
            veri["urls"]["raw"] = f"http://127.0.0.1:{port}/img/premium_photo-123?ixid=premium"
            self._json(veri)
            return
        if foto_id == "riskli1":
            veri = _foto_json(foto_id, 4000, 3000, port)
            veri["alt_description"] = "businesswoman portrait in modern office"
            self._json(veri)
            return
        veri = _foto_json(foto_id, 4000, 3000, port)
        if SUNUCU["guvensiz_gorsel"]:
            veri["urls"]["raw"] = "http://example.com/kotu.webp?ixid=x"
        self._json(veri)

    def _tetik(self, yol: str) -> None:
        if SUNUCU["tetik_zorla"]:
            durum = SUNUCU["tetik_zorla"].pop(0)
            if durum != 200:
                self._json({"errors": ["test hatasi"]}, durum)
                return
        self._json({"id": yol.rsplit("/", 2)[-2]})

    def _gorsel(self, parca) -> None:
        if SUNUCU["gorsel_zorla"]:
            durum = SUNUCU["gorsel_zorla"].pop(0)
            if durum != 200:
                self._json({"errors": ["test hatasi"]}, durum)
                return
        if SUNUCU["bozuk_gorsel"]:
            self._gonder(200, b"<html>gorsel degil</html>", "text/html")
            return
        self._gonder(200, _sahte_webp(), "image/webp")


class AracTestleri(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sunucu = ThreadingHTTPServer(("127.0.0.1", 0), SahteUnsplash)
        cls.is_parcacigi = threading.Thread(target=cls.sunucu.serve_forever, daemon=True)
        cls.is_parcacigi.start()
        cls.taban = f"http://127.0.0.1:{cls.sunucu.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.sunucu.shutdown()
        cls.sunucu.server_close()

    def setUp(self) -> None:
        _sunucu_sifirla()
        self.gecici = tempfile.TemporaryDirectory()
        self.addCleanup(self.gecici.cleanup)
        self.klasor = Path(self.gecici.name)

    def _calistir(self, *argumanlar: str) -> subprocess.CompletedProcess:
        ortam = os.environ.copy()
        ortam.update({
            "UNSPLASH_API_TABANI": self.taban,
            "UNSPLASH_ACCESS_KEY": "test-anahtar",
            "PYTHONIOENCODING": "utf-8",
            "NO_PROXY": "127.0.0.1,localhost",
            "no_proxy": "127.0.0.1,localhost",
        })
        return subprocess.run(
            [sys.executable, str(ARAC), *argumanlar],
            cwd=self.klasor,
            env=ortam,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=90,
        )

    @staticmethod
    def _json(metin: str) -> dict:
        return json.loads(metin)

    def test_slug_uret_turkce_ve_ascii(self) -> None:
        import importlib.util
        belirtec = importlib.util.spec_from_file_location("unsplash_gorsel", ARAC)
        modul = importlib.util.module_from_spec(belirtec)
        sys.modules[belirtec.name] = modul
        belirtec.loader.exec_module(modul)  # type: ignore[union-attr]
        self.assertEqual(modul.slug_uret("Hakkımızda Çalışma Şeklimiz"), "hakkimizda-calisma-seklimiz")
        self.assertEqual(modul.slug_uret("  Modern   OFİS -- 2026  "), "modern-ofis-2026")
        self.assertEqual(modul.slug_uret("!!!", yedek="unsplash-foto1"), "unsplash-foto1")
        self.assertLessEqual(len(modul.slug_uret("a" * 200, yedek="x")), 60)

    def test_ara_filtreler_ve_basliklar(self) -> None:
        sonuc = self._calistir("ara", "--sorgu", "modern office", "--adet", "5", "--yon", "landscape", "--min-genislik", "1600")
        self.assertEqual(sonuc.returncode, 0, sonuc.stderr)
        veri = self._json(sonuc.stdout)
        self.assertEqual(len(veri["sonuclar"]), 1)
        foto = veri["sonuclar"][0]
        self.assertEqual(foto["id"], "foto1")
        self.assertIn("ixid=test-ixid-foto1", foto["ham_url"])
        self.assertIn("utm_source=", foto["fotografci"]["profil_url"])
        self.assertEqual(veri["kota"]["kalan"], 49)
        arama = [k for k in SUNUCU["kayitlar"] if k["yol"] == "/search/photos"][0]
        self.assertEqual(arama["basliklar"]["authorization"], "Client-ID test-anahtar")
        self.assertEqual(arama["basliklar"]["accept-version"], "v1")
        sorgu = parse_qs(arama["sorgu"])
        self.assertEqual(sorgu["content_filter"], ["high"])
        self.assertEqual(sorgu["orientation"], ["landscape"])
        self.assertLessEqual(int(sorgu["per_page"][0]), 30)

    def test_indir_tetikleyici_once_ve_dosyalar(self) -> None:
        sonuc = self._calistir("indir", "--id", "foto1", "--ad", "hakkimizda-kapak", "--genislikler", "640,960")
        self.assertEqual(sonuc.returncode, 0, sonuc.stderr)
        veri = self._json(sonuc.stdout)
        self.assertEqual(veri["durum"], "indirildi")
        dosya_adlari = sorted(p.name for p in (self.klasor / "assets" / "img").glob("*.webp"))
        self.assertEqual(dosya_adlari, ["hakkimizda-kapak-640.webp", "hakkimizda-kapak-960.webp"])
        self.assertIn("hakkimizda-kapak-640.webp 640w", veri["srcset"])
        self.assertIn("Unsplash", veri["atif_html"])
        kaynak = self._json((self.klasor / "assets" / "img" / "credits.json").read_text(encoding="utf-8"))
        self.assertEqual(kaynak["fotograflar"][0]["id"], "foto1")
        yollar = [k["yol"] for k in SUNUCU["kayitlar"]]
        tetik = yollar.index("/photos/foto1/download")
        gorsel = min(i for i, y in enumerate(yollar) if y.startswith("/img/foto1"))
        self.assertLess(tetik, gorsel)
        gorsel_kayit = [k for k in SUNUCU["kayitlar"] if k["yol"].startswith("/img/foto1")][0]
        self.assertNotIn("authorization", gorsel_kayit["basliklar"])
        self.assertIn("ixid=test-ixid-foto1", gorsel_kayit["sorgu"])
        self.assertIn("fm=webp", gorsel_kayit["sorgu"])
        self.assertIn("w=640", gorsel_kayit["sorgu"])
        self.assertNotIn("test-anahtar", sonuc.stdout + sonuc.stderr)

    def test_indir_ikinci_calistirma_onbellek(self) -> None:
        ilk = self._calistir("indir", "--id", "foto1", "--ad", "hakkimizda-kapak", "--genislikler", "640")
        self.assertEqual(ilk.returncode, 0, ilk.stderr)
        tetik_once = sum(1 for k in SUNUCU["kayitlar"] if k["yol"] == "/photos/foto1/download")
        gorsel_once = sum(1 for k in SUNUCU["kayitlar"] if k["yol"].startswith("/img/foto1"))
        ikinci = self._calistir("indir", "--id", "foto1", "--ad", "hakkimizda-kapak", "--genislikler", "640")
        self.assertEqual(ikinci.returncode, 0, ikinci.stderr)
        self.assertEqual(self._json(ikinci.stdout)["durum"], "onbellek")
        self.assertEqual(sum(1 for k in SUNUCU["kayitlar"] if k["yol"] == "/photos/foto1/download"), tetik_once)
        self.assertEqual(sum(1 for k in SUNUCU["kayitlar"] if k["yol"].startswith("/img/foto1")), gorsel_once)

    def test_gecersiz_anahtar_kodu_3(self) -> None:
        SUNUCU["arama_zorla"] = [401]
        sonuc = self._calistir("ara", "--sorgu", "test")
        self.assertEqual(sonuc.returncode, 3)
        hata = self._json(sonuc.stderr)
        self.assertEqual(hata["kod"], 3)
        self.assertIn("anahtar", hata["hata"].lower())

    def test_500_sonrasi_yeniden_deneme(self) -> None:
        SUNUCU["arama_zorla"] = [500]
        sonuc = self._calistir("ara", "--sorgu", "test")
        self.assertEqual(sonuc.returncode, 0, sonuc.stderr)
        self.assertEqual(sum(1 for k in SUNUCU["kayitlar"] if k["yol"] == "/search/photos"), 2)

    def test_tetikleyici_hatasi_kodu_7(self) -> None:
        SUNUCU["tetik_zorla"] = [500, 500, 500]
        sonuc = self._calistir("indir", "--id", "foto1", "--ad", "kapak")
        self.assertEqual(sonuc.returncode, 7)
        self.assertFalse(list((self.klasor / "assets" / "img").glob("*.webp")))

    def test_bozuk_gorsel_kodu_6(self) -> None:
        SUNUCU["bozuk_gorsel"] = True
        sonuc = self._calistir("indir", "--id", "foto1", "--ad", "kapak")
        self.assertEqual(sonuc.returncode, 6)
        klasor = self.klasor / "assets" / "img"
        self.assertFalse(list(klasor.glob("*.webp")))
        self.assertFalse(list(klasor.glob("*.tmp*")))

    def test_guvensiz_url_kodu_6(self) -> None:
        SUNUCU["guvensiz_gorsel"] = True
        sonuc = self._calistir("indir", "--id", "foto1", "--ad", "kapak")
        self.assertEqual(sonuc.returncode, 6)
        self.assertFalse(any(k["yol"].startswith("/img/") for k in SUNUCU["kayitlar"]))

    def test_bozuk_manifest_yedeklenir(self) -> None:
        klasor = self.klasor / "assets" / "img"
        klasor.mkdir(parents=True)
        (klasor / "credits.json").write_text("{bozuk", encoding="utf-8")
        sonuc = self._calistir("indir", "--id", "foto1", "--ad", "kapak", "--genislikler", "640")
        self.assertEqual(sonuc.returncode, 0, sonuc.stderr)
        self.assertTrue(list(klasor.glob("credits.json.bozuk-*")))
        self.assertIn("fotograflar", self._json((klasor / "credits.json").read_text(encoding="utf-8")))


    def test_baglantidan_indir_yuksek_cozunurluk(self) -> None:
        kaynak = f"{self.taban}/img/tarayici?ixid=web-ixid&w=400&q=80&fm=jpg&crop=entropy&cs=srgb"
        sonuc = self._calistir(
            "baglantidan-indir",
            "--url", kaynak,
            "--ad", "hakkimizda-kapak",
            "--genislik", "2400",
            "--kalite", "92",
            "--fotografci", "Test Foto",
            "--profil-url", "https://unsplash.com/@testfoto",
            "--fotograf-sayfasi", "https://unsplash.com/photos/abc123",
            "--fotograf-id", "abc123",
            "--sorgu", "modern office",
        )
        self.assertEqual(sonuc.returncode, 0, sonuc.stderr)
        veri = self._json(sonuc.stdout)
        self.assertEqual(veri["durum"], "indirildi")
        dosya = self.klasor / "assets" / "img" / "hakkimizda-kapak-2400.webp"
        self.assertTrue(dosya.is_file())
        self.assertIn("utm_source=", veri["atif_html"])
        kaynak_json = self._json((self.klasor / "assets" / "img" / "credits.json").read_text(encoding="utf-8"))
        kayit = kaynak_json["fotograflar"][0]
        self.assertEqual(kayit["id"], "abc123")
        self.assertEqual(kayit["kaynak"], "tarayici")
        self.assertEqual(kayit["ticari_durum"], "manuel_dogrulama_gerekli")
        gorsel_kayit = [k for k in SUNUCU["kayitlar"] if k["yol"].startswith("/img/tarayici")][0]
        sorgu = parse_qs(gorsel_kayit["sorgu"])
        self.assertEqual(sorgu["w"], ["2400"])
        self.assertEqual(sorgu["q"], ["92"])
        self.assertEqual(sorgu["fm"], ["webp"])
        self.assertEqual(sorgu["fit"], ["max"])
        self.assertEqual(sorgu["ixid"], ["web-ixid"])
        self.assertNotIn("crop", sorgu)
        self.assertNotIn("cs", sorgu)
        self.assertNotIn("authorization", gorsel_kayit["basliklar"])

    def test_baglantidan_indir_guvensiz_url(self) -> None:
        sonuc = self._calistir("baglantidan-indir", "--url", "http://example.com/kotu.webp", "--ad", "kapak")
        self.assertEqual(sonuc.returncode, 6)
        self.assertFalse(list((self.klasor / "assets" / "img").glob("*.webp")))

    def test_baglantidan_indir_bozuk_gorsel(self) -> None:
        SUNUCU["bozuk_gorsel"] = True
        sonuc = self._calistir("baglantidan-indir", "--url", f"{self.taban}/img/tarayici", "--ad", "kapak")
        self.assertEqual(sonuc.returncode, 6)
        self.assertFalse(list((self.klasor / "assets" / "img").glob("*.webp")))

    def test_baglantidan_indir_onbellek(self) -> None:
        argumanlar = ("baglantidan-indir", "--url", f"{self.taban}/img/tarayici", "--ad", "kapak", "--genislik", "2400")
        ilk = self._calistir(*argumanlar)
        self.assertEqual(ilk.returncode, 0, ilk.stderr)
        gorsel_once = sum(1 for k in SUNUCU["kayitlar"] if k["yol"].startswith("/img/tarayici"))
        ikinci = self._calistir(*argumanlar)
        self.assertEqual(ikinci.returncode, 0, ikinci.stderr)
        self.assertEqual(self._json(ikinci.stdout)["durum"], "onbellek")
        self.assertEqual(sum(1 for k in SUNUCU["kayitlar"] if k["yol"].startswith("/img/tarayici")), gorsel_once)


    def test_ara_ticari_degerlendirme(self) -> None:
        portre = self._calistir("ara", "--sorgu", "office", "--yon", "portrait", "--min-genislik", "1000")
        self.assertEqual(portre.returncode, 0, portre.stderr)
        riskli = self._json(portre.stdout)["sonuclar"][0]
        self.assertEqual(riskli["id"], "foto3")
        self.assertEqual(riskli["ticari_degerlendirme"]["durum"], "engelli")
        self.assertTrue(riskli["ticari_degerlendirme"]["engel_nedenleri"])
        notr = self._calistir("ara", "--sorgu", "office", "--adet", "1", "--min-genislik", "1000")
        self.assertEqual(notr.returncode, 0, notr.stderr)
        self.assertEqual(self._json(notr.stdout)["sonuclar"][0]["ticari_degerlendirme"]["durum"], "manuel_dogrulama_gerekli")

    def test_indir_ticari_engel_premium(self) -> None:
        sonuc = self._calistir("indir", "--id", "premium1", "--ad", "premium-test")
        self.assertEqual(sonuc.returncode, 8)
        self.assertEqual(self._json(sonuc.stderr)["kod"], 8)
        self.assertFalse(any(k["yol"].endswith("/download") for k in SUNUCU["kayitlar"]))
        self.assertFalse(list((self.klasor / "assets" / "img").glob("*.webp")))

    def test_indir_ticari_engel_kisi(self) -> None:
        sonuc = self._calistir("indir", "--id", "riskli1", "--ad", "riskli-test")
        self.assertEqual(sonuc.returncode, 8)
        self.assertIn("ticari", self._json(sonuc.stderr)["hata"].lower())
        self.assertFalse(list((self.klasor / "assets" / "img").glob("*.webp")))

    def test_ticari_onay_akisi(self) -> None:
        ilk = self._calistir("indir", "--id", "foto1", "--ad", "ticari-kapak", "--genislikler", "640")
        self.assertEqual(ilk.returncode, 0, ilk.stderr)
        self.assertEqual(self._json(ilk.stdout)["ticari_durum"], "manuel_dogrulama_gerekli")
        manifest_yolu = self.klasor / "assets" / "img" / "credits.json"
        once = self._json(manifest_yolu.read_text(encoding="utf-8"))["fotograflar"][0]
        self.assertEqual(once["ticari_durum"], "manuel_dogrulama_gerekli")
        onay = self._calistir(
            "onayla", "--id", "foto1", "--ad", "ticari-kapak", "--karar", "uygun",
            "--onaylayan", "Test Ajan", "--not", "Logo/insan yok",
        )
        self.assertEqual(onay.returncode, 0, onay.stderr)
        self.assertEqual(self._json(onay.stdout)["ticari_durum"], "onaylandi")
        sonra = self._json(manifest_yolu.read_text(encoding="utf-8"))["fotograflar"][0]
        self.assertEqual(sonra["ticari_durum"], "onaylandi")
        self.assertEqual(sonra["ticari_onay"]["onaylayan"], "Test Ajan")

    def test_onayla_bulunamadi(self) -> None:
        sonuc = self._calistir("onayla", "--id", "yokid", "--ad", "yok", "--karar", "uygun")
        self.assertEqual(sonuc.returncode, 4)

    def test_baglantidan_indir_ticari_engel(self) -> None:
        sonuc = self._calistir("baglantidan-indir", "--url", f"{self.taban}/img/premium_photo-123?ixid=x", "--ad", "premium")
        self.assertEqual(sonuc.returncode, 8)
        self.assertFalse(any(k["yol"].startswith("/img/") for k in SUNUCU["kayitlar"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
