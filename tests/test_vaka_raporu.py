"""Vaka raporu motoru: Karlov referansıyla birebir eşleşme (çevrimdışı), deterministik tablolar, denetimler,
LLM modu (sahte sağlayıcı) ve PDF (küçük örnek)."""
import json
import re
import shutil

import pytest

from medya.rapor import tablolar as T
from medya.rapor.vaka_raporu import VakaRaporHatasi, atif_denetimi, vaka_raporu_uret
from medya.rapor.yapi import BOLUMLER
from medya.uzman.saglayici import Saglayici
from medya.vaka_paketi import VakaPaketi
from tests.conftest import ROOT

REF = ROOT / "vakalar" / "karlov" / "referans" / "analiz_v2.md"
# Bilinen tek fark: R50 (Hürriyet, 2017-06-03) girdi dosyasında "yurt içi muhalif/bağımsız"; platform Hürriyet'e
# 2018 öncesi için sahiplik düzeltmesini (Doğan dönemi) tutarlı uygular, referans bu satırda uygulamamıştı.
R50_REF = "| R50 | Hürriyet | 2017-06-03 | yurt içi muhalif/bağımsız | B1 |"
R50_YENI = "| R50 | Hürriyet | 2017-06-03 | yurt içi ana akım (Doğan dönemi)† | B1 |"


def _norm(t):
    return re.sub(r"\]\([^)]*gdelt_(gunluk|saatlik)\.png\)", r"](\1.png)", t)


@pytest.fixture(scope="module")
def karlov(tmp_path_factory):
    return vaka_raporu_uret("karlov", cevrimdisi=True, pdf=False, cikti=tmp_path_factory.mktemp("karlov"))


def _divler(md):
    return dict(re.findall(r'<div class="(tbl-[a-z_]+|box)">\n\n(.*?)\n</div>', md, re.S))


def test_karlov_cevrimdisi_referansla_birebir(karlov):
    uretilen = _norm(karlov.md.read_text(encoding="utf-8"))
    referans = _norm(REF.read_text(encoding="utf-8")).replace(R50_REF, R50_YENI)
    assert uretilen == referans


@pytest.mark.parametrize("sinif", ["tbl-kr_a", "tbl-kr_b", "tbl-kr_c", "tbl-kr_d", "tbl-g_daily", "tbl-g_first",
                                   "tbl-g_frames", "tbl-g_tone", "tbl-ach", "box"])
def test_karlov_deterministik_tablolar_birebir(karlov, sinif):
    assert _divler(karlov.md.read_text(encoding="utf-8"))[sinif] == _divler(REF.read_text(encoding="utf-8"))[sinif]


def test_karlov_kapak_kaynak_tabani_ve_kart_dizini(karlov):
    md = karlov.md.read_text(encoding="utf-8")
    ref = REF.read_text(encoding="utf-8")
    assert md.split("\n# ")[0] == ref.split("\n# ")[0]                       # kapak
    assert "TASLAK — İNSAN ONAYI BEKLİYOR" in md and "The GDELT Project" in md.split("\n# ")[0]
    tablo = lambda t: re.search(r"\| Dosya \| Kart/satır.*?URL düzeyinde sayım; bkz\. Ek B \|", t, re.S).group(0)
    assert tablo(md) == tablo(ref)
    eka = _divler(md)["tbl-eka"]
    assert eka == _divler(ref)["tbl-eka"].replace(R50_REF, R50_YENI)
    assert eka.count("\n| K") + eka.count("\n| R") >= 294


def test_karlov_ozet_ve_kapsam(karlov):
    assert karlov.kapsam.tamam
    assert karlov.kullanilan_kart > 250
    assert any("bağlanmamış" in u for u in karlov.uyarilar)
    oz = json.loads((karlov.md.parent / "rapor_ozeti.json").read_text(encoding="utf-8"))
    assert oz["mod"] == "cevrimdisi" and len(oz["kapsam"]) == 5


def test_ach_hesap_ve_siralama():
    m = VakaPaketi("karlov").alt_ayar("ach_matris")
    r = T.ach_hesapla(m)
    assert [round(r["celiski"][h], 2) for h in m["hipotezler"]] == [5.27, 2.09, 1.02, 1.53, 0.0, 0.0]
    assert r["siralama"][:2] == ["H4", "H5a"] and r["siralama"][-1] == "H1"
    assert T.ach_kart_kimlikleri("RD18–RD22, K30") == ["RD18", "RD19", "RD20", "RD21", "RD22", "K30"]
    assert T.ach_kart_kimlikleri("K18 × K24") == ["K18", "K24"]


