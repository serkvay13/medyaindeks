"""Bağlamsal ve tarihsel analiz protokolü (tasarım belgesi, "her raporun zorunlu çekirdeği").

Her adım aynı biçimde döner:
    {"adim": int, "ad": str, "durum": "tamam" | "bos_gerekceli" | "eksik", "cikti": ..., "kanit_ids": [...],
     "notlar": [...], "reddedilen": [...]}

- "eksik": adım için girdi verilmedi. Protokol tamamlanmış sayılmaz; raporun 3, 5, 11, 12. bölümleri
  üretilmez.
- "bos_gerekceli": girdi boş ama analist nedenini yazdı (ör. "bu vakada önceden işaret bulunamadı").
- Kanıt kimliği taşımayan girdi satırları çıktıya girmez, "reddedilen" listesine yazılır.

Hiçbir adım nedensellik kurmaz: zamansal çakışma ve kazanç, kasıt ya da neden kanıtı değildir.
"""
from datetime import date

import pandas as pd

ADIMLAR = {
    1: "Çok şeritli zaman çizgisi",
    2: "Neden şimdi?",
    3: "Çıkar haritası (cui bono)",
    4: "Tez soykütüğü",
    5: "Tarihsel benzerler",
    6: "Önceden işaret",
    7: "Temel varsayımlar",
    8: "Rakip hipotezler",
    9: "Şeytanın avukatı",
    10: "İzlenecek göstergeler",
}
SERITLER = ("ic_siyaset", "dis_politika", "bolgesel_catisma", "ekonomi", "yargi", "guvenlik",
            "uluslararasi_aktorler")
KAZANC_NOTU = "Kazanmak kasıt kanıtı değildir."
ZAMAN_NOTU = "Zamansal çakışma neden kanıtı değildir; kırılma noktaları yalnızca tetikleyici adaylarıdır."


def _adim(no: int, durum: str, cikti, kanit_ids=(), notlar=(), reddedilen=()) -> dict:
    return {"adim": no, "ad": ADIMLAR[no], "durum": durum, "cikti": cikti,
            "kanit_ids": sorted(set(kanit_ids)), "notlar": list(notlar), "reddedilen": list(reddedilen)}


def _tarih(x) -> date:
    return x if isinstance(x, date) else date.fromisoformat(str(x)[:10])


def _ay_kaydir(d: date, ay: int) -> date:
    y, m = divmod(d.month - 1 + ay, 12)
    yil, aydx = d.year + y, m + 1
    gun = min(d.day, [31, 29 if yil % 4 == 0 and (yil % 100 != 0 or yil % 400 == 0) else 28, 31, 30, 31, 30, 31,
                      31, 30, 31, 30, 31][aydx - 1])
    return date(yil, aydx, gun)


def _kanitli(satirlar, alan="kanit_ids"):
    iyi, kotu = [], []
    for s in satirlar or []:
        ids = s.get(alan) or ([s["kanit_id"]] if s.get("kanit_id") else [])
        if ids:
            iyi.append({**s, "kanit_ids": list(ids)})
        else:
            kotu.append({"satir": s, "neden": "kanıt kimliği yok"})
    return iyi, kotu


def _bos(no, girdi, gerekce):
    if girdi is None:
        return _adim(no, "eksik", [], notlar=["Girdi verilmedi."])
    if not girdi:
        if gerekce:
            return _adim(no, "bos_gerekceli", [], notlar=[gerekce])
        return _adim(no, "eksik", [], notlar=["Girdi boş ve gerekçe yazılmadı."])
    return None


