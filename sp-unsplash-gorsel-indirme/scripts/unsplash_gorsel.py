#!/usr/bin/env python3
"""Unsplash görsel arama ve indirme aracı (yalnız Python standart kütüphanesi)."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VARSAYILAN_API_TABANI = "https://api.unsplash.com"
VARSAYILAN_KLASOR = "assets/img"
VARSAYILAN_GENISLIKLER = "640,960,1440"
VARSAYILAN_KALITE = 82
VARSAYILAN_TARAYICI_GENISLIGI = 2400
VARSAYILAN_TARAYICI_KALITE = 92
TARAYICI_ID_ONEKI = "tarayici-"
VARSAYILAN_UYGULAMA = "sp-gorsel-indirme"
MANIFEST_ADI = "credits.json"
ORTAM_ANAHTARI = "UNSPLASH_ACCESS_KEY"
ORTAM_API_TABANI = "UNSPLASH_API_TABANI"
ORTAM_UYGULAMA = "UNSPLASH_UTM_SOURCE"
ISTEK_ZAMAN_ASIMI = 20
YENIDEN_DENEME = 3
GERI_CEKILME = (1.0, 2.0, 4.0)
AZAMI_JSON_BAYT = 2 * 1024 * 1024
AZAMI_GORSEL_BAYT = 20 * 1024 * 1024
AZAMI_GENISLIK = 3840
ASGARI_GENISLIK = 320
AZAMI_PER_PAGE = 30
SLUG_AZAMI = 60
YEREL_HOSTLAR = frozenset({"127.0.0.1", "localhost", "::1"})
API_HOSTLARI = frozenset({"api.unsplash.com"}) | YEREL_HOSTLAR
GORSEL_HOST_ONEKI = ".unsplash.com"
KOTA_UYARI_ESIGI = 5
TICARI_KULLANIM = "ticari"
EDITORIAL_KULLANIM = "editorial"
TICARI_DURUM_ENGELLI = "engelli"
TICARI_DURUM_MANUEL = "manuel_dogrulama_gerekli"
TICARI_DURUM_ONAYLANDI = "onaylandi"
TICARI_DURUM_REDDEDILDI = "reddedildi"
TICARI_DURUM_EDITORIAL = "editorial"
TICARI_ONAY_KARARLARI = ("uygun", "uygun-degil")
TICARI_ENGEL_TERIMLERI = (
    "man", "men", "woman", "women", "person", "people", "child", "children", "kid", "kids",
    "baby", "face", "portrait", "selfie", "group", "team", "businessman", "businesswoman",
    "model", "girl", "boy", "family", "couple", "hands",
    "logo", "brand", "trademark", "billboard", "storefront",
    "nike", "adidas", "coca-cola", "starbucks", "mcdonald", "iphone", "apple store",
    "ferrari", "lamborghini", "bmw", "mercedes", "toyota", "tesla",
    "painting", "artwork", "sculpture", "mural", "graffiti", "statue",
    "gun", "rifle", "weapon", "violence", "blood", "nude", "naked", "drug", "cannabis",
    "cigarette", "smoking", "alcohol", "beer", "wine", "whiskey", "gambling", "casino",
    "politics", "political", "protest", "religion", "religious", "church", "mosque",
    "military", "soldier", "police", "uniform", "money", "cash", "credit card",
    "passport", "id card", "syringe", "hospital", "medical", "eiffel tower", "private property",
    "insan", "kişi", "kadın", "erkek", "çocuk", "bebek", "yüz", "portre", "grup", "ekip",
    "aile", "çift", "eller", "marka", "tabela", "asker", "polis", "silah", "şiddet", "kan",
    "çıplak", "uyuşturucu", "sigara", "alkol", "bira", "şarap", "kumar", "siyaset",
    "protesto", "din", "kilise", "cami", "para", "nakit", "kredi kartı", "pasaport",
    "kimlik", "hastane", "tıbbi", "eyfel",
)

CIKIS_TAMAM = 0
CIKIS_KULLANIM = 2
CIKIS_ANAHTAR = 3
CIKIS_BULUNAMADI = 4
CIKIS_API = 5
CIKIS_DOGRULAMA = 6
CIKIS_UYUM = 7
CIKIS_TICARI = 8

_TURKCE_HARFLER = str.maketrans({
    "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g", "ı": "i", "İ": "i",
    "ö": "o", "Ö": "o", "ş": "s", "Ş": "s", "ü": "u", "Ü": "u",
})


class AracHatasi(Exception):
    """Kullanıcıya Türkçe mesaj ve çıkış kodu taşıyan beklenen hata."""

    def __init__(self, kod: int, mesaj: str) -> None:
        super().__init__(mesaj)
        self.kod = kod
        self.mesaj = mesaj


@dataclass(frozen=True)
class Yanit:
    durum: int
    govde: bytes
    basliklar: dict[str, str]
    son_url: str


@dataclass
class Islem:
    foto_id: str
    ad_ham: str
    bicim: str
    genislikler: tuple[int, ...]
    klasor: Path
    kalite: int
    uygulama: str
    sorgu: str
    uzerine: bool
    ad: str = ""
    mevcut_kayit: dict[str, Any] | None = None
    kullanim_turu: str = TICARI_KULLANIM
    ticari_durum: str = TICARI_DURUM_MANUEL
    ticari_degerlendirme: dict[str, Any] | None = None


def slug_uret(metin: str, yedek: str = "unsplash-gorsel") -> str:
    cevrilmis = (metin or "").translate(_TURKCE_HARFLER)
    normal = unicodedata.normalize("NFKD", cevrilmis)
    ascii_metin = "".join(karakter for karakter in normal if not unicodedata.combining(karakter))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_metin.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)[:SLUG_AZAMI].strip("-")
    return slug or yedek


def _simdi() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _tam_sayi(deger: Any) -> int:
    try:
        return int(deger)
    except (TypeError, ValueError):
        return 0


def _kisalt(metin: str, sinir: int) -> str:
    temiz = (metin or "").strip()
    if len(temiz) <= sinir:
        return temiz
    return temiz[: sinir - 1].rstrip() + "…"


def _oran(genislik: int, yukseklik: int) -> str:
    if genislik <= 0 or yukseklik <= 0:
        return ""
    bolen = math.gcd(genislik, yukseklik)
    return f"{genislik // bolen}:{yukseklik // bolen}"


def _goreli(yol: Path) -> str:
    try:
        return yol.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return yol.resolve().as_posix()


def _utm_ekle(url: str, uygulama: str) -> str:
    ayirac = "&" if urllib.parse.urlsplit(url).query else "?"
    return f"{url}{ayirac}{urllib.parse.urlencode({'utm_source': uygulama, 'utm_medium': 'referral'})}"


def _atif_html(fotografci: str, profil_url: str, uygulama: str) -> str:
    return (
        f'Fotoğraf: <a href="{_utm_ekle(profil_url, uygulama)}">{html.escape(fotografci)}</a> / '
        f'<a href="{_utm_ekle("https://unsplash.com/", uygulama)}">Unsplash</a>'
    )


def _parametre_ekle(url: str, parametreler: dict[str, Any]) -> str:
    ayirac = "&" if urllib.parse.urlsplit(url).query else "?"
    return f"{url}{ayirac}{urllib.parse.urlencode(parametreler)}"


def _gorsel_url_olustur(ham: str, genislik: int, bicim: str, kalite: int) -> str:
    return _parametre_ekle(ham, {"w": genislik, "q": kalite, "fm": bicim, "fit": "max"})


def _api_url_guvenli(url: str) -> bool:
    parca = urllib.parse.urlsplit(url)
    ana_makine = parca.hostname or ""
    if parca.scheme == "https" and ana_makine in API_HOSTLARI:
        return True
    return parca.scheme == "http" and ana_makine in YEREL_HOSTLAR


def _gorsel_url_guvenli(url: str) -> bool:
    parca = urllib.parse.urlsplit(url)
    ana_makine = parca.hostname or ""
    if parca.scheme == "https" and ana_makine.endswith(GORSEL_HOST_ONEKI):
        return True
    return parca.scheme == "http" and ana_makine in YEREL_HOSTLAR


def _api_basliklari(anahtar: str) -> dict[str, str]:
    return {
        "Authorization": f"Client-ID {anahtar}",
        "Accept-Version": "v1",
        "Accept": "application/json",
        "User-Agent": f"{VARSAYILAN_UYGULAMA}/1.0",
    }


def _hata_ayrintisi(govde: bytes) -> str:
    try:
        veri = json.loads(govde.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return ""
    hatalar = veri.get("errors") if isinstance(veri, dict) else None
    if isinstance(hatalar, list):
        return _kisalt("; ".join(str(hata) for hata in hatalar[:2]), 200)
    return ""


def _durum_hatasi(kod: int, govde: bytes, basliklar: dict[str, str]) -> AracHatasi:
    mesajlar = {
        400: "İstek geçersiz; parametreleri kontrol edin.",
        401: "API anahtarı geçersiz veya yetkisiz. UNSPLASH_ACCESS_KEY değerini kontrol edin.",
        403: "Erişim reddedildi. Hız limiti dolmuş veya uygulama izni yok olabilir.",
        404: "İstenen kaynak bulunamadı.",
        410: "Sorgu spam olarak işaretlenmiş olabilir; arama terimini değiştirin.",
        429: "Hız limiti aşıldı. Demo modunda saatlik 50 JSON isteği sınırı vardır.",
    }
    mesaj = mesajlar.get(kod, f"Unsplash API hatası (HTTP {kod}).")
    ayrinti = _hata_ayrintisi(govde)
    if ayrinti:
        mesaj = f"{mesaj} Ayrıntı: {ayrinti}"
    kalan = basliklar.get("x-ratelimit-remaining")
    if kod == 429 and kalan is not None:
        mesaj = f"{mesaj} Kalan kota: {kalan}."
    if kod == 401:
        return AracHatasi(CIKIS_ANAHTAR, mesaj)
    if kod == 404:
        return AracHatasi(CIKIS_BULUNAMADI, mesaj)
    return AracHatasi(CIKIS_API, mesaj)


def _bekle(deneme: int, retry_after: str | None) -> None:
    if retry_after:
        try:
            sure = max(0.0, min(float(retry_after), 5.0))
        except ValueError:
            sure = GERI_CEKILME[min(deneme, len(GERI_CEKILME) - 1)]
    else:
        sure = GERI_CEKILME[min(deneme, len(GERI_CEKILME) - 1)]
    time.sleep(sure)


def _govde_oku(yanit: Any, azami_bayt: int, hata_kodu: int) -> bytes:
    parcalar: list[bytes] = []
    toplam = 0
    while True:
        parca = yanit.read(65536)
        if not parca:
            break
        toplam += len(parca)
        if toplam > azami_bayt:
            raise AracHatasi(hata_kodu, "Sunucu yanıtı izin verilen boyutu aştı; indirme reddedildi.")
        parcalar.append(parca)
    return b"".join(parcalar)


def _tek_istek(url: str, basliklar: dict[str, str], azami_bayt: int, hata_kodu: int) -> Yanit:
    istek = urllib.request.Request(url, headers=basliklar)
    with urllib.request.urlopen(istek, timeout=ISTEK_ZAMAN_ASIMI) as yanit:
        govde = _govde_oku(yanit, azami_bayt, hata_kodu)
        yanit_basliklari = {anahtar.lower(): deger for anahtar, deger in yanit.headers.items()}
        return Yanit(yanit.status, govde, yanit_basliklari, yanit.geturl())


def _istek(url: str, basliklar: dict[str, str], azami_bayt: int, hata_kodu: int) -> Yanit:
    son_hata: Exception | None = None
    son_kod: int | None = None
    for deneme in range(YENIDEN_DENEME):
        try:
            return _tek_istek(url, basliklar, azami_bayt, hata_kodu)
        except urllib.error.HTTPError as hata:
            son_hata = hata
            son_kod = hata.code
            govde = hata.read() if hata.fp else b""
            basliklar_hata = {anahtar.lower(): deger for anahtar, deger in (hata.headers or {}).items()}
            if hata.code != 429 and not 500 <= hata.code < 600:
                raise _durum_hatasi(hata.code, govde, basliklar_hata) from hata
            if deneme + 1 >= YENIDEN_DENEME:
                break
            _bekle(deneme, basliklar_hata.get("retry-after"))
        except (urllib.error.URLError, TimeoutError, OSError) as hata:
            son_hata = hata
            if deneme + 1 >= YENIDEN_DENEME:
                break
            time.sleep(GERI_CEKILME[min(deneme, len(GERI_CEKILME) - 1)])
    kod_metni = f" (HTTP {son_kod})" if son_kod else ""
    raise AracHatasi(
        CIKIS_API,
        f"Unsplash isteği tamamlanamadı{kod_metni}. İnternet, proxy ve hız limitini kontrol edip yeniden deneyin. "
        f"Son hata: {type(son_hata).__name__ if son_hata else 'bilinmiyor'}.",
    )


def _api_istek(url: str, anahtar: str) -> tuple[dict[str, Any], dict[str, str]]:
    if not _api_url_guvenli(url):
        raise AracHatasi(CIKIS_DOGRULAMA, "Güvenli olmayan API adresi reddedildi.")
    yanit = _istek(url, _api_basliklari(anahtar), AZAMI_JSON_BAYT, CIKIS_API)
    if not _api_url_guvenli(yanit.son_url):
        raise AracHatasi(CIKIS_DOGRULAMA, "API isteği güvenli olmayan adrese yönlendi.")
    try:
        veri = json.loads(yanit.govde.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as hata:
        raise AracHatasi(CIKIS_API, "Unsplash API yanıtı geçerli JSON değil.") from hata
    if not isinstance(veri, dict):
        raise AracHatasi(CIKIS_API, "Unsplash API yanıtı beklenen nesne biçiminde değil.")
    return veri, yanit.basliklar


def _api_url_olustur(yol: str, parametreler: dict[str, Any]) -> str:
    temel = os.environ.get(ORTAM_API_TABANI, VARSAYILAN_API_TABANI).rstrip("/")
    url = f"{temel}{yol}"
    if parametreler:
        url = f"{url}?{urllib.parse.urlencode(parametreler)}"
    return url


def _env_dosyasini_yukle(yol: Path) -> None:
    if not yol.is_file():
        return
    try:
        satirlar = yol.read_text(encoding="utf-8").splitlines()
    except OSError as hata:
        raise AracHatasi(CIKIS_DOGRULAMA, f".env dosyası okunamadı: {hata.strerror or 'bilinmeyen hata'}.") from hata
    for satir in satirlar:
        temiz = satir.strip()
        if not temiz or temiz.startswith("#") or "=" not in temiz:
            continue
        ad, deger = temiz.split("=", 1)
        ad = ad.strip()
        deger = deger.strip().strip('"').strip("'")
        if ad and ad not in os.environ:
            os.environ[ad] = deger


def _anahtar_al(env_dosyasi: str) -> str:
    _env_dosyasini_yukle(Path(env_dosyasi) if env_dosyasi else Path(".env"))
    anahtar = os.environ.get(ORTAM_ANAHTARI, "").strip()
    if not anahtar:
        raise AracHatasi(
            CIKIS_ANAHTAR,
            "UNSPLASH_ACCESS_KEY tanımlı değil. Anahtarı ortam değişkenine veya proje kökündeki .env dosyasına ekleyin "
            "(UNSPLASH_ACCESS_KEY=...). Anahtar https://unsplash.com/oauth/applications adresinden alınır.",
        )
    if len(anahtar) < 8 or anahtar.startswith("BURAYA") or any(karakter.isspace() for karakter in anahtar):
        raise AracHatasi(
            CIKIS_ANAHTAR,
            "UNSPLASH_ACCESS_KEY biçimi geçersiz görünüyor. Gerçek Access Key değerini kullanın; yer tutucu veya boşluk bırakmayın.",
        )
    return anahtar


def _uygulama_adi(arguman: str | None) -> str:
    ham = (os.environ.get(ORTAM_UYGULAMA) or arguman or VARSAYILAN_UYGULAMA).strip()
    temiz = re.sub(r"[^A-Za-z0-9_-]+", "-", ham).strip("-")
    return temiz or VARSAYILAN_UYGULAMA


def _fotografci_bilgisi(foto: dict[str, Any], uygulama: str) -> dict[str, str]:
    kullanici = foto.get("user") if isinstance(foto.get("user"), dict) else {}
    ad = str(kullanici.get("name") or "Unsplash").strip() or "Unsplash"
    kullanici_adi = str(kullanici.get("username") or "").strip()
    baglantilar = kullanici.get("links") if isinstance(kullanici.get("links"), dict) else {}
    profil = str(baglantilar.get("html") or "").strip()
    if not profil and kullanici_adi:
        profil = f"https://unsplash.com/@{urllib.parse.quote(kullanici_adi)}"
    foto_baglantilari = foto.get("links") if isinstance(foto.get("links"), dict) else {}
    sayfa = str(foto_baglantilari.get("html") or "").strip() or f"https://unsplash.com/photos/{foto.get('id', '')}"
    return {
        "ad": ad,
        "kullanici": kullanici_adi,
        "profil_url": _utm_ekle(profil or "https://unsplash.com/", uygulama),
        "fotograf_sayfasi": _utm_ekle(sayfa, uygulama),
        "atif_html": _atif_html(ad, profil or "https://unsplash.com/", uygulama),
    }


def _ticari_kaynak_riski(url: str, fotografci: str = "") -> list[str]:
    kucuk_url = (url or "").casefold()
    kucuk_kisi = (fotografci or "").casefold()
    nedenler: list[str] = []
    if "plus.unsplash.com" in kucuk_url or "premium_photo" in kucuk_url:
        nedenler.append("Unsplash+ premium görsel: standart Unsplash License kapsamaz, abonelik gerekir")
    if "gettyimages" in kucuk_kisi or "unsplash+" in kucuk_kisi:
        nedenler.append("Getty/Unsplash+ kaynaklı görsel: ayrı lisans gerekir")
    return nedenler


def _ticari_metin_riski(metin: str) -> list[str]:
    kucuk = (metin or "").casefold()
    if not kucuk:
        return []
    eslesen = [terim for terim in TICARI_ENGEL_TERIMLERI if re.search(rf"(?<!\w){re.escape(terim)}(?!\w)", kucuk)]
    return list(dict.fromkeys(eslesen))


def ticari_degerlendir(
    url: str,
    aciklama: str = "",
    fotografci: str = "",
    kullanim_turu: str = TICARI_KULLANIM,
) -> dict[str, Any]:
    kaynak = _ticari_kaynak_riski(url, fotografci)
    if kaynak:
        return {"durum": TICARI_DURUM_ENGELLI, "engel_nedenleri": kaynak, "metin_riskleri": [], "not": "Unsplash+ ayrı lisans"}
    metin = _ticari_metin_riski(aciklama)
    if kullanim_turu == EDITORIAL_KULLANIM:
        return {"durum": TICARI_DURUM_EDITORIAL, "engel_nedenleri": [], "metin_riskleri": metin, "not": "Yalnız editoryal kullanım"}
    if metin:
        return {"durum": TICARI_DURUM_ENGELLI, "engel_nedenleri": metin, "metin_riskleri": metin, "not": "Marka/kişi/eser/hassas içerik riski"}
    return {"durum": TICARI_DURUM_MANUEL, "engel_nedenleri": [], "metin_riskleri": [], "not": "Görsel gözle doğrulanmalı"}


def _ticari_kapisi(degerlendirme: dict[str, Any]) -> None:
    if degerlendirme.get("durum") != TICARI_DURUM_ENGELLI:
        return
    nedenler = "; ".join(degerlendirme.get("engel_nedenleri") or ["bilinmeyen risk"])
    raise AracHatasi(
        CIKIS_TICARI,
        f"Ticari kullanım için uygun değil: {nedenler}. Görsel indirilmedi; farklı bir aday seçin veya hukuki onay alın.",
    )


def _ticari_uyarisi(degerlendirme: dict[str, Any]) -> str:
    if degerlendirme.get("durum") == TICARI_DURUM_EDITORIAL:
        return "Editoryal kayıt: ticari reklam/tanıtımda kullanmayın; yalnız editoryal bağlamda kullanın."
    return (
        "Ticari kullanımdan önce görseli gözle doğrulayın (kişi/logo/marka/eser/özel mülk/hassas içerik olmamalı) "
        "ve onayla --karar uygun çalıştırın; onaylanmadan ticari sayfaya eklemeyin."
    )


def _kayit_ticari_durumu(islem: Islem, onceki: dict[str, Any]) -> str:
    eski = str(onceki.get("ticari_durum") or "")
    if eski in (TICARI_DURUM_ONAYLANDI, TICARI_DURUM_REDDEDILDI):
        return eski
    return islem.ticari_durum


def _fotograf_ozeti(foto: dict[str, Any], uygulama: str) -> dict[str, Any]:
    urls = foto.get("urls") if isinstance(foto.get("urls"), dict) else {}
    ham = str(urls.get("raw") or "").strip()
    if not ham:
        raise AracHatasi(CIKIS_API, "API yanıtında görsel adresi (urls.raw) eksik.")
    genislik = _tam_sayi(foto.get("width"))
    yukseklik = _tam_sayi(foto.get("height"))
    bilgi = _fotografci_bilgisi(foto, uygulama)
    kullan_genislik = min(1600, genislik) if genislik else 1600
    return {
        "id": str(foto.get("id") or ""),
        "aciklama": _kisalt(str(foto.get("alt_description") or foto.get("description") or ""), 160),
        "fotografci": {"ad": bilgi["ad"], "kullanici": bilgi["kullanici"], "profil_url": bilgi["profil_url"]},
        "fotograf_sayfasi": bilgi["fotograf_sayfasi"],
        "genislik": genislik,
        "yukseklik": yukseklik,
        "oran": _oran(genislik, yukseklik),
        "renk": foto.get("color"),
        "ham_url": ham,
        "regular_url": str(urls.get("regular") or "").strip(),
        "kullan_url": _gorsel_url_olustur(ham, kullan_genislik, "webp", VARSAYILAN_KALITE),
        "atif_html": bilgi["atif_html"],
        "ticari_degerlendirme": ticari_degerlendir(ham, str(foto.get("alt_description") or foto.get("description") or ""), bilgi["ad"]),
    }


def _kota(basliklar: dict[str, str]) -> dict[str, int] | None:
    try:
        return {
            "limit": int(basliklar.get("x-ratelimit-limit", "")),
            "kalan": int(basliklar.get("x-ratelimit-remaining", "")),
        }
    except (TypeError, ValueError):
        return None


def _sayfa_boyu(adet: int) -> int:
    return min(AZAMI_PER_PAGE, max(10, adet * 2))


def _sorgu_dogrula(sorgu: str) -> str:
    temiz = (sorgu or "").strip()
    if not temiz:
        raise AracHatasi(CIKIS_KULLANIM, "Arama terimi boş olamaz (--sorgu).")
    if len(temiz) > 200:
        raise AracHatasi(CIKIS_KULLANIM, "Arama terimi 200 karakteri aşamaz.")
    return temiz


def _fotograf_id_dogrula(foto_id: str) -> str:
    temiz = (foto_id or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]{5,40}", temiz):
        raise AracHatasi(CIKIS_KULLANIM, "Fotoğraf kimliği geçersiz; Unsplash kimliği 5-40 harf, rakam, tire veya alt çizgi olmalı.")
    return temiz


def _arama_girdileri(ayar: argparse.Namespace) -> dict[str, Any]:
    sorgu = _sorgu_dogrula(ayar.sorgu)
    adet = _tam_sayi(ayar.adet)
    if not 1 <= adet <= AZAMI_PER_PAGE:
        raise AracHatasi(CIKIS_KULLANIM, f"--adet 1-{AZAMI_PER_PAGE} aralığında olmalı.")
    sayfa = _tam_sayi(ayar.sayfa)
    if sayfa < 1:
        raise AracHatasi(CIKIS_KULLANIM, "--sayfa en az 1 olmalı.")
    min_genislik = _tam_sayi(ayar.min_genislik)
    if not 1 <= min_genislik <= AZAMI_GENISLIK:
        raise AracHatasi(CIKIS_KULLANIM, f"--min-genislik 1-{AZAMI_GENISLIK} aralığında olmalı.")
    parametreler: dict[str, Any] = {
        "query": sorgu,
        "page": sayfa,
        "per_page": _sayfa_boyu(adet),
        "content_filter": "high",
        "orientation": ayar.yon,
    }
    if ayar.renk:
        parametreler["color"] = ayar.renk
    return {"sorgu": sorgu, "adet": adet, "min_genislik": min_genislik, "parametreler": parametreler}


def _arama_sonuclari(veri: dict[str, Any], girdi: dict[str, Any], uygulama: str) -> list[dict[str, Any]]:
    sonuclar: list[dict[str, Any]] = []
    for foto in veri.get("results") or []:
        if not isinstance(foto, dict) or _tam_sayi(foto.get("width")) < _tam_sayi(girdi["min_genislik"]):
            continue
        sonuclar.append(_fotograf_ozeti(foto, uygulama))
        if len(sonuclar) >= _tam_sayi(girdi["adet"]):
            break
    if not sonuclar:
        raise AracHatasi(
            CIKIS_BULUNAMADI,
            f"'{girdi['sorgu']}' için uygun görsel bulunamadı. Terimi İngilizce/genel yapın, --min-genislik değerini düşürün veya --sayfa artırın.",
        )
    return sonuclar


def _kota_uyarisi_ekle(cikti: dict[str, Any], basliklar: dict[str, str]) -> None:
    kota = _kota(basliklar)
    if isinstance(kota, dict) and kota.get("kalan", 99) <= KOTA_UYARI_ESIGI:
        cikti["uyari"] = (
            f"Demo kotası azalıyor (kalan: {kota['kalan']}). Demo modunda saatlik 50 JSON isteği vardır; "
            "üretim için uygulama onayı gerekir."
        )


def ara(ayar: argparse.Namespace) -> dict[str, Any]:
    girdi = _arama_girdileri(ayar)
    anahtar = _anahtar_al(ayar.env_dosyasi)
    uygulama = _uygulama_adi(ayar.uygulama_adi)
    veri, basliklar = _api_istek(_api_url_olustur("/search/photos", girdi["parametreler"]), anahtar)
    cikti: dict[str, Any] = {
        "durum": "basarili",
        "sorgu": girdi["sorgu"],
        "toplam": veri.get("total"),
        "kota": _kota(basliklar),
        "sonuclar": _arama_sonuclari(veri, girdi, uygulama),
    }
    _kota_uyarisi_ekle(cikti, basliklar)
    return cikti


def _klasor_coz(ham: str) -> Path:
    yol = Path(ham or VARSAYILAN_KLASOR).expanduser().resolve()
    try:
        yol.mkdir(parents=True, exist_ok=True)
    except OSError as hata:
        raise AracHatasi(CIKIS_DOGRULAMA, f"Görsel klasörü oluşturulamadı: {yol} ({hata.strerror or 'bilinmeyen hata'}).") from hata
    if not yol.is_dir():
        raise AracHatasi(CIKIS_DOGRULAMA, f"Görsel klasörü bir dizin değil: {yol}")
    return yol


def _genislikleri_coz(metin: str) -> tuple[int, ...]:
    parcalar = [parca.strip() for parca in (metin or "").split(",") if parca.strip()]
    if not parcalar:
        raise AracHatasi(CIKIS_KULLANIM, "--genislikler en az bir genişlik içermeli (örn. 640,960,1440).")
    geçerli: set[int] = set()
    for parca in parcalar:
        try:
            genislik = int(parca)
        except ValueError as hata:
            raise AracHatasi(CIKIS_KULLANIM, f"Geçersiz genişlik: {parca}") from hata
        if not ASGARI_GENISLIK <= genislik <= AZAMI_GENISLIK:
            raise AracHatasi(CIKIS_KULLANIM, f"Genişlik {genislik} desteklenmiyor ({ASGARI_GENISLIK}-{AZAMI_GENISLIK}).")
        geçerli.add(genislik)
    return tuple(sorted(geçerli))


def _manifest_oku(klasor: Path) -> tuple[dict[str, Any], str | None]:
    yol = klasor / MANIFEST_ADI
    if not yol.is_file():
        return {"surum": 1, "uygulama": VARSAYILAN_UYGULAMA, "fotograflar": []}, None
    try:
        veri = json.loads(yol.read_text(encoding="utf-8"))
        if not isinstance(veri, dict) or not isinstance(veri.get("fotograflar"), list):
            raise ValueError("beklenen yapı yok")
        return veri, None
    except (OSError, ValueError) as hata:
        yedek = yol.with_name(f"{MANIFEST_ADI}.bozuk-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        try:
            yol.replace(yedek)
        except OSError as yedek_hatasi:
            raise AracHatasi(
                CIKIS_DOGRULAMA,
                "Bozuk credits.json yedeklenemedi; dosyayı elle kontrol edin.",
            ) from yedek_hatasi
        return (
            {"surum": 1, "uygulama": VARSAYILAN_UYGULAMA, "fotograflar": []},
            f"Bozuk credits.json yedeklendi: {yedek.name}. Yeni kayıt başlatıldı ({type(hata).__name__}).",
        )


def _manifest_yaz(klasor: Path, manifest: dict[str, Any]) -> None:
    veri = {
        "surum": 1,
        "guncellendi": _simdi(),
        "uygulama": str(manifest.get("uygulama") or VARSAYILAN_UYGULAMA),
        "fotograflar": manifest.get("fotograflar") if isinstance(manifest.get("fotograflar"), list) else [],
    }
    _atomik_yaz(klasor / MANIFEST_ADI, (json.dumps(veri, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def _manifest_guncelle(manifest: dict[str, Any], kayit: dict[str, Any], uygulama: str) -> None:
    kayitlar = [k for k in manifest.get("fotograflar", []) if isinstance(k, dict)]
    for sira, mevcut in enumerate(kayitlar):
        if (
            mevcut.get("id") == kayit.get("id")
            and mevcut.get("ad") == kayit.get("ad")
            and mevcut.get("bicim") == kayit.get("bicim")
        ):
            kayitlar[sira] = kayit
            break
    else:
        kayitlar.append(kayit)
    manifest["fotograflar"] = kayitlar
    manifest["uygulama"] = uygulama


def _atomik_yaz(hedef: Path, veri: bytes) -> None:
    gecici = hedef.with_name(f".{hedef.name}.tmp-{os.getpid()}-{time.time_ns()}")
    try:
        hedef.parent.mkdir(parents=True, exist_ok=True)
        with open(gecici, "wb") as dosya:
            dosya.write(veri)
            dosya.flush()
            os.fsync(dosya.fileno())
        os.replace(gecici, hedef)
    except OSError as hata:
        try:
            gecici.unlink(missing_ok=True)
        except OSError:
            pass
        raise AracHatasi(CIKIS_DOGRULAMA, f"Dosya yazılamadı: {hedef.name} ({hata.strerror or 'bilinmeyen hata'}).") from hata


def _gorsel_dogrula(govde: bytes, bicim: str) -> None:
    if len(govde) < 100:
        raise AracHatasi(CIKIS_DOGRULAMA, "İndirilen görsel dosyası çok küçük; geçersiz yanıt reddedildi.")
    if bicim == "webp":
        gecerli = govde[:4] == b"RIFF" and govde[8:12] == b"WEBP"
    else:
        gecerli = govde[:3] == b"\xff\xd8\xff"
    if not gecerli:
        raise AracHatasi(CIKIS_DOGRULAMA, f"İndirilen dosya geçerli {bicim.upper()} imzası taşımıyor; indirme reddedildi.")


def _gorsel_indir(url: str, bicim: str) -> bytes:
    if not _gorsel_url_guvenli(url):
        raise AracHatasi(CIKIS_DOGRULAMA, "Görsel adresi güvenli değil (https/Unsplash veya yerel test bekleniyor).")
    basliklar = {"Accept": "image/*", "User-Agent": f"{VARSAYILAN_UYGULAMA}/1.0"}
    yanit = _istek(url, basliklar, AZAMI_GORSEL_BAYT, CIKIS_DOGRULAMA)
    if not _gorsel_url_guvenli(yanit.son_url):
        raise AracHatasi(CIKIS_DOGRULAMA, "Görsel isteği güvenli olmayan adrese yönlendi.")
    icerik_turu = str(yanit.basliklar.get("content-type") or "").lower()
    if icerik_turu and not icerik_turu.startswith("image/"):
        raise AracHatasi(CIKIS_DOGRULAMA, f"Görsel yerine '{icerik_turu}' içerik döndü; indirme reddedildi.")
    _gorsel_dogrula(yanit.govde, bicim)
    return yanit.govde


def _tetikle(anahtar: str, foto: dict[str, Any]) -> None:
    baglantilar = foto.get("links") if isinstance(foto.get("links"), dict) else {}
    link = str(baglantilar.get("download_location") or "").strip()
    if not link or not _api_url_guvenli(link):
        raise AracHatasi(CIKIS_UYUM, "Fotoğrafın geçerli download_location bağlantısı yok; Unsplash API kuralı gereği indirme durduruldu.")
    try:
        yanit = _istek(link, _api_basliklari(anahtar), AZAMI_JSON_BAYT, CIKIS_API)
    except AracHatasi as hata:
        raise AracHatasi(
            CIKIS_UYUM,
            f"İndirme tetikleyicisi çağrılamadı; görsel indirilmedi. Ayrıntı: {hata.mesaj}",
        ) from hata
    if not _api_url_guvenli(yanit.son_url):
        raise AracHatasi(CIKIS_UYUM, "İndirme tetikleyicisi güvenli olmayan adrese yönlendi.")


def _foto_detayi(anahtar: str, foto_id: str) -> dict[str, Any]:
    yol = f"/photos/{urllib.parse.quote(foto_id, safe='')}"
    foto, _ = _api_istek(_api_url_olustur(yol, {}), anahtar)
    if not isinstance(foto, dict) or str(foto.get("id") or "") != foto_id:
        raise AracHatasi(CIKIS_BULUNAMADI, f"'{foto_id}' kimliğine sahip fotoğraf bulunamadı.")
    if not isinstance(foto.get("width"), int) or not isinstance(foto.get("urls"), dict):
        raise AracHatasi(CIKIS_API, "API fotoğraf ayrıntısı beklenen biçimde değil.")
    return foto


def _foto_genisliklerine_sigdir(islem: Islem, foto_genislik: int) -> tuple[int, ...]:
    istenen = tuple(genislik for genislik in islem.genislikler if genislik <= foto_genislik)
    if istenen:
        return istenen
    guvenli = max(ASGARI_GENISLIK, min(foto_genislik or islem.genislikler[0], islem.genislikler[-1]))
    return (guvenli,)


def _ad_belirle(islem: Islem, foto: dict[str, Any]) -> str:
    kaynak = islem.ad_ham or str(foto.get("alt_description") or foto.get("description") or "")
    return slug_uret(kaynak, f"unsplash-{islem.foto_id}")


def _kayit_bul(manifest: dict[str, Any], islem: Islem) -> dict[str, Any] | None:
    for kayit in manifest.get("fotograflar", []):
        if not isinstance(kayit, dict):
            continue
        if (
            str(kayit.get("id")) == islem.foto_id
            and kayit.get("ad") == islem.ad
            and kayit.get("bicim") == islem.bicim
        ):
            return kayit
    return None


def _onbellek_bul(manifest: dict[str, Any], islem: Islem) -> dict[str, Any] | None:
    if islem.uzerine:
        return None
    aday = slug_uret(islem.ad_ham) if islem.ad_ham.strip() else None
    istenen = set(islem.genislikler)
    for kayit in manifest.get("fotograflar", []):
        if not isinstance(kayit, dict):
            continue
        if str(kayit.get("id")) != islem.foto_id or kayit.get("bicim") != islem.bicim:
            continue
        if aday and kayit.get("ad") != aday:
            continue
        kayitli = {_tam_sayi(dosya.get("genislik")) for dosya in kayit.get("dosyalar", []) if isinstance(dosya, dict)}
        if not istenen <= kayitli:
            continue
        if all(
            (islem.klasor / str(dosya.get("dosya") or "")).is_file()
            for dosya in kayit.get("dosyalar", [])
            if isinstance(dosya, dict) and _tam_sayi(dosya.get("genislik")) in istenen
        ):
            return kayit
    return None


def _ad_cakisiyor(manifest: dict[str, Any], islem: Islem, aday: str) -> bool:
    for kayit in manifest.get("fotograflar", []):
        if not isinstance(kayit, dict) or str(kayit.get("id")) == islem.foto_id:
            continue
        if kayit.get("ad") == aday and kayit.get("bicim") == islem.bicim:
            return True
    for genislik in islem.genislikler:
        if (islem.klasor / f"{aday}-{genislik}.{islem.bicim}").exists():
            return True
    return False


def _benzersiz_ad(manifest: dict[str, Any], islem: Islem) -> str:
    for sira in range(2, 50):
        aday = islem.ad if sira == 2 else f"{islem.ad[: SLUG_AZAMI - 5]}-{sira}"
        if not _ad_cakisiyor(manifest, islem, aday):
            return aday
    raise AracHatasi(CIKIS_DOGRULAMA, "Çakışmasız dosya adı üretilemedi; --ad değerini değiştirin.")


def _indirme_planla(islem: Islem, foto: dict[str, Any]) -> list[dict[str, Any]]:
    mevcut: dict[int, str] = {}
    for dosya in (islem.mevcut_kayit or {}).get("dosyalar", []):
        if isinstance(dosya, dict):
            mevcut[_tam_sayi(dosya.get("genislik"))] = str(dosya.get("dosya") or "")
    urls = foto.get("urls") if isinstance(foto.get("urls"), dict) else {}
    ham = str(urls.get("raw") or "").strip()
    if not ham:
        raise AracHatasi(CIKIS_API, "API yanıtında görsel adresi (urls.raw) eksik.")
    plan: list[dict[str, Any]] = []
    for genislik in islem.genislikler:
        dosya_adi = mevcut.get(genislik) or f"{islem.ad}-{genislik}.{islem.bicim}"
        hedef = islem.klasor / dosya_adi
        if genislik in mevcut and hedef.is_file():
            continue
        plan.append({
            "genislik": genislik,
            "dosya": dosya_adi,
            "hedef": hedef,
            "url": _gorsel_url_olustur(ham, genislik, islem.bicim, islem.kalite),
        })
    return plan


def _dosyalari_indir(islem: Islem, plan: list[dict[str, Any]]) -> list[dict[str, Any]]:
    indirilen: list[dict[str, Any]] = []
    for hedef in plan:
        veri = _gorsel_indir(str(hedef["url"]), islem.bicim)
        _atomik_yaz(hedef["hedef"], veri)
        indirilen.append({"dosya": str(hedef["dosya"]), "genislik": _tam_sayi(hedef["genislik"])})
    return indirilen


def _kayit_olustur(islem: Islem, foto: dict[str, Any], indirilen: list[dict[str, Any]]) -> dict[str, Any]:
    onceki = islem.mevcut_kayit or {}
    dosyalar: dict[int, dict[str, Any]] = {}
    for dosya in onceki.get("dosyalar", []):
        if isinstance(dosya, dict):
            dosyalar[_tam_sayi(dosya.get("genislik"))] = {
                "dosya": str(dosya.get("dosya") or ""),
                "genislik": _tam_sayi(dosya.get("genislik")),
            }
    for dosya in indirilen:
        dosyalar[_tam_sayi(dosya.get("genislik"))] = {
            "dosya": str(dosya.get("dosya") or ""),
            "genislik": _tam_sayi(dosya.get("genislik")),
        }
    bilgi = _fotografci_bilgisi(foto, islem.uygulama)
    urls = foto.get("urls") if isinstance(foto.get("urls"), dict) else {}
    return {
        "id": islem.foto_id,
        "ad": islem.ad,
        "bicim": islem.bicim,
        "aciklama": _kisalt(str(foto.get("alt_description") or foto.get("description") or ""), 240),
        "dosyalar": [dosyalar[genislik] for genislik in sorted(dosyalar)],
        "fotografci": {"ad": bilgi["ad"], "kullanici": bilgi["kullanici"], "profil_url": bilgi["profil_url"]},
        "fotograf_sayfasi": bilgi["fotograf_sayfasi"],
        "lisans": "Unsplash License",
        "lisans_url": "https://unsplash.com/license",
        "kaynak": "https://unsplash.com/",
        "atif_html": bilgi["atif_html"],
        "hotlink_url": str(urls.get("regular") or "").strip(),
        "indirme_tarihi": str(onceki.get("indirme_tarihi") or _simdi()),
        "sorgu": islem.sorgu or str(onceki.get("sorgu") or ""),
        "ticari_durum": _kayit_ticari_durumu(islem, onceki),
        "ticari_degerlendirme": islem.ticari_degerlendirme or onceki.get("ticari_degerlendirme") or {},
        "ticari_onay": onceki.get("ticari_onay") or {},
    }


def _cikti_uret(islem: Islem, durum: str, uyari: str | None) -> dict[str, Any]:
    kayit = islem.mevcut_kayit
    if not isinstance(kayit, dict):
        raise AracHatasi(CIKIS_API, "Kayıt bilgisi bulunamadı; işlem tamamlanamadı.")
    istenen = set(islem.genislikler)
    secili: list[dict[str, Any]] = []
    for dosya in kayit.get("dosyalar", []):
        if not isinstance(dosya, dict):
            continue
        genislik = _tam_sayi(dosya.get("genislik"))
        if genislik not in istenen:
            continue
        yol = islem.klasor / str(dosya.get("dosya") or "")
        if not yol.is_file():
            raise AracHatasi(CIKIS_DOGRULAMA, f"Beklenen görsel dosyası bulunamadı: {yol.name}")
        secili.append({"yol": _goreli(yol), "genislik": genislik, "bayt": yol.stat().st_size})
    secili.sort(key=lambda kayit_dosya: int(kayit_dosya["genislik"]))
    fotografci = kayit.get("fotografci") if isinstance(kayit.get("fotografci"), dict) else {}
    cikti: dict[str, Any] = {
        "durum": durum,
        "fotograf": {
            "id": kayit.get("id"),
            "aciklama": kayit.get("aciklama", ""),
            "fotografci": fotografci.get("ad", ""),
            "lisans": kayit.get("lisans", "Unsplash License"),
            "lisans_url": kayit.get("lisans_url", "https://unsplash.com/license"),
        },
        "dosyalar": secili,
        "srcset": ", ".join(f"{dosya['yol']} {dosya['genislik']}w" for dosya in secili),
        "atif_html": kayit.get("atif_html", ""),
        "hotlink_url": kayit.get("hotlink_url", ""),
        "kaynak": kayit.get("kaynak", "api"),
        "ticari_durum": kayit.get("ticari_durum", TICARI_DURUM_MANUEL),
        "ticari_degerlendirme": kayit.get("ticari_degerlendirme") or {},
        "ticari_onay": kayit.get("ticari_onay") or {},
        "credits": _goreli(islem.klasor / MANIFEST_ADI),
    }
    if uyari:
        cikti["uyari"] = uyari
    return cikti


def _unsplash_hostu_mu(host: str) -> bool:
    return host == "unsplash.com" or host.endswith(GORSEL_HOST_ONEKI)


def _yuksek_cozunurluk_url(url: str, genislik: int, bicim: str, kalite: int) -> str:
    if not _gorsel_url_guvenli(url):
        raise AracHatasi(CIKIS_DOGRULAMA, "Görsel adresi güvenli değil (https/Unsplash veya yerel test bekleniyor).")
    parca = urllib.parse.urlsplit(url)
    eski = urllib.parse.parse_qs(parca.query, keep_blank_values=True)
    parametreler: dict[str, Any] = {"w": genislik, "q": kalite, "fm": bicim, "fit": "max"}
    ixid = (eski.get("ixid") or [""])[0]
    if ixid:
        parametreler = {"ixid": ixid, **parametreler}
    return urllib.parse.urlunsplit((parca.scheme, parca.netloc, parca.path, urllib.parse.urlencode(parametreler), ""))


def _atif_urlu_dogrula(url: str, alan: str) -> str:
    temiz = (url or "").strip()
    if not temiz:
        return ""
    parca = urllib.parse.urlsplit(temiz)
    if parca.scheme != "https" or not _unsplash_hostu_mu(parca.hostname or ""):
        raise AracHatasi(CIKIS_KULLANIM, f"{alan} bağlantısı https ve unsplash.com alan adında olmalı.")
    return temiz


def _baglanti_kimligi(verilen: str | None, url: str) -> str:
    temiz = str(verilen or "").strip()
    if temiz:
        return _fotograf_id_dogrula(temiz)
    return TARAYICI_ID_ONEKI + hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]


def _uyari_ekle(uyari: str | None, yeni: str) -> str:
    return f"{uyari} {yeni}" if uyari else yeni


def _baglanti_kaydi(islem: Islem, bilgi: dict[str, str], url_yuksek: str) -> dict[str, Any]:
    onceki = islem.mevcut_kayit or {}
    fotografci = bilgi.get("fotografci") or "Bilinmiyor"
    profil = bilgi.get("profil_url") or "https://unsplash.com/"
    sayfa = bilgi.get("fotograf_sayfasi") or ""
    if not sayfa:
        sayfa = "https://unsplash.com/" if islem.foto_id.startswith(TARAYICI_ID_ONEKI) else f"https://unsplash.com/photos/{islem.foto_id}"
    return {
        "id": islem.foto_id,
        "ad": islem.ad,
        "bicim": islem.bicim,
        "aciklama": "",
        "dosyalar": [{"dosya": f"{islem.ad}-{islem.genislikler[0]}.{islem.bicim}", "genislik": islem.genislikler[0]}],
        "fotografci": {"ad": fotografci, "kullanici": "", "profil_url": _utm_ekle(profil, islem.uygulama)},
        "fotograf_sayfasi": _utm_ekle(sayfa, islem.uygulama),
        "lisans": "Unsplash License",
        "lisans_url": "https://unsplash.com/license",
        "kaynak": "tarayici",
        "atif_html": _atif_html(fotografci, profil, islem.uygulama),
        "hotlink_url": url_yuksek,
        "indirme_tarihi": _simdi(),
        "sorgu": islem.sorgu,
        "ticari_durum": _kayit_ticari_durumu(islem, onceki),
        "ticari_degerlendirme": islem.ticari_degerlendirme or {},
        "ticari_onay": onceki.get("ticari_onay") or {},
    }


def _baglanti_girdileri(ayar: argparse.Namespace) -> dict[str, Any]:
    if not 1 <= _tam_sayi(ayar.kalite) <= 100:
        raise AracHatasi(CIKIS_KULLANIM, "--kalite 1-100 aralığında olmalı.")
    genislik = _tam_sayi(ayar.genislik)
    if not ASGARI_GENISLIK <= genislik <= AZAMI_GENISLIK:
        raise AracHatasi(CIKIS_KULLANIM, f"--genislik {ASGARI_GENISLIK}-{AZAMI_GENISLIK} aralığında olmalı.")
    url_ham = str(ayar.url or "").strip()
    if not _gorsel_url_guvenli(url_ham):
        raise AracHatasi(CIKIS_DOGRULAMA, "Görsel adresi güvenli değil (https/Unsplash veya yerel test bekleniyor).")
    kullanim_turu = getattr(ayar, "kullanim_turu", TICARI_KULLANIM)
    bilgi = {
        "fotografci": _kisalt(str(ayar.fotografci or "").strip(), 120),
        "profil_url": _atif_urlu_dogrula(ayar.profil_url, "Profil"),
        "fotograf_sayfasi": _atif_urlu_dogrula(ayar.fotograf_sayfasi, "Fotoğraf sayfası"),
    }
    degerlendirme = ticari_degerlendir(
        url_ham, str(getattr(ayar, "aciklama", "") or ""), bilgi["fotografci"], kullanim_turu
    )
    _ticari_kapisi(degerlendirme)
    return {
        "url": url_ham,
        "genislik": genislik,
        "bilgi": bilgi,
        "kullanim_turu": kullanim_turu,
        "degerlendirme": degerlendirme,
        "uyari": None,
    }


def _baglanti_islemi(ayar: argparse.Namespace, girdi: dict[str, Any]) -> Islem:
    return Islem(
        foto_id=_baglanti_kimligi(ayar.fotograf_id, girdi["url"]),
        ad_ham=str(ayar.ad or "").strip(),
        bicim=ayar.format,
        genislikler=(girdi["genislik"],),
        klasor=_klasor_coz(ayar.klasor),
        kalite=_tam_sayi(ayar.kalite),
        uygulama=_uygulama_adi(ayar.uygulama_adi),
        kullanim_turu=girdi["kullanim_turu"],
        ticari_durum=(
            TICARI_DURUM_EDITORIAL
            if girdi["degerlendirme"]["durum"] == TICARI_DURUM_EDITORIAL
            else TICARI_DURUM_MANUEL
        ),
        ticari_degerlendirme=girdi["degerlendirme"],
        sorgu=str(ayar.sorgu or "").strip(),
        uzerine=bool(ayar.uzerine_yaz),
    )


def _baglanti_onbellek(manifest: dict[str, Any], islem: Islem, uyari: str | None) -> dict[str, Any] | None:
    onbellek = _onbellek_bul(manifest, islem)
    if onbellek is None:
        return None
    islem.mevcut_kayit = onbellek
    return _cikti_uret(islem, "onbellek", uyari)


def _baglanti_kaydet(islem: Islem, manifest: dict[str, Any], girdi: dict[str, Any]) -> dict[str, Any]:
    islem.ad = slug_uret(islem.ad_ham or Path(urllib.parse.urlsplit(girdi["url"]).path).stem, f"unsplash-{islem.foto_id}")
    islem.mevcut_kayit = _kayit_bul(manifest, islem)
    if islem.mevcut_kayit is None:
        islem.ad = _benzersiz_ad(manifest, islem)
    if not girdi["bilgi"]["fotografci"]:
        girdi["uyari"] = _uyari_ekle(girdi["uyari"], "Fotoğrafçı adı verilmedi; atıf için sayfadan alıp kaydı tamamlayın.")
    girdi["uyari"] = _uyari_ekle(girdi["uyari"], _ticari_uyarisi(girdi["degerlendirme"]))
    url_yuksek = _yuksek_cozunurluk_url(girdi["url"], girdi["genislik"], islem.bicim, islem.kalite)
    veri = _gorsel_indir(url_yuksek, islem.bicim)
    _atomik_yaz(islem.klasor / f"{islem.ad}-{girdi['genislik']}.{islem.bicim}", veri)
    islem.mevcut_kayit = _baglanti_kaydi(islem, girdi["bilgi"], url_yuksek)
    _manifest_guncelle(manifest, islem.mevcut_kayit, islem.uygulama)
    _manifest_yaz(islem.klasor, manifest)
    return _cikti_uret(islem, "indirildi", girdi["uyari"])


def baglantidan_indir(ayar: argparse.Namespace) -> dict[str, Any]:
    girdi = _baglanti_girdileri(ayar)
    islem = _baglanti_islemi(ayar, girdi)
    manifest, manifest_uyarisi = _manifest_oku(islem.klasor)
    girdi["uyari"] = manifest_uyarisi
    onbellek = _baglanti_onbellek(manifest, islem, manifest_uyarisi)
    if onbellek is not None:
        return onbellek
    return _baglanti_kaydet(islem, manifest, girdi)


def _indir_islemi(ayar: argparse.Namespace) -> Islem:
    if not 1 <= _tam_sayi(ayar.kalite) <= 100:
        raise AracHatasi(CIKIS_KULLANIM, "--kalite 1-100 aralığında olmalı.")
    return Islem(
        foto_id=_fotograf_id_dogrula(ayar.fotograf_id),
        ad_ham=str(ayar.ad or "").strip(),
        bicim=ayar.format,
        genislikler=_genislikleri_coz(ayar.genislikler),
        klasor=_klasor_coz(ayar.klasor),
        kalite=_tam_sayi(ayar.kalite),
        uygulama=_uygulama_adi(ayar.uygulama_adi),
        kullanim_turu=ayar.kullanim_turu,
        sorgu=str(ayar.sorgu or "").strip(),
        uzerine=bool(ayar.uzerine_yaz),
    )


def _indir_ticari_kontrol(islem: Islem, foto: dict[str, Any], uyari: str | None) -> str | None:
    aciklama = str(foto.get("alt_description") or foto.get("description") or "")
    kisi = str((foto.get("user") or {}).get("name") or "")
    islem.ticari_degerlendirme = ticari_degerlendir(
        str((foto.get("urls") or {}).get("raw") or ""), aciklama, kisi, islem.kullanim_turu
    )
    _ticari_kapisi(islem.ticari_degerlendirme)
    islem.ticari_durum = (
        TICARI_DURUM_EDITORIAL
        if islem.ticari_degerlendirme["durum"] == TICARI_DURUM_EDITORIAL
        else TICARI_DURUM_MANUEL
    )
    return _uyari_ekle(uyari, _ticari_uyarisi(islem.ticari_degerlendirme))


def indir(ayar: argparse.Namespace) -> dict[str, Any]:
    islem = _indir_islemi(ayar)
    manifest, manifest_uyarisi = _manifest_oku(islem.klasor)
    onbellek = _onbellek_bul(manifest, islem)
    if onbellek is not None:
        islem.mevcut_kayit = onbellek
        return _cikti_uret(islem, "onbellek", manifest_uyarisi)
    anahtar = _anahtar_al(ayar.env_dosyasi)
    foto = _foto_detayi(anahtar, islem.foto_id)
    manifest_uyarisi = _indir_ticari_kontrol(islem, foto, manifest_uyarisi)
    islem.genislikler = _foto_genisliklerine_sigdir(islem, _tam_sayi(foto.get("width")))
    islem.ad = _ad_belirle(islem, foto)
    islem.mevcut_kayit = _kayit_bul(manifest, islem)
    if islem.mevcut_kayit is None:
        islem.ad = _benzersiz_ad(manifest, islem)
    plan = _indirme_planla(islem, foto)
    if not plan:
        return _cikti_uret(islem, "onbellek", manifest_uyarisi)
    for hedef in plan:
        if not _gorsel_url_guvenli(str(hedef["url"])):
            raise AracHatasi(CIKIS_DOGRULAMA, "Görsel adresi güvenli değil; indirme reddedildi.")
    _tetikle(anahtar, foto)
    indirilen = _dosyalari_indir(islem, plan)
    islem.mevcut_kayit = _kayit_olustur(islem, foto, indirilen)
    _manifest_guncelle(manifest, islem.mevcut_kayit, islem.uygulama)
    _manifest_yaz(islem.klasor, manifest)
    return _cikti_uret(islem, "indirildi", manifest_uyarisi)


def _ortak_argumanlar(ayristirici: argparse.ArgumentParser) -> None:
    ayristirici.add_argument("--env-dosyasi", default=".env", help="API anahtarını okuyacak .env dosyası (varsayılan: .env)")
    ayristirici.add_argument("--uygulama-adi", default=None, help="Atıf bağlantılarında kullanılacak UTM uygulama adı")


def _onay_hedefi(manifest: dict[str, Any], foto_id: str, ad_ham: str) -> dict[str, Any]:
    aday_ad = slug_uret(ad_ham) if (ad_ham or "").strip() else ""
    eslesen = [k for k in manifest.get("fotograflar", []) if isinstance(k, dict) and str(k.get("id")) == foto_id]
    if aday_ad:
        eslesen = [k for k in eslesen if k.get("ad") == aday_ad]
    if not eslesen:
        raise AracHatasi(CIKIS_BULUNAMADI, f"'{foto_id}' için onaylanacak kayıt bulunamadı.")
    if len(eslesen) > 1:
        raise AracHatasi(CIKIS_KULLANIM, "Aynı kimlik için birden fazla kayıt var; --ad ile seçin.")
    return eslesen[0]


def onayla(ayar: argparse.Namespace) -> dict[str, Any]:
    klasor = _klasor_coz(ayar.klasor)
    manifest, _ = _manifest_oku(klasor)
    kayit = _onay_hedefi(manifest, _fotograf_id_dogrula(ayar.fotograf_id), str(ayar.ad or ""))
    if kayit.get("ticari_durum") == TICARI_DURUM_EDITORIAL:
        raise AracHatasi(CIKIS_TICARI, "Editoryal kayıt ticari kullanım için onaylanamaz.")
    degerlendirme = kayit.get("ticari_degerlendirme") if isinstance(kayit.get("ticari_degerlendirme"), dict) else {}
    if degerlendirme.get("durum") == TICARI_DURUM_ENGELLI:
        raise AracHatasi(CIKIS_TICARI, "Engelli kayıt ticari kullanım için onaylanamaz.")
    onaylayan = _kisalt(str(ayar.onaylayan or "").strip(), 120) or "ajan"
    yeni_durum = TICARI_DURUM_ONAYLANDI if ayar.karar == "uygun" else TICARI_DURUM_REDDEDILDI
    kayit["ticari_durum"] = yeni_durum
    kayit["ticari_onay"] = {
        "karar": ayar.karar,
        "onaylayan": onaylayan,
        "tarih": _simdi(),
        "not": _kisalt(str(ayar.not_metni or "").strip(), 500),
    }
    _manifest_guncelle(manifest, kayit, str(manifest.get("uygulama") or VARSAYILAN_UYGULAMA))
    _manifest_yaz(klasor, manifest)
    return {
        "durum": yeni_durum,
        "id": kayit.get("id"),
        "ad": kayit.get("ad"),
        "ticari_durum": yeni_durum,
        "ticari_onay": kayit["ticari_onay"],
        "credits": _goreli(klasor / MANIFEST_ADI),
    }


def _ust_ayristirici() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        prog="unsplash_gorsel.py",
        description="Unsplash'ten görsel arar, uygun fotoğrafı SEO adlı WebP/JPG varlık olarak indirir ve atıf kaydı üretir.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Örnekler:\n"
            "  python unsplash_gorsel.py ara --sorgu \"modern office\" --adet 8 --yon landscape\n"
            "  python unsplash_gorsel.py indir --id FOTO_ID --ad hakkimizda-kapak --genislikler 640,960,1440\n"
            "  python unsplash_gorsel.py baglantidan-indir --url https://images.unsplash.com/... --ad kapak\n"
            "  python unsplash_gorsel.py onayla --id FOTO_ID --ad kapak --karar uygun --onaylayan \"ad\"\n"
            "Çıkış kodları: 0 başarı, 2 kullanım, 3 anahtar, 4 bulunamadı, 5 API, 6 doğrulama, 7 uyum, 8 ticari risk."
        ),
    )


def _arama_altkomutu(alt: Any) -> None:
    arama = alt.add_parser("ara", help="Fotoğraf arar; dosya indirmez.")
    arama.add_argument("--sorgu", required=True, help="İngilizce arama terimi (örn. 'minimalist office')")
    arama.add_argument("--adet", type=int, default=10, help="İstenen sonuç sayısı (1-30, varsayılan: 10)")
    arama.add_argument("--sayfa", type=int, default=1, help="Sayfa numarası (varsayılan: 1)")
    arama.add_argument("--yon", choices=("landscape", "portrait", "squarish"), default="landscape", help="Görsel yönü")
    arama.add_argument("--min-genislik", type=int, default=1600, help="En küçük genişlik (varsayılan: 1600)")
    arama.add_argument(
        "--renk",
        choices=("black_and_white", "black", "white", "yellow", "orange", "red", "purple", "magenta", "green", "teal", "blue"),
        default=None,
        help="Renk filtresi (isteğe bağlı)",
    )
    _ortak_argumanlar(arama)


def _indirme_altkomutu(alt: Any) -> None:
    indirme = alt.add_parser("indir", help="Seçilen fotoğrafı indirir ve credits.json günceller.")
    indirme.add_argument("--id", dest="fotograf_id", required=True, help="Unsplash fotoğraf kimliği")
    indirme.add_argument("--ad", default="", help="SEO uyumlu dosya adı kökü (örn. 'hakkimizda-kapak')")
    indirme.add_argument("--klasor", default=VARSAYILAN_KLASOR, help=f"Çıktı klasörü (varsayılan: {VARSAYILAN_KLASOR})")
    indirme.add_argument("--genislikler", default=VARSAYILAN_GENISLIKLER, help=f"Virgüllü genişlikler (varsayılan: {VARSAYILAN_GENISLIKLER})")
    indirme.add_argument("--format", choices=("webp", "jpg"), default="webp", help="Çıktı biçimi (varsayılan: webp)")
    indirme.add_argument("--kalite", type=int, default=VARSAYILAN_KALITE, help=f"Sıkıştırma kalitesi (varsayılan: {VARSAYILAN_KALITE})")
    indirme.add_argument("--sorgu", default="", help="Kayıt için isteğe bağlı arama terimi")
    indirme.add_argument("--uzerine-yaz", action="store_true", help="Önbelleği yok sayıp yeniden indir")
    indirme.add_argument(
        "--kullanim-turu",
        choices=(TICARI_KULLANIM, EDITORIAL_KULLANIM),
        default=TICARI_KULLANIM,
        help="Ticari (varsayılan) veya editoryal kullanım",
    )
    _ortak_argumanlar(indirme)


def _baglanti_altkomutu(alt: Any) -> None:
    baglanti = alt.add_parser(
        "baglantidan-indir",
        help="Tarayıcıdan alınan Unsplash görsel URL'sini API anahtarı olmadan yüksek çözünürlükte indirir.",
    )
    baglanti.add_argument("--url", required=True, help="images.unsplash.com görsel URL'si")
    baglanti.add_argument("--ad", default="", help="SEO uyumlu dosya adı kökü")
    baglanti.add_argument("--klasor", default=VARSAYILAN_KLASOR, help=f"Çıktı klasörü (varsayılan: {VARSAYILAN_KLASOR})")
    baglanti.add_argument("--genislik", type=int, default=VARSAYILAN_TARAYICI_GENISLIGI, help=f"Hedef genişlik (varsayılan: {VARSAYILAN_TARAYICI_GENISLIGI})")
    baglanti.add_argument("--format", choices=("webp", "jpg"), default="webp", help="Çıktı biçimi (varsayılan: webp)")
    baglanti.add_argument("--kalite", type=int, default=VARSAYILAN_TARAYICI_KALITE, help=f"Sıkıştırma kalitesi (varsayılan: {VARSAYILAN_TARAYICI_KALITE})")
    baglanti.add_argument("--fotografci", default="", help="Fotoğrafçı adı (atıf için)")
    baglanti.add_argument("--profil-url", default="", help="Fotoğrafçının unsplash.com profil bağlantısı")
    baglanti.add_argument("--fotograf-sayfasi", default="", help="Fotoğrafın unsplash.com sayfa bağlantısı")
    baglanti.add_argument("--fotograf-id", default="", help="Unsplash fotoğraf kimliği (isteğe bağlı)")
    baglanti.add_argument("--sorgu", default="", help="Kayıt için isteğe bağlı arama terimi")
    baglanti.add_argument("--aciklama", default="", help="Alt açıklama (ticari risk taraması için)")
    baglanti.add_argument(
        "--kullanim-turu",
        choices=(TICARI_KULLANIM, EDITORIAL_KULLANIM),
        default=TICARI_KULLANIM,
        help="Ticari (varsayılan) veya editoryal kullanım",
    )
    baglanti.add_argument("--uzerine-yaz", action="store_true", help="Önbelleği yok sayıp yeniden indir")
    _ortak_argumanlar(baglanti)


def _onay_altkomutu(alt: Any) -> None:
    onay = alt.add_parser("onayla", help="Ticari kullanım için görseli onaylar/reddeder; credits.json denetim kaydı yazar.")
    onay.add_argument("--id", dest="fotograf_id", required=True, help="Unsplash fotoğraf kimliği")
    onay.add_argument("--ad", default="", help="Kayıt adı (birden fazla kayıt varsa zorunlu)")
    onay.add_argument("--karar", choices=TICARI_ONAY_KARARLARI, required=True, help="uygun veya uygun-degil")
    onay.add_argument("--onaylayan", default="ajan", help="Onayı veren kişi/ajan adı")
    onay.add_argument("--not", dest="not_metni", default="", help="Görsel denetim notu")
    onay.add_argument("--klasor", default=VARSAYILAN_KLASOR, help=f"Çıktı klasörü (varsayılan: {VARSAYILAN_KLASOR})")


def _argumanlari_ayristir(argv: list[str] | None) -> argparse.Namespace:
    ayristirici = _ust_ayristirici()
    alt = ayristirici.add_subparsers(dest="komut", required=True)
    _arama_altkomutu(alt)
    _indirme_altkomutu(alt)
    _baglanti_altkomutu(alt)
    _onay_altkomutu(alt)
    return ayristirici.parse_args(argv)


def _cikti_kodlamasi() -> None:
    for akis in (sys.stdout, sys.stderr):
        try:
            akis.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _json_yaz(veri: dict[str, Any], akis: Any = None) -> None:
    print(json.dumps(veri, ensure_ascii=False, indent=2), file=akis or sys.stdout)


def _komut_calistir(ayarlar: argparse.Namespace) -> dict[str, Any]:
    if ayarlar.komut == "ara":
        return ara(ayarlar)
    if ayarlar.komut == "baglantidan-indir":
        return baglantidan_indir(ayarlar)
    if ayarlar.komut == "onayla":
        return onayla(ayarlar)
    return indir(ayarlar)


def main(argv: list[str] | None = None) -> int:
    _cikti_kodlamasi()
    try:
        ayarlar = _argumanlari_ayristir(argv)
        cikti = _komut_calistir(ayarlar)
    except AracHatasi as hata:
        _json_yaz({"hata": hata.mesaj, "kod": hata.kod}, sys.stderr)
        return hata.kod
    except KeyboardInterrupt:
        _json_yaz({"hata": "İşlem kullanıcı tarafından durduruldu.", "kod": 130}, sys.stderr)
        return 130
    except Exception as hata:  # pragma: no cover - beklenmeyen hata kullanıcıya özetlenir
        _json_yaz(
            {"hata": f"Beklenmeyen hata: {type(hata).__name__}. Ayrıntı için UNSPLASH_AYRINTILI=1 ile çalıştırın.", "kod": CIKIS_API},
            sys.stderr,
        )
        return CIKIS_API
    _json_yaz(cikti)
    return CIKIS_TAMAM


if __name__ == "__main__":
    sys.exit(main())
