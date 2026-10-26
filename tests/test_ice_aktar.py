"""Kart içe aktarıcı: K/KR/R/RD şemaları, kararlı kimlik, erişim durumu, çelişki ve sınıf düzeltmesi."""
import json

import pytest

from medya.kanit import KanitDeposu
from medya.kanit.ice_aktar import kayitlari_donustur, klasor_ice_aktar, sema_tani
from medya.kanit.siniflar import REJIM_DISI, grup_adlandir, kurum_temizle, sinif_duzelt
from medya.metin import fold_tr
from tests.conftest import ROOT

KARLOV = ROOT / "vakalar" / "karlov"

KR_ORNEK = [{"id": "K001", "tarih": "2016-12-19", "saat": "19:05", "saat_turu": "olay saati",
             "donem": "1-olay günü", "olay": "Sergide silahlı saldırı oldu.", "kaynak_url": "https://ornek.org/1",
             "yayin": "Hürriyet", "yayin_tarihi": "2016-12-20", "alinti": "saldırı oldu",
             "kaynak_sinifi": "yurt içi muhalif/bağımsız", "sinif_notu": None,
             "dogrulama": "sayfa açıldı (web_fetch/curl)", "celiski": "Saat kaynaklara göre değişiyor.", "not_": None},
            {"id": "K002", "tarih": "2016-12-19", "saat": "saat belirtilmemiş", "saat_turu": "", "donem": "1-olay günü",
             "olay": "Kaynağı bulunamayan satır.", "kaynak_url": None, "yayin": None, "yayin_tarihi": None,
             "alinti": None, "kaynak_sinifi": None, "sinif_notu": None, "dogrulama": "bulunamadı",
             "celiski": None, "not_": None}]


def test_sema_tanima():
    assert sema_tani(KR_ORNEK) == "KR"
    assert sema_tani([{"aktor": "a", "ifade_olay": "b"}]) == "R"
    assert sema_tani({"kartlar": [{"olgu": "a", "sinif": "b"}]}) == "RD"
    assert sema_tani({"kartlar": [{"kurum_yayin": "a", "kaynak_derecesi": "B"}]}) == "K"
    assert sema_tani({"baska": 1}) is None


def test_kronoloji_satiri_kararli_kimlik_erisim_celiski():
    s = kayitlari_donustur(KR_ORNEK, "KR", "kronoloji.json")
    assert not s.hatalar
    a, b = s.kartlar
    assert a.gorunen_id == "KR-001" and a.derecesiz and a.derece == "açıldı"
    assert a.celiski.startswith("Saat") and a.saat == "19:05"
    # Hürriyet 2016: Doğan dönemi ana akım (düzeltildi, raporda †)
    assert a.kaynak_sinifi == "yurt içi ana akım (Doğan dönemi)" and a.sinif_duzeltildi
    assert b.erisim_durumu == "bulunamadı" and b.kaynak_url == "" and b.derece == "bulunamadı"


def test_sahiplik_donemi_duzeltmesi():
    assert sinif_duzelt("Hürriyet Daily News", "hükümete yakın yayın", "2017-12-18")[0] == \
        "yurt içi ana akım (Doğan dönemi)"
    assert sinif_duzelt("Hürriyet Daily News", "hükümete yakın yayın", "2018-03-09")[0].endswith("(2018 geçiş yılı)")
    assert sinif_duzelt("CNN Türk", "x", "2020-01-01") == ("hükümete yakın yayın (Demirören dönemi)", True)
    assert sinif_duzelt("Diken (Hürriyet aktarımı)", "yurt içi muhalif/bağımsız", "2016-12-20")[1] is False
    # sınıf dönemi zaten söylüyorsa yeniden düzeltilmez
    assert sinif_duzelt("Hürriyet", "yurt içi ana akım (Doğan grubu dönemi)", "2017-01-01")[1] is False


def test_gulen_siniflari_rejim_kontrolunde_olmayan():
    assert sinif_duzelt("TR724", "Gülen yanlısı/sürgün", "2017-01-01")[0] == REJIM_DISI
    assert grup_adlandir("Gülen hareketine yakın") == "Rejim kontrolünde olmayan kaynaklar"
    assert kurum_temizle("Turkish Minute (Gülen hareketine yakın, sürgün yayın)") == "Turkish Minute"
    assert kurum_temizle("Daily Sabah (hükümet yanlısı)") == "Daily Sabah"


def test_iso_olmayan_tarih_uydurulmaz():
    veri = {"kartlar": [{"kanit_id": "K01", "tur": "haber", "kaynak_url": "https://o.org", "kurum_yayin": "X",
                         "yayin_tarihi": "2019-03 (güncelleme 2021-04-02)", "olay_tarihi": "2016-12-19",
                         "ozet": "Özet.", "alinti": "a", "kaynak_derecesi": "C", "bilgi_derecesi": 3,
                         "serit": "Gülen yanlısı/sürgün", "devlet_baglantili": False}]}
    k = kayitlari_donustur(veri, "K").kartlar[0]
    assert k.yayin_tarihi == "" and k.ek["yayin_tarihi_ham"].startswith("2019-03")
    assert k.kaynak_sinifi == REJIM_DISI and k.derece == "C3"


def test_karlov_paketi_tumu_ice_aktarilir():
    s = klasor_ice_aktar(KARLOV / "kartlar")
    assert not s.hatalar
    assert {ad: len(s.sema(ad)) for ad in ("K", "KR", "R", "RD")} == {"K": 42, "KR": 127, "R": 69, "RD": 56}
    d = s.sozluk()
    assert len(d) == 294 and {"K01", "KR-001", "KR-127", "R69", "RD56"} <= set(d)
    assert sum(1 for k in s.sema("KR") if k.celiski) == 49
    assert not any("gulen" in fold_tr(k.kaynak_sinifi) for k in s.kartlar)
    assert d["R50"].sinif_duzeltildi                     # Hürriyet 2017: Doğan dönemi
    assert s.hipotezler and s.ach


def test_depo_kararli_kimligi_korur(tmp_path):
    s = kayitlari_donustur(KR_ORNEK, "KR")
    with KanitDeposu(tmp_path / "k.duckdb") as d:
        for k in s.kartlar:
            d.ekle(k, vaka_id="v")
        geri = d.vaka_sozluk("v", gorunen=True)
    assert set(geri) == {"KR-001", "KR-002"}
    assert geri["KR-001"].derecesiz and geri["KR-001"].ek["_sema"] == "KR" and geri["KR-001"].sinif_duzeltildi


def test_cli_vaka_ice_aktar(capsys):
    from medya.cli import main
    from medya.vaka import Vaka
    main(["vaka-ice-aktar", str(KARLOV), "karlov-deneme"])
    out = capsys.readouterr().out
    assert "294 kart" in out and "ön kaydedildi" in out
    m = Vaka("karlov-deneme").ach()
    assert m.on_kayit["ids"] == ["H1", "H2", "H3", "H4", "H5"]
    assert all(m.hipotezler[h].sonradan_eklendi for h in ("H3a", "H3b", "H5a"))
    with KanitDeposu() as d:
        assert len(d.vaka_sozluk("karlov-deneme", gorunen=True)) == 294
    main(["vaka-ice-aktar", str(KARLOV), "karlov-deneme"])        # ikinci kez: yeni kart yok, ön kayıt bozulmaz
    assert "(0 yeni)" in capsys.readouterr().out