# --------------------------------------------------------------------------------
# 1. Çok şeritli zaman çizgisi
# --------------------------------------------------------------------------------
def zaman_cizgisi(olaylar: list[dict] | None, olay_tarihi, once_ay: int = 12, sonra_ay: int = 6,
                  gerekce: str = "") -> dict:
    """olaylar: [{"tarih", "serit", "metin", "kanit_ids"}]. Pencere dışı ve kanıtsız satırlar ayrılır.
    Tek kanıta dayanan satırlar "tek_kaynak" olarak işaretlenir."""
    b = _bos(1, olaylar, gerekce)
    if b:
        return b
    ot = _tarih(olay_tarihi)
    bas, son = _ay_kaydir(ot, -once_ay), _ay_kaydir(ot, sonra_ay)
    iyi, red = _kanitli(olaylar)
    seritler = {s: [] for s in SERITLER}
    pencere_disi = 0
    for o in iyi:
        if o.get("serit") not in SERITLER:
            red.append({"satir": o, "neden": f"bilinmeyen şerit {o.get('serit')!r} ({', '.join(SERITLER)})"})
            continue
        t = _tarih(o["tarih"])
        if not bas <= t <= son:
            pencere_disi += 1
            continue
        seritler[o["serit"]].append({"tarih": t.isoformat(), "metin": o["metin"], "kanit_ids": o["kanit_ids"],
                                     "tek_kaynak": len(o["kanit_ids"]) == 1,
                                     "olaya_gore_gun": (t - ot).days})
    for s in seritler.values():
        s.sort(key=lambda x: x["tarih"])
    bos_serit = [s for s, v in seritler.items() if not v]
    notlar = [f"Pencere: {bas:%d.%m.%Y} – {son:%d.%m.%Y} (olaydan {once_ay} ay önce, {sonra_ay} ay sonra)."]
    if pencere_disi:
        notlar.append(f"{pencere_disi} satır pencere dışında kaldı.")
    if bos_serit:
        notlar.append("Kaydı olmayan şeritler: " + ", ".join(bos_serit) + " (boşluk, olay olmadığı anlamına gelmez).")
    ids = [k for v in seritler.values() for o in v for k in o["kanit_ids"]]
    return _adim(1, "tamam", {"pencere": [bas.isoformat(), son.isoformat()], "seritler": seritler}, ids, notlar, red)


# --------------------------------------------------------------------------------
# 2. "Neden şimdi?" — günlük serilerde kırılma noktaları
# --------------------------------------------------------------------------------
def neden_simdi(seriler: dict[str, pd.Series] | None, olay_tarihi, taban_gun: int = 180, pencere_gun: int = 30,
                esik_z: float = 3.0, esik_yuzdelik: float = 0.99, kanit_ids: dict[str, list] | None = None,
                gerekce: str = "") -> dict:
    """Her seri (gün indeksli) için olaydan önceki `pencere_gun` gün, ondan önceki `taban_gun` günlük
    tabana göre taranır. Değer tabanın `esik_yuzdelik` yüzdeliğini aşar VE z ≥ esik_z ise aday.
    Çıktı her aday için n (taban gün sayısı), taban ortalaması/sapması, z ve yüzdeliği söyler.
    Neden dili kullanılmaz."""
    b = _bos(2, seriler, gerekce)
    if b:
        return b
    ot = pd.Timestamp(_tarih(olay_tarihi))
    adaylar, notlar, ids = [], [ZAMAN_NOTU], []
    for ad, s in seriler.items():
        s = pd.Series(s).copy()
        s.index = pd.to_datetime(s.index)
        s = s.sort_index().astype(float)
        p_bas = ot - pd.Timedelta(days=pencere_gun)
        t_bas = p_bas - pd.Timedelta(days=taban_gun)
        taban = s[(s.index >= t_bas) & (s.index < p_bas)].dropna()
        pencere = s[(s.index >= p_bas) & (s.index <= ot)].dropna()
        n = len(taban)
        if n < 30:
            notlar.append(f"{ad}: taban yetersiz (n={n} gün < 30); kırılma aranmadı.")
            continue
        ort, sap = float(taban.mean()), float(taban.std(ddof=1))
        esik = float(taban.quantile(esik_yuzdelik))
        for t, v in pencere.items():
            z = (v - ort) / sap if sap > 0 else (float("inf") if v > ort else 0.0)
            yuzdelik = float((taban < v).mean())
            if v > esik and z >= esik_z:
                adaylar.append({"seri": ad, "tarih": t.date().isoformat(), "deger": v, "z": round(z, 2),
                                "taban_yuzdeligi": round(yuzdelik, 4), "n_taban": n,
                                "taban_ortalama": round(ort, 3), "taban_sapma": round(sap, 3),
                                "olaya_gore_gun": (t - ot).days,
                                "kanit_ids": list((kanit_ids or {}).get(ad, []))})
        ids += list((kanit_ids or {}).get(ad, []))
    seri_ids = kanit_ids or {}
    eksik_kaynak = [a for a in seriler if not seri_ids.get(a)]
    if eksik_kaynak:
        notlar.append("Kaynağı (veri_serisi kanıt kartı) bağlanmamış seriler: " + ", ".join(eksik_kaynak) + ".")
    return _adim(2, "tamam", {"adaylar": adaylar, "parametre": {"taban_gun": taban_gun, "pencere_gun": pencere_gun,
                                                                "esik_z": esik_z, "esik_yuzdelik": esik_yuzdelik}},
                 ids, notlar)


