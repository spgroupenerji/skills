"""sp-gorsel-tedarik komut satırı: ara, toplu-ara, indir, onayla, denetle, kaynaklar."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from . import guvenlik, indirici, manifest, yonlendirme
from .hata import AracHatasi
from .kaynaklar import KAYNAKLAR
from .model import Aday, AramaIstegi
from .ortak import anahtar_ortamdan, env_dosyasini_yukle, ikili_istek, metin_temizle, slug_uret, taban_ortamdan
from .sabitler import (
    AZAMI_ADET,
    ASGARI_GENISLIK,
    AZAMI_GENISLIK,
    CIKIS_ANAHTAR,
    CIKIS_API,
    CIKIS_BULUNAMADI,
    CIKIS_DOGRULAMA,
    CIKIS_KAYNAK,
    CIKIS_KULLANIM,
    CIKIS_TAMAM,
    CIKIS_TICARI,
    CIKIS_UYUM,
    KATEGORILER,
    MANIFEST_ADI,
    TICARI_ENGELLI,
    VARSAYILAN_ADET,
    VARSAYILAN_GENISLIKLER,
    VARSAYILAN_KALITE,
    VARSAYILAN_KLASOR,
    YEREL_ONAY,
    YONLER,
)


def _gorunen_ad(ad: str) -> str:
    return {"pexels": "Pexels", "pixabay": "Pixabay", "unsplash": "Unsplash", "openverse": "Openverse",
            "wikimedia": "Wikimedia Commons", "smithsonian": "Smithsonian", "met": "The Met",
            "nasa": "NASA", "polyhaven": "Poly Haven", "flickr": "Flickr"}.get(ad, ad.title())


def _json_yaz(veri: Any, akis: Any = None) -> None:
    akis = akis or sys.stdout
    akis.write(json.dumps(veri, ensure_ascii=False, separators=(",", ":")) + "\n")
    akis.flush()


def _kaynaklari_coz(kaynak_arg: str, kategori: str) -> tuple[tuple[str, ...], bool]:
    """--kaynak değerini kaynak listesine çevirir; ikinci değer açık seçim mi?"""
    ham = (kaynak_arg or "auto").strip().lower()
    if ham in ("auto", "otomatik", ""):
        kullanilabilir = {
            ad for ad, tanim in KAYNAKLAR.items()
            if not tanim.anahtar_ortami or anahtar_ortamdan(tanim.anahtar_ortami)
        }
        secilen = yonlendirme.otomatik_sec(kategori, kullanilabilir)
        if not secilen:
            raise AracHatasi(CIKIS_KAYNAK, "Kullanılabilir kaynak yok; API anahtarlarını veya ağı kontrol et.")
        return secilen, False
    adlar = tuple(parca.strip() for parca in ham.split(",") if parca.strip())
    bilinmeyen = [ad for ad in adlar if ad not in KAYNAKLAR]
    if bilinmeyen:
        raise AracHatasi(CIKIS_KULLANIM, f"Bilinmeyen kaynak: {', '.join(bilinmeyen)}.", ", ".join(KAYNAKLAR))
    return adlar, True


def _gorsel_anahtari(aday: Aday) -> str:
    if not aday.varyantlar:
        return f"{aday.kaynak}:{aday.kimlik}"
    from urllib.parse import urlsplit
    parca = urlsplit(max(aday.varyantlar, key=lambda varyant: varyant.genislik).url)
    return f"{parca.netloc.lower()}{parca.path}"


BICIM_ONCELIK = {"jpg": 0, "webp": 1, "png": 2}


def _aday_dict(aday: Aday, tanim: Any, ticari: dict[str, Any]) -> dict[str, Any]:
    if not aday.varyantlar:
        buyuk = kucuk = ""
    else:
        buyuk = max(aday.varyantlar, key=lambda varyant: (varyant.genislik, -BICIM_ONCELIK.get(varyant.bicim, 3))).url
        kucuk = min(aday.varyantlar, key=lambda varyant: (varyant.genislik, BICIM_ONCELIK.get(varyant.bicim, 3))).url
    return {
        "kaynak": aday.kaynak,
        "kimlik": str(aday.kimlik),
        "baslik": metin_temizle(aday.baslik, 90) or metin_temizle(aday.aciklama, 90) or "adsiz",
        "genislik": aday.genislik,
        "yukseklik": aday.yukseklik,
        "lisans": {"ad": aday.lisans_adi, "sinif": aday.lisans_sinifi, "atif": tanim.atif_zorunlu},
        "ticari": ticari,
        "gorsel": {"indir": buyuk, "kucuk": kucuk},
        "sayfa": aday.sayfa_url,
        "atif_html": indirici.atif_html_uret(aday, _gorunen_ad(tanim.ad), tanim.atif_zorunlu),
        "yerel_indirme": tanim.yerel_indirme,
    }


def _arama_calistir(
    kaynak_adlari: tuple[str, ...], istek: AramaIstegi, zorunlu: bool
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sonuclar: list[dict[str, Any]] = []
    uyarilar: list[dict[str, Any]] = []
    gorulen: set[str] = set()
    for ad in kaynak_adlari:
        tanim = KAYNAKLAR[ad]
        anahtar = anahtar_ortamdan(tanim.anahtar_ortami)
        if tanim.anahtar_ortami and not anahtar:
            if zorunlu:
                raise AracHatasi(CIKIS_ANAHTAR, f"{ad}: API anahtarı yok ({tanim.anahtar_ortami}).")
            uyarilar.append({"kaynak": ad, "kod": CIKIS_ANAHTAR, "mesaj": f"anahtar yok ({tanim.anahtar_ortami})"})
            continue
        taban = taban_ortamdan(tanim.taban_ortami, tanim.varsayilan_taban)
        try:
            adaylar = tanim.ara(istek, anahtar, taban)
        except AracHatasi as hata:
            if zorunlu:
                raise
            uyarilar.append({"kaynak": ad, "kod": hata.kod, "mesaj": hata.mesaj})
            continue
        for aday in adaylar[: istek.adet * 3]:
            if istek.min_genislik and aday.genislik < istek.min_genislik:
                continue
            ticari = guvenlik.ticari_degerlendir(aday)
            if ticari.get("durum") == TICARI_ENGELLI:
                continue
            anahtar_url = _gorsel_anahtari(aday)
            if anahtar_url in gorulen:
                continue
            gorulen.add(anahtar_url)
            sonuclar.append(_aday_dict(aday, tanim, ticari))
    return sonuclar, uyarilar


def _temiz_konu(konu: str) -> str:
    temiz = re.sub(r"\s+", " ", (konu or "")).strip()
    if len(temiz) < 2:
        raise AracHatasi(CIKIS_KULLANIM, "--konu en az 2 karakter olmalı.")
    return temiz[:120]


def _adet_coz(adet: int) -> int:
    if not 1 <= adet <= AZAMI_ADET:
        raise AracHatasi(CIKIS_KULLANIM, f"--adet 1-{AZAMI_ADET} aralığında olmalı.")
    return adet


def _genislikleri_coz(metin: str) -> tuple[int, ...]:
    parcalar = [parca.strip() for parca in (metin or "").split(",") if parca.strip()]
    if not parcalar:
        raise AracHatasi(CIKIS_KULLANIM, "--genislikler en az bir genişlik içermeli (örn. 640,960,1440).")
    gecerli: set[int] = set()
    for parca in parcalar:
        try:
            genislik = int(parca)
        except ValueError as hata:
            raise AracHatasi(CIKIS_KULLANIM, f"Geçersiz genişlik: {parca}") from hata
        if not ASGARI_GENISLIK <= genislik <= AZAMI_GENISLIK:
            raise AracHatasi(CIKIS_KULLANIM, f"Genişlik {genislik} desteklenmiyor ({ASGARI_GENISLIK}-{AZAMI_GENISLIK}).")
        gecerli.add(genislik)
    return tuple(sorted(gecerli))


def _kaynak_ve_anahtar(ad: str) -> tuple[Any, str | None, str]:
    tanim = KAYNAKLAR.get(ad)
    if tanim is None:
        raise AracHatasi(CIKIS_KULLANIM, f"Bilinmeyen kaynak: {ad}.", ", ".join(KAYNAKLAR))
    anahtar = anahtar_ortamdan(tanim.anahtar_ortami)
    if tanim.anahtar_ortami and not anahtar:
        raise AracHatasi(CIKIS_ANAHTAR, f"{ad}: API anahtarı yok ({tanim.anahtar_ortami}).")
    return tanim, anahtar, taban_ortamdan(tanim.taban_ortami, tanim.varsayilan_taban)


def komut_kaynaklar(_ayar: argparse.Namespace) -> dict[str, Any]:
    kaynaklar = []
    for ad, tanim in KAYNAKLAR.items():
        anahtar_durumu = "gerekmez"
        if tanim.anahtar_ortami:
            anahtar_durumu = "var" if anahtar_ortamdan(tanim.anahtar_ortami) else "yok"
        kategoriler = [kategori for kategori, siralar in yonlendirme.KATEGORI_KAYNAKLARI.items() if ad in siralar]
        kaynaklar.append({
            "ad": ad,
            "lisans": tanim.lisans_adi,
            "anahtar": anahtar_durumu,
            "ortam": tanim.anahtar_ortami,
            "yerel_indirme": tanim.yerel_indirme,
            "atif_zorunlu": tanim.atif_zorunlu,
            "kategoriler": kategoriler,
        })
    return {
        "komut": "kaynaklar",
        "cevirici": {"pillow": indirici.cevirici_var()},
        "kaynaklar": kaynaklar,
        "ipucu": "Kategori seçimi için SKILL.md yönlendirme tablosunu kullan; anahtarsız kaynaklar hazır.",
    }


def komut_ara(ayar: argparse.Namespace) -> dict[str, Any]:
    istek = AramaIstegi(
        konu=_temiz_konu(ayar.konu),
        adet=_adet_coz(ayar.adet),
        yon=ayar.yon,
        min_genislik=max(0, int(ayar.min_genislik)),
        sayfa=max(1, int(ayar.sayfa)),
        kategori=ayar.kategori,
    )
    kaynak_adlari, acik = _kaynaklari_coz(ayar.kaynak, ayar.kategori)
    sonuclar, uyarilar = _arama_calistir(kaynak_adlari, istek, acik and len(kaynak_adlari) == 1)
    if not sonuclar:
        if uyarilar:
            raise AracHatasi(uyarilar[0].get("kod", CIKIS_API), "Hiçbir kaynak sonuç veremedi; uyarıları incele.", str(uyarilar))
        raise AracHatasi(CIKIS_BULUNAMADI, "Sonuç bulunamadı; terimi ve filtreleri değiştir.")
    return {
        "komut": "ara",
        "konu": istek.konu,
        "kategori": istek.kategori,
        "kaynaklar": list(kaynak_adlari),
        "sonuclar": sonuclar,
        "uyarilar": uyarilar,
        "ipucu": "Seçilen aday için: indir --kaynak <ad> --id <kimlik> --ad <seo-ad>",
    }


def komut_toplu_ara(ayar: argparse.Namespace) -> dict[str, Any]:
    dosya = Path(ayar.plan)
    if not dosya.is_file():
        raise AracHatasi(CIKIS_KULLANIM, f"Plan dosyası bulunamadı: {dosya}")
    try:
        ham = json.loads(dosya.read_text(encoding="utf-8"))
    except ValueError as hata:
        raise AracHatasi(CIKIS_KULLANIM, "Plan dosyası geçerli JSON değil.", str(hata)) from hata
    if not isinstance(ham, list) or not ham:
        raise AracHatasi(CIKIS_KULLANIM, "Plan bir varlık listesi olmalı (ad, konu, kategori).")
    varliklar = []
    for sira, ham_varlik in enumerate(ham[:12]):
        if not isinstance(ham_varlik, dict):
            raise AracHatasi(CIKIS_KULLANIM, f"Plan {sira + 1}. öğe nesne değil.")
        ad = str(ham_varlik.get("ad") or f"varlik-{sira + 1}")
        kategori = str(ham_varlik.get("kategori") or ayar.kategori)
        if kategori not in KATEGORILER:
            raise AracHatasi(CIKIS_KULLANIM, f"Geçersiz kategori: {kategori}")
        istek = AramaIstegi(
            konu=_temiz_konu(str(ham_varlik.get("konu") or ad)),
            adet=_adet_coz(int(ham_varlik.get("adet") or ayar.adet)),
            yon=ham_varlik.get("yon") if ham_varlik.get("yon") in YONLER else None,
            min_genislik=max(0, int(ayar.min_genislik)),
            kategori=kategori,
        )
        kaynak_adlari, _acik = _kaynaklari_coz(str(ham_varlik.get("kaynak") or ayar.kaynak), kategori)
        sonuclar, uyarilar = _arama_calistir(kaynak_adlari, istek, False)
        varliklar.append({"ad": ad, "konu": istek.konu, "kategori": kategori,
                          "kaynaklar": list(kaynak_adlari), "sonuclar": sonuclar, "uyarilar": uyarilar})
    return {"komut": "toplu-ara", "varliklar": varliklar, "ipucu": "Her varlık için bir aday seç; indir komutunu ayrı çalıştır."}


def _tetikle_ve_indir(aday: Aday, tanim: Any, ayar: argparse.Namespace) -> dict[str, Any]:
    ticari = guvenlik.ticari_degerlendir(aday)
    guvenlik.kapi(ticari)
    if tanim.yerel_indirme == YEREL_ONAY and not ayar.yerel_kabul:
        raise AracHatasi(
            CIKIS_TICARI,
            f"{tanim.ad} API kuralı hotlink ister; yerel indirme için --yerel-kabul bayrağını bilinçli kullan.",
        )
    tetik = aday.ek.get("tetik_url")
    if isinstance(tetik, str) and tetik.strip():
        try:
            ikili_istek(tetik.strip(), None, azami_bayt=64 * 1024)
        except AracHatasi as hata:
            raise AracHatasi(CIKIS_UYUM, "İndirme tetikleyicisi başarısız; görsel indirilmedi.", hata.mesaj) from hata
    klasor = Path(ayar.klasor)
    genislikler = _genislikleri_coz(ayar.genislikler)
    plan, uyarilar = indirici.plan_olustur(aday, genislikler, ayar.format)
    manifest_veri, manifest_uyari = manifest.manifest_oku(klasor)
    if manifest_uyari:
        uyarilar.append(manifest_uyari)
    onceki = manifest.kayit_bul(manifest_veri, aday.kaynak, str(aday.kimlik))
    ad = manifest.ad_benzersiz(manifest_veri, slug_uret(ayar.ad), aday.kaynak, str(aday.kimlik))
    dosyalar, indirme_uyarilari = indirici.indir(
        plan, klasor, ad, int(ayar.kalite), bool(ayar.uzerine_yaz), tanim.gorsel_hostlari
    )
    uyarilar.extend(indirme_uyarilari)
    atif = indirici.atif_html_uret(aday, _gorunen_ad(tanim.ad), tanim.atif_zorunlu)
    kayit = manifest.kayit_uret(aday, ad, dosyalar, atif, ticari, aday.ek.get("lisans_url") or "")
    if isinstance(onceki, dict):
        kayit["ticari_durum"] = onceki.get("ticari_durum") or kayit["ticari_durum"]
        kayit["ticari_onay"] = onceki.get("ticari_onay") or {}
        kayit["kayit_zamani"] = onceki.get("kayit_zamani") or kayit["kayit_zamani"]
    manifest.kayit_ekle(manifest_veri, kayit)
    manifest.manifest_yaz(klasor, manifest_veri)
    return {
        "durum": "indirildi",
        "kaynak": aday.kaynak,
        "kimlik": str(aday.kimlik),
        "ad": ad,
        "tarih": kayit["kayit_zamani"],
        "dosyalar": dosyalar,
        "srcset": indirici.srcset_uret(dosyalar),
        "img": indirici.img_etiketleri(dosyalar, metin_temizle(aday.baslik, 120) or ad, aday),
        "atif_html": atif,
        "credits": {"dosya": (klasor / MANIFEST_ADI).as_posix(), "surum": manifest.MANIFEST_SURUM},
        "ticari": {
            "degerlendirme": ticari,
            "durum": kayit["ticari_durum"],
            "onay_gerekli": True,
            "sonraki": f"onayla --kaynak {aday.kaynak} --id {aday.kimlik} --karar uygun --onaylayan <ad>",
        },
        "uyarilar": uyarilar,
    }


def komut_indir(ayar: argparse.Namespace) -> dict[str, Any]:
    tanim, anahtar, taban = _kaynak_ve_anahtar(ayar.kaynak)
    if not str(ayar.id or "").strip():
        raise AracHatasi(CIKIS_KULLANIM, "--id zorunlu.")
    if not str(ayar.ad or "").strip():
        raise AracHatasi(CIKIS_KULLANIM, "--ad zorunlu (SEO dostu Türkçe ad).")
    if not 1 <= int(ayar.kalite) <= 100:
        raise AracHatasi(CIKIS_KULLANIM, "--kalite 1-100 aralığında olmalı.")
    aday = tanim.detay(str(ayar.id).strip(), anahtar, taban)
    return _tetikle_ve_indir(aday, tanim, ayar)


def komut_onayla(ayar: argparse.Namespace) -> dict[str, Any]:
    if not ayar.id and not ayar.ad:
        raise AracHatasi(CIKIS_KULLANIM, "--id veya --ad zorunlu.")
    if ayar.id and not ayar.kaynak:
        raise AracHatasi(CIKIS_KULLANIM, "--id ile birlikte --kaynak zorunlu.")
    klasor = Path(ayar.klasor)
    manifest_veri, uyari = manifest.manifest_oku(klasor)
    karar = guvenlik.onay_kaydi(ayar.karar, ayar.onaylayan, ayar.not_metni)
    durum = guvenlik.onay_durumu(karar["karar"])
    kayit = manifest.onay_yaz(
        manifest_veri, karar, durum,
        kaynak=ayar.kaynak, kimlik=ayar.id, ad=ayar.ad_ham,
    )
    manifest.manifest_yaz(klasor, manifest_veri)
    return {
        "komut": "onayla",
        "durum": durum,
        "kaynak": kayit.get("kaynak"),
        "kimlik": kayit.get("kimlik"),
        "ad": kayit.get("ad"),
        "ticari": {"durum": durum, "onay": karar},
        "uyari": uyari,
    }


def komut_denetle(ayar: argparse.Namespace) -> dict[str, Any]:
    klasor = Path(ayar.klasor)
    manifest_veri, uyari = manifest.manifest_oku(klasor)
    kayitlar = manifest_veri.get("kayitlar", [])
    onaysiz = manifest.onaysiz_kayitlar(manifest_veri)
    eksik = manifest.eksik_dosyalar(manifest_veri)
    siniflar: dict[str, int] = {}
    for kayit in kayitlar:
        sinif = str(kayit.get("lisans_sinifi") or "bilinmiyor")
        siniflar[sinif] = siniflar.get(sinif, 0) + 1
    sonuc = {
        "komut": "denetle",
        "manifest": (klasor / MANIFEST_ADI).as_posix(),
        "toplam": len(kayitlar),
        "onaysiz": [{"kaynak": kayit.get("kaynak"), "kimlik": kayit.get("kimlik"), "ad": kayit.get("ad")} for kayit in onaysiz],
        "eksik_dosyalar": eksik,
        "lisans_siniflari": siniflar,
        "uyari": uyari,
    }
    if eksik:
        raise AracHatasi(CIKIS_DOGRULAMA, f"{len(eksik)} kayıtlı dosya diskte yok.", json.dumps(sonuc, ensure_ascii=False))
    return sonuc


def _ortak_argumanlar(ayristirici: argparse.ArgumentParser) -> None:
    ayristirici.add_argument("--env-dosyasi", default=".env", help="Ortam dosyası yolu (varsayılan .env).")


def _ust_ayristirici() -> argparse.ArgumentParser:
    ayristirici = argparse.ArgumentParser(prog="gorsel_tedarik", description="Ticari güvenli görsel tedarik aracı.")
    alt = ayristirici.add_subparsers(dest="komut", required=True)

    kaynaklar = alt.add_parser("kaynaklar", help="Kaynakları, lisansları ve anahtar durumunu listeler.")
    _ortak_argumanlar(kaynaklar)

    ara = alt.add_parser("ara", help="Tek konu için kaynaklarda arama yapar.")
    ara.add_argument("--konu", required=True)
    ara.add_argument("--kaynak", default="auto", help="auto veya virgüllü liste (pexels,pixabay...).")
    ara.add_argument("--kategori", default="genel", choices=KATEGORILER)
    ara.add_argument("--adet", type=int, default=VARSAYILAN_ADET)
    ara.add_argument("--yon", choices=YONLER, default=None)
    ara.add_argument("--min-genislik", type=int, default=0)
    ara.add_argument("--sayfa", type=int, default=1)
    _ortak_argumanlar(ara)

    toplu = alt.add_parser("toplu-ara", help="Plan dosyasındaki çoklu varlıklar için arama yapar.")
    toplu.add_argument("--plan", required=True, help="[{ad, konu, kategori, yon}] JSON dosyası.")
    toplu.add_argument("--kaynak", default="auto")
    toplu.add_argument("--kategori", default="genel", choices=KATEGORILER)
    toplu.add_argument("--adet", type=int, default=VARSAYILAN_ADET)
    toplu.add_argument("--min-genislik", type=int, default=0)
    _ortak_argumanlar(toplu)

    indir = alt.add_parser("indir", help="Seçilen adayı indirir, credits.json günceller.")
    indir.add_argument("--kaynak", required=True)
    indir.add_argument("--id", required=True)
    indir.add_argument("--ad", required=True)
    indir.add_argument("--klasor", default=VARSAYILAN_KLASOR)
    indir.add_argument("--genislikler", default=VARSAYILAN_GENISLIKLER)
    indir.add_argument("--format", default="webp", choices=("webp", "jpg", "png"))
    indir.add_argument("--kalite", type=int, default=VARSAYILAN_KALITE)
    indir.add_argument("--yerel-kabul", action="store_true", help="Hotlink isteyen kaynakta yerel indirmeyi kabul et.")
    indir.add_argument("--uzerine-yaz", action="store_true")
    _ortak_argumanlar(indir)

    onayla = alt.add_parser("onayla", help="Görsel denetim onayını credits.json'a işler.")
    onayla.add_argument("--kaynak")
    onayla.add_argument("--id")
    onayla.add_argument("--ad")
    onayla.add_argument("--karar", required=True, choices=("uygun", "uygun-degil"))
    onayla.add_argument("--onaylayan", required=True)
    onayla.add_argument("--not", dest="not_metni", default="")
    onayla.add_argument("--klasor", default=VARSAYILAN_KLASOR)
    _ortak_argumanlar(onayla)

    denetle = alt.add_parser("denetle", help="credits.json kayıtlarını ve onay durumunu denetler.")
    denetle.add_argument("--klasor", default=VARSAYILAN_KLASOR)
    _ortak_argumanlar(denetle)
    return ayristirici


def _komut_calistir(ayar: argparse.Namespace) -> dict[str, Any]:
    env_dosyasini_yukle(getattr(ayar, "env_dosyasi", ".env"))
    komutlar = {
        "kaynaklar": komut_kaynaklar,
        "ara": komut_ara,
        "toplu-ara": komut_toplu_ara,
        "indir": komut_indir,
        "onayla": komut_onayla,
        "denetle": komut_denetle,
    }
    isleyici = komutlar.get(ayar.komut)
    if isleyici is None:
        raise AracHatasi(CIKIS_KULLANIM, f"Bilinmeyen komut: {ayar.komut}")
    if hasattr(ayar, "kaynak") and getattr(ayar, "kaynak", None):
        ayar.kaynak = str(ayar.kaynak).strip().lower()
    if hasattr(ayar, "id") and getattr(ayar, "id", None) is not None:
        ayar.id = str(ayar.id).strip()
    ayar.ad_ham = getattr(ayar, "ad", None)
    return isleyici(ayar)


def _cikti_kodlamasi() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


def _hata_yaz(hata: AracHatasi) -> None:
    govde: dict[str, Any] = {"hata": hata.mesaj, "kod": hata.kod}
    if hata.ayrinti:
        govde["ayrinti"] = hata.ayrinti
    sys.stderr.write(json.dumps(govde, ensure_ascii=False) + "\n")
    sys.stderr.flush()


def main(argv: list[str] | None = None) -> int:
    _cikti_kodlamasi()
    try:
        ayar = _ust_ayristirici().parse_args(argv)
    except SystemExit as cikis:
        return int(cikis.code or CIKIS_KULLANIM)
    try:
        sonuc = _komut_calistir(ayar)
    except AracHatasi as hata:
        _hata_yaz(hata)
        return hata.kod
    except KeyboardInterrupt:
        return 130
    _json_yaz(sonuc)
    return CIKIS_TAMAM