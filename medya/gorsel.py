"""Görsel dil: MK renk sözlüğü app.py'den AST ile okunur (app.py içe aktarılmaz; arayüzü çalıştırırdı).
Okunamazsa nötr renklere düşülür."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTR = {"ink": "#1f2328", "muted": "#59636e", "line": "#d0d7de", "line_strong": "#afb8c1", "paper": "#f6f8fa",
        "surface": "#ffffff", "surface_deep": "#eaeef2", "red": "#a40e26", "cyan": "#0a6c74", "amber": "#9a6700",
        "amber_text": "#7d4e00", "green": "#1a7f37"}


def mk_renkleri() -> dict:
    try:
        agac = ast.parse((ROOT / "app.py").read_text(encoding="utf-8"))
        for dugum in agac.body:
            if isinstance(dugum, ast.Assign) and any(getattr(t, "id", None) == "MK" for t in dugum.targets):
                renk = ast.literal_eval(dugum.value)
                if isinstance(renk, dict) and "ink" in renk:
                    return renk
    except Exception:
        pass
    return dict(NOTR)