# --------------------------------------------------------------------------------
# 3. Çıkar haritası
# --------------------------------------------------------------------------------
def cui_bono(aktorler: list[dict] | None, gerekce: str = "") -> dict:
    """aktorler: [{"aktor", "once_hedefler": [{"metin","kanit_ids"}], "sonra_degisiklikler": [{"metin","tarih",
    "kanit_ids"}]}]. Kanıtsız hedef/değişiklik tabloya girmez."""
    b = _bos(3, aktorler, gerekce)
    if b:
        return b
    tablo, red, ids = [], [], []
    for a in aktorler:
        hedef, r1 = _kanitli(a.get("once_hedefler"))
        degisim, r2 = _kanitli(a.get("sonra_degisiklikler"))
        red += [{**x, "aktor": a.get("aktor")} for x in r1 + r2]
        tablo.append({"aktor": a.get("aktor", ""), "once_hedefler": hedef, "sonra_degisiklikler": degisim})
        ids += [k for x in hedef + degisim for k in x["kanit_ids"]]
    return _adim(3, "tamam", {"tablo": tablo}, ids, [KAZANC_NOTU], red)


# --------------------------------------------------------------------------------
# 4. Tez soykütüğü
# --------------------------------------------------------------------------------
def tez_soykutugu(iddialar: list[dict] | None, olay_tarihi, bulgu_tarihi=None, gerekce: str = "") -> dict:
    """iddialar: [{"tez", "kaynak", "tarih", "kanit_id", "kanit_durumu"}] — her görünüş ayrı satır.
    Tez başına ilk görünüş, olaydan gecikme, soruşturma bulgularından (bulgu_tarihi) önce mi sonra mı
    çıktığı ve yayılma sırası."""
    b = _bos(4, iddialar, gerekce)
    if b:
        return b
    ot = _tarih(olay_tarihi)
    bt = _tarih(bulgu_tarihi) if bulgu_tarihi else None
    iyi, red = _kanitli(iddialar)
    tezler: dict[str, list] = {}
    for i in iyi:
        tezler.setdefault(i["tez"], []).append(i)
    cikti = []
    for tez, gorunus in tezler.items():
        gorunus.sort(key=lambda x: (str(x["tarih"]), x.get("kaynak", "")))
        ilk = gorunus[0]
        it = _tarih(ilk["tarih"])
        cikti.append({"tez": tez, "ilk_kaynak": ilk.get("kaynak", ""), "ilk_tarih": it.isoformat(),
                      "olaydan_gecikme_gun": (it - ot).days,
                      "bulguya_gore": ("bulgu tarihi bilinmiyor" if not bt else
                                       "bulgulardan önce" if it < bt else "bulgulardan sonra"),
                      "kanit_durumu": ilk.get("kanit_durumu", "belirtilmedi"),
                      "yayilma_sirasi": [{"kaynak": g.get("kaynak", ""), "tarih": str(g["tarih"])[:10],
                                          "kanit_ids": g["kanit_ids"]} for g in gorunus],
                      "kanit_ids": sorted({k for g in gorunus for k in g["kanit_ids"]})})
    cikti.sort(key=lambda x: x["ilk_tarih"])
    notlar = [] if bt else ["Soruşturma bulgularının tarihi verilmedi; önce/sonra ayrımı yapılamadı."]
    return _adim(4, "tamam", {"tezler": cikti}, [k for c in cikti for k in c["kanit_ids"]], notlar, red)


