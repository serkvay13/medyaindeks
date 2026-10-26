"""Rapor motoru: tasarım belgesindeki 14 bölümlük tabloyu doldurur.

Akış: bölüm için kart seçimi → uzman katmanı (bolum_yaz) → doğrulayıcı → yalnızca geçen cümleler.
Tablolar (zaman çizgisi, çıkar haritası, ACH) koddan basılır; içlerindeki olgu satırları da doğrulayıcıdan
geçer. Rapor kurulmadan önce tutulan tüm cümleler yeniden doğrulanır (`kesin_dogrula`); biri bile geçmezse
rapor kurulmaz.

Durum: taslak → dogrulandi → onaylandi. `onaylandi` için onaylayanın adı ve tarih zorunludur.
"""
import subprocess
from datetime import date, datetime
from pathlib import Path

import medya
from medya.baglam import KAZANC_NOTU, protokol_calistir
from medya.dogrulayici import Cumle, dogrula, kesin_dogrula
from medya.dogrulayici.model import TUR_ETIKETI
from medya.hipotez import agirlik
from medya.kanit import KanitDeposu, KanitKarti
from medya.kanit.kart import BILGI_DERECELERI, KAYNAK_DERECELERI
from medya.metin import tarih_tr
from medya.uzman import bolum_yaz
from medya.uzman.saglayici import Saglayici
from medya.vaka import Vaka, kutuphane_yukle

ROOT = Path(__file__).resolve().parents[2]
DURUMLAR = ("taslak", "dogrulandi", "onaylandi")
DURUM_ETIKETI = {"taslak": "Taslak", "dogrulandi": "Doğrulandı", "onaylandi": "Onaylandı"}

# (no, başlık, cevapladığı soru) — tasarım belgesindeki tablo
BOLUMLER = [
    (1, "Soru ve kapsam", "Tam olarak ne soruldu, hangi dönem ve kimler?"),
    (2, "Özet bulgular", "Cevabın kısası"),
    (3, "Olayın gelişimi", "Ne zaman ne oldu?"),
    (4, "Aktörler", "Kimler rol aldı, nasıl anıldı?"),
    (5, "Bağlantılar", "Aktörler birbirine ve kamuoyunca bilinen başka kişilere nasıl bağlı?"),
    (6, "Resmi anlatı", "Hükümet ve kurumlar ne dedi, anlatı zamanla değişti mi?"),
    (7, "Ana akım medyanın senaryosu", "Medya grupları olayı hangi hikâyeyle anlattı?"),
    (8, "Senaryonun zayıf noktaları", "Hikâyenin neresi tutmuyor?"),
    (9, "Manipülasyon göstergeleri", "Sessizlik, eşzamanlı söylem, gündem kaydırma var mı?"),
    (10, "Suç isnatları", "Kim kime hangi suçu, hangi kanıtla isnat etti; hukuki durum ne?"),
    (11, "İsnadın olası amaçları", "İsnat neden yapılmış olabilir, neye ulaşmak istenmiş olabilir?"),
    (12, "Olayın kök nedenleri", "Olay neden olmuş olabilir, gerçekte ne yaşanmış olabilir?"),
    (13, "İstatistiksel bağlam", "Olayla ilgili göstergeler ne diyor?"),
    (14, "Yöntem, kapsam, kaynaklar", "Rapor neye dayanıyor?"),
]
BASLIK = {no: b for no, b, _ in BOLUMLER}
TUM_TURLER = None
# Uzman katmanının yazdığı bölümler ve kart seçimi (tür kümesi; None = tümü). "bolum:N" etiketli kart
# türünden bağımsız olarak o bölüme girer.
KART_SECIMI = {
    3: {"olay_kaydi", "haber", "resmi_aciklama", "mahkeme_kaydi", "uluslararasi_basin", "arsiv"},
    4: {"haber", "resmi_aciklama", "uluslararasi_basin", "arastirma_kurumu", "mahkeme_kaydi"},
    6: {"resmi_aciklama"},
    7: {"haber"},
    8: TUM_TURLER,
    10: {"mahkeme_kaydi", "resmi_aciklama", "haber"},
    11: {"mahkeme_kaydi", "arastirma_kurumu", "uluslararasi_basin", "uluslararasi_kurum", "resmi_aciklama", "haber"},
    12: {"arastirma_kurumu", "uluslararasi_kurum", "uluslararasi_basin", "mahkeme_kaydi", "olay_kaydi",
         "veri_serisi", "haber", "resmi_aciklama"},
    13: {"veri_serisi"},
}
ACH_BOLUMLERI = {8, 11, 12}
# Bağlam protokolü tamamlanmadan üretilmeyen bölümler (tasarım belgesi)
PROTOKOL_GEREKTIREN = {3, 5, 11, 12}
BOLUM_KART_SINIRI = 25
GDELT_SINIR_NOTU = ("Kapsam GDELT'in taradığı sitelerle sınırlıdır; tam sayım değil, geniş bir örneklemdir. "
                    "GDELT tam metin saklamaz; ton ve kişi alanları Türkçede zayıftır.")


