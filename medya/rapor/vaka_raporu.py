"""Vaka raporu motoru (referans rapor yapısı): vaka paketinden Markdown + HTML + PDF.

Akış:
1. Vaka paketi okunur: kart dosyaları içe aktarılır (K/KR/R/RD), hipotez ön kaydı ACH modülüyle kurulur
   (SHA-256), GDELT istatistiği, ACH matrisi ve çelişki kayıtları yüklenir.
2. **Kapsam denetimi** (araştırma protokolü, beş hat) rapordan önce çalışır; eksikler raporlanır
   (`kati=True` ise rapor üretilmez).
3. Deterministik parçalar koddan üretilir (medya.rapor.tablolar): kapak (Taslak — insan onayı bekliyor + GDELT
   atfı), kaynak tabanı, 4 dönemlik kronoloji, çelişki tablosu, GDELT tabloları ve grafikleri, ACH matrisi,
   kart dizini.
4. Anlatı: çevrimdışı modda vaka paketindeki hazır metin (`anlati/`); aksi halde LLM yazım katmanı
   (medya.uzman.yazim) bölüm bölüm yazar, her cümle doğrulanır, geçmeyen düşürülür ve raporlanır.
5. Atıf denetimi: gövdede geçen her [kimlik] kart olarak var olmalı (ya da izinli etiket olmalı).
6. Çıktı: Markdown, HTML (pandoc), PDF (WeasyPrint). Yayımlama yoktur; rapor taslaktır.
"""
import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from medya import GDELT_ATTRIBUTION_DUZ
from medya import gdelt as gd
from medya.arastirma import kapsam_denetle
from medya.hipotez.kayit import hipotez_metni, matrise_kaydet
from medya.hipotez.ach import agirlik
from medya.kanit.kart import KanitKarti
from medya.rapor import tablolar as T
from medya.rapor.yapi import BOLUMLER, DIV_SINIFI, baslik, dosya_adi
from medya.vaka_paketi import VakaPaketi

ROOT = Path(__file__).resolve().parents[2]
_ATIF = re.compile(r"\[([^\[\]\s][^\[\]]{0,40})\]")
_KIMLIK = re.compile(r"^(KR-\d{3}|RD\d{2}|R\d{2}|K\d{2}|E\d{2}|GD-\d+|RAD-\d+)$")


class VakaRaporHatasi(RuntimeError):
    pass


@dataclass
class RaporSonucu:
    md: Path | None = None
    html: Path | None = None
    pdf: Path | None = None
    sayfa: int = 0
    kapsam: object = None
    uyarilar: list = field(default_factory=list)
    reddedilenler: list = field(default_factory=list)
    kullanilan_kart: int = 0
    mod: str = "cevrimdisi"
    sayac: dict = field(default_factory=dict)

    def ozet(self) -> dict:
        return {"md": str(self.md), "html": str(self.html or ""), "pdf": str(self.pdf or ""), "sayfa": self.sayfa,
                "mod": self.mod, "kapsam_tamam": self.kapsam.tamam if self.kapsam else None,
                "kapsam_eksikleri": self.kapsam.eksikler if self.kapsam else [], "uyarilar": self.uyarilar,
                "reddedilen_cumle": len(self.reddedilenler), "kullanilan_kart": self.kullanilan_kart,
                "sayac": self.sayac}


# --------------------------------------------------------------------------------
def _hipotez_matrisi(paket: VakaPaketi):
    h = paket.ice_aktarim.hipotezler
    return matrise_kaydet(h, paket.ayar.get("hipotez_turleri")) if h else None


def kapsam_raporu(paket: VakaPaketi, ist: dict | None = None, kati: bool = False):
    ist = ist if ist is not None else gd.yukle(paket.yol("gdelt", "istatistik.json"))
    ach_m = paket.alt_ayar("ach_matris")
    kavram = [paket.yol(p) for p in ((paket.ayar.get("arastirma") or {}).get("kavram_dosyalari") or [])]
    return kapsam_denetle(paket.kartlar, paket.olay_tarihi, vaka_ayari=paket.ayar, gdelt_ist=ist,
                          on_kayit=_hipotez_matrisi(paket), ach_satiri=len(ach_m.get("satirlar", [])),
                          kavram_dosyalari=kavram, kati=kati)


