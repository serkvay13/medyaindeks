"""Vaka raporunun deterministik parçaları: hepsi koddan, kart dosyalarından ve hesaplanmış istatistikten üretilir.

Hiçbir parça elle yazılmış sayı içermez. Hücre metinlerine anonimleştirme (özel kişiler rolüyle) uygulanır.
Sayılar Türkçe yazımla (ondalık virgül) basılır.
"""
import re
from collections import Counter

from medya import GDELT_ATTRIBUTION_DUZ  # noqa: F401  (atıf metni kapakta ayrıca yazılır)
from medya.gdelt.gruplar import YAYIN_ADLARI, alan_grubu_haritasi
from medya.metin import sayi_tr, tr_lower

# --------------------------------------------------------------------------------
# Yardımcılar
# --------------------------------------------------------------------------------
def esc(s) -> str:
    return (s or "").replace("|", "/").replace("\n", " ")


def kisa(s, n: int = 230) -> str:
    s = esc(s)
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


def ondalik(s) -> str:
    """Rakamlar arasındaki ondalık noktayı virgüle çevirir (Türkçe yazım)."""
    return re.sub(r"(?<=\d)\.(?=\d)", ",", str(s))


def iyelik(n: int) -> str:
    """Sayıya iyelik eki: 54'ü, 8'i, 52'si, 6'sı, 10'u, 40'ı, 100'ü, 1000'i."""
    n = int(n)
    if n == 0:
        return f"{n}'ı"
    if n % 1000 == 0 and n % 1_000_000:
        return f"{n}'i"
    if n % 100 == 0:
        return f"{n}'ü"
    birler = {1: "i", 2: "si", 3: "ü", 4: "ü", 5: "i", 6: "sı", 7: "si", 8: "i", 9: "u"}
    onlar = {1: "u", 2: "si", 3: "u", 4: "ı", 5: "si", 6: "ı", 7: "i", 8: "i", 9: "ı"}
    ek = birler[n % 10] if n % 10 else onlar[(n // 10) % 10]
    return f"{n}'{ek}"


def _anonim(a):
    return a or (lambda x: x)


def sinif_metni(k) -> str:
    return (k.kaynak_sinifi or "—") + ("†" if k.sinif_duzeltildi else "")


def _sema(kartlar: dict, ad: str) -> list:
    return sorted((k for k in kartlar.values() if k.ek.get("_sema") == ad), key=lambda k: k.ek.get("_sira", 0))


def _div(sinif: str, icerik: str) -> str:
    return f'<div class="{sinif}">\n\n{icerik}\n</div>'


# --------------------------------------------------------------------------------
# Kronoloji
# --------------------------------------------------------------------------------
KR_BASLIK = ["| KR | Tarih | Saat (TSİ) | Olay | Kaynak · sınıf | Erişim / çelişki |", "|---|---|---|---|---|---|"]


def kronoloji_tablosu(kartlar: list, anonim=None) -> str:
    a = _anonim(anonim)
    out = list(KR_BASLIK)
    for k in kartlar:
        er = {"açıldı": "açıldı", "arama özeti": "**arama özeti**"}.get(k.erisim_durumu, "**bulunamadı**")
        cel = " · ⚠ çelişki notu" if k.celiski else ""
        yayin = k.ek.get("yayin_ham") or "—"
        tarih = k.olay_tarihi or k.ek.get("olay_tarihi_ham", "")
        saat = esc(k.saat).replace("saat belirtilmemiş", "—")
        out.append(f"| {k.gorunen_id} | {tarih} | {saat} | {kisa(a(k.ozet), 260)} | {esc(yayin)} · {esc(sinif_metni(k))} "
                   f"| {er}{cel} |")
    return "\n".join(out) + "\n"


def kronoloji_donemleri(kartlar: dict) -> list[list]:
    """KR satırlarını dönem önekine (0, 1, 2, 3 …) göre gruplar (dosya sırası korunur)."""
    gruplar: dict[str, list] = {}
    for k in _sema(kartlar, "KR"):
        gruplar.setdefault((k.donem or "?")[0], []).append(k)
    return [gruplar[d] for d in sorted(gruplar)]


# --------------------------------------------------------------------------------
# Çelişki tablosu
# --------------------------------------------------------------------------------
def celiski_tablosu(celiskiler: dict) -> str:
    bas = celiskiler.get("basliklar", ["Konu", "Versiyonlar", "Kart", "Değerlendirme"])
    sat = ["| " + " | ".join(bas) + " |", "|" + "---|" * len(bas)]
    for c in celiskiler.get("kayitlar", []):
        kart = ", ".join(f"[{x}]" for x in c.get("kartlar", []))
        sat.append(f"| {esc(c['konu'])} | {esc(c['versiyonlar'])} | {kart} | {esc(c['degerlendirme'])} |")
    return f'<div class="box">\n\n{celiskiler.get("giris", "")}\n\n' + "\n".join(sat) + "\n\n</div>"


def celiski_denetimi(celiskiler: dict, kartlar: dict, izinli: set) -> tuple[list, list]:
    """(var olmayan kart kimlikleri, çelişki notu olup hiçbir kayda bağlanmamış KR satırları)."""
    bilinmeyen = sorted({x for c in celiskiler.get("kayitlar", []) for x in c.get("kartlar", [])
                         if x not in kartlar and x not in izinli})
    bagli = {x for c in celiskiler.get("kayitlar", []) for x in c.get("kartlar", [])}
    bagsiz = [k.gorunen_id for k in _sema(kartlar, "KR") if k.celiski and k.gorunen_id not in bagli]
    return bilinmeyen, bagsiz


# --------------------------------------------------------------------------------
# GDELT tabloları
# --------------------------------------------------------------------------------
def gdelt_gunluk(ist: dict) -> str:
    out = ["| Gün | Çekirdek küme (haber) | Türkçe GKG toplam kayıt | Pay (%) |", "|---|---|---|---|"]
    for d, v in ist["gunluk"].items():
        out.append(f"| {d[6:]}.{d[4:6]}.{d[:4]} | {v['haber']} | {sayi_tr(v['tum'])} | {ondalik(v['pay_yuzde'])} |")
    return "\n".join(out) + "\n"


def _zaman(u: str, fark: int = 0) -> str:
    from datetime import datetime, timedelta
    t = datetime.strptime(u[:12], "%Y%m%d%H%M") + timedelta(hours=fark)
    return t.strftime("%d.%m %H:%M")


def gdelt_ilk_haber(ist: dict, fark: int = 3) -> str:
    grup = ist.get("izlenen_yayin_grubu") or alan_grubu_haritasi()
    out = ["| Yayın | Grup (KEY_OUTLETS) | İlk GDELT dosyası (UTC) | TSİ | Çekirdek kümede haber |",
           "|---|---|---|---|---|"]
    for s, u in ist["izlenen_yayin_ilk_haber_utc"].items():
        out.append(f"| {s} | {grup.get(s, '—')} | {_zaman(u)} | {_zaman(u, fark)} | "
                   f"{ist['izlenen_yayin_sayi'].get(s, '—')} |")
    return "\n".join(out) + "\n"


def gdelt_cerceve(ist: dict, tablo: dict) -> str:
    c = ist["cerceve"]
    sut, bas = tablo["sutunlar"], tablo.get("basliklar", tablo["sutunlar"])
    pay, payda = tablo.get("oran", [None, None])
    out = ["| Grup | n | " + " | ".join(bas) + f" | {tablo.get('oran_basligi', 'oran')} |",
           "|---|---|" + "---|" * len(bas) + "---|"]
    for g in tablo.get("satirlar") or list(c["n"]):
        if g not in c["n"]:
            continue
        gg = c["grup"].get(g, {})
        f, k = gg.get(pay, 0), gg.get(payda, 0)
        oran = f"{f}:{k}" + (f" (≈{f / k:.1f}×)" if k else f" ({tablo.get('oran_sifir_notu', 'payda 0')})")
        out.append(f"| {g} | {c['n'][g]} | " + " | ".join(str(gg.get(x, 0)) for x in sut) + f" | {ondalik(oran)} |")
    return "\n".join(out) + "\n"


def gdelt_ton(ist: dict) -> str:
    out = ["| Grup | Ortalama ton | Medyan ton | n |", "|---|---|---|---|"]
    for g, v in sorted(ist["ton_grup"].items(), key=lambda x: x[1][0]):
        out.append(f"| {g} | {ondalik(v[0])} | {ondalik(v[1])} | {v[2]} |")
    out.append(f"| **Tümü** | {ondalik(ist['ton_tum'])} | — | {ist['tekil_url']} |")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------------
# ACH matrisi
# --------------------------------------------------------------------------------
_KIMLIK = re.compile(r"(KR-\d{3}|RD\d{2}|R\d{2}|K\d{2})")


def ach_kart_kimlikleri(metin: str) -> list[str]:
    """"RD18–RD22, K30" → ["RD18", "RD19", …, "RD22", "K30"] (aralıklar açılır)."""
    out = []
    for parca in re.split(r",|×", metin):
        parca = parca.strip()
        m = re.fullmatch(r"([A-Z]+-?)(\d+)\s*[–-]\s*([A-Z]+-?)(\d+)", parca)
        if m and m.group(1) == m.group(3):
            g = len(m.group(2))
            out += [f"{m.group(1)}{i:0{g}d}" for i in range(int(m.group(2)), int(m.group(4)) + 1)]
        else:
            out += _KIMLIK.findall(parca)
    return out


def ach_agirligi(derece: str, agirlik: dict) -> float:
    return round(float(agirlik["kaynak"][derece[0]]) * float(agirlik["bilgi"][str(derece[1])]), 2)


def ach_hesapla(matris: dict) -> dict:
    H = matris["hipotezler"]
    ag = matris["agirlik"]
    sc = {h: 0.0 for h in H}
    cc = {h: 0.0 for h in H}
    nc = {h: 0 for h in H}
    for e in matris["satirlar"]:
        w = ach_agirligi(e["derece"], ag)
        for h, v in zip(H, e["isaretler"].split()):
            if v == "Ç":
                sc[h] += w
                nc[h] += 1
            elif v == "T":
                cc[h] += w
    sira = sorted(H, key=lambda h: sc[h])
    return {"celiski": sc, "tutarlilik": cc, "celiski_sayisi": nc, "siralama": sira}


def ach_matrisi(matris: dict) -> str:
    H = matris["hipotezler"]
    ag = matris["agirlik"]
    r = ach_hesapla(matris)
    sat = ["| # | Kanıt | Kart(lar) | Derece (ağırlık) | " + " | ".join(H) + " |", "|---|---|---|---|" + "---|" * len(H)]
    for e in matris["satirlar"]:
        w = ach_agirligi(e["derece"], ag)
        sat.append(f"| {e['id']} | {e['aciklama']} | {e['kartlar']} | {e['derece']} ({ondalik(f'{w:g}')}) | "
                   + " | ".join(e["isaretler"].split()) + " |")
    sat.append("| | **Ağırlıklı tutarsızlık (Σ Ç)** | | | " + " | ".join(f"**{ondalik(f'{r['celiski'][h]:.2f}')}**" for h in H) + " |")
    sat.append("| | Ağırlıklı tutarlılık (Σ T) | | | " + " | ".join(ondalik(f"{r['tutarlilik'][h]:.2f}") for h in H) + " |")
    sat.append("| | Çelişki sayısı | | | " + " | ".join(str(r["celiski_sayisi"][h]) for h in H) + " |")
    return "\n".join(sat) + "\n"


def ach_denetimi(matris: dict, kartlar: dict) -> list[str]:
    """Var olmayan kart, hipotez sayısıyla uyuşmayan işaret, kartlarından hiçbirinin derecesine uymayan derece."""
    sorun = []
    n = len(matris["hipotezler"])
    for e in matris["satirlar"]:
        ids = ach_kart_kimlikleri(e["kartlar"])
        yok = [i for i in ids if i not in kartlar]
        if yok:
            sorun.append(f"{e['id']}: var olmayan kart {', '.join(yok)}")
        if len(e["isaretler"].split()) != n or set(e["isaretler"].split()) - {"T", "Ç", "N"}:
            sorun.append(f"{e['id']}: işaretler {n} hipotez için T/Ç/N olmalı")
        dereceler = {kartlar[i].derece for i in ids if i in kartlar}
        if dereceler and e["derece"] not in dereceler:
            sorun.append(f"{e['id']}: derece {e['derece']} dayanak kartlarının hiçbirinde yok ({', '.join(sorted(dereceler))})")
    return sorun


# --------------------------------------------------------------------------------
# Kart dizini (Ek A)
# --------------------------------------------------------------------------------
def _aralik(ks: list) -> str:
    return f"{ks[0].gorunen_id}–{ks[-1].gorunen_id}" if ks else ""


def kart_dizini(kartlar: dict, ayar: dict, anonim=None) -> str:
    """ayar: vaka.yaml > rapor.kart_dizini: {semalar: [{sema, baslik, kr_notu?, ...}], erisim_etiketleri: {...}}."""
    a = _anonim(anonim)
    et = {"arama özeti": " (arama özeti)", "devralındı": " (temel kartlardan)", **(ayar.get("erisim_etiketleri") or {})}
    lines = []
    for i, s in enumerate(ayar.get("semalar", [])):
        ks = _sema(kartlar, s["sema"])
        if not ks:
            continue
        dosya = ks[0].ek.get("_dosya", "")
        if i:
            lines.append("")
        lines += [f"### {s['baslik'].format(aralik=_aralik(ks), dosya=dosya)} {{.unnumbered}}", ""]
        if s["sema"] == "KR":
            if s.get("not"):
                lines += [s["not"], ""]
            lines += ["| Kimlik | Kaynak | Yayın tarihi | Sınıf | Derece |", "|---|---|---|---|---|"]
            for k in ks:
                lines.append(f"| {k.gorunen_id} | {kisa(k.ek.get('yayin_ham') or '—', 45)} | "
                             f"{k.yayin_tarihi or k.ek.get('yayin_tarihi_ham') or '—'} | "
                             f"{esc(sinif_metni(k))} | {k.erisim_durumu}{' ⚠' if k.celiski else ''} |")
            continue
        tarih_basligi = s.get("tarih_basligi", "Yayın tarihi")
        lines += [f"| Kimlik | Kaynak | {tarih_basligi} | Sınıf | Derece | Kısa içerik |", "|---|---|---|---|---|---|"]
        for k in ks:
            if s["sema"] == "K":
                cl = (k.kaynak_sinifi or "—") + (" · devlet bağlantılı" if k.ek.get("devlet_baglantili") else "")
                lines.append(f"| {k.gorunen_id} | {kisa(k.kurum, 70)} | {k.yayin_tarihi or k.ek.get('yayin_tarihi_ham', '')} | "
                             f"{esc(cl)} | {k.derece} | {kisa(a(k.ozet), 75)} |")
            elif s["sema"] == "R":
                er = "" if k.erisim_durumu == "açıldı" else et.get(k.erisim_durumu, "")
                tarih = k.olay_tarihi or k.ek.get("olay_tarihi_ham", "")
                lines.append(f"| {k.gorunen_id} | {kisa(k.kurum, 45)} | {tarih} | {esc(sinif_metni(k))} | "
                             f"{k.derece}{er} | {kisa(a(k.ek.get('aktor', '') + ': ' + k.ozet), 75)} |")
            else:   # RD ve benzerleri
                er = "" if k.erisim_durumu == "açıldı" else et.get(k.erisim_durumu, "")
                tarih = k.yayin_tarihi or k.ek.get("yayin_tarihi_ham", "")
                lines.append(f"| {k.gorunen_id} | {kisa(a(k.kurum), 45)} | {tarih} | {esc(sinif_metni(k))} | "
                             f"{k.derece}{er} | {kisa(a(k.ozet), 75)} |")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------------
# Kaynak tabanı tablosu
# --------------------------------------------------------------------------------
def _dagilim(ks: list, kurallar: list) -> str:
    """Sınıf dağılımı: kurallar [kalıp (regex, re.search), etiket] sırasıyla (ilk eşleşen); çıktı sırası kural
    sırasıdır."""
    sayim: Counter = Counter()
    for k in ks:
        sinif = k.kaynak_sinifi or ""
        for kalip, etiket in kurallar:
            if re.search(kalip, sinif):
                sayim[etiket] += 1
                break
        else:
            sayim[sinif or "sınıfsız"] += 1
    sira = list(dict.fromkeys(e for _, e in kurallar)) + [e for e in sayim if e not in {x for _, x in kurallar}]
    return " · ".join(f"{e} {sayim[e]}" for e in sira if sayim.get(e))


def _sayim(degerler, sira) -> str:
    c = Counter(degerler)
    return " · ".join(f"{d} {c[d]}" for d in sira if c.get(d))


def _erisim_metni(ks: list, etiketler: dict, buyuk: bool = False) -> str:
    c = Counter(k.erisim_durumu for k in ks)
    parca = [f"{etiketler.get(d, d)} {c[d]}" for d in ("açıldı", "arama özeti", "bulunamadı", "devralındı") if c.get(d)]
    if buyuk and parca:
        parca[0] = parca[0][0].upper() + parca[0][1:]
    return " · ".join(parca)


def _derece_metni(sema: str, ks: list, etiketler: dict) -> str:
    kaynak = _sayim([k.kaynak_derecesi for k in ks], "ABCDEF")
    bilgi = " · ".join(f"{b}→{n}" for b, n in sorted(Counter(k.bilgi_derecesi for k in ks).items()))
    if sema == "K":
        return f"Kaynak: {kaynak}. Bilgi: {bilgi}"
    if sema == "KR":
        return f"{_erisim_metni(ks, {'arama özeti': 'yalnızca arama özeti', **etiketler}, buyuk=True)}; " \
               f"çelişki notlu {sum(1 for k in ks if k.celiski)}"
    if sema == "R":
        return f"{kaynak}; bilgi {bilgi}; {_erisim_metni(ks, etiketler)}"
    return f"{kaynak}; {_erisim_metni(ks, etiketler)}"


def _grup_etiketi(g: str) -> str:
    return tr_lower(g[:1]) + g[1:].replace(" / ", "/")


def kaynak_tabani(kartlar: dict, ist: dict | None, ayar: dict, olay_tarihi: str) -> str:
    """ayar: vaka.yaml > rapor.kaynak_tabani: {semalar: [{sema, siniflar: [[kalıp, etiket]…]}], erisim_etiketleri}."""
    et = ayar.get("erisim_etiketleri") or {}
    sat = ["| Dosya | Kart/satır | Sınıf dağılımı (kaynak sınıfı) | Derece / erişim |", "|---|---|---|---|"]
    for s in ayar.get("semalar", []):
        ks = _sema(kartlar, s["sema"])
        if not ks:
            continue
        adet = str(len(ks))
        if s["sema"] == "KR":
            adet += f" ({iyelik(sum(1 for k in ks if k.olay_tarihi == olay_tarihi))} olay günü)"
        dag = _dagilim(ks, s.get("siniflar", []))
        if any("devlet_baglantili" in k.ek for k in ks):
            dag += f"; devlet bağlantılı {sum(1 for k in ks if k.ek.get('devlet_baglantili'))}/{len(ks)}"
        sat.append(f"| `{ks[0].ek.get('_dosya', '')}` ({_aralik(ks)}) | {adet} | {dag} | {_derece_metni(s['sema'], ks, et)} |")
    if ist:
        c = ist["cerceve"]["n"]
        gruplar = sorted(((g, n) for g, n in c.items() if g != "TÜMÜ"), key=lambda x: (x[0].startswith("Diğer"), -x[1]))
        sat.append(f"| GDELT GKG 2.1 yeniden kurulumu | {sayi_tr(ist['dosya_sayisi'])} adet 15 dakikalık dosya "
                   f"({iyelik(ist['bos_dosya'])} boş); Türkçe kaynaklı {sayi_tr(ist['turkce_toplam_kayit_pencere'])} kayıt; "
                   f"çekirdek küme {sayi_tr(ist['tekil_url'])} haber, {ist['tekil_site']} site | Yayın grupları: "
                   + " · ".join(f"{_grup_etiketi(g)} {sayi_tr(n)}" for g, n in gruplar)
                   + " | URL düzeyinde sayım; bkz. Ek B |")
    return "\n".join(sat)


# --------------------------------------------------------------------------------
# Kapak
# --------------------------------------------------------------------------------
def _tarih_gg(t: str) -> str:
    return f"{t[8:10]}.{t[5:7]}.{t[:4]}"


def kapak(kartlar: dict, ist: dict | None, ayar: dict, hipotezler: list, gdelt_ayar: dict | None = None) -> str:
    """ayar: vaka.yaml > rapor.kapak. "Taslak — insan onayı bekliyor" ve GDELT atfı her zaman yazılır."""
    semalar = [(s, len(_sema(kartlar, s))) for s in ("K", "KR", "R", "RD") if _sema(kartlar, s)]
    toplam = sum(n for _, n in semalar)
    taban = f"{toplam} kanıt kartı/satırı ({' · '.join(f'{s} {n}' for s, n in semalar)})"
    if ist:
        taban += f" + GDELT GKG 2.1 yeniden kurulumu ({sayi_tr(ist['tekil_url'])} haber, {ist['tekil_site']} site)"
    sat = ['<div class="cover">', '<div class="draft">TASLAK — İNSAN ONAYI BEKLİYOR</div>',
           f'<p class="kicker">{ayar.get("kicker", "Açık kaynak istihbarat (OSINT) analizi")}</p>',
           f'<h1 class="title">{ayar["baslik"]}</h1>']
    if ayar.get("alt_baslik"):
        sat.append(f'<p class="subtitle">{ayar["alt_baslik"]}</p>')
    sat += ['<table class="covermeta">',
            f'<tr><td>Hazırlanma</td><td>{ayar.get("hazirlanma", "")}</td></tr>',
            f'<tr><td>Kaynak tabanı</td><td>{taban}</td></tr>',
            f'<tr><td>Hipotezler</td><td>Ön kayıtlı: {", ".join(hipotezler)} (kanıt toplamadan önce zaman damgalı)</td></tr>',
            f'<tr><td>Durum</td><td>{ayar.get("durum", "Taslak; insan onayı olmadan dağıtılmamalıdır")}</td></tr>',
            '</table>']
    if ist:
        g = gdelt_ayar or {}
        sat.append('<p class="gdelt">Medya verisi: <b>The GDELT Project</b> (https://www.gdeltproject.org) — Global '
                   'Knowledge Graph 2.1, çeviri akışı (translation GKG), Türkçe kaynaklı kayıtlar, '
                   f'{_tarih_gg(str(g.get("baslangic", "")))}–{_tarih_gg(str(g.get("bitis", "")))}. GDELT verisinin '
                   'kullanımı kaynak gösterimini zorunlu kılar; bu raporda GDELT\'ten türetilen her sayı '
                   '[GDELT-istatistik] veya [GDELT-ek] etiketiyle işaretlidir.</p>')
    else:
        sat.append('<p class="gdelt">Medya verisi kullanılmadı.</p>')
    sat.append("</div>")
    return "\n".join(sat)


__all__ = ["kronoloji_tablosu", "kronoloji_donemleri", "celiski_tablosu", "celiski_denetimi", "gdelt_gunluk",
           "gdelt_ilk_haber", "gdelt_cerceve", "gdelt_ton", "ach_matrisi", "ach_hesapla", "ach_denetimi",
           "ach_kart_kimlikleri", "kart_dizini", "kaynak_tabani", "kapak", "iyelik", "YAYIN_ADLARI"]