class RaporHatasi(RuntimeError):
    pass


def git_commit() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True,
                           timeout=5)
        return r.stdout.strip() or "bilinmiyor"
    except Exception:
        return "bilinmiyor"


def _kart_sec(no: int, kartlar: list[KanitKarti]) -> list[KanitKarti]:
    turler = KART_SECIMI.get(no, set())
    secili = [k for k in kartlar if (turler is None or k.tur in turler) or f"bolum:{no}" in k.etiketler]
    secili.sort(key=lambda k: (-agirlik(k), k.olay_tarihi or k.yayin_tarihi or "", k.kanit_id))
    return secili[:BOLUM_KART_SINIRI]


def _ach_ozeti(ach, kartlar: dict) -> dict:
    if not ach or not ach.hipotezler:
        return {}
    sira = ach.sirala(kartlar)
    return {"siralama": sira, "kanit_ids": [k for k in ach.kanit_idleri() if k in kartlar],
            "guven_onerisi": ach.guven_onerisi(kartlar) if ach.kanit_idleri() else "belirlenemedi",
            "matris": [{"kanit_id": k, "hipotez_id": h, **v} for (k, h), v in ach.hucreler.items()],
            "not": "Sıralama en az çürütülen sırasıdır; hiçbir hipotez doğru kabul edilmez."}


def _ek_adlar(ach, profiller=()) -> str:
    """Değerlendirme ve açık sorularda adların aranabileceği ek metin: hipotez kimlik ve metinleri."""
    parcalar = []
    if ach:
        parcalar += [f"{h.id} {h.metin}" for h in ach.hipotezler.values()]
    parcalar += [p.aktor for p in profiller]
    return "\n".join(parcalar)


def _cumle_md(c: dict, kartlar: dict) -> str:
    etiket = TUR_ETIKETI.get(c["tur"], c["tur"])
    if c["tur"] == "degerlendirme" and c.get("guven"):
        etiket += f" · {c['guven']}"
    kanit = ", ".join(f"`{k}` ({kartlar[k].derece})" if k in kartlar else f"`{k}`" for k in c.get("kanit_ids", []))
    ek = f" — kanıt: {kanit}" if kanit else ""
    if c.get("dayanak"):
        ek += f" — dayanak: {', '.join(c['dayanak'])}"
    return f"- **[{etiket}]** {c['metin']}{ek}"


# --------------------------------------------------------------------------------
# Tablo satırlarının doğrulanması
# --------------------------------------------------------------------------------
def _satir_dogrula(metin: str, kanit_ids: list, kartlar: dict, etiket: str, red: list) -> bool:
    c = Cumle("olgu", metin, kanit_ids, id=etiket)
    s = dogrula([c], kartlar)
    if s.red:
        red += [{"bolum": etiket.split(":")[0], **r.to_dict()} for r in s.red]
        return False
    return True


def _zaman_tablosu(adim: dict, kartlar: dict, red: list) -> str:
    if adim["durum"] != "tamam":
        return ""
    govde = []
    for serit, olaylar in adim["cikti"]["seritler"].items():
        for o in olaylar:
            if not _satir_dogrula(o["metin"], o["kanit_ids"], kartlar, f"3:zaman:{o['tarih']}", red):
                continue
            govde.append((o["tarih"], f"| {tarih_tr(o['tarih'])} | {serit} | {o['metin']} | "
                                      f"{', '.join('`' + k + '`' for k in o['kanit_ids'])} | "
                                      f"{'tek kaynak' if o['tek_kaynak'] else ''} |"))
    if not govde:
        return ""
    govde.sort(key=lambda x: x[0])
    return "\n".join(["| Tarih | Şerit | Olay | Kanıt | Not |", "|---|---|---|---|---|"] + [g for _, g in govde])


