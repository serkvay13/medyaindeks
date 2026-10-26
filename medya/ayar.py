"""Ayar dosyası okuyucu: YAML (.yaml/.yml) ya da JSON. YAML için PyYAML gerekir (requirements-platform.txt)."""
import json
from pathlib import Path


class AyarHatasi(ValueError):
    pass


def yukle(yol: str | Path, varsayilan=None):
    yol = Path(yol)
    if not yol.exists():
        if varsayilan is not None:
            return varsayilan
        raise AyarHatasi(f"Ayar dosyası bulunamadı: {yol}")
    metin = yol.read_text(encoding="utf-8")
    if yol.suffix in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError as e:   # pragma: no cover
            raise AyarHatasi("YAML ayarı için PyYAML gerekli: pip install pyyaml") from e
        return yaml.safe_load(metin) or {}
    return json.loads(metin)


def ilk_bulunan(dizin: str | Path, ad: str) -> Path | None:
    """<ad>.yaml, <ad>.yml ya da <ad>.json — ilk bulunanı döner."""
    for uz in (".yaml", ".yml", ".json"):
        p = Path(dizin) / f"{ad}{uz}"
        if p.exists():
            return p
    return None
