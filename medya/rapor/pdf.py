"""Markdown → HTML (pandoc) → PDF (WeasyPrint). Yazı tipi DejaVu (Türkçe karakterler); stil `stil/style.css`.

İçindekiler kapaktan sonraya taşınır; pandoc'un sütun genişliği (`colgroup`) kaldırılır (geniş tablolar sayfaya
sığsın). Sayfa üst bilgisi vaka ayarından gelir (`rapor.ust_bilgi`).
"""
import re
import shutil
import subprocess
from pathlib import Path

STIL = Path(__file__).with_name("stil") / "style.css"


class PdfHatasi(RuntimeError):
    pass


def araclar_var_mi() -> tuple[bool, str]:
    if not shutil.which("pandoc"):
        return False, "pandoc bulunamadı"
    try:
        import weasyprint  # noqa: F401
    except Exception as e:  # pragma: no cover - sistem kütüphanesi eksik olabilir
        return False, f"weasyprint yüklenemedi: {e}"
    return True, ""


def stil_yaz(hedef: str | Path, ust_bilgi: str) -> Path:
    css = STIL.read_text(encoding="utf-8").replace("{{UST_BILGI}}", ust_bilgi.replace('"', "'"))
    Path(hedef).write_text(css, encoding="utf-8")
    return Path(hedef)


def html_uret(md_yol: str | Path, html_yol: str | Path, css_yol: str | Path, baslik: str = "OSINT") -> Path:
    md_yol, html_yol = Path(md_yol), Path(html_yol)
    r = subprocess.run(["pandoc", str(md_yol), "-f", "markdown-smart+raw_html", "-t", "html5", "-s", "-N", "--toc",
                        "--toc-depth=2", "--metadata", f"pagetitle={baslik}", "--metadata", "lang=tr",
                        "-c", Path(css_yol).name, "-o", str(html_yol)], capture_output=True, text=True,
                       cwd=md_yol.parent)
    if r.returncode != 0:
        raise PdfHatasi(f"pandoc hata verdi: {r.stderr[:500]}")
    h = html_yol.read_text(encoding="utf-8")
    toc = re.search(r'<nav id="TOC".*?</nav>', h, re.S)
    if toc:
        h = h.replace(toc.group(0), "", 1)
        i = re.search(r'<h1(?! class="title")', h)
        if i:
            h = h[:i.start()] + toc.group(0) + h[i.start():]
    h = re.sub(r"<colgroup>.*?</colgroup>", "", h, flags=re.S)
    html_yol.write_text(h, encoding="utf-8")
    return html_yol


def pdf_uret(html_yol: str | Path, pdf_yol: str | Path) -> int:
    """PDF'i yazar, sayfa sayısını döner."""
    from weasyprint import HTML
    html_yol = Path(html_yol)
    belge = HTML(filename=str(html_yol), base_url=str(html_yol.parent) + "/").render()
    belge.write_pdf(str(pdf_yol))
    return len(belge.pages)
