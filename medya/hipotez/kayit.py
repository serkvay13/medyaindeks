"""Araştırma dosyasındaki hipotez kaydını (hipotezler.json) ACH ön kaydına çevirir.

Beklenen biçim: {"on_kayit_zaman_damgasi": "...", "hipotezler": [{"id","ad","tanim"}...],
"sonradan_eklenen_rafinasyonlar": [{"id","ust","ad","tanim","zaman_damgasi"}...]}.
Ana hipotezler ön kayda girer (küme SHA-256 ile kilitlenir); rafinasyonlar kilitten sonra eklenmiş sayılır ve
"sonradan eklendi" işaretlenir. Hipotezler nötr kodlarla (H1…Hn) anılır; metin kişiye/analiste atıf taşımaz.
"""
from medya.hipotez.ach import ACHMatrisi, Hipotez


def hipotez_metni(h: dict) -> str:
    ad, tanim = (h.get("ad") or "").strip(), (h.get("tanim") or h.get("metin") or "").strip()
    return f"{ad}: {tanim}" if ad and tanim else (ad or tanim)


def matrise_kaydet(veri: dict, turler: dict | None = None, m: ACHMatrisi | None = None) -> ACHMatrisi:
    turler = turler or {}
    m = m or ACHMatrisi()
    ana = [Hipotez(id=h["id"], metin=hipotez_metni(h), tur=turler.get(h["id"], "diger"))
           for h in veri.get("hipotezler", [])]
    m.on_kaydet(ana)
    if veri.get("on_kayit_zaman_damgasi"):
        m.on_kayit["kaynak_zaman_damgasi"] = veri["on_kayit_zaman_damgasi"]
    rafine = veri.get("sonradan_eklenen_rafinasyonlar", [])
    if rafine:
        # Rafinasyonlar kanıt görüldükten sonra yazıldı: kilit, ilk rafinasyonun zaman damgasıyla kapanır
        m.kilit_zamani = m.kilit_zamani or rafine[0].get("zaman_damgasi") or m.on_kayit["zaman"]
        for h in rafine:
            eklenen = m.ekle(Hipotez(id=h["id"], metin=hipotez_metni(h), tur=turler.get(h["id"], "diger")))
            eklenen.sonradan_eklendi = True
    return m
