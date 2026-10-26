import pytest

from medya.cli import main
from medya.vaka import Vaka


def test_cli_uctan_uca(capsys):
    main(["ornek", "kur"])
    main(["baglam", "ornek-liman"])
    main(["rapor", "uret", "ornek-liman"])
    with pytest.raises(Exception):
        main(["onayla", "ornek-liman", "--onaylayan", "Analist", "--tarih", "2026-10-26"])   # doğrulanmadı
    main(["rapor", "dogrula", "ornek-liman"])
    main(["onayla", "ornek-liman", "--onaylayan", "Analist", "--tarih", "2026-10-26"])
    assert Vaka("ornek-liman").rapor_oku()["durum"] == "onaylandi"
    main(["soru", "ekle", "ornek-liman", "Olaydan önce limanda denetim yapıldı mı?"])
    main(["soru", "isle", "ornek-liman", "S1"])
    assert Vaka("ornek-liman").rapor_surumleri() == [1, 2]
    main(["aktor", "dogrula"])
    cikti = capsys.readouterr().out
    assert "onaylandı" in cikti and "rapora girmez" in cikti


def test_cli_vaka_yeni_ve_hipotez(tmp_path, capsys):
    main(["vaka", "yeni", "deneme-vaka", "--ad", "Deneme", "--soru", "Ne oldu?", "--olay-tarihi", "2025-01-01"])
    hj = tmp_path / "h.json"
    hj.write_text('[{"id":"H1","metin":"Resmi tez","tur":"resmi_tez"},{"id":"H2","metin":"Alt","tur":"alternatif"},'
                  '{"id":"H3","metin":"Masum","tur":"masum"}]', encoding="utf-8")
    main(["hipotez", "kaydet", "deneme-vaka", str(hj)])
    main(["kanit", "ekle", "deneme-vaka", "--tur", "haber", "--url", "https://example.org/x", "--kurum", "Örnek",
          "--ozet", "Özet.", "--kaynak", "B", "--bilgi", "2"])
    out = capsys.readouterr().out
    kid = out.split("[OK] ")[-1].split()[0]
    main(["ach", "degerlendir", "deneme-vaka", "--kanit", kid, "--hipotez", "H1", "--deger", "Ç"])
    main(["hipotez", "ekle", "deneme-vaka", "--id", "H4", "--tur", "yapisal", "--metin", "Sonradan"])
    assert "SONRADAN EKLENDİ" in capsys.readouterr().out