def _cui_bono_tablosu(adim: dict, kartlar: dict, red: list) -> str:
    if adim["durum"] != "tamam":
        return ""
    sat = ["| Aktör | Olay öncesi hedefler | Olay sonrası değişiklikler |", "|---|---|---|"]
    for r in adim["cikti"]["tablo"]:
        h = [x for x in r["once_hedefler"] if _satir_dogrula(x["metin"], x["kanit_ids"], kartlar, "11:cui-bono", red)]
        d = [x for x in r["sonra_degisiklikler"]
             if _satir_dogrula(x["metin"], x["kanit_ids"], kartlar, "11:cui-bono", red)]
        hm = "<br>".join(f"{x['metin']} ({', '.join(x['kanit_ids'])})" for x in h) or "—"
        dm = "<br>".join(f"{x['metin']} ({', '.join(x['kanit_ids'])})" for x in d) or "—"
        sat.append(f"| {r['aktor']} | {hm} | {dm} |")
    return "\n".join(sat) + f"\n\n*{KAZANC_NOTU}*"


def _soykutugu_tablosu(adim: dict) -> str:
    if adim["durum"] != "tamam":
        return ""
    sat = ["| Tez | İlk kaynak | İlk tarih | Olaydan gecikme (gün) | Bulgulara göre | Kanıt durumu | Yayılma |",
           "|---|---|---|---|---|---|---|"]
    for t in adim["cikti"]["tezler"]:
        yay = " → ".join(y["kaynak"] for y in t["yayilma_sirasi"])
        sat.append(f"| {t['tez']} | {t['ilk_kaynak']} | {tarih_tr(t['ilk_tarih'])} | {t['olaydan_gecikme_gun']} | "
                   f"{t['bulguya_gore']} | {t['kanit_durumu']} | {yay} |")
    return "\n".join(sat)


def _siralama_tablosu(ach_oz: dict) -> str:
    if not ach_oz:
        return ""
    sat = ["| Sıra | Hipotez | Tür | Ağırlıklı çelişki | Çelişen kanıt | Tanısal tutarlılık | Not |",
           "|---|---|---|---|---|---|---|"]
    for r in ach_oz["siralama"]:
        sat.append(f"| {r['sira']} | {r['hipotez_id']}: {r['metin']} | {r['tur']} | {r['agirlikli_celiski']:.2f} | "
                   f"{r['celisen_kanit']} | {r['tanisal_tutarlilik']:.2f} | "
                   f"{'; '.join(x for x in ('sonradan eklendi' if r['sonradan_eklendi'] else '', 'az kanıtla sınandı' if r.get('az_kanit') else '') if x)} |")
    return ("\n".join(sat) + "\n\n*Sıralama en az çürütülenden en çok çürütülene doğrudur (Heuer). Öne çıkan "
            "hipotez de bir çıkarımdır; hiçbir hipotez doğru kabul edilmez. Ağırlık = kaynak × bilgi derecesi.*")


def _baglam_ek_md(baglam: dict) -> str:
    """12. bölüm için protokol adımları 5, 6, 7, 9, 10."""
    a = {x["adim"]: x for x in baglam["adimlar"]}
    out = []
    b = a[5]
    if b["durum"] == "tamam" and b["cikti"]["benzerler"]:
        out.append("**Tarihsel benzerler** (etiket benzerliği; aynı faili ya da nedeni göstermez)\n")
        out.append("| Vaka | Benzerlik | Ortak etiketler | Nihai durum |\n|---|---|---|---|")
        for x in b["cikti"]["benzerler"]:
            out.append(f"| {x['ad']} | {x['benzerlik']:.2f} | {', '.join(x['ortak_etiketler'])} | "
                       f"{(x['nihai_sonuc'] or {}).get('durum', '—')} |")
    b = a[6]
    if b["durum"] == "tamam" and b["cikti"]["isaretler"]:
        out.append("\n**Önceden işaret** (yalnızca olaydan önce tarihli ve kaynaklı)\n")
        for x in b["cikti"]["isaretler"]:
            out.append(f"- {tarih_tr(x['tarih'])} · {x.get('aktor', '')}: {x['metin']} "
                       f"({', '.join(x['kanit_ids'])})")
    b = a[7]
    if b["durum"] == "tamam" and b["cikti"]["tablo"]:
        out.append("\n**Temel varsayımlar** (analist girdisi)\n")
        out.append("| Hipotez | Varsayım | Durum | Çökerse | Kanıt |\n|---|---|---|---|---|")
        for x in b["cikti"]["tablo"]:
            out.append(f"| {x['hipotez_id']} | {x['varsayim']} | {x['durum']} | {x['coker_ise']} | "
                       f"{', '.join(x['kanit_ids']) or '—'} |")
    b = a[9]
    if b["durum"] == "tamam":
        out.append(f"\n**Şeytanın avukatı** ({b['cikti']['yapan']}, hipotez {b['cikti']['hipotez_id']})\n")
        for x in b["cikti"]["karsi_argumanlar"]:
            out.append(f"- Karşı argüman: {x['arguman']}" + (f" — yanıt: {x['yanit']}" if x.get("yanit") else
                                                             " — yanıt: *henüz yazılmadı*"))
    b = a[10]
    if b["cikti"] and b["cikti"].get("gostergeler"):
        out.append("\n**İzlenecek göstergeler**\n")
        for x in b["cikti"]["gostergeler"]:
            out.append(f"- {x['hipotez_id']} ({x['yon']}): {x['gosterge']}")
    return "\n".join(out)


