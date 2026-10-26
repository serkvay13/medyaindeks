"""Streamlit sayfası duman testi (streamlit kurulu değilse atlanır)."""
import pytest

st_test = pytest.importorskip("streamlit.testing.v1")

from tests.conftest import ROOT  # noqa: E402

SAYFA = str(ROOT / "pages" / "vaka_raporu.py")


def test_sayfa_vaka_yokken_acilir():
    at = st_test.AppTest.from_file(SAYFA, default_timeout=60).run()
    assert not at.exception
    assert any("Kayıtlı vaka yok" in i.value for i in at.info)


def test_sayfa_rapor_ve_ek_soru(ornek, depo):
    v, _ = ornek
    depo.kapat()   # sayfa depoyu kendisi açar (DuckDB tek yazıcı)
    at = st_test.AppTest.from_file(SAYFA, default_timeout=60).run()
    assert not at.exception
    next(b for b in at.button if b.label == "Yeni rapor sürümü üret").click().run()
    assert not at.exception
    assert v.rapor_surumleri() == [1]
    assert v.rapor_oku()["kanit_ids"], "sayfa vakanın kanıt deposunu okumalı"
    at.text_area(key="vr_soru").input("Olaydan önce limanda denetim yapıldı mı?").run()
    next(b for b in at.button if b.label == "Soruyu kaydet ve plan üret").click().run()
    assert not at.exception
    assert v.sorular()[0]["id"] == "S1"
    assert any("öneri — kanıt aranacak" in c.value for c in at.caption)


def test_parola_kapisi(monkeypatch):
    import hashlib
    monkeypatch.setenv("PANEL_PAROLA_OZETI", hashlib.sha256(b"gizli").hexdigest())
    at = st_test.AppTest.from_file(SAYFA, default_timeout=60).run()
    assert not at.exception
    assert any(t.label == "Erişim parolası" for t in at.text_input)
    assert not any(b.label == "Yeni rapor sürümü üret" for b in at.button)
