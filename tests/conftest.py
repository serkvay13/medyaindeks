"""Ortak test düzeneği: her test geçici bir çalışma alanı ve kanıt deposu kullanır; ağ yoktur."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def gecici_ortam(tmp_path, monkeypatch):
    monkeypatch.setenv("MEDYA_CALISMA", str(tmp_path / "calisma"))
    monkeypatch.setenv("MEDYA_KANIT_DB", str(tmp_path / "kanit.duckdb"))
    monkeypatch.setenv("MEDYA_LLM_SAGLAYICI", "offline")
    yield tmp_path


@pytest.fixture
def depo(tmp_path):
    from medya.kanit import KanitDeposu
    d = KanitDeposu(tmp_path / "kanit.duckdb")
    yield d
    d.kapat()


@pytest.fixture
def ornek(depo):
    from medya.ornek_veri import kartlar, ornek_kur
    v = ornek_kur(depo)
    return v, kartlar()
