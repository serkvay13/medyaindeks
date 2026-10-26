"""Uzman analist adımları.

a) hipotez_uret: vaka tanımı + bağlam çıktısından rakip hipotez ÖNERİLERİ (resmi tez, alternatif,
   yapısal/jeopolitik, dış konjonktür, masum) ve her biri için aranacak kanıt/sorgu. Çıktı her zaman
   "öneri — kanıt aranacak" etiketlidir; ön kayda alınması analistin kararıdır.
b) bolum_yaz: model yalnızca o bölüm için seçilmiş kanıt kartlarını + ACH + bağlam çıktısını görür,
   cümle modeli biçiminde JSON yazar. Her cümle doğrulayıcıdan geçer; doğrulama da YALNIZCA o bölümün
   kartlarına karşı yapılır (model görmediği karta dayanamaz).
"""
import json
import re
from pathlib import Path

from medya.dogrulayici import Cumle, DogrulamaSonucu, Red, cumleler_from_json, dogrula
from medya.hipotez.ach import HIPOTEZ_TURLERI
from medya.kanit.kart import TURLER, KanitKarti
from medya.uzman.saglayici import Saglayici

ISTEM_DIZINI = Path(__file__).resolve().parent / "istemler"
ONERI_ETIKETI = "öneri — kanıt aranacak"
PAKET_ISARETI = "GİRDİ PAKETİ (JSON):"
ZORUNLU_ONERI_TURLERI = ("resmi_tez", "alternatif", "yapisal", "dis_konjonktur", "masum")


def istem(ad: str) -> str:
    ortak = (ISTEM_DIZINI / "ortak_kurallar.md").read_text(encoding="utf-8")
    return (ISTEM_DIZINI / f"{ad}.md").read_text(encoding="utf-8").replace("{{ORTAK_KURALLAR}}", ortak)


def _json_blok(ham: str):
    metin = ham or ""
    blok = re.search(r"```(?:json)?\s*(.*?)```", metin, re.S)
    if blok:
        metin = blok.group(1)
    kose = re.search(r"\{.*\}", metin, re.S)
    if kose:
        metin = kose.group(0)
    try:
        return json.loads(metin)
    except json.JSONDecodeError:
        return None


def _cagir(saglayici: Saglayici, gorev: str, paket: dict, max_tokens: int = 3000):
    kullanici = f"{PAKET_ISARETI}\n{json.dumps(paket, ensure_ascii=False, default=str)}"
    ham = saglayici.tamamla(istem(gorev), kullanici, gorev, max_tokens=max_tokens)
    return _json_blok(ham), ham


def kart_paketi(k: KanitKarti) -> dict:
    """Modele giden kart görünümü. Resmi açıklama başlıkta "<kurum> iddiası" olarak işaretlidir."""
    return {"kanit_id": k.kanit_id, "tur": k.tur, "tur_adi": TURLER[k.tur], "baslik": k.baslik(), "kurum": k.kurum,
            "ozet": k.ozet, "alinti": k.alinti, "yayin_tarihi": k.yayin_tarihi, "olay_tarihi": k.olay_tarihi,
            "derece": k.derece, "yayin_grubu": k.grup_metni()}


# --------------------------------------------------------------------------------
# a) hipotez_uret
# --------------------------------------------------------------------------------
def hipotez_uret(saglayici: Saglayici, vaka: dict, baglam: dict | None = None) -> dict:
    paket = {"vaka": {k: vaka.get(k) for k in ("id", "ad", "soru", "olay_tarihi", "yer", "etiketler",
                                               "resmi_tez")},
             "baglam_ozeti": _baglam_ozeti(baglam)}
    veri, ham = _cagir(saglayici, "hipotez_uret", paket)
    if not isinstance(veri, dict):
        return {"etiket": ONERI_ETIKETI, "hipotezler": [], "hata": "model JSON döndürmedi", "ham": ham[:2000]}
    hipotezler = []
    for i, h in enumerate(veri.get("hipotezler", []), 1):
        if not isinstance(h, dict) or not str(h.get("metin", "")).strip():
            continue
        tur = h.get("tur") if h.get("tur") in HIPOTEZ_TURLERI else "diger"
        hipotezler.append({"id": str(h.get("id") or f"Ö{i}"), "tur": tur, "metin": str(h["metin"]).strip(),
                           "destekleyen_kanit": list(h.get("destekleyen_kanit", [])),
                           "curuten_kanit": list(h.get("curuten_kanit", [])),
                           "kaynak_turleri": [t for t in h.get("kaynak_turleri", []) if t in TURLER],
                           "arama_sorgulari": list(h.get("arama_sorgulari", []))})
    eksik = [t for t in ZORUNLU_ONERI_TURLERI if t not in {h["tur"] for h in hipotezler}]
    return {"etiket": ONERI_ETIKETI, "hipotezler": hipotezler, "eksik_turler": eksik,
            "not": "Bu liste bir öneridir; olgu değildir. Ön kayda almadan önce analist gözden geçirir.",
            "saglayici": f"{saglayici.ad}/{saglayici.model}"}