def deterministik_parcalar(paket: VakaPaketi, ist: dict | None, grafik_yollari: dict) -> dict[str, str]:
    kartlar, a, r = paket.kartlar, paket.anonim, paket.ayar.get("rapor", {})
    gayar = paket.alt_ayar("gdelt")
    ach_m = paket.alt_ayar("ach_matris")
    p = {"KAYNAK_TABANI": T.kaynak_tabani(kartlar, ist, r.get("kaynak_tabani", {}), paket.olay_tarihi)}
    for i, ks in enumerate(T.kronoloji_donemleri(kartlar)[:4]):
        p[f"KRONOLOJI:{i}"] = T.kronoloji_tablosu(ks, a)
    cel = paket.alt_ayar("celiskiler")
    p["CELISKI_TABLOSU"] = T.celiski_tablosu(cel) if cel else ""
    if ist:
        p["GDELT_GUNLUK"] = T.gdelt_gunluk(ist)
        p["GDELT_ILK_HABER"] = T.gdelt_ilk_haber(ist, int(gayar.get("saat_farki", 3)))
        p["GDELT_CERCEVE"] = T.gdelt_cerceve(ist, gayar.get("cerceve_tablosu", {"sutunlar": list(gayar.get("cerceveler", {}))}))
        p["GDELT_TON"] = T.gdelt_ton(ist)
    if ach_m:
        p["ACH_MATRISI"] = T.ach_matrisi(ach_m)
    p["KART_DIZINI"] = T.kart_dizini(kartlar, r.get("kart_dizini", {}), a)
    for ad, yol in grafik_yollari.items():
        p[f"GRAFIK:{ad}"] = yol
    return {k: (f'<div class="{DIV_SINIFI[k]}">\n\n{v}\n</div>' if k in DIV_SINIFI and v else v) for k, v in p.items()}


def yer_tutuculari_doldur(metin: str, parcalar: dict) -> str:
    def _r(m):
        k = m.group(1)
        if k not in parcalar:
            raise VakaRaporHatasi(f"Yer tutucu için veri yok: {{{{{k}}}}}")
        return parcalar[k]
    return re.sub(r"\{\{([A-Z_]+(?::[a-z0-9]+)?)\}\}", _r, metin)


def atif_denetimi(md: str, kartlar: dict, izinli: set, kaliplar: list[str]) -> tuple[set, list]:
    """(kullanılan kimlikler, bilinmeyen atıflar). Yalnızca Ek A'dan önceki gövde taranır."""
    govde = md.split("\n# Ek A")[0]
    kullanilan, bilinmeyen = set(), []
    for m in _ATIF.finditer(govde):
        for parca in re.split(r"\s*[,–]\s*", m.group(1)):
            parca = parca.strip()
            if not parca:
                continue
            if parca in kartlar:
                kullanilan.add(parca)
            elif _KIMLIK.match(parca):
                bilinmeyen.append(parca)
            elif parca in izinli or any(re.fullmatch(k, parca) for k in kaliplar):
                continue
    return kullanilan, sorted(set(bilinmeyen))


# --------------------------------------------------------------------------------
# LLM modu: bölüm kart seçimi ve sözde kartlar (GDELT, kavram notu, ACH satırları)
# --------------------------------------------------------------------------------
def _sozde(stabil_id: str, kurum: str, ozet: str, url: str, tur: str = "veri_serisi") -> KanitKarti:
    return KanitKarti(tur=tur, kaynak_url=url, kurum=kurum, ozet=ozet[:600], kaynak_derecesi="B", bilgi_derecesi="2",
                      stabil_id=stabil_id, ek={"_sema": "SOZDE"})


