import pytest

from medya.uzman import ONERI_ETIKETI, OfflineSaglayici, SaglayiciHatasi, hipotez_uret, saglayici_al
from medya.uzman.adimlar import istem


def test_hipotez_uret_oneri_etiketli_ve_turleri_kapsar():
    sag = OfflineSaglayici()
    o = hipotez_uret(sag, {"id": "x", "ad": "Örnek olay", "soru": "Ne oldu?", "olay_tarihi": "2025-01-01"})
    assert o["etiket"] == ONERI_ETIKETI
    turler = {h["tur"] for h in o["hipotezler"]}
    assert {"resmi_tez", "alternatif", "yapisal", "dis_konjonktur", "masum"} <= turler
    assert o["eksik_turler"] == []
    assert all(h["arama_sorgulari"] and h["kaynak_turleri"] for h in o["hipotezler"])


def test_hipotez_uret_eksik_turleri_bildirir():
    sag = OfflineSaglayici({"hipotez_uret": {"hipotezler": [{"id": "Ö1", "tur": "resmi_tez", "metin": "Resmi tez"}]}})
    o = hipotez_uret(sag, {"id": "x", "ad": "y"})
    assert "masum" in o["eksik_turler"] and "yapisal" in o["eksik_turler"]


def test_bozuk_json():
    sag = OfflineSaglayici({"hipotez_uret": "bu JSON değil"})
    assert hipotez_uret(sag, {"id": "x"})["hipotezler"] == []


def test_istemler_turkce_ve_kurallar_icerir():
    for ad in ("hipotez_uret", "bolum_yaz", "arastirma_plani", "kirmizi_takim"):
        m = istem(ad)
        assert "Resmi açıklama olgu değildir" in m and "{{" not in m


def test_saglayici_secimi(monkeypatch):
    assert saglayici_al().ad == "offline"
    with pytest.raises(SaglayiciHatasi):
        saglayici_al("bilinmeyen")