def _baglam_ozeti(baglam: dict | None) -> dict:
    if not baglam:
        return {}
    out = {}
    for a in baglam.get("adimlar", []):
        out[f"{a['adim']}. {a['ad']}"] = {"durum": a["durum"], "cikti": a["cikti"], "notlar": a["notlar"]}
    return out


# --------------------------------------------------------------------------------
# b) bolum_yaz
# --------------------------------------------------------------------------------
def bolum_yaz(saglayici: Saglayici, bolum: dict, kartlar: list[KanitKarti], ach_ozeti: dict | None = None,
              baglam_ozeti: dict | None = None, ek_adlar: str = "") -> DogrulamaSonucu:
    """bolum: {"no", "baslik", "soru"}. Dönen sonuçta kabul ve red listesi vardır."""
    paket = {"bolum": bolum, "kartlar": [kart_paketi(k) for k in kartlar], "ach": ach_ozeti or {},
             "baglam": baglam_ozeti or {}}
    veri, ham = _cagir(saglayici, "bolum_yaz", paket)
    if not isinstance(veri, dict):
        return DogrulamaSonucu(kabul=[], red=[Red(Cumle("olgu", (ham or "")[:300] or "(boş yanıt)"),
                                                  ["model JSON döndürmedi"])])
    try:
        cumleler = cumleler_from_json(veri)
    except (TypeError, ValueError) as e:
        return DogrulamaSonucu(kabul=[], red=[Red(Cumle("olgu", str(veri)[:300]), [f"cümle modeli bozuk: {e}"])])
    sozluk = {k.kanit_id: k for k in kartlar}
    for i, c in enumerate(cumleler, 1):
        c.id = f"b{bolum['no']}-{i}"
    return dogrula(cumleler, sozluk, ek_adlar=ek_adlar)


# --------------------------------------------------------------------------------
# Derinleştirme: araştırma planı
# --------------------------------------------------------------------------------
def arastirma_plani(saglayici: Saglayici, vaka: dict, soru: dict, hipotezler: list[dict],
                    kanit_sayilari: dict) -> dict:
    paket = {"vaka": {k: vaka.get(k) for k in ("id", "ad", "soru", "olay_tarihi", "etiketler")},
             "ek_soru": soru, "kayitli_hipotezler": hipotezler, "kanit_sayilari_turlere_gore": kanit_sayilari}
    veri, ham = _cagir(saglayici, "arastirma_plani", paket)
    if not isinstance(veri, dict):
        return {"etiket": ONERI_ETIKETI, "hata": "model JSON döndürmedi", "ham": (ham or "")[:2000]}
    etk = [int(b) for b in veri.get("etkilenen_bolumler", []) if str(b).isdigit() and 1 <= int(b) <= 14]
    return {"etiket": ONERI_ETIKETI, "alt_hipotezler": veri.get("alt_hipotezler", []),
            "kanit_ihtiyaclari": [x for x in veri.get("kanit_ihtiyaclari", []) if isinstance(x, dict)],
            "kaynaklar_sorgular": [x for x in veri.get("kaynaklar_sorgular", []) if isinstance(x, dict)],
            "etkilenen_bolumler": sorted(set(etk)), "saglayici": f"{saglayici.ad}/{saglayici.model}"}


# --------------------------------------------------------------------------------
# Kırmızı takım önerisi (ayrı oturum)
# --------------------------------------------------------------------------------
def kirmizi_takim_oner(saglayici: Saglayici, lider: dict, kartlar: list[KanitKarti], matris: list[dict]) -> dict:
    paket = {"one_cikan_hipotez": lider, "kartlar": [kart_paketi(k) for k in kartlar], "matris": matris}
    veri, _ = _cagir(saglayici, "kirmizi_takim", paket)
    gecerli = {k.kanit_id for k in kartlar}
    argumanlar = []
    for a in (veri or {}).get("karsi_argumanlar", []):
        if isinstance(a, dict) and str(a.get("arguman", "")).strip():
            argumanlar.append({"arguman": str(a["arguman"]).strip(), "yanit": "",
                               "kanit_ids": [k for k in a.get("kanit_ids", []) if k in gecerli]})
    return {"etiket": ONERI_ETIKETI, "hipotez_id": lider.get("hipotez_id"), "karsi_argumanlar": argumanlar,
            "yapan": f"llm-ayri-oturum: {saglayici.ad}/{saglayici.model}"}
