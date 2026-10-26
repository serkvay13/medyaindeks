import json

import pytest

from medya.kanit import KanitHatasi, KanitKarti, kanit_id_uret


def _kart(**ek):
    d = dict(tur="haber", kaynak_url="https://example.org/a", kurum="Örnek Gazete", ozet="Özet metni.",
             kaynak_derecesi="B", bilgi_derecesi="2", alinti="Kısa alıntı.")
    d.update(ek)
    return KanitKarti(**d)


def test_kimlik_kararli():
    a, b = _kart(), _kart(ozet="Başka özet.")
    assert a.kanit_id == b.kanit_id == kanit_id_uret("https://example.org/a", "Kısa alıntı.")
    assert _kart(alinti="Farklı.").kanit_id != a.kanit_id


def test_gecersiz_kartlar():
    with pytest.raises(KanitHatasi):
        _kart(alinti="x" * 301)
    with pytest.raises(KanitHatasi):
        _kart(kaynak_derecesi="G")
    with pytest.raises(KanitHatasi):
        _kart(tur="blog")
    with pytest.raises(KanitHatasi):
        _kart(kaynak_url="")
    with pytest.raises(KanitHatasi):   # grup tarihsiz/dayanaksız olamaz
        _kart(yayin_grubu="muhalif")


def test_resmi_aciklama_iddia_olarak_gosterilir():
    k = _kart(tur="resmi_aciklama", kurum="Örnek Bakanlığı")
    assert k.baslik() == "Örnek Bakanlığı iddiası"
    assert k.iddia_mi


def test_depo_ice_disa_aktar(depo, tmp_path):
    k1, k2 = _kart(), _kart(kaynak_url="https://example.org/b", tur="mahkeme_kaydi")
    assert depo.ekle(k1, "vaka-a") and depo.ekle(k2, "vaka-a", alt_soru="S1")
    assert not depo.ekle(k1, "vaka-a")
    yol = tmp_path / "disa.json"
    assert depo.disa_aktar("vaka-a", yol) == 2
    from medya.kanit import KanitDeposu
    d2 = KanitDeposu(tmp_path / "ikinci.duckdb")
    n, hatalar = d2.ice_aktar(yol)
    assert n == 2 and not hatalar
    assert d2.alt_soru_haritasi("vaka-a")[k2.kanit_id] == "S1"
    assert d2.getir(k1.kanit_id).to_dict() == k1.to_dict()
    # bozuk kart nedeniyle reddedilir, diğerleri yüklenir
    veri = json.loads(yol.read_text())
    veri["kartlar"].append({"tur": "haber", "kaynak_url": "", "kurum": "x", "ozet": "y", "kaynak_derecesi": "A",
                            "bilgi_derecesi": "1"})
    yol.write_text(json.dumps(veri))
    n, hatalar = KanitDeposu(tmp_path / "ucuncu.duckdb").ice_aktar(yol)
    assert n == 2 and len(hatalar) == 1