# --------------------------------------------------------------------------------
# 5. Tarihsel benzerler
# --------------------------------------------------------------------------------
def tarihsel_benzerler(etiketler: list[str] | None, kutuphane: list[dict], en_az: float = 0.2,
                       gerekce: str = "") -> dict:
    """Vaka kütüphanesinde etiket benzerliği (Jaccard). Her benzer için ilk atıf ile nihai sonuç yan yana."""
    b = _bos(5, etiketler, gerekce)
    if b:
        return b
    e = {x.strip().lower() for x in etiketler}   # etiketler ASCII anahtar sözcüklerdir
    out = []
    for v in kutuphane:
        ve = {x.strip().lower() for x in v.get("etiketler", [])}
        if not ve:
            continue
        j = len(e & ve) / len(e | ve)
        if j >= en_az:
            out.append({"vaka_id": v.get("id"), "ad": v.get("ad"), "benzerlik": round(j, 3),
                        "ortak_etiketler": sorted(e & ve), "durum": v.get("durum", ""),
                        "ilk_atiflar": v.get("ilk_atiflar", []), "nihai_sonuc": v.get("nihai_sonuc", {}),
                        "kaynaklar": v.get("kaynaklar", [])})
    out.sort(key=lambda x: -x["benzerlik"])
    notlar = ["Benzerlik etiket örtüşmesidir; aynı faili ya da nedeni göstermez."]
    if not out:
        notlar.append("Kütüphanede eşik üstü benzer vaka bulunamadı.")
    return _adim(5, "tamam", {"benzerler": out}, [], notlar)


# --------------------------------------------------------------------------------
# 6. Önceden işaret
# --------------------------------------------------------------------------------
def erken_isaretler(isaretler: list[dict] | None, olay_tarihi, gerekce: str = "") -> dict:
    """[{"tarih", "aktor", "metin", "kanit_ids"}] — yalnızca olaydan önce tarihli ve kanıtlı olanlar."""
    b = _bos(6, isaretler, gerekce)
    if b:
        return b
    ot = _tarih(olay_tarihi)
    iyi, red = _kanitli(isaretler)
    liste = []
    for i in iyi:
        t = _tarih(i["tarih"])
        if t >= ot:
            red.append({"satir": i, "neden": "olaydan önce tarihli değil"})
            continue
        liste.append({**i, "tarih": t.isoformat(), "olaydan_once_gun": (ot - t).days})
    liste.sort(key=lambda x: x["tarih"])
    notlar = ["Örgüt söylemi doğrudan taranmaz; yalnızca araştırma kurumları ve mahkeme kayıtlarının "
              "aktardığı biçimiyle, kaynaklı olarak kullanılır."]
    return _adim(6, "tamam", {"isaretler": liste}, [k for x in liste for k in x["kanit_ids"]], notlar, red)


# --------------------------------------------------------------------------------
# 7. Temel varsayımlar
# --------------------------------------------------------------------------------
VARSAYIM_DURUMLARI = ("destekli", "sorgulanabilir", "desteksiz")


def temel_varsayimlar(varsayimlar: list[dict] | None, gerekce: str = "") -> dict:
    """[{"hipotez_id", "varsayim", "kanit_ids", "coker_ise", "durum"}]. Kanıtsız varsayım 'desteksiz' sayılır."""
    b = _bos(7, varsayimlar, gerekce)
    if b:
        return b
    tablo = []
    for v in varsayimlar:
        ids = list(v.get("kanit_ids") or [])
        durum = v.get("durum") if v.get("durum") in VARSAYIM_DURUMLARI else "sorgulanabilir"
        if not ids:
            durum = "desteksiz"
        tablo.append({"hipotez_id": v.get("hipotez_id", ""), "varsayim": v.get("varsayim", ""),
                      "coker_ise": v.get("coker_ise", ""), "durum": durum, "kanit_ids": ids})
    desteksiz = [t for t in tablo if t["durum"] == "desteksiz"]
    notlar = [f"{len(desteksiz)} varsayım kanıtla desteklenmiyor."] if desteksiz else []
    return _adim(7, "tamam", {"tablo": tablo}, [k for t in tablo for k in t["kanit_ids"]], notlar)


