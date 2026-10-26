import ast

from medya.metin import TR_FOLD, fold_tr, sayilari_bul, tarihleri_bul, tr_lower
from tests.conftest import ROOT


def test_fold_tr_app_ile_ayni():
    """medya.metin.TR_FOLD, app.py'deki tablonun birebir kopyası olmalı."""
    agac = ast.parse((ROOT / "app.py").read_text(encoding="utf-8"))
    for d in agac.body:
        if isinstance(d, ast.Assign) and any(getattr(t, "id", None) == "TR_FOLD" for t in d.targets):
            app_tablo = str.maketrans(ast.literal_eval(d.value.args[0]))
            break
    else:
        raise AssertionError("app.py'de TR_FOLD bulunamadı")
    assert app_tablo == TR_FOLD


def test_turkce_kucultme():
    assert tr_lower("IĞDIR İLİ") == "ığdır ili"
    assert fold_tr("Iğdır İli Şırnak") == "igdir ili sirnak"


def test_tarih_bicimleri():
    assert [t for t, _ in tarihleri_bul("19 Aralık 2016'da")] == [(2016, 12, 19)]
    assert [t for t, _ in tarihleri_bul("19.12.2016 günü")] == [(2016, 12, 19)]
    assert [t for t, _ in tarihleri_bul("2016-12-19")] == [(2016, 12, 19)]
    assert [t for t, _ in tarihleri_bul("Aralık 2016 sonunda")] == [(2016, 12, None)]
    assert [t for t, _ in tarihleri_bul("31.02.2016")] == []


def test_sayilar():
    assert sayilari_bul("1.000 kişi, %3,5 artış, beş sanık") == ["1000", "3.5", "5"]
    assert sayilari_bul("ön plana çıktı") == []           # katlanmış "on" sayı sayılmaz
    assert sayilari_bul("H1 ve A2 kimlikleri") == []