def gdelt_kartlari(ist: dict) -> list[KanitKarti]:
    if not ist:
        return []
    url, kurum = "https://www.gdeltproject.org/", "The GDELT Project (hesaplama: medya.gdelt)"
    g = sorted(ist["gunluk"].items(), key=lambda x: -x[1]["haber"])[:6]
    c = ist["cerceve"]
    parca = [
        f"Çekirdek küme {ist['tekil_url']} haber, {ist['tekil_site']} site; Türkçe kaynaklı toplam {ist['turkce_toplam_kayit_pencere']} "
        "kayıt. En yüksek günler: " + "; ".join(f"{d[6:]}.{d[4:6]}.{d[:4]} {v['haber']} haber (%{T.ondalik(v['pay_yuzde'])})" for d, v in g),
        "Çerçeve sayımları (URL): " + "; ".join(
            f"{grp} n={c['n'][grp]}: " + ", ".join(f"{k} {v}" for k, v in c["grup"].get(grp, {}).items())
            for grp in ("Hükümete yakın", "Muhalif / bağımsız", "TÜMÜ") if grp in c["n"]),
        "İlk haber (UTC dosya zamanı): " + "; ".join(f"{s} {u[6:8]}.{u[4:6]} {u[8:10]}:{u[10:12]}" for s, u in
                                                     list(ist["izlenen_yayin_ilk_haber_utc"].items())[:8]),
        "Ton ortalaması: " + "; ".join(f"{grp} {T.ondalik(v[0])}" for grp, v in ist["ton_grup"].items())
        + f"; tümü {T.ondalik(ist['ton_tum'])}",
    ]
    gs = ist.get("gostergeler", {})
    if gs.get("atif_aklama"):
        parca.append("Atıf aklama adayı: " + "; ".join(f"{x['cerceve']} ilk dosya {x['ilk_dosya_utc']} {x['site']}"
                                                         for x in gs["atif_aklama"][:4]))
    return [_sozde(f"GD-{i}", kurum, p, url) for i, p in enumerate(parca, 1)]


def kavram_kartlari(paket: VakaPaketi) -> list[KanitKarti]:
    out, n = [], 0
    for p in ((paket.ayar.get("arastirma") or {}).get("kavram_dosyalari") or []):
        yol = paket.yol(p)
        if not yol.exists():
            continue
        for parca in re.split(r"\n(?=#{2,3} )", yol.read_text(encoding="utf-8")):
            temiz = re.sub(r"\s+", " ", parca).strip()
            if len(temiz) < 80:
                continue
            n += 1
            out.append(_sozde(f"RAD-{n}", f"Kavram notu ({yol.name})", temiz, f"file://{p}", "arastirma_kurumu"))
    return out


def ach_kartlari(ach_m: dict) -> list[KanitKarti]:
    H = ach_m.get("hipotezler", [])
    return [_sozde(e["id"], "ACH matrisi (analist değerlendirmesi)",
                   f"{e['aciklama']}. Dayanak kartlar: {e['kartlar']}. Derece {e['derece']}. "
                   f"İşaretler ({' '.join(H)}): {e['isaretler']}.", "file://ach_matris.yaml")
            for e in ach_m.get("satirlar", [])]


def bolum_kartlari(bolum: dict, paket: VakaPaketi, ist: dict | None, ach_m: dict) -> list[KanitKarti]:
    sec = bolum.get("secim", {})
    out = []
    for s in sec.get("semalar", []):
        if s == "GDELT":
            out += gdelt_kartlari(ist)
        elif s == "RAD":
            out += kavram_kartlari(paket)
        elif s == "ACH":
            out += ach_kartlari(ach_m)
        else:
            out += [k for k in paket.kartlar.values() if k.ek.get("_sema") == s]
    if sec.get("celiskili_once"):
        out.sort(key=lambda k: (not k.celiski,))
    elif sec.get("azami"):
        out.sort(key=lambda k: (-agirlik(k), k.olay_tarihi or "", k.gorunen_id))
    return out[:sec["azami"]] if sec.get("azami") else out


