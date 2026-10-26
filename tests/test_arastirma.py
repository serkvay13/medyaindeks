"""Araştırma protokolü: protokol → görev listesi, ön kayıt kilidi, sağlayıcılar, kapsam denetçisi."""
import json

import pytest

from medya.arastirma import (HATLAR, ArastirmaHatasi, ManuelSaglayici, WebAramaSaglayici, gorev_listesi,
                             kapsam_denetle, on_kayit_dogrula, on_kayit_kilitle, protokol_yukle)
from medya.hipotez.kayit import matrise_kaydet
from medya.vaka_paketi import VakaPaketi

HIPOTEZ = {"hipotezler": [{"id": "H1", "ad": "Resmî tez", "tanim": "Kurumun açıkladığı fail ağı"},
                          {"id": "H2", "ad": "Yalnız aktör", "tanim": "Örgütsel bağ yok"},
                          {"id": "H3", "ad": "Güvenlik ihmali", "tanim": "Koruma eksikliği"}]}
AYAR = {"id": "ornek", "olay_tarihi": "2020-01-01",
        "arastirma": {"ek_diller": ["ar"],
                      "degiskenler": {"olay": {"tr": "Örnek saldırı", "en": "Example attack", "ru": "атака"},
                                      "fail": {"tr": "Fail Adı"}, "tarih": {"tr": "1 Ocak 2020", "en": "1 January 2020"}},
                      "aktorler": [{"tr": "Rusya", "en": "Russia"}, "NATO"],
                      "kavramlar": ["radikalleşme"], "kavram_ceviri": {"radikalleşme": {"en": "radicalization"}}}}


def test_protokol_bes_hat_ve_gecersiz_kilma():
    p = protokol_yukle(AYAR)
    assert tuple(p["hatlar"]) == HATLAR
    assert [p["hatlar"][h]["kod"] for h in HATLAR] == ["a", "b", "c", "d", "e"]
    p2 = protokol_yukle({"arastirma": {"protokol": {"hatlar": {"kronoloji": {"esikler": {"asgari_kart": 99}}}}}})
    assert p2["hatlar"]["kronoloji"]["esikler"] == {"asgari_kart": 99, "olay_gunu_satir": 20}


def test_on_kayit_olmadan_gorev_uretilmez(tmp_path):
    with pytest.raises(ArastirmaHatasi, match="ön kaydı"):
        gorev_listesi(AYAR)
    k = on_kayit_kilitle(HIPOTEZ, tmp_path / "on_kayit.json")
    assert len(k["ozet"]) == 64 and k["ids"] == ["H1", "H2", "H3"]
    with pytest.raises(ArastirmaHatasi, match="zaten var"):
        on_kayit_kilitle(HIPOTEZ, tmp_path / "on_kayit.json")
    # kilitli kümeyi değiştirmek fark edilir
    veri = json.loads((tmp_path / "on_kayit.json").read_text())
    h2 = veri["ach"]["hipotezler"]["H2"] if isinstance(veri["ach"]["hipotezler"], dict) else \
        next(h for h in veri["ach"]["hipotezler"] if h["id"] == "H2")
    h2["metin"] = "Sonradan değiştirilmiş"
    with pytest.raises(Exception):
        on_kayit_dogrula(veri)


def test_gorev_listesi_cok_dilli(tmp_path):
    on_kayit_kilitle(HIPOTEZ, tmp_path / "on_kayit.json")
    g = gorev_listesi(AYAR, on_kayit=tmp_path / "on_kayit.json")
    hatlar = {x["hat"] for x in g}
    assert hatlar == set(HATLAR)
    kr = [x for x in g if x["hat"] == "kronoloji"]
    assert {x["dil"] for x in kr} >= {"tr", "en", "ru"}
    assert all("{" not in x["sorgu"] for x in g if x["tur"] == "arama")
    assert any(x["sorgu"] == "Example attack Russia reaction" for x in g)      # aktör × dil
    assert any("NATO" in x.get("sorgu", "") and x.get("dil") == "ru" for x in g)          # dile çevrilmemiş aktör adı
    assert any(x["sorgu"] == "radicalization definition academic review" for x in g)
    assert not any(x.get("dil") == "ru" and "{fail}" in x.get("sorgu", "") for x in g)
    assert kr[0]["kart_semasi"] == "KR" and "celiski" in kr[0]["alanlar"]
    assert [x["komut"] for x in g if x["hat"] == "gdelt"][0] == "python -m medya gdelt indir ornek"
    assert len({x["id"] for x in g}) == len(g)
    assert gorev_listesi(AYAR, on_kayitsiz=True)[0]["on_kayitsiz"] is True


