"""Vaka çalışma alanı: vaka tanımı, hipotez/ACH kaydı, bağlam girdisi, ek sorular ve rapor sürümleri.

Yerleşim (kök `MEDYA_CALISMA`, varsayılan `data/vakalar_calisma/`, git dışı):
    <kök>/<vaka_id>/vaka.json        vaka tanımı (soru, olay tarihi, kapsam, etiketler …)
    <kök>/<vaka_id>/ach.json         hipotez ön kaydı + matris + kırmızı takım
    <kök>/<vaka_id>/baglam.json      bağlam protokolü girdisi
    <kök>/<vaka_id>/sorular.json     ek sorular (alt_soru) ve araştırma planları
    <kök>/<vaka_id>/raporlar/v<N>.json / v<N>.md   rapor sürümleri (eskiler silinmez)
Kanıt kartları ayrı DuckDB deposundadır (medya.kanit).
"""
import json
import os
import re
import tomllib
from datetime import date, datetime
from pathlib import Path

from medya.hipotez import ACHMatrisi

ROOT = Path(__file__).resolve().parents[1]
KUTUPHANE_DIZINI = ROOT / "vakalar"


def calisma_koku() -> Path:
    return Path(os.environ.get("MEDYA_CALISMA", ROOT / "data" / "vakalar_calisma"))


class VakaHatasi(ValueError):
    pass


def _oku(yol: Path, varsayilan):
    return json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else varsayilan


def _yaz(yol: Path, veri):
    yol.parent.mkdir(parents=True, exist_ok=True)
    tmp = yol.with_suffix(yol.suffix + ".tmp")
    tmp.write_text(json.dumps(veri, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    tmp.replace(yol)


class Vaka:
    def __init__(self, vaka_id: str, kok: Path | str | None = None):
        if not re.fullmatch(r"[a-z0-9][a-z0-9_\-]{1,60}", vaka_id):
            raise VakaHatasi("Vaka kimliği küçük harf, rakam, - ve _ içermeli (ör. ankara-2016)")
        self.id = vaka_id
        self.dizin = Path(kok or calisma_koku()) / vaka_id

    # ---------------------------------------------------------------- oluşturma
    @classmethod
    def yeni(cls, vaka_id: str, ad: str, soru: str, olay_tarihi: str, kok=None, **ek) -> "Vaka":
        v = cls(vaka_id, kok)
        if (v.dizin / "vaka.json").exists():
            raise VakaHatasi(f"{vaka_id} zaten var")
        date.fromisoformat(olay_tarihi)
        tanim = {"id": vaka_id, "ad": ad, "soru": soru, "olay_tarihi": olay_tarihi,
                 "olusturma": datetime.now().isoformat(timespec="seconds"),
                 "kapsam_onayi": None,           # analist kapsamı onaylamadan arama başlamaz
                 "kapsam": {},                    # yayın grubu -> kapsam oranı (0–1) ya da açıklama
                 "kaliplar": [], "etiketler": [], "kod_kitabi_surumu": "", "veri_anlik_goruntu": "",
                 "yer": "", "resmi_tez": ""}
        tanim.update(ek)
        _yaz(v.dizin / "vaka.json", tanim)
        return v

    @classmethod
    def liste(cls, kok=None) -> list[str]:
        k = Path(kok or calisma_koku())
        return sorted(p.parent.name for p in k.glob("*/vaka.json")) if k.exists() else []

    def var_mi(self) -> bool:
        return (self.dizin / "vaka.json").exists()

    # ---------------------------------------------------------------- tanım
    @property
    def tanim(self) -> dict:
        if not self.var_mi():
            raise VakaHatasi(f"Vaka bulunamadı: {self.id} ({self.dizin})")
        return _oku(self.dizin / "vaka.json", {})

    def tanim_guncelle(self, **alanlar) -> dict:
        t = self.tanim
        t.update(alanlar)
        _yaz(self.dizin / "vaka.json", t)
        return t

    # ---------------------------------------------------------------- ACH
    def ach(self) -> ACHMatrisi:
        return ACHMatrisi.from_dict(_oku(self.dizin / "ach.json", {}))

    def ach_kaydet(self, m: ACHMatrisi) -> None:
        _yaz(self.dizin / "ach.json", m.to_dict())

    # ---------------------------------------------------------------- bağlam
    def baglam_girdisi(self) -> dict:
        return _oku(self.dizin / "baglam.json", {})

    def baglam_girdisi_kaydet(self, g: dict) -> None:
        _yaz(self.dizin / "baglam.json", g)

    # ---------------------------------------------------------------- sorular
    def sorular(self) -> list[dict]:
        return _oku(self.dizin / "sorular.json", [])

    def sorular_kaydet(self, s: list[dict]) -> None:
        _yaz(self.dizin / "sorular.json", s)

    # ---------------------------------------------------------------- raporlar
    def rapor_surumleri(self) -> list[int]:
        d = self.dizin / "raporlar"
        return sorted(int(p.stem[1:]) for p in d.glob("v*.json")) if d.exists() else []

    def rapor_oku(self, surum: int | None = None) -> dict | None:
        s = self.rapor_surumleri()
        if not s:
            return None
        surum = surum or s[-1]
        return _oku(self.dizin / "raporlar" / f"v{surum}.json", None)

    def rapor_yaz(self, rapor: dict, markdown: str, uzerine: bool = False) -> None:
        d = self.dizin / "raporlar"
        j = d / f"v{rapor['surum']}.json"
        if j.exists() and not uzerine:
            raise VakaHatasi(f"v{rapor['surum']} zaten var; eski sürümler değiştirilmez")
        _yaz(j, rapor)
        (d / f"v{rapor['surum']}.md").write_text(markdown, encoding="utf-8")


def kutuphane_yukle(dizin: Path | str | None = None) -> list[dict]:
    """Vaka kütüphanesi (vakalar/*.toml). Kamusal rolü olmayan kişi adı içermez."""
    d = Path(dizin) if dizin else KUTUPHANE_DIZINI
    out = []
    for p in sorted(d.glob("*.toml")):
        v = tomllib.loads(p.read_text(encoding="utf-8"))
        v.setdefault("id", p.stem)
        out.append(v)
    return out


def ilk_atif_isabet_sicili(kutuphane: list[dict]) -> list[dict]:
    """İlk atıf isabet sicili: kaynak (yayın/kurum/yetkili rolü) başına, nihai sonucu belli vakalarda ilk
    atfın sonuçla uyumu. Yalnızca `nihai_sonuc.durum = "kesinlesti"` olan vakalar sayılır."""
    sicil: dict[str, dict] = {}
    for v in kutuphane:
        if (v.get("nihai_sonuc") or {}).get("durum") != "kesinlesti":
            continue
        for a in v.get("ilk_atiflar", []):
            uyum = a.get("nihai_ile_uyum", "belirsiz")
            s = sicil.setdefault(a.get("kaynak", "?"), {"kaynak": a.get("kaynak", "?"), "kaynak_turu":
                                                        a.get("kaynak_turu", ""), "n": 0, "tutarli": 0,
                                                        "kismen": 0, "celisik": 0, "belirsiz": 0})
            s["n"] += 1
            s[uyum if uyum in ("tutarli", "kismen", "celisik") else "belirsiz"] += 1
    return sorted(sicil.values(), key=lambda x: (-x["n"], x["kaynak"]))