# --------------------------------------------------------------------------------
# 8–10. ACH'den gelen adımlar
# --------------------------------------------------------------------------------
def rakip_hipotezler_adimi(ach, kartlar) -> dict:
    if ach is None or not ach.hipotezler:
        return _adim(8, "eksik", [], notlar=["Hipotez ön kaydı yok."])
    sira = ach.sirala(kartlar)
    notlar = ["Sıralama 'en az çürütülen' sırasıdır; hiçbir hipotez doğru kabul edilmez.",
              f"Ön kayıt: {ach.on_kayit.get('zaman', '—')} · SHA-256 {ach.on_kayit.get('ozet', '')[:16]}…"]
    if any(r["sonradan_eklendi"] for r in sira):
        notlar.append("Bazı hipotezler kanıt bağlandıktan sonra eklendi (sonradan eklendi).")
    if not ach.kanit_idleri():
        return _adim(8, "eksik", {"siralama": sira}, notlar=notlar + ["Matriste kanıt yok."])
    return _adim(8, "tamam", {"siralama": sira, "guven_onerisi": ach.guven_onerisi(kartlar)},
                 [k for k in ach.kanit_idleri() if k in kartlar], notlar)


def kirmizi_takim_adimi(ach, kartlar) -> dict:
    if ach is None or not ach.hipotezler:
        return _adim(9, "eksik", [], notlar=["Hipotez ön kaydı yok."])
    kt = ach.onde_gelen_icin_kirmizi_takim(kartlar)
    if not kt:
        return _adim(9, "eksik", [], notlar=["Öne çıkan hipotez için kırmızı takım geçişi yapılmadı."])
    ids = [k for a in kt.karsi_argumanlar for k in a.get("kanit_ids", [])]
    return _adim(9, "tamam", kt.to_dict(), ids)


def izlenecek_gostergeler(ach) -> dict:
    if ach is None or not ach.hipotezler:
        return _adim(10, "eksik", [], notlar=["Hipotez ön kaydı yok."])
    g = ach.izlenecek_gostergeler()
    eksik = [h for h in ach.hipotezler.values() if not (h.destekleyici_gostergeler or h.curutucu_gostergeler)]
    notlar = [f"Göstergesi tanımlanmamış hipotezler: {', '.join(h.id for h in eksik)}."] if eksik else []
    return _adim(10, "tamam" if g and not eksik else "eksik", {"gostergeler": g}, notlar=notlar)


# --------------------------------------------------------------------------------
def protokol_calistir(girdi: dict, olay_tarihi, ach=None, kartlar=None, kutuphane=None) -> dict:
    """Bağlam girdisi (baglam.json) ile on adımı çalıştırır.

    girdi anahtarları: zaman_cizgisi, seriler ({ad: {tarih: değer}}), seri_kanitlari, cui_bono, iddialar,
    bulgu_tarihi, etiketler, erken_isaretler, varsayimlar, once_ay, sonra_ay, gerekceler ({adım_no: metin}).
    """
    kartlar = kartlar or {}
    g = girdi or {}
    ger = {int(k): v for k, v in (g.get("gerekceler") or {}).items()}
    seriler = g.get("seriler")
    if seriler is not None:
        seriler = {ad: pd.Series(v) for ad, v in seriler.items()}
    adimlar = [
        zaman_cizgisi(g.get("zaman_cizgisi"), olay_tarihi, g.get("once_ay", 12), g.get("sonra_ay", 6), ger.get(1, "")),
        neden_simdi(seriler, olay_tarihi, kanit_ids=g.get("seri_kanitlari"), gerekce=ger.get(2, "")),
        cui_bono(g.get("cui_bono"), ger.get(3, "")),
        tez_soykutugu(g.get("iddialar"), olay_tarihi, g.get("bulgu_tarihi"), ger.get(4, "")),
        tarihsel_benzerler(g.get("etiketler"), kutuphane or [], gerekce=ger.get(5, "")),
        erken_isaretler(g.get("erken_isaretler"), olay_tarihi, ger.get(6, "")),
        temel_varsayimlar(g.get("varsayimlar"), ger.get(7, "")),
        rakip_hipotezler_adimi(ach, kartlar),
        kirmizi_takim_adimi(ach, kartlar),
        izlenecek_gostergeler(ach),
    ]
    # Var olmayan kanıt kimliği taşıyan adımlar işaretlenir
    for a in adimlar:
        yok = [k for k in a["kanit_ids"] if kartlar and k not in kartlar]
        if yok:
            a["notlar"].append(f"Depoda bulunmayan kanıt kimlikleri: {', '.join(yok)}.")
    return {"olay_tarihi": str(olay_tarihi), "adimlar": adimlar,
            "tamamlandi": all(a["durum"] != "eksik" for a in adimlar),
            "eksik_adimlar": [a["adim"] for a in adimlar if a["durum"] == "eksik"]}
