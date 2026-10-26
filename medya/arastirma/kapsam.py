"""Kapsam denetçisi: rapor üretilmeden önce beş hattın her biri için asgari kanıt var mı?

Hat ataması: kartın `hat:<ad>` etiketi varsa o; yoksa şemasından (KR → kronoloji, R → aktörler, RD → kavram,
K → kanıt/ACH). Eksikler raporlanır; `kati=True` ise rapor üretimi durdurulur.
"""
import re
from dataclasses import dataclass, field
from pathlib import Path

from medya.arastirma.gorevler import ArastirmaHatasi, HATLAR, protokol_yukle
from medya.metin import fold_tr

SEMA_HAT = {"KR": "kronoloji", "R": "aktorler", "RD": "kavram", "K": "kanit_ach"}


@dataclass
class KapsamRaporu:
    hatlar: list = field(default_factory=list)       # [{"hat", "ad", "olcumler", "eksikler", "tamam"}]

    @property
    def tamam(self) -> bool:
        return all(h["tamam"] for h in self.hatlar)

    @property
    def eksikler(self) -> list[str]:
        return [f"({h['kod']}) {h['ad']}: {e}" for h in self.hatlar for e in h["eksikler"]]

    def markdown(self) -> str:
        sat = ["| Hat | Ölçüm | Durum |", "|---|---|---|"]
        for h in self.hatlar:
            olc = " · ".join(f"{k} {v}" for k, v in h["olcumler"].items())
            sat.append(f"| ({h['kod']}) {h['ad']} | {olc} | {'tamam' if h['tamam'] else 'eksik: ' + '; '.join(h['eksikler'])} |")
        return "\n".join(sat)


def _hat(k) -> str | None:
    for e in k.etiketler:
        if e.startswith("hat:"):
            return e[4:]
    return SEMA_HAT.get(k.ek.get("_sema"))


def kapsam_denetle(kartlar: dict, olay_tarihi: str, protokol: dict | None = None, vaka_ayari: dict | None = None,
                   gdelt_ist: dict | None = None, on_kayit=None, ach_satiri: int = 0,
                   kavram_dosyalari: list | None = None, kati: bool = False) -> KapsamRaporu:
    """kartlar: görünen kimlik -> KanitKarti. on_kayit: ACHMatrisi (ön kayıtlı) ya da None."""
    p = protokol or protokol_yukle(vaka_ayari)
    esik_ust = ((vaka_ayari or {}).get("arastirma") or {}).get("esikler", {})
    gruplar: dict[str, list] = {h: [] for h in HATLAR}
    for k in kartlar.values():
        h = _hat(k)
        if h in gruplar:
            gruplar[h].append(k)
    rapor = KapsamRaporu()
    for hat in HATLAR:
        tanim = p["hatlar"][hat]
        esik = {**tanim.get("esikler", {}), **esik_ust.get(hat, {})}
        ks = gruplar[hat]
        olc, eksik = {}, []
        if hat != "gdelt":
            olc["kart"] = len(ks)
            if len(ks) < esik.get("asgari_kart", 0):
                eksik.append(f"{len(ks)} kart < asgari {esik['asgari_kart']}")
        if hat == "kronoloji":
            gun = [k for k in ks if k.olay_tarihi == olay_tarihi]
            olc["olay günü satırı"] = len(gun)
            olc["çelişki işaretli"] = sum(1 for k in ks if k.celiski)
            olc["saatli satır"] = sum(1 for k in gun if re.match(r"\d{1,2}[:.]\d{2}", k.saat or ""))
            if len(gun) < esik.get("olay_gunu_satir", 0):
                eksik.append(f"olay günü {len(gun)} satır < eşik {esik['olay_gunu_satir']}")
        elif hat == "aktorler":
            temalar = tanim.get("zorunlu_temalar", {})
            if isinstance(temalar, list):
                temalar = {t: t for t in temalar}
            for ad, kalip in temalar.items():
                n = sum(1 for k in ks if re.search(kalip, fold_tr(" ".join(
                    [k.ek.get("tema", ""), k.ek.get("aktor", ""), k.ozet]))))
                olc[ad] = n
                if not n:
                    eksik.append(f"zorunlu tema için kart yok: {ad}")
        elif hat == "kavram":
            dosyalar = [Path(d) for d in (kavram_dosyalari or [])]
            olc["kavram notu"] = sum(1 for d in dosyalar if d.exists())
            if tanim.get("kavram_dosyasi_gerekli") and not olc["kavram notu"]:
                eksik.append("akademik kavram notu (literatür künyeli) yok")
        elif hat == "gdelt":
            n = (gdelt_ist or {}).get("tekil_url", 0)
            olc["çekirdek haber"] = n
            if not gdelt_ist:
                eksik.append("GDELT istatistiği yok (python -m medya gdelt istatistik <vaka>)")
            elif n < esik.get("asgari_cekirdek", 0):
                eksik.append(f"çekirdek küme {n} < asgari {esik['asgari_cekirdek']}")
        elif hat == "kanit_ach":
            olc["ACH satırı"] = ach_satiri
            olc["ön kayıt"] = "var" if on_kayit is not None and on_kayit.on_kayit else "yok"
            if olc["ön kayıt"] == "yok":
                eksik.append("hipotez ön kaydı (SHA-256 kilidi) yok")
            if ach_satiri < esik.get("asgari_ach_satiri", 0):
                eksik.append(f"ACH matrisi {ach_satiri} satır < asgari {esik['asgari_ach_satiri']}")
        rapor.hatlar.append({"hat": hat, "kod": tanim["kod"], "ad": tanim["ad"], "olcumler": olc, "eksikler": eksik,
                             "tamam": not eksik})
    if kati and not rapor.tamam:
        raise ArastirmaHatasi("Kapsam eksik, rapor üretilmedi: " + " | ".join(rapor.eksikler))
    return rapor