def _neden_simdi_md(adim: dict) -> str:
    if adim["durum"] != "tamam":
        return ""
    ad = adim["cikti"]["adaylar"]
    p = adim["cikti"]["parametre"]
    bas = (f"**Neden şimdi?** Olaydan önceki {p['pencere_gun']} gün, ondan önceki {p['taban_gun']} günlük tabana "
           f"göre tarandı (eşik: z ≥ {p['esik_z']} ve taban yüzdeliği > {p['esik_yuzdelik']}).")
    if not ad:
        return bas + " Eşik üstü kırılma bulunmadı.\n\n*" + adim["notlar"][0] + "*"
    sat = [bas, "", "| Seri | Tarih | Değer | z | Taban yüzdeliği | n (taban gün) | Taban ort. ± sapma |",
           "|---|---|---|---|---|---|---|"]
    for x in ad:
        sat.append(f"| {x['seri']} | {tarih_tr(x['tarih'])} | {x['deger']:g} | {x['z']} | {x['taban_yuzdeligi']} | "
                   f"{x['n_taban']} | {x['taban_ortalama']} ± {x['taban_sapma']} |")
    return "\n".join(sat) + "\n\n*" + adim["notlar"][0] + "*"


# --------------------------------------------------------------------------------
def rapor_uret(vaka: Vaka, depo: KanitDeposu, saglayici: Saglayici, onceki: dict | None = None,
               ek_sorular: list[dict] | None = None, yeniden_yazilacak: set | None = None,
               profiller=()) -> dict:
    """Yeni rapor sürümü kurar (kaydetmez). `onceki` verilir ve `yeniden_yazilacak` bölüm kümesi
    belirtilirse, kümede olmayan bölümlerin cümleleri önceki sürümden alınır — ama hepsi yeniden doğrulanır."""
    tanim = vaka.tanim
    kart_listesi = depo.vaka_kartlari(vaka.id)
    kartlar = {k.kanit_id: k for k in kart_listesi}
    alt_harita = depo.alt_soru_haritasi(vaka.id)
    ach = vaka.ach()
    ach_oz = _ach_ozeti(ach, kartlar)
    baglam = protokol_calistir(vaka.baglam_girdisi(), tanim["olay_tarihi"], ach=ach, kartlar=kartlar,
                               kutuphane=kutuphane_yukle())
    adim = {a["adim"]: a for a in baglam["adimlar"]}
    ek_adlar = _ek_adlar(ach, profiller)
    eksik: list[str] = []
    red: list[dict] = []
    bolumler = []
    onceki_bolum = {str(b["no"]): b for b in (onceki or {}).get("bolumler", [])}

    def _yaz(no, bolum_kartlari, ach_kullan=False, baglam_oz=None, soru=None):
        anahtar = str(no)
        if onceki is not None and yeniden_yazilacak is not None and anahtar not in {str(x) for x in yeniden_yazilacak} \
                and anahtar in onceki_bolum:
            cs = [Cumle.from_dict(c) for c in onceki_bolum[anahtar]["cumleler"]]
            s = dogrula(cs, kartlar, ek_adlar=ek_adlar)
        else:
            s = bolum_yaz(saglayici, {"no": no, "baslik": BASLIK.get(no, f"Ek soru {no}"),
                                      "soru": soru or dict((n, q) for n, _, q in BOLUMLER).get(no, "")},
                          bolum_kartlari, ach_oz if ach_kullan else None, baglam_oz, ek_adlar)
        red.extend({"bolum": anahtar, **r.to_dict()} for r in s.red)
        return [c.to_dict() for c in s.kabul]

    protokol_tamam = baglam["tamamlandi"]
    if not protokol_tamam:
        eksik.append("Bağlam protokolü tamamlanmadı (eksik adımlar: " +
                     ", ".join(f"{n}. {adim[n]['ad']}" for n in baglam["eksik_adimlar"]) +
                     "); 3, 5, 11 ve 12. bölümler üretilmedi.")

    for no, baslik, soru in BOLUMLER:
        b = {"no": no, "baslik": baslik, "soru": soru, "cumleler": [], "tablolar_md": "", "notlar": [],
             "kanit_ids": []}
        if no in PROTOKOL_GEREKTIREN and not protokol_tamam:
            b["notlar"].append("Bağlam protokolü tamamlanmadan bu bölüm üretilmez.")
            bolumler.append(b)
            continue
        if no in (1, 2, 14):
            bolumler.append(b)          # aşağıda koddan doldurulur
            continue
        if no == 5:
            b["notlar"].append("Tipli ilişki grafiği modülü henüz yok. 'Birlikte anılma' ilişki sayılmaz; "
                               "kaynaksız kenar yazılmaz.")
            eksik.append("5. Bağlantılar: ilişki grafiği (belge ve kayıt katmanı) henüz kurulmadı.")
            bolumler.append(b)
            continue
        if no == 9:
            b["notlar"].append("Manipülasyon göstergesi modülleri (sessizlik, eşzamanlı söylem, değişiklik/silme, "
                               "gündem kaydırma) bu sürümde ölçülmedi; gösterge yazılmadı. Her göstergenin masum "
                               "açıklaması da test edilecektir.")
            eksik.append("9. Manipülasyon göstergeleri: modül 1, 3, 7, 8 çıktıları yok.")
            bolumler.append(b)
            continue
        secili = _kart_sec(no, kart_listesi)
        if not secili:
            eksik.append(f"{no}. {baslik}: bu bölüm için kanıt kartı yok.")
        baglam_oz = None
        if no == 3:
            b["tablolar_md"] = _zaman_tablosu(adim[1], kartlar, red)
            baglam_oz = {"zaman_cizgisi": adim[1]["cikti"], "notlar": adim[1]["notlar"]}
        elif no == 6:
            b["tablolar_md"] = _soykutugu_tablosu(adim[4])
            baglam_oz = {"tez_soykutugu": adim[4]["cikti"]}
        elif no == 7:
            b["notlar"].append("Çerçeve, dil ve kaynak seçimi modülleri (2, 4, 5) doğrulanmış etiketleme "
                               "gerektirir; bu sürümde yalnızca kanıt kartları kullanıldı.")
        elif no == 11:
            b["tablolar_md"] = "\n\n".join(x for x in (_siralama_tablosu(ach_oz),
                                                        _cui_bono_tablosu(adim[3], kartlar, red)) if x)
            baglam_oz = {"cui_bono": adim[3]["cikti"], "not": KAZANC_NOTU}
        elif no == 12:
            b["tablolar_md"] = "\n\n".join(x for x in (ach.matris_markdown(kartlar) if ach.hipotezler else "",
                                                        _baglam_ek_md(baglam)) if x)
            baglam_oz = {f"{a['adim']}. {a['ad']}": a["cikti"] for a in baglam["adimlar"] if a["adim"] in (2, 5, 6, 7, 9, 10)}
        elif no == 13:
            b["tablolar_md"] = _neden_simdi_md(adim[2])
            baglam_oz = {"neden_simdi": adim[2]["cikti"]}
        b["cumleler"] = _yaz(no, secili, no in ACH_BOLUMLERI, baglam_oz)
        bolumler.append(b)

    # Ek sorular (derinleştirme)
    for i, s in enumerate(ek_sorular or [], 1):
        no = f"E{i}"
        soru_kartlari = [k for k in kart_listesi if alt_harita.get(k.kanit_id) == s["id"]]
        b = {"no": no, "baslik": f"Ek soru {i}", "soru": s["metin"], "cumleler": [], "tablolar_md": "",
             "notlar": [f"Soru kimliği {s['id']} · eklendi {s['zaman']}"], "kanit_ids": []}
        if not soru_kartlari:
            eksik.append(f"Ek soru {i} ({s['id']}): soruya bağlı kanıt kartı henüz eklenmedi.")
        b["cumleler"] = _yaz(no, soru_kartlari + _kart_sec(12, kart_listesi)[:5], True, None, s["metin"])
        bolumler.append(b)

    # 2. Özet bulgular: diğer bölümlerin doğrulanmış cümlelerinden seçilir
    ozet = []
    for kaynak_no, tur, adet in ((11, "degerlendirme", 1), (12, "degerlendirme", 1), (3, "olgu", 2),
                                 (6, "olgu", 1), (12, "acik_soru", 1)):
        b = next(x for x in bolumler if x["no"] == kaynak_no)
        for c in [c for c in b["cumleler"] if c["tur"] == tur][:adet]:
            if c["metin"] not in {o["metin"] for o in ozet}:
                ozet.append({**c, "id": f"ozet-{c['id']}", "dayanak": []})
    bolumler[1]["cumleler"] = [c for c in ozet if c["tur"] != "degerlendirme" or c["kanit_ids"]]
    if not ozet:
        bolumler[1]["notlar"].append("Özetlenecek doğrulanmış bulgu yok.")

    # 1. Soru ve kapsam (koddan)
    kapsam = tanim.get("kapsam") or {}
    if not kapsam:
        eksik.append("Yayın grubu başına kapsam oranı ölçülmedi (coverage_report çıktısı vakaya eklenmeli).")
    if not tanim.get("kapsam_onayi"):
        eksik.append("Kapsam analist tarafından onaylanmadı (soru → rapor akışının ilk insan onayı).")
    if not tanim.get("veri_anlik_goruntu"):
        eksik.append("Veri anlık görüntüsünün tarihi vaka tanımında yok.")
    profiller = list(profiller)
    if not ach.hipotezler:
        eksik.append("Hipotez ön kaydı yok: 11 ve 12. bölümlerde ACH yapılamadı.")
    elif adim[9]["durum"] != "tamam":
        eksik.append("Öne çıkan hipotez için kırmızı takım (şeytanın avukatı) geçişi yapılmadı.")
    if ach.eksik_kanitlar(kartlar):
        eksik.append("ACH matrisinde depoda bulunmayan kanıt kimlikleri var: " + ", ".join(ach.eksik_kanitlar(kartlar)))
    for t in ("mahkeme_kaydi", "uluslararasi_basin", "arastirma_kurumu"):
        if not any(k.tur == t for k in kart_listesi):
            eksik.append(f"'{t}' türünde kanıt yok: olay yalnızca kısmi kaynaklarla görülüyor.")
    if red:
        eksik.append(f"Doğrulayıcı {len(red)} cümleyi/satırı reddetti (analist listesine bakın).")
    eksik.append(GDELT_SINIR_NOTU)

    # Tutulan tüm cümleler son kez doğrulanır: biri bile geçmezse rapor kurulmaz
    for b in bolumler:
        cs = [Cumle.from_dict(c) for c in b["cumleler"]]
        if b["no"] == 2:
            # özet cümleleri kaynak bölümlerdeki olgulara dayanır; dayanak bağı burada aranmaz
            cs = [Cumle(c.tur, c.metin, c.kanit_ids, c.guven, [], c.id) for c in cs]
        kesin_dogrula(cs, kartlar, ek_adlar=ek_adlar)
        b["kanit_ids"] = sorted({k for c in b["cumleler"] for k in c["kanit_ids"]})

    surum = ((onceki or {}).get("surum", 0) + 1) if onceki else (max(vaka.rapor_surumleri() or [0]) + 1)
    rapor = {
        "vaka_id": vaka.id, "vaka_ad": tanim["ad"], "surum": surum, "durum": "taslak",
        "olusturma": datetime.now().isoformat(timespec="seconds"),
        "saglayici": f"{saglayici.ad}/{saglayici.model}",
        "meta": {"veri_anlik_goruntu": tanim.get("veri_anlik_goruntu", ""), "git_commit": git_commit(),
                 "kod_kitabi_surumu": tanim.get("kod_kitabi_surumu", "") or "yok",
                 "platform_surumu": medya.__version__, "kapsam": kapsam, "kaliplar": tanim.get("kaliplar", []),
                 "soru": tanim.get("soru", ""), "olay_tarihi": tanim["olay_tarihi"],
                 "kapsam_onayi": tanim.get("kapsam_onayi"),
                 "ach_on_kayit": ach.on_kayit, "protokol_tamamlandi": protokol_tamam,
                 # Değerlendirme/açık sorularda adların arandığı ek metin (hipotez metinleri, aktör adları)
                 "ek_adlar": ek_adlar,
                 "aktor_profilleri": [p.aktor for p in profiller]},
        "bolumler": bolumler, "reddedilenler": red, "eksik_veri": eksik,
        "kanit_ids": sorted({k for b in bolumler for k in b["kanit_ids"]}),
        "alt_sorular": [s["id"] for s in (ek_sorular or [])],
        "onay": None, "dogrulama": None, "onceki_surum": (onceki or {}).get("surum"), "degisiklikler": [],
    }
    return rapor


