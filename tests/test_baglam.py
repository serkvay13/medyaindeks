from datetime import date, timedelta

import pandas as pd

from medya.baglam import KAZANC_NOTU, cui_bono, neden_simdi, protokol_calistir, tarihsel_benzerler, zaman_cizgisi


def _seri(sicrama_gun=3, taban=180):
    ot = date(2025, 3, 14)
    s = {ot - timedelta(days=i): 10.0 + (i % 3) for i in range(taban + 40, -1, -1)}
    s[ot - timedelta(days=sicrama_gun)] = 80.0
    return pd.Series(s), ot


def test_neden_simdi_kirilma_n_ve_taban_raporlar():
    s, ot = _seri()
    a = neden_simdi({"hacim": s}, ot, kanit_ids={"hacim": ["k-1"]})
    assert a["durum"] == "tamam"
    ad = a["cikti"]["adaylar"]
    assert len(ad) == 1 and ad[0]["olaya_gore_gun"] == -3
    assert ad[0]["n_taban"] == 180 and "taban_ortalama" in ad[0]
    assert any("neden kanıtı değildir" in n for n in a["notlar"])


def test_neden_simdi_kisa_tabanda_aramaz():
    s, ot = _seri(taban=10)
    a = neden_simdi({"hacim": s.iloc[-25:]}, ot)
    assert a["cikti"]["adaylar"] == [] and any("taban yetersiz" in n for n in a["notlar"])


def test_zaman_cizgisi_kanitsiz_satiri_reddeder():
    a = zaman_cizgisi([{"tarih": "2025-03-01", "serit": "guvenlik", "metin": "x", "kanit_ids": ["k-1"]},
                       {"tarih": "2025-03-02", "serit": "guvenlik", "metin": "kanıtsız"},
                       {"tarih": "2020-01-01", "serit": "ekonomi", "metin": "pencere dışı", "kanit_ids": ["k-2"]}],
                      "2025-03-14")
    assert len(a["cikti"]["seritler"]["guvenlik"]) == 1
    assert a["cikti"]["seritler"]["guvenlik"][0]["tek_kaynak"]
    assert len(a["reddedilen"]) == 1
    assert "uluslararasi_aktorler" in a["cikti"]["seritler"]


def test_cui_bono_notu():
    a = cui_bono([{"aktor": "X", "once_hedefler": [{"metin": "hedef"}],
                   "sonra_degisiklikler": [{"metin": "değişiklik", "kanit_ids": ["k-1"]}]}])
    assert KAZANC_NOTU in a["notlar"]
    assert len(a["cikti"]["tablo"][0]["sonra_degisiklikler"]) == 1 and len(a["reddedilen"]) == 1


def test_benzerler():
    kut = [{"id": "v1", "ad": "A", "etiketler": ["suikast", "diplomat", "ankara"]},
           {"id": "v2", "ad": "B", "etiketler": ["deprem"]}]
    a = tarihsel_benzerler(["suikast", "diplomat"], kut)
    assert [x["vaka_id"] for x in a["cikti"]["benzerler"]] == ["v1"]


def test_protokol_eksik_ve_gerekceli_bos():
    p = protokol_calistir({}, "2025-03-14")
    assert not p["tamamlandi"] and 1 in p["eksik_adimlar"]
    p = protokol_calistir({"erken_isaretler": [], "gerekceler": {"6": "bulunamadı"}}, "2025-03-14")
    adim6 = p["adimlar"][5]
    assert adim6["durum"] == "bos_gerekceli"
