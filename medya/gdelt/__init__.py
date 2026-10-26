"""GDELT ham veri modülü: indirme, vaka sorgusu, istatistikler, manipülasyon göstergeleri ve grafikler.

Kaynak gösterimi zorunludur: GDELT verisi sunulan her çıktıda `medya.GDELT_ATTRIBUTION` yer alır.

Akış (vaka ayarı `vakalar/<vaka>/gdelt.yaml`):
    indir (masterfile/translation GKG 15 dk dosyaları, Türkçe satırlar) → tara (önbellekli) →
    istatistik → göstergeler → grafikler → `vakalar/<vaka>/gdelt/istatistik.json`
"""
import json
import os
from pathlib import Path

from medya.gdelt.gostergeler import hepsi as gostergeleri_hesapla
from medya.gdelt.istatistik import istatistik_hesapla
from medya.gdelt.sorgu import SorguSonucu, VakaSorgusu

ROOT = Path(__file__).resolve().parents[2]


def ham_dizin(ayar: dict, vaka_id: str = "") -> Path:
    """Ham veri dizini: MEDYA_GDELT_HAM ortam değişkeni > vaka ayarı `ham_veri` > data/gdelt/<vaka>/tr."""
    yol = os.environ.get("MEDYA_GDELT_HAM") or ayar.get("ham_veri") or f"data/gdelt/{vaka_id}/tr"
    yol = Path(yol)
    return yol if yol.is_absolute() else ROOT / yol


def vaka_istatistigi(ayar: dict, vaka_id: str = "", ham: str | Path | None = None) -> tuple[dict, SorguSonucu]:
    """Ham veriden istatistik + göstergeler. Ham veri yoksa FileNotFoundError."""
    d = Path(ham) if ham else ham_dizin(ayar, vaka_id)
    if not d.is_dir() or not any(d.glob("*.tsv")):
        raise FileNotFoundError(f"GDELT ham verisi bulunamadı: {d} (python -m medya gdelt indir {vaka_id})")
    s = VakaSorgusu.ayardan(ayar, d).sonuc()
    ist = istatistik_hesapla(s, ayar)
    ist["gostergeler"] = gostergeleri_hesapla(ist, s.cekirdek, ayar)
    ist["ayar"] = {k: ayar.get(k) for k in ("baslangic", "bitis", "akis", "dil", "alan_soneki", "ad_kalibi",
                                            "url_kalibi", "saat_farki")}
    return ist, s


def kaydet(ist: dict, yol: str | Path) -> Path:
    Path(yol).parent.mkdir(parents=True, exist_ok=True)
    Path(yol).write_text(json.dumps(ist, ensure_ascii=False, indent=1, default=list), encoding="utf-8")
    return Path(yol)


def yukle(yol: str | Path) -> dict | None:
    p = Path(yol)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