# --------------------------------------------------------------------------------
def rapor_dogrula(rapor: dict, kartlar: dict, ek_adlar: str | None = None) -> dict:
    """taslak → dogrulandi. Tüm cümleler güncel depoya karşı yeniden doğrulanır; kapsam onayı ve
    "Eksik veri" bölümü zorunludur. `ek_adlar` verilmezse raporun üretildiği andaki hipotez metinleri kullanılır."""
    if ek_adlar is None:
        ek_adlar = rapor["meta"].get("ek_adlar", "")
    if rapor["durum"] != "taslak":
        raise RaporHatasi(f"Yalnızca taslak doğrulanabilir (şu an: {rapor['durum']})")
    if not rapor["meta"].get("kapsam_onayi"):
        raise RaporHatasi("Kapsam onaylanmadan rapor doğrulanamaz (vaka kapsam-onayla)")
    if not rapor.get("eksik_veri"):
        raise RaporHatasi("Eksik veri bölümü boş olamaz")
    for b in rapor["bolumler"]:
        cs = [Cumle.from_dict(c) for c in b["cumleler"]]
        cs = [Cumle(c.tur, c.metin, c.kanit_ids, c.guven, [] if str(b["no"]) == "2" else c.dayanak, c.id) for c in cs]
        kesin_dogrula(cs, kartlar, ek_adlar=ek_adlar)
    rapor["durum"] = "dogrulandi"
    rapor["dogrulama"] = {"zaman": datetime.now().isoformat(timespec="seconds"),
                          "cumle_sayisi": sum(len(b["cumleler"]) for b in rapor["bolumler"])}
    return rapor


