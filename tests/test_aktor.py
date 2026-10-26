import pandas as pd
import pytest

from medya.aktor import ProfilHatasi, profil_yukle, profilleri_yukle, tepki_olasiligi, wilson
from tests.conftest import ROOT


def test_wilson():
    lo, hi = wilson(5, 10)
    assert 0.23 < lo < 0.24 and 0.76 < hi < 0.77
    assert wilson(0, 0) == (0.0, 1.0)


def _olaylar(n_tetik, tepki_her=1, gun_arasi=10, baslangic="2024-01-01"):
    """A→B tetik (sınıf 4) her `gun_arasi` günde; B→A tepki (sınıf 3) tetikten 2 gün sonra, her `tepki_her`
    tetikte bir. Ayrıca arka planda tetikten bağımsız seyrek tepkiler."""
    sat = []
    t0 = pd.Timestamp(baslangic)
    for i in range(n_tetik):
        g = t0 + pd.Timedelta(days=i * gun_arasi)
        sat.append({"tarih": g, "aktor1": "AAA", "aktor2": "BBB", "QuadClass": 4, "GoldsteinScale": -5.0})
        if i % tepki_her == 0:
            sat.append({"tarih": g + pd.Timedelta(days=2), "aktor1": "BBB", "aktor2": "AAA", "QuadClass": 3,
                        "GoldsteinScale": -2.0})
    sat.append({"tarih": t0 + pd.Timedelta(days=n_tetik * gun_arasi + 30), "aktor1": "CCC", "aktor2": "AAA",
                "QuadClass": 1, "GoldsteinScale": 1.0})
    return pd.DataFrame(sat)


def test_tepki_fonksiyonu_yeterli_n():
    df = _olaylar(30)
    r = tepki_olasiligi(df, "AAA", "BBB", 4, 3, n_gun=3)
    assert r.n == 30 and r.basari == 30 and r.oran == 1.0
    assert not r.yetersiz
    assert r.taban_oran < r.oran and r.oran_farki > 1
    assert r.ga[0] > 0.8 and r.n_taban > 0
    assert r.goldstein_ort == -2.0
    assert "n=30" in str(r)


def test_tepki_fonksiyonu_kucuk_n_isaretlenir():
    r = tepki_olasiligi(_olaylar(8, tepki_her=2), "AAA", "BBB", 4, 3, n_gun=3)
    assert r.n == 8 and r.basari == 4 and r.yetersiz
    assert "YETERSİZ" in str(r)
    assert r.ga[1] - r.ga[0] > 0.4      # küçük n'de geniş aralık


def test_tetik_yoksa_oran_yok_ama_n_var():
    r = tepki_olasiligi(_olaylar(5), "BBB", "AAA", 4, 3)
    assert r.n == 0 and r.oran is None and r.yetersiz


def test_aktif_profilde_kaynaksiz_kayit_reddedilir(tmp_path):
    p = tmp_path / "x.toml"
    p.write_text('aktor = "Örnek Kurum"\ntur = "devlet_kurumu"\ndurum = "aktif"\ngozden_gecirme = "2027-01-01"\n'
                 '[[tipik_hamleler]]\nmetin = "Kaynaksız iddia"\nkaynaklar = []\n', encoding="utf-8")
    with pytest.raises(ProfilHatasi):
        profil_yukle(p)
    p.write_text('aktor = "Örnek Kurum"\ntur = "devlet_kurumu"\ndurum = "aktif"\ngozden_gecirme = "2027-01-01"\n'
                 '[[tipik_hamleler]]\nmetin = "Tarihsiz kaynak"\nkaynaklar = [{url = "https://example.org"}]\n',
                 encoding="utf-8")
    with pytest.raises(ProfilHatasi):
        profil_yukle(p)


def test_gozden_gecirme_tarihi_zorunlu(tmp_path):
    p = tmp_path / "x.toml"
    p.write_text('aktor = "Örnek"\ntur = "medya"\ndurum = "taslak"\n', encoding="utf-8")
    with pytest.raises(ProfilHatasi):
        profil_yukle(p)


def test_kaynakli_aktif_profil_ve_taslak_dislanir(tmp_path):
    (tmp_path / "a.toml").write_text(
        'aktor = "Örnek Kurum"\ntur = "devlet_kurumu"\ndurum = "aktif"\ngozden_gecirme = "2027-01-01"\n'
        '[[tipik_hamleler]]\nmetin = "Açıklama yapar"\nkaynaklar = [{url = "https://example.org/k", tarih = "2025-01-01"}]\n',
        encoding="utf-8")
    (tmp_path / "b.toml").write_text(
        'aktor = "Taslak Kurum"\ntur = "medya"\ndurum = "taslak"\ngozden_gecirme = "2027-01-01"\n'
        '[[cikarlar]]\nmetin = "TODO"\nkaynaklar = []\n', encoding="utf-8")
    hepsi = profilleri_yukle(tmp_path)
    assert len(hepsi) == 2
    rapor = profilleri_yukle(tmp_path, yalniz_raporlanabilir=True)
    assert [p.aktor for p in rapor] == ["Örnek Kurum"]


def test_repodaki_ornek_profiller_taslak():
    profiller = profilleri_yukle(ROOT / "aktorler")
    assert len(profiller) >= 2
    assert not any(p.raporlanabilir for p in profiller)