def test_manuel_saglayici_gidis_donus(tmp_path):
    sag = ManuelSaglayici(tmp_path / "g")
    yol = sag.gorevleri_yaz([{"id": "a-001", "tur": "arama", "sorgu": "x"}], "ornek")
    veri = json.loads(yol.read_text())
    assert veri["gorevler"][0]["id"] == "a-001" and "kurum iddiası" in veri["talimat"]
    (tmp_path / "g" / "kartlar" / "kronoloji.json").write_text(json.dumps([{
        "id": "K001", "tarih": "2020-01-01", "saat": "10:00", "donem": "1-olay günü", "olay": "Bir olay oldu.",
        "kaynak_url": "https://ornek.org/1", "yayin": "Ornek", "yayin_tarihi": "2020-01-01", "alinti": "olay oldu",
        "kaynak_sinifi": "yabancı bağımsız medya", "dogrulama": "açıldı", "celiski": None}]), encoding="utf-8")
    r = sag.sonuclari_al()
    assert not r.hatalar and [k.gorunen_id for k in r.kartlar] == ["KR-001"]


def test_web_saglayici_yapilandirma_ve_sonuc():
    with pytest.raises(RuntimeError, match="MEDYA_ARAMA_URL"):
        WebAramaSaglayici(url_sablonu="").ara("x")
    istenen = []

    def getir(url):
        istenen.append(url)
        return {"results": [{"title": "Başlık", "url": "https://a.org", "content": "özet"}]}
    sag = WebAramaSaglayici("https://arama.ornek/s?q={q}&l={dil}", anahtar="", getir=getir)
    s = sag.gorevleri_calistir([{"id": "a-1", "tur": "arama", "sorgu": "Örnek saldırı", "dil": "tr"},
                                {"id": "d-1", "tur": "komut", "komut": "x"}])
    assert list(s) == ["a-1"] and s["a-1"][0]["erisim"] == "arama özeti"
    assert istenen == ["https://arama.ornek/s?q=%C3%96rnek%20sald%C4%B1r%C4%B1&l=tr"]


def test_kapsam_denetcisi_eksikleri_raporlar():
    paket = VakaPaketi("karlov")
    ist = {"tekil_url": 4185}
    m = matrise_kaydet(paket.ice_aktarim.hipotezler)
    tam = kapsam_denetle(paket.kartlar, paket.olay_tarihi, vaka_ayari=paket.ayar, gdelt_ist=ist, on_kayit=m,
                         ach_satiri=22, kavram_dosyalari=[paket.yol("kaynaklar", "radikallesme.md")])
    assert tam.tamam, tam.eksikler
    kr = next(h for h in tam.hatlar if h["hat"] == "kronoloji")
    assert kr["olcumler"]["olay günü satırı"] == 54 and kr["olcumler"]["kart"] == 127
    # olay günü eşiği ve eksik hatlar
    yalniz_kr = {k: v for k, v in paket.kartlar.items() if v.ek["_sema"] == "KR"}
    eksik = kapsam_denetle(yalniz_kr, paket.olay_tarihi, vaka_ayari={"arastirma": {"esikler": {
        "kronoloji": {"olay_gunu_satir": 60}}}})
    assert not eksik.tamam
    metin = " | ".join(eksik.eksikler)
    assert "olay günü 54 satır < eşik 60" in metin and "GDELT istatistiği yok" in metin
    assert "ön kaydı" in metin and "mağdur yakınları" in metin and "kavram notu" in metin
    with pytest.raises(ArastirmaHatasi, match="Kapsam eksik"):
        kapsam_denetle(yalniz_kr, paket.olay_tarihi, kati=True)