def onayla(rapor: dict, onaylayan: str, tarih: str) -> dict:
    """dogrulandi → onaylandi. Onaylayanın adı ve tarih zorunludur ve rapora yazılır."""
    if not (onaylayan or "").strip():
        raise RaporHatasi("Onay için onaylayanın adı zorunlu")
    if not (tarih or "").strip():
        raise RaporHatasi("Onay için tarih zorunlu")
    try:
        date.fromisoformat(tarih.strip())
    except ValueError as e:
        raise RaporHatasi("Onay tarihi YYYY-AA-GG olmalı") from e
    if rapor["durum"] != "dogrulandi":
        raise RaporHatasi(f"Yalnızca doğrulanmış rapor onaylanabilir (şu an: {rapor['durum']})")
    rapor["durum"] = "onaylandi"
    rapor["onay"] = {"onaylayan": onaylayan.strip(), "tarih": tarih.strip()}
    return rapor


# --------------------------------------------------------------------------------
def markdown_uret(rapor: dict, kartlar: dict) -> str:
    m = rapor["meta"]
    kapsam = m.get("kapsam") or {}
    kapsam_md = "; ".join(f"{g}: {v:.0%}" if isinstance(v, (int, float)) else f"{g}: {v}" for g, v in kapsam.items()) \
        or "ölçülmedi"
    onay = rapor.get("onay")
    sat = [
        f"# {rapor['vaka_ad']} — Olay raporu",
        "",
        f"**Sürüm {rapor['surum']} · {DURUM_ETIKETI[rapor['durum']]}**"
        + (f" · Onaylayan: {onay['onaylayan']}, {tarih_tr(onay['tarih'])}" if onay else " · Yayımlanmadı (insan onayı yok)"),
        "",
        "| | |", "|---|---|",
        f"| Veri anlık görüntüsü | {m.get('veri_anlik_goruntu') or 'belirtilmedi'} |",
        f"| Git commit | `{m.get('git_commit')}` |",
        f"| Kod kitabı sürümü | {m.get('kod_kitabi_surumu')} |",
        f"| Platform sürümü | medya {m.get('platform_surumu')} |",
        f"| Yayın grubu başına kapsam | {kapsam_md} |",
        f"| Oluşturma | {rapor['olusturma']} · {rapor['saglayici']} |",
        "",
        medya.GDELT_ATTRIBUTION,
        "",
        "> Cümle türleri: **[Olgu]** kanıt kimliğiyle · **[Değerlendirme]** analitik çıkarım, Kent ölçeğinde güven "
        "düzeyiyle · **[Açık soru]** kanıtın cevaplayamadığı. Resmi açıklamalar \"kurum iddiası\" olarak aktarılır.",
        "",
    ]
    for b in rapor["bolumler"]:
        no = b["no"]
        sat.append(f"## {no}. {b['baslik']}" if isinstance(no, int) else f"## {b['baslik']}")
        sat.append(f"*{b['soru']}*")
        sat.append("")
        if no == 1:
            sat += [f"- **Soru:** {m.get('soru')}", f"- **Olay tarihi:** {tarih_tr(m.get('olay_tarihi'))}",
                    f"- **Arama kalıpları:** {', '.join('`' + k + '`' for k in m.get('kaliplar', [])) or 'tanımlanmadı'}",
                    f"- **Kapsam (yayın grubu başına):** {kapsam_md}",
                    "- **Kapsam onayı:** " + (f"{m['kapsam_onayi']['onaylayan']}, {m['kapsam_onayi']['tarih']}"
                                               if m.get("kapsam_onayi") else "yok"), ""]
        for n in b["notlar"]:
            sat.append(f"*{n}*")
        if b["notlar"]:
            sat.append("")
        if b.get("tablolar_md"):
            sat += [b["tablolar_md"], ""]
        for c in b["cumleler"]:
            sat.append(_cumle_md(c, kartlar))
        if b["cumleler"]:
            sat.append("")
        if no == 14:
            sat += ["### Eksik veri", ""] + [f"- {e}" for e in rapor["eksik_veri"]] + [""]
            sat += ["### Derecelendirme", "",
                    "Kaynak güvenilirliği: " + ", ".join(f"{k} {v}" for k, v in KAYNAK_DERECELERI.items()) + ".  ",
                    "Bilginin doğruluğu: " + ", ".join(f"{k} {v}" for k, v in BILGI_DERECELERI.items()) + ".  ",
                    "Aynı ölçek resmi, iktidara yakın, muhalif ve yabancı kaynaklara aynı biçimde uygulanır.", ""]
            sat += ["### Yöntem", "",
                    "- Rapordaki her olgu cümlesi kanıt kartına bağlıdır; sayı, tarih, ad ve alıntılar otomatik "
                    "doğrulayıcıyla kartlara karşı denetlendi. Eşleşmeyen cümleler rapordan çıkarıldı.",
                    "- Hipotezler kanıta bakılmadan önce kaydedildi (ön kayıt zamanı ve SHA-256 özeti: "
                    f"{(m.get('ach_on_kayit') or {}).get('zaman', '—')}, "
                    f"`{((m.get('ach_on_kayit') or {}).get('ozet') or '—')[:16]}`).",
                    "- Dil modeli ölçmez; yalnızca seçilmiş kanıt kartlarını cümleye çevirir.", ""]
            sat += ["### Kaynaklar", ""]
            kullanilan = [kartlar[k] for k in rapor["kanit_ids"] if k in kartlar]
            sat += [k.markdown() for k in kullanilan] or ["_Raporda kullanılan kanıt yok._"]
            sat.append("")
    if rapor.get("degisiklikler"):
        sat += ["## Değişiklik günlüğü", ""] + [f"- {d}" for d in rapor["degisiklikler"]] + [""]
    if rapor["durum"] != "onaylandi" and rapor.get("reddedilenler"):
        sat += ["## Analist için: doğrulayıcının reddettiği cümleler", "",
                "*Bu bölüm yayımlanan rapora girmez.*", ""]
        for r in rapor["reddedilenler"]:
            sat.append(f"- [{r['bolum']}] “{r['cumle']['metin']}” — {'; '.join(r['nedenler'])}")
        sat.append("")
    sat += ["---", medya.GDELT_ATTRIBUTION, ""]
    return "\n".join(sat)
