
import pytest

from medya.dogrulayici import DogrulamaHatasi
from medya.rapor import BOLUMLER, RaporHatasi, markdown_uret, onayla, rapor_dogrula, rapor_uret
from medya.uzman import OfflineSaglayici


def test_bolum_tablosu_14():
    assert [b[0] for b in BOLUMLER] == list(range(1, 15))
    assert BOLUMLER[0][1] == "Soru ve kapsam" and BOLUMLER[-1][1] == "Yöntem, kapsam, kaynaklar"


def test_rapor_uret_ve_icerik(ornek, depo):
    v, k = ornek
    r = rapor_uret(v, depo, OfflineSaglayici())
    assert r["durum"] == "taslak" and len([b for b in r["bolumler"] if isinstance(b["no"], int)]) == 14
    assert r["meta"]["git_commit"] and r["meta"]["veri_anlik_goruntu"]
    assert r["eksik_veri"], "Eksik veri bölümü zorunlu"
    # bağlam girdisindeki uydurma satır ("999 sefer") reddedildi ve rapora girmedi
    assert any("999" in x["cumle"]["metin"] for x in r["reddedilenler"])
    md = markdown_uret(r, depo.vaka_sozluk(v.id))
    assert "999" not in md.split("## Analist için")[0]
    assert "https://www.gdeltproject.org/" in md and "### Eksik veri" in md
    assert "Örnek Valiliği iddiası" in md
    for c in (c for b in r["bolumler"] for c in b["cumleler"]):
        if c["tur"] == "olgu":
            assert c["kanit_ids"]


def test_llm_uydurmasi_rapora_giremez(ornek, depo):
    v, k = ornek
    sahte = {"cumleler": [
        {"tur": "olgu", "metin": "Patlamada 47 kişi öldü.", "kanit_ids": [k["haber_ajans"].kanit_id]},
        {"tur": "olgu", "metin": "Valilik kamuoyunu kandırdı.", "kanit_ids": [k["valilik"].kanit_id]},
        {"tur": "olgu", "metin": "Kuzey Limanı'ndaki depoda patlama oldu.", "kanit_ids": ["k-uydurma"]},
        {"tur": "olgu", "metin": "Kuzey Limanı'ndaki bir depoda patlama oldu.",
         "kanit_ids": [k["haber_ajans"].kanit_id]},
    ]}
    r = rapor_uret(v, depo, OfflineSaglayici({"bolum_yaz": sahte}))
    tutulan = [c["metin"] for b in r["bolumler"] for c in b["cumleler"]]
    assert "Patlamada 47 kişi öldü." not in tutulan
    assert "Valilik kamuoyunu kandırdı." not in tutulan
    assert "Kuzey Limanı'ndaki bir depoda patlama oldu." in tutulan
    nedenler = " ".join(n for x in r["reddedilenler"] for n in x["nedenler"])
    assert "sayı kanıtta yok: 47" in nedenler and "niyet atfı" in nedenler and "var olmayan" in nedenler


def test_bolum_yalniz_kendi_kartlarina_dayanabilir(ornek, depo):
    """6. bölüm (resmi anlatı) yalnızca resmi açıklama kartlarını görür; başka karta atıf reddedilir."""
    v, k = ornek
    sahte = {"cumleler": [{"tur": "olgu", "metin": "Enstitü raporu depoda uygunsuz depolama tespit etti.",
                           "kanit_ids": [k["enstitu"].kanit_id]}]}
    r = rapor_uret(v, depo, OfflineSaglayici({"bolum_yaz": sahte}))
    b6 = next(b for b in r["bolumler"] if b["no"] == 6)
    assert b6["cumleler"] == []
    assert any(x["bolum"] == "6" for x in r["reddedilenler"])


def test_onay_akisi(ornek, depo):
    v, _ = ornek
    kartlar = depo.vaka_sozluk(v.id)
    r = rapor_uret(v, depo, OfflineSaglayici())
    with pytest.raises(RaporHatasi):        # doğrulanmadan onay yok
        onayla(r, "Analist", "2026-10-26")
    rapor_dogrula(r, kartlar)
    assert r["durum"] == "dogrulandi"
    with pytest.raises(RaporHatasi):
        onayla(r, "", "2026-10-26")         # onaylayan adı zorunlu
    with pytest.raises(RaporHatasi):
        onayla(r, "Analist", "")            # tarih zorunlu
    with pytest.raises(RaporHatasi):
        onayla(r, "Analist", "26.10.2026")  # ISO tarih
    assert r["durum"] == "dogrulandi"
    onayla(r, "Analist (örnek)", "2026-10-26")
    assert r["durum"] == "onaylandi" and r["onay"]["onaylayan"] == "Analist (örnek)"
    md = markdown_uret(r, kartlar)
    assert "Onaylayan: Analist (örnek)" in md and "Analist için" not in md


def test_kapsam_onayi_olmadan_dogrulanamaz(ornek, depo):
    v, _ = ornek
    v.tanim_guncelle(kapsam_onayi=None)
    r = rapor_uret(v, depo, OfflineSaglayici())
    assert any("Kapsam analist tarafından onaylanmadı" in e for e in r["eksik_veri"])
    with pytest.raises(RaporHatasi):
        rapor_dogrula(r, depo.vaka_sozluk(v.id))


def test_kayitli_rapor_degistirilirse_dogrulanamaz(ornek, depo):
    v, k = ornek
    r = rapor_uret(v, depo, OfflineSaglayici())
    r["bolumler"][2]["cumleler"].append({"tur": "olgu", "metin": "Patlamada 300 kişi öldü.",
                                         "kanit_ids": [k["haber_ajans"].kanit_id], "guven": "", "dayanak": [],
                                         "id": "elle"})
    with pytest.raises(DogrulamaHatasi):
        rapor_dogrula(r, depo.vaka_sozluk(v.id))


def test_protokol_eksikse_3_5_11_12_uretilmez(ornek, depo):
    v, _ = ornek
    v.baglam_girdisi_kaydet({})
    r = rapor_uret(v, depo, OfflineSaglayici())
    for no in (3, 5, 11, 12):
        b = next(b for b in r["bolumler"] if b["no"] == no)
        assert b["cumleler"] == [] and any("protokol" in n.lower() for n in b["notlar"])
    assert any("Bağlam protokolü tamamlanmadı" in e for e in r["eksik_veri"])


def test_surumler_kaydedilir(ornek, depo):
    v, _ = ornek
    r = rapor_uret(v, depo, OfflineSaglayici())
    v.rapor_yaz(r, markdown_uret(r, depo.vaka_sozluk(v.id)))
    assert v.rapor_surumleri() == [1]
    from medya.vaka import VakaHatasi
    with pytest.raises(VakaHatasi):
        v.rapor_yaz(r, "")