# --------------------------------------------------------------------------------
def vaka_raporu_uret(vaka_id: str, cevrimdisi: bool = True, saglayici=None, cikti: str | Path | None = None,
                     pdf: bool = True, kati: bool = False, paket_koku=None, sayac=None) -> RaporSonucu:
    paket = VakaPaketi(vaka_id, paket_koku)
    imp = paket.ice_aktarim
    if imp.hatalar:
        raise VakaRaporHatasi("Kart dosyalarında hata: " + "; ".join(imp.hatalar[:5]))
    kartlar = paket.kartlar
    ist = gd.yukle(paket.yol("gdelt", "istatistik.json"))
    ach_m = paket.alt_ayar("ach_matris")
    r_ayar = paket.ayar.get("rapor", {})
    sonuc = RaporSonucu(mod="cevrimdisi" if cevrimdisi else "llm")
    sonuc.uyarilar += [f"içe aktarma: {u}" for u in imp.uyarilar]

    # 2. kapsam
    sonuc.kapsam = kapsam_raporu(paket, ist, kati=kati)

    # tutarlılık denetimleri
    izinli = set(r_ayar.get("izinli_etiketler", []))
    if ach_m:
        sorun = T.ach_denetimi(ach_m, kartlar)
        if any("var olmayan" in s for s in sorun):
            raise VakaRaporHatasi("ACH matrisi: " + "; ".join(sorun))
        sonuc.uyarilar += [f"ACH: {s}" for s in sorun]
    cel = paket.alt_ayar("celiskiler")
    if cel:
        bilinmeyen, bagsiz = T.celiski_denetimi(cel, kartlar, izinli)
        if bilinmeyen:
            raise VakaRaporHatasi("Çelişki tablosunda var olmayan kart: " + ", ".join(bilinmeyen))
        if bagsiz:
            sonuc.uyarilar.append(f"çelişki notu olup çelişki tablosuna bağlanmamış {len(bagsiz)} kronoloji satırı: "
                                  + ", ".join(bagsiz))
    if ist and ist.get("gurultu", {}).get("uyari"):
        sonuc.uyarilar.append("GDELT: " + ist["gurultu"]["uyari"])

    # 3. deterministik parçalar
    cikti = Path(cikti or ROOT / "data" / "raporlar" / vaka_id)
    cikti.mkdir(parents=True, exist_ok=True)
    grafikler = {}
    for ad in ("gunluk", "saatlik"):
        kaynak = paket.yol("gdelt", f"{ad}.png")
        if kaynak.exists():
            shutil.copyfile(kaynak, cikti / f"gdelt_{ad}.png")
            grafikler[ad] = f"gdelt_{ad}.png"
    parcalar = deterministik_parcalar(paket, ist, grafikler)

    # 4. anlatı
    hipotezler = {}
    if imp.hipotezler:
        for h in imp.hipotezler.get("hipotezler", []) + imp.hipotezler.get("sonradan_eklenen_rafinasyonlar", []):
            hipotezler[h["id"]] = hipotez_metni(h)
    govdeler = {}
    if cevrimdisi:
        for b in BOLUMLER:
            metin = paket.anlati(dosya_adi(b["id"]))
            if metin is None:
                raise VakaRaporHatasi(f"Çevrimdışı mod: anlatı dosyası yok: anlati/{dosya_adi(b['id'])}.md")
            govdeler[b["id"]] = metin
    else:
        from medya.uzman.yazim import bolum_yaz
        if saglayici is None:
            raise VakaRaporHatasi("LLM modu için sağlayıcı gerekli (ya da --cevrimdisi)")
        if sayac is not None:
            saglayici.sayac = getattr(saglayici, "sayac", None) or sayac
        tum = [k.dogrulama_metni() for k in kartlar.values()]
        for b in BOLUMLER:
            hazir = paket.anlati(dosya_adi(b["id"]))
            if not b.get("llm"):
                govdeler[b["id"]] = hazir if hazir is not None else "\n" + "\n\n".join(
                    (f"## {alt}\n\n" if alt else "") + ph for alt, ph in b.get("parcalar", [])) + "\n\n"
                continue
            ks = bolum_kartlari(b, paket, ist, ach_m)
            bs = bolum_yaz(saglayici, {"id": b["id"], "baslik": baslik(b["id"], paket.ayar)[2:], "amac": b.get("amac", "")},
                           ks, hipotezler, paket.anonim, tum)
            sonuc.reddedilenler += [{"bolum": b["id"], **x} for x in bs.red]
            ek = "\n\n".join((f"## {alt}\n\n" if alt else "") + ph for alt, ph in b.get("parcalar", []))
            govdeler[b["id"]] = "\n" + (bs.markdown() or "*Bu bölüm için doğrulanmış cümle yok.*") + \
                ("\n\n" + ek if ek else "") + "\n\n"
        if sayac is not None:
            sonuc.sayac = sayac.ozet()

    # birleştir
    kapak = T.kapak(kartlar, ist, r_ayar.get("kapak", {}), ach_m.get("hipotezler") or list(hipotezler),
                    paket.alt_ayar("gdelt"))
    md = kapak + "\n\n" + "".join(baslik(b["id"], paket.ayar) + "\n" + govdeler[b["id"]] for b in BOLUMLER)
    md = yer_tutuculari_doldur(md, parcalar)
    if "gdeltproject.org" not in md:
        md += "\n\n" + GDELT_ATTRIBUTION_DUZ + "\n"

    # 5. atıf denetimi
    kullanilan, bilinmeyen = atif_denetimi(md, kartlar, izinli, r_ayar.get("izinli_etiket_kaliplari", []))
    sozde = {k.gorunen_id for b in BOLUMLER if not cevrimdisi and b.get("llm")
             for k in bolum_kartlari(b, paket, ist, ach_m) if k.ek.get("_sema") == "SOZDE"}
    bilinmeyen = [b for b in bilinmeyen if b not in sozde]
    if bilinmeyen:
        raise VakaRaporHatasi("Gövdede var olmayan kart kimliğine atıf: " + ", ".join(bilinmeyen))
    sonuc.kullanilan_kart = len(kullanilan)

    # 6. çıktı
    ad = r_ayar.get("dosya_adi", f"{vaka_id}-analiz")
    sonuc.md = cikti / f"{ad}.md"
    sonuc.md.write_text(md, encoding="utf-8")
    (cikti / "rapor_ozeti.json").write_text(json.dumps({**sonuc.ozet(), "reddedilenler": sonuc.reddedilenler,
                                                        "kapsam": sonuc.kapsam.hatlar}, ensure_ascii=False,
                                                       indent=1, default=str), encoding="utf-8")
    if pdf:
        from medya.rapor import pdf as P
        tamam, neden = P.araclar_var_mi()
        if not tamam:
            sonuc.uyarilar.append(f"PDF üretilmedi: {neden}")
            return sonuc
        css = P.stil_yaz(cikti / "style.css", r_ayar.get("ust_bilgi", "OSINT analizi · TASLAK — insan onayı bekliyor"))
        sonuc.html = P.html_uret(sonuc.md, cikti / f"{ad}.html", css, r_ayar.get("kapak", {}).get("kicker", "OSINT"))
        sonuc.pdf = cikti / f"{ad}.pdf"
        sonuc.sayfa = P.pdf_uret(sonuc.html, sonuc.pdf)
        (cikti / "rapor_ozeti.json").write_text(json.dumps({**sonuc.ozet(), "reddedilenler": sonuc.reddedilenler,
                                                            "kapsam": sonuc.kapsam.hatlar}, ensure_ascii=False,
                                                           indent=1, default=str), encoding="utf-8")
    return sonuc
