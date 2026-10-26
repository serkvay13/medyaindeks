"""Protokol tanımı → görev listesi; hipotez ön kaydı kilidi.

Ön kayıt mevcut hipotez modülüyle (medya.hipotez.ACHMatrisi) yapılır: küme SHA-256 ile kilitlenir ve
`on_kayit.json` olarak yazılır. Görev listesi ön kayıt olmadan üretilmez: hipotezler kanıta bakılmadan önce
yazılmalıdır (Heuer). Kilitli kümenin özeti her denetimde yeniden hesaplanır.
"""
import copy
import json
import re
from datetime import datetime
from pathlib import Path

from medya.ayar import yukle
from medya.hipotez import ACHMatrisi, set_ozeti
from medya.hipotez.kayit import matrise_kaydet
from medya.kanit.ice_aktar import SEMA_ALANLARI

PROTOKOL_YOLU = Path(__file__).with_name("protokol.yaml")
HATLAR = ("kronoloji", "aktorler", "kavram", "gdelt", "kanit_ach")
_DEGISKEN = re.compile(r"\{(\w+)\}")


class ArastirmaHatasi(RuntimeError):
    pass


def _birlestir(taban: dict, ust: dict) -> dict:
    out = copy.deepcopy(taban)
    for k, v in (ust or {}).items():
        out[k] = _birlestir(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def protokol_yukle(vaka_ayari: dict | None = None, yol: str | Path | None = None) -> dict:
    """Varsayılan protokol + vaka ayarındaki `arastirma.protokol` geçersiz kılmaları."""
    p = yukle(yol or PROTOKOL_YOLU)
    ust = ((vaka_ayari or {}).get("arastirma") or {}).get("protokol") or {}
    p = _birlestir(p, ust)
    eksik = [h for h in HATLAR if h not in p.get("hatlar", {})]
    if eksik:
        raise ArastirmaHatasi(f"Protokolde zorunlu hat eksik: {', '.join(eksik)}")
    return p


# --------------------------------------------------------------------------------
# Ön kayıt
# --------------------------------------------------------------------------------
def on_kayit_kilitle(hipotez_verisi: dict, hedef: str | Path, turler: dict | None = None) -> dict:
    """Hipotezleri ön kaydeder ve kilidi `hedef` (on_kayit.json) dosyasına yazar. Dosya varsa üzerine yazmaz."""
    hedef = Path(hedef)
    if hedef.exists():
        raise ArastirmaHatasi(f"Ön kayıt zaten var: {hedef} (hipotezler kanıttan sonra yeniden yazılamaz)")
    m = matrise_kaydet(hipotez_verisi, turler, ACHMatrisi())
    kayit = {"zaman": datetime.now().isoformat(timespec="seconds"), "ach": m.to_dict(),
             "ozet": m.on_kayit["ozet"], "ids": m.on_kayit["ids"]}
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(json.dumps(kayit, ensure_ascii=False, indent=1), encoding="utf-8")
    return kayit


def on_kayit_dogrula(kayit: dict | str | Path) -> ACHMatrisi:
    """Kilit bütünlüğü: kayıtlı küme özeti yeniden hesaplanır; değişmişse ACHHatasi."""
    if not isinstance(kayit, dict):
        kayit = json.loads(Path(kayit).read_text(encoding="utf-8"))
    m = ACHMatrisi.from_dict(kayit["ach"])          # butunluk_denetimi içerir
    ilk = [m.hipotezler[i] for i in kayit["ids"]]
    if set_ozeti(ilk) != kayit["ozet"]:
        raise ArastirmaHatasi("Ön kayıt özeti uyuşmuyor: hipotez kümesi değiştirilmiş")
    return m


# --------------------------------------------------------------------------------
# Görev listesi
# --------------------------------------------------------------------------------
def _doldur(sablon: str, degerler: dict) -> str | None:
    adlar = _DEGISKEN.findall(sablon)
    if any(not degerler.get(a) for a in adlar):
        return None
    return _DEGISKEN.sub(lambda m: str(degerler[m.group(1)]), sablon)


def gorev_listesi(vaka_ayari: dict, protokol: dict | None = None, on_kayit: dict | str | Path | None = None,
                  on_kayitsiz: bool = False) -> list[dict]:
    """Beş hat için görevler: her dil × şablon × (aktör/kavram) bir arama görevi; kart şeması alanlarıyla.
    Ön kayıt verilmezse ArastirmaHatasi (bilerek atlamak için on_kayitsiz=True; görevler işaretlenir)."""
    if on_kayit is None and not on_kayitsiz:
        raise ArastirmaHatasi("Hipotez ön kaydı yok: önce `arastirma baslat --hipotezler` ile kilitleyin "
                              "(hipotezler kart toplamadan önce yazılır)")
    if on_kayit is not None:
        on_kayit_dogrula(on_kayit)
    p = protokol or protokol_yukle(vaka_ayari)
    a = vaka_ayari.get("arastirma") or {}
    diller = list(dict.fromkeys(list(p.get("diller", [])) + list(a.get("ek_diller", []))))
    degiskenler = a.get("degiskenler", {})
    aktorler = a.get("aktorler", [])
    kavramlar = a.get("kavramlar", [])
    kavram_ceviri = a.get("kavram_ceviri", {})
    gorevler = []
    for hat in HATLAR:
        h = p["hatlar"][hat]
        if hat == "gdelt":
            for i, k in enumerate(h.get("komutlar", []), 1):
                gorevler.append({"id": f"{h['kod']}-{i:03d}", "hat": hat, "tur": "komut",
                                 "komut": k.format(vaka=vaka_ayari.get("id", "")), "ad": h["ad"]})
            continue
        n = 0
        for dil in diller:
            temel = {ad: (deger.get(dil) if isinstance(deger, dict) else deger) for ad, deger in degiskenler.items()}
            for sablon in h.get("sorgular", {}).get(dil, []):
                genisler = [{}]
                if "{aktor}" in sablon:
                    genisler = [{"aktor": x.get(dil, x.get("tr")) if isinstance(x, dict) else x} for x in aktorler]
                if "{kavram}" in sablon:
                    genisler = [{"kavram": kavram_ceviri.get(k, {}).get(dil, k if dil == "tr" else None)}
                                for k in kavramlar]
                for g in genisler:
                    sorgu = _doldur(sablon, {**temel, **g})
                    if not sorgu:
                        continue
                    n += 1
                    gorevler.append({"id": f"{h['kod']}-{n:03d}", "hat": hat, "tur": "arama", "dil": dil,
                                     "sorgu": sorgu, "kart_semasi": h.get("kart_semasi"),
                                     "alanlar": SEMA_ALANLARI.get(h.get("kart_semasi"), {}), "ad": h["ad"],
                                     "on_kayitsiz": on_kayit is None})
    return gorevler
