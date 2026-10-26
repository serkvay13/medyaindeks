import pytest

from medya.hipotez import ACHHatasi, ACHMatrisi, Hipotez, KirmiziTakim, set_ozeti
from medya.kanit import KanitKarti


def _kart(i, kd="B", bd="2"):
    return KanitKarti(tur="haber", kaynak_url=f"https://example.org/{i}", kurum="Örnek", ozet=f"Özet {i}.",
                      kaynak_derecesi=kd, bilgi_derecesi=bd)


def _hipotezler():
    return [Hipotez("H1", "Resmi tez", "resmi_tez"), Hipotez("H2", "Alternatif", "alternatif"),
            Hipotez("H3", "Masum açıklama", "masum")]


def test_on_kayit_ozeti_ve_kilit():
    m = ACHMatrisi()
    ozet = m.on_kaydet(_hipotezler())
    assert ozet == set_ozeti(_hipotezler()) and len(ozet) == 64
    assert m.on_kayit["zaman"]
    assert not m.kilit_zamani
    k = _kart(1)
    m.degerlendir(k.kanit_id, "H1", "T")
    assert m.kilit_zamani
    h = m.ekle(Hipotez("H4", "Sonradan akla gelen", "yapisal"))
    assert h.sonradan_eklendi
    with pytest.raises(ACHHatasi):
        m.on_kaydet(_hipotezler())


def test_kilitten_once_eklenen_sonradan_degil():
    m = ACHMatrisi()
    m.on_kaydet(_hipotezler())
    assert not m.ekle(Hipotez("H4", "Kanıttan önce eklenen", "yapisal")).sonradan_eklendi


def test_kanit_hipotezden_once_baglanamaz():
    with pytest.raises(ACHHatasi):
        ACHMatrisi().degerlendir("k-1", "H1", "T")


def test_on_kayit_degistirilirse_yakalanir():
    m = ACHMatrisi()
    m.on_kaydet(_hipotezler())
    d = m.to_dict()
    d["hipotezler"][0]["metin"] = "Veriye bakıldıktan sonra yeniden yazılmış tez"
    with pytest.raises(ACHHatasi):
        ACHMatrisi.from_dict(d)


def test_simetri_kurali():
    with pytest.raises(ACHHatasi):     # tek hipotez
        ACHMatrisi().on_kaydet([Hipotez("H1", "Resmi tez", "resmi_tez")])
    with pytest.raises(ACHHatasi):     # resmi tez + tek rakip
        ACHMatrisi().on_kaydet([Hipotez("H1", "Resmi tez", "resmi_tez"), Hipotez("H2", "Alt", "alternatif")])


def test_siralama_agirlikli_celiski():
    k_guclu, k_zayif, k_notr = _kart(1, "A", "1"), _kart(2, "E", "5"), _kart(3)
    kartlar = {k.kanit_id: k for k in (k_guclu, k_zayif, k_notr)}
    m = ACHMatrisi()
    m.on_kaydet(_hipotezler())
    # Güçlü kanıt H1 ile çelişiyor; zayıf kanıt H2 ile çelişiyor; H3 hiçbiriyle çelişmiyor
    m.degerlendir(k_guclu.kanit_id, "H1", "Ç")
    m.degerlendir(k_guclu.kanit_id, "H2", "T")
    m.degerlendir(k_guclu.kanit_id, "H3", "T")
    m.degerlendir(k_zayif.kanit_id, "H2", "C")      # C = Ç
    m.degerlendir(k_zayif.kanit_id, "H3", "T")
    for h in ("H1", "H2", "H3"):
        m.degerlendir(k_notr.kanit_id, h, "T")       # tanısal değil
    s = m.sirala(kartlar)
    assert [r["hipotez_id"] for r in s] == ["H3", "H2", "H1"]
    assert s[0]["agirlikli_celiski"] == 0 and s[2]["agirlikli_celiski"] == 1.0
    assert m.tanisallik(k_notr.kanit_id) == 0.0
    assert m.tanisallik(k_guclu.kanit_id) > 0


def test_resmi_tez_esitlikte_onde_degil():
    k = _kart(1)
    m = ACHMatrisi()
    m.on_kaydet([Hipotez("H2", "Alt", "alternatif"), Hipotez("H1", "Resmi", "resmi_tez"), Hipotez("H3", "Masum", "masum")])
    for h in ("H1", "H2", "H3"):
        m.degerlendir(k.kanit_id, h, "N")
    s = m.sirala({k.kanit_id: k})
    assert [r["hipotez_id"] for r in s] == ["H1", "H2", "H3"]   # tür değil kimlik sırası


def test_kirmizi_takim_ve_kalicilik():
    k = _kart(1)
    m = ACHMatrisi()
    m.on_kaydet(_hipotezler())
    m.degerlendir(k.kanit_id, "H1", "Ç")
    lider = m.sirala({k.kanit_id: k})[0]["hipotez_id"]
    with pytest.raises(ACHHatasi):
        m.kirmizi_takim_ekle(KirmiziTakim(lider, [], "insan"))
    m.kirmizi_takim_ekle(KirmiziTakim(lider, [{"arguman": "Tek kaynak", "yanit": ""}], "insan: analist"))
    m2 = ACHMatrisi.from_dict(m.to_dict())
    assert m2.onde_gelen_icin_kirmizi_takim({k.kanit_id: k}).hipotez_id == lider
    assert m2.deger(k.kanit_id, "H1") == "Ç"
