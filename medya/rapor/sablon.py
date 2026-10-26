"""Var olan (elle derlenmiş) bir rapordan çevrimdışı anlatı dosyaları çıkarır.

Raporun deterministik parçaları (kapak, kaynak tabanı tablosu, `<div class="tbl-…">` tabloları, çelişki kutusu,
grafik yolları) yer tutucuyla değiştirilir; geri kalan metin bölüm bölüm `anlati/<sıra>_<kimlik>.md`
dosyalarına yazılır. Böylece rapor motoru aynı anlatıyı koddan üretilen güncel tablolarla yeniden kurar.

    python -m medya vaka-anlati-cikar <referans.md> <vaka>
"""
import re
from pathlib import Path

from medya.rapor.yapi import BOLUMLER, DIV_SINIFI, dosya_adi

_SINIF_YER = {v: k for k, v in DIV_SINIFI.items()}


class SablonHatasi(ValueError):
    pass


def anlati_cikar(referans: str, grafikler: dict[str, str] | None = None) -> dict[str, str]:
    """Referans Markdown → {bolum_id: gövde}. Bölüm sırası ve sayısı yapi.BOLUMLER ile aynı olmalı.
    grafikler: {"gunluk": "gdelt_gunluk.png", …} resim dosya adının sonuyla eşleştirilir."""
    metin = referans
    # deterministik bloklar
    metin = re.sub(r'<div class="(tbl-[a-z_]+)">\n\n.*?\n</div>',
                   lambda m: "{{" + _SINIF_YER[m.group(1)] + "}}" if m.group(1) in _SINIF_YER else m.group(0),
                   metin, flags=re.S)
    metin = re.sub(r'<div class="box">\n\n.*?\n\n</div>', "{{CELISKI_TABLOSU}}", metin, count=1, flags=re.S)
    metin = re.sub(r"\| Dosya \| Kart/satır \|.*?\| URL düzeyinde sayım; bkz\. Ek B \|", "{{KAYNAK_TABANI}}", metin,
                   count=1, flags=re.S)
    for ad, dosya in (grafikler or {}).items():
        metin = re.sub(r"(!\[[^\]]*\]\()[^)]*" + re.escape(dosya) + r"\)", r"\1{{GRAFIK:" + ad + "}})", metin)
    # kapak: ilk H1 bölümüne kadar
    ilk = re.search(r"^# ", metin, re.M)
    if not ilk:
        raise SablonHatasi("Referansta bölüm başlığı (# …) yok")
    govdeler = re.split(r"^# .*\n", metin[ilk.start():], flags=re.M)[1:]
    basliklar = re.findall(r"^# .*$", metin[ilk.start():], flags=re.M)
    if len(govdeler) != len(BOLUMLER):
        raise SablonHatasi(f"Referansta {len(govdeler)} bölüm var; yapı {len(BOLUMLER)} bölüm bekliyor: {basliklar}")
    return {b["id"]: g for b, g in zip(BOLUMLER, govdeler)} | {"_basliklar": basliklar}


def anlati_yaz(govdeler: dict, dizin: str | Path) -> list[Path]:
    dizin = Path(dizin)
    dizin.mkdir(parents=True, exist_ok=True)
    out = []
    for b in BOLUMLER:
        p = dizin / f"{dosya_adi(b['id'])}.md"
        p.write_text(govdeler[b["id"]], encoding="utf-8")
        out.append(p)
    return out
