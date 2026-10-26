"""Derinleştirme akışı.

1. Kullanıcı rapora bir soru ekler → `alt_soru` olarak kimlik (S1, S2 …) ve zaman damgasıyla saklanır.
2. Uzman katmanı bir araştırma planı önerir (alt hipotezler, kanıt ihtiyacı, kaynak/sorgu) —
   "öneri — kanıt aranacak".
3. Yeni kanıt kartları soruya bağlanarak eklenir.
4. Etkilenen bölümler yeniden yazılır, "Ek soru N" bölümü eklenir; diğer bölümler önceki sürümden alınır.
   Her cümle (alınanlar dahil) yeniden doğrulanır.
5. Yeni sürüm değişiklik günlüğüyle kaydedilir; eski sürümler silinmez ve değiştirilmez.
"""
from collections import Counter
from datetime import datetime

from medya.kanit import KanitDeposu, KanitKarti
from medya.rapor import markdown_uret, rapor_uret
from medya.rapor.motor import KART_SECIMI
from medya.uzman import arastirma_plani
from medya.uzman.saglayici import Saglayici
from medya.vaka import Vaka


class DerinlestirmeHatasi(RuntimeError):
    pass


def soru_ekle(vaka: Vaka, metin: str, saglayici: Saglayici, depo: KanitDeposu) -> dict:
    metin = (metin or "").strip()
    if len(metin) < 5:
        raise DerinlestirmeHatasi("Soru metni çok kısa")
    sorular = vaka.sorular()
    sid = f"S{len(sorular) + 1}"
    soru = {"id": sid, "metin": metin, "zaman": datetime.now().isoformat(timespec="seconds"), "durum": "plan_hazir",
            "rapor_surumu": None}
    ach = vaka.ach()
    hipotezler = [{"id": h.id, "tur": h.tur, "metin": h.metin} for h in ach.hipotezler.values()]
    sayilar = dict(Counter(k.tur for k in depo.vaka_kartlari(vaka.id)))
    soru["plan"] = arastirma_plani(saglayici, vaka.tanim, {"id": sid, "metin": metin}, hipotezler, sayilar)
    sorular.append(soru)
    vaka.sorular_kaydet(sorular)
    return soru


def degisiklik_gunlugu(eski: dict, yeni: dict) -> list[str]:
    out = [f"v{eski['surum']} → v{yeni['surum']}"]
    eb = {str(b["no"]): b for b in eski["bolumler"]}
    for b in yeni["bolumler"]:
        k = str(b["no"])
        yeni_m = {c["metin"] for c in b["cumleler"]}
        if k not in eb:
            out.append(f"Yeni bölüm: {b['baslik']} ({len(yeni_m)} cümle)")
            continue
        eski_m = {c["metin"] for c in eb[k]["cumleler"]}
        eklendi, cikti = len(yeni_m - eski_m), len(eski_m - yeni_m)
        if eklendi or cikti:
            out.append(f"{k}. {b['baslik']}: {eklendi} cümle eklendi, {cikti} cümle çıktı")
    yeni_kanit = sorted(set(yeni["kanit_ids"]) - set(eski["kanit_ids"]))
    if yeni_kanit:
        out.append("Yeni kanıt: " + ", ".join(yeni_kanit))
    yeni_soru = sorted(set(yeni.get("alt_sorular", [])) - set(eski.get("alt_sorular", [])))
    if yeni_soru:
        out.append("Yanıtlanan ek soru: " + ", ".join(yeni_soru))
    out.append(f"Doğrulayıcı: {sum(len(b['cumleler']) for b in yeni['bolumler'])} cümle yeniden doğrulandı, "
               f"{len(yeni['reddedilenler'])} cümle/satır reddedildi.")
    return out


def soru_isle(vaka: Vaka, soru_id: str, depo: KanitDeposu, saglayici: Saglayici,
              yeni_kartlar: list[KanitKarti] = (), profiller=()) -> dict:
    sorular = vaka.sorular()
    soru = next((s for s in sorular if s["id"] == soru_id), None)
    if not soru:
        raise DerinlestirmeHatasi(f"Soru bulunamadı: {soru_id}")
    onceki = vaka.rapor_oku()
    if not onceki:
        raise DerinlestirmeHatasi("Önce bir rapor sürümü üretilmeli (rapor uret)")
    for k in yeni_kartlar:
        depo.ekle(k, vaka_id=vaka.id, alt_soru=soru_id)
    turler = {k.tur for k in depo.vaka_kartlari(vaka.id, alt_soru=soru_id)}
    etkilenen = set((soru.get("plan") or {}).get("etkilenen_bolumler", [])) | {2}
    etkilenen |= {no for no, sec in KART_SECIMI.items() if sec is None or (sec & turler)}
    islenmis = [s for s in sorular if s["durum"] == "islendi" and s["id"] != soru_id] + [soru]
    sira = {s["id"]: i for i, s in enumerate(sorular)}
    islenmis.sort(key=lambda s: sira[s["id"]])
    ek_no = f"E{islenmis.index(soru) + 1}"
    yeni = rapor_uret(vaka, depo, saglayici, onceki=onceki, ek_sorular=islenmis,
                      yeniden_yazilacak={str(x) for x in etkilenen} | {ek_no}, profiller=profiller)
    yeni["surum"] = max(vaka.rapor_surumleri()) + 1
    yeni["onceki_surum"] = onceki["surum"]
    yeni["degisiklikler"] = degisiklik_gunlugu(onceki, yeni)
    kartlar = depo.vaka_sozluk(vaka.id)
    vaka.rapor_yaz(yeni, markdown_uret(yeni, kartlar))
    soru.update({"durum": "islendi", "rapor_surumu": yeni["surum"],
                 "islenme": datetime.now().isoformat(timespec="seconds")})
    vaka.sorular_kaydet(sorular)
    return yeni
