"""Docker imajı: platform dosyaları ve bağımlılıklar imaja giriyor mu (statik denetim)."""
import fnmatch

from tests.conftest import ROOT


def test_dockerfile_platformu_kopyalar():
    d = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    for satir in ("COPY medya/ ./medya/", "COPY pages/ ./pages/", "COPY vakalar/ ./vakalar/",
                  "COPY aktorler/ ./aktorler/", "requirements-platform.txt", "pandoc", "fonts-dejavu-core"):
        assert satir in d, satir
    assert "secrets.toml" not in d.replace("# ", "").split("COPY")[-1]


def test_requirements_platform_rapor_bagimliliklari():
    r = (ROOT / "requirements-platform.txt").read_text(encoding="utf-8")
    for paket in ("pyyaml", "matplotlib", "weasyprint", "pandas", "duckdb"):
        assert paket in r, paket


def test_dockerignore_istem_ve_anlatiyi_disarida_birakmaz():
    kurallar = [s.strip() for s in (ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
                if s.strip() and not s.startswith("#")]

    def dislanir(yol):
        sonuc = False
        for k in kurallar:
            negatif = k.startswith("!")
            kalip = k.lstrip("!").rstrip("/")
            if fnmatch.fnmatch(yol, kalip) or fnmatch.fnmatch(yol, kalip + "/*") or yol.startswith(kalip + "/"):
                sonuc = not negatif
        return sonuc

    assert not dislanir("medya/uzman/istemler/rapor_yazim.md")
    assert not dislanir("vakalar/karlov/anlati/01_yonetici_ozeti.md")
    assert not dislanir("llm/butce.py")
    assert dislanir(".streamlit/secrets.toml") and dislanir("data/gdelt/karlov/tr")