def test_ach_ve_celiski_denetimleri():
    paket = VakaPaketi("karlov")
    m = json.loads(json.dumps(paket.alt_ayar("ach_matris")))
    assert T.ach_denetimi(m, paket.kartlar) == []
    m["satirlar"][0]["kartlar"] += ", K99"
    m["satirlar"][1]["derece"] = "F6"
    s = " ".join(T.ach_denetimi(m, paket.kartlar))
    assert "var olmayan kart K99" in s and "E02: derece F6" in s
    bilinmeyen, _ = T.celiski_denetimi({"kayitlar": [{"kartlar": ["KR-999", "GDELT-ek"]}]}, paket.kartlar,
                                       {"GDELT-ek"})
    assert bilinmeyen == ["KR-999"]


def test_atif_denetimi_var_olmayan_karti_yakalar():
    paket = VakaPaketi("karlov")
    k, b = atif_denetimi("Metin [KR-001], [K99] ve [GDELT-istatistik] [RAD-A§3].\n# Ek A\n[K98]", paket.kartlar,
                         {"GDELT-istatistik"}, [r"RAD-A§\d+"])
    assert k == {"KR-001"} and b == ["K99"]


def test_yardimcilar():
    assert [T.iyelik(n) for n in (54, 8, 52, 6, 10, 40, 100, 1000, 3, 9)] == \
        ["54'ü", "8'i", "52'si", "6'sı", "10'u", "40'ı", "100'ü", "1000'i", "3'ü", "9'u"]
    assert T.ondalik("≈14.7× 3.42") == "≈14,7× 3,42"


# ---------------------------------------------------------------- LLM modu (sahte sağlayıcı)
class Sahte(Saglayici):
    ad, model = "sahte", "sahte-1"

    def __init__(self):
        self.gorevler = []

    def tamamla(self, sistem, kullanici, gorev, max_tokens=2000):
        self.gorevler.append(gorev)
        paket = json.loads(kullanici.split("(JSON):", 1)[1])
        k = paket["kartlar"][0]
        return json.dumps({"cumleler": [
            {"tur": "O", "metin": f"{k['kaynak']} bu kaydı yayımladı.", "kanit": [k["id"]]},
            {"tur": "O", "metin": "Uydurma bir olay 1999'da oldu.", "kanit": ["K99"]},
            {"tur": "S", "metin": "Hangi belge bunu kapatır?", "kanit": []}]}, ensure_ascii=False)


def test_llm_modu_bolum_bazli_ve_dogrulamali(tmp_path):
    sag = Sahte()
    s = vaka_raporu_uret("karlov", cevrimdisi=False, saglayici=sag, pdf=False, cikti=tmp_path)
    llm = [b["id"] for b in BOLUMLER if b.get("llm")]
    assert sag.gorevler == [f"yazim-{b}" for b in llm]
    assert len(s.reddedilenler) == len(llm) and all("K99" in json.dumps(r, ensure_ascii=False) for r in s.reddedilenler)
    md = s.md.read_text(encoding="utf-8")
    assert md.count("**[S]** Hangi belge bunu kapatır?") == len(llm)
    assert "Uydurma" not in md
    d = _divler(md)
    assert d["tbl-ach"] == _divler(REF.read_text(encoding="utf-8"))["tbl-ach"]          # tablolar yine koddan
    assert "## Olay günü" in md and "TASLAK — İNSAN ONAYI BEKLİYOR" in md


def test_cevrimdisi_anlati_eksikse_hata(tmp_path):
    kok = tmp_path / "vakalar"
    shutil.copytree(ROOT / "vakalar" / "karlov", kok / "karlov")
    (kok / "karlov" / "anlati" / "01_yonetici_ozeti.md").unlink()
    with pytest.raises(VakaRaporHatasi, match="anlatı dosyası yok"):
        vaka_raporu_uret("karlov", cevrimdisi=True, pdf=False, cikti=tmp_path / "o", paket_koku=kok)


def test_pdf_kucuk_ornek(tmp_path):
    from medya.rapor import pdf as P
    tamam, neden = P.araclar_var_mi()
    if not tamam:
        pytest.skip(neden)
    md = tmp_path / "r.md"
    md.write_text('<div class="cover">\n<div class="draft">TASLAK — İNSAN ONAYI BEKLİYOR</div>\n'
                  '<h1 class="title">Örnek</h1>\n</div>\n\n# Bölüm\n\n**[O]** Çağrı şöyle [K01].\n\n'
                  '| a | b |\n|---|---|\n| ğ | ş |\n', encoding="utf-8")
    css = P.stil_yaz(tmp_path / "style.css", "Örnek · TASLAK")
    h = P.html_uret(md, tmp_path / "r.html", css, "Örnek")
    html = h.read_text(encoding="utf-8")
    assert "<colgroup>" not in html and html.index('class="cover"') < html.index('id="TOC"')
    assert P.pdf_uret(h, tmp_path / "r.pdf") >= 2 and (tmp_path / "r.pdf").read_bytes()[:4] == b"%PDF"
