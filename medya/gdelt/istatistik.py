"""Vaka haber kümesinin istatistikleri.

Ölçülenler (hepsi çekirdek küme üzerinde, URL'ye göre tekilleştirilmiş):
- günlük hacim ve Türkçe arşivdeki pay (%), saatlik eğri (UTC ve yerel saat: TSİ = UTC + 3),
- izlenen yayınların ilk haber zamanı (GDELT dosya zamanı; yayın anı değil) ve haber sayısı,
- yayın grubu dağılımı (medya.gdelt.gruplar), ton ortalaması/medyanı (V2Tone ilk bileşeni),
- kopya-slug kümeleri (aynı URL sonu ≥3 sitede), en çok haber veren siteler,
- çerçeve sayımları (grup ve gün bazında) — sözlük vaka ayarında.

Çerçeve eşleştirme: URL yüzde kodlaması çözülür, Türkçe katlanır (fold_tr), harf/rakam dışı her şey "-" olur ve
başına "-" eklenir. Sözlük kalıpları "-" ile başlar: eşleşme yalnızca sözcük başında olur. Böylece "dışişleri"
("-disisleri") içindeki "isis" ya da "saldırısıdır" içindeki "isid" çerçeve sayılmaz. Kalıp sonunda "-" varsa
sözcüğün tamamı aranır (ör. "abd" ≠ "abdullah"). Kalıplar RE2 uyumludur.

GDELT 2019 öncesinde başlık tutmadığı için çerçeve sayımı URL'ye dayanır: başlığa/URL'ye taşınmayan çerçeveyi
kaçırır. Bu bir kapsam sınırıdır ve raporda yazılır.
"""
import re
import statistics as st
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from urllib.parse import unquote

from medya.gdelt.gruplar import DIGER, GRUPLAR, alan_grubu_haritasi
from medya.metin import fold_tr

TUM = "TÜMÜ"
CERCEVE_DIGER = "Diğer (yerel/portal)"


def url_tokenleri(url: str) -> str:
    """Çerçeve eşleştirmesi için URL: "-" + katlanmış, harf/rakam dışı "-" olmuş metin."""
    return "-" + re.sub(r"[^a-z0-9]+", "-", fold_tr(unquote(url or "")))


def cerceve_derle(sozluk: dict[str, str]) -> dict[str, re.Pattern]:
    out = {}
    for ad, kalip in sozluk.items():
        if not kalip.startswith("-"):
            raise ValueError(f"Çerçeve kalıbı sözcük başı sınırı için '-' ile başlamalı: {ad}: {kalip!r}")
        if re.search(r"\.[*+{]", kalip):
            raise ValueError(f"Çerçeve kalıbında joker kullanılmaz: {ad}: {kalip!r}")
        out[ad] = re.compile(kalip)
    return out


def cerceveler_bul(url: str, derli: dict[str, re.Pattern]) -> list[str]:
    t = url_tokenleri(url)
    return [ad for ad, k in derli.items() if k.search(t)]


def slug(url: str) -> str:
    """URL'nin son parçası; sondaki rakamlı ek ve uzantı atılmış (kopya haber kümelemesi için)."""
    son = unquote(url or "").rstrip("/").split("/")[-1]
    return re.sub(r"[-_]\d+.*$", "", fold_tr(son).split(".")[0])


def yerel_saat(utc_ts: str, fark_saat: int = 3) -> datetime:
    return datetime.strptime(utc_ts[:14], "%Y%m%d%H%M%S") + timedelta(hours=fark_saat)


def istatistik_hesapla(sonuc, ayar: dict, gruplar: dict | None = None) -> dict:
    """SorguSonucu + vaka GDELT ayarı → istatistik sözlüğü (JSON'a yazılabilir)."""
    R = sonuc.cekirdek
    T = sonuc.gun_toplam
    harita = alan_grubu_haritasi(gruplar or GRUPLAR)
    fark = int(ayar.get("saat_farki", 3))
    out: dict = {"dosya_sayisi": sonuc.dosya_sayisi, "bos_dosya": sonuc.bos_dosya,
                 "turkce_toplam_kayit_pencere": sum(T.values()), "genis_kume": len(sonuc.genis),
                 "toplam_kayit": len(R), "tekil_url": len({r["url"] for r in R}),
                 "tekil_site": len({r["src"] for r in R}), "gurultu": sonuc.gurultu_uyarisi()}
    d = Counter(r["date"][:8] for r in R)
    out["gunluk"] = {k: {"haber": d.get(k, 0), "tum": T[k], "pay_yuzde": round(100 * d.get(k, 0) / T[k], 2)}
                     for k in sorted(T)}
    out["saatlik_utc"] = dict(sorted(Counter(r["date"][:10] for r in R).items()))
    yerel = Counter(yerel_saat(r["date"], fark).strftime("%Y%m%d %H") for r in R)
    out["saatlik_yerel"] = dict(sorted(yerel.items()))
    out["ceyrek_utc"] = dict(sorted(Counter(r["date"][:12] for r in R).items()))
    src = Counter(r["src"] for r in R)
    out["site_top40"] = src.most_common(40)
    out["grup"] = dict(Counter(harita.get(r["src"], DIGER) for r in R))
    ilk = {}
    for r in R:
        if r["src"] in harita and r["src"] not in ilk:
            ilk[r["src"]] = r["date"]
    out["izlenen_yayin_ilk_haber_utc"] = dict(sorted(ilk.items(), key=lambda x: x[1]))
    out["izlenen_yayin_sayi"] = {s: src[s] for s in harita if src.get(s)}
    out["izlenen_yayin_grubu"] = {s: harita[s] for s in out["izlenen_yayin_sayi"]}
    tg = defaultdict(list)
    for r in R:
        if r["tone"] is not None:
            tg[harita.get(r["src"], DIGER)].append(r["tone"])
    out["ton_grup"] = {g: (round(st.mean(v), 2), round(st.median(v), 2), len(v)) for g, v in tg.items()}
    tonlar = [r["tone"] for r in R if r["tone"] is not None]
    out["ton_tum"] = round(st.mean(tonlar), 2) if tonlar else None
    out["ton_medyan_tum"] = round(st.median(tonlar), 2) if tonlar else None
    kelime = [r["wc"] for r in R if r["wc"]]
    out["ort_kelime"] = round(st.mean(kelime), 0) if kelime else None
    sl = defaultdict(set)
    for r in R:
        s = slug(r["url"])
        if len(s) > 25:
            sl[s].add(r["src"])
    out["ayni_slug_cok_site"] = sorted(((len(v), k, sorted(v)[:8]) for k, v in sl.items() if len(v) >= 3),
                                       reverse=True)[:20]
    out["ilk_30"] = [(r["date"], r["src"], unquote(r["url"])[:140]) for r in R[:30]]
    out["cerceve"] = cerceve_sayimlari(R, ayar.get("cerceveler", {}), harita, ayar.get("cerceve_diger_etiketi",
                                                                                         CERCEVE_DIGER))
    return out


def cerceve_sayimlari(R: list, sozluk: dict, harita: dict, diger_etiketi: str = CERCEVE_DIGER) -> dict:
    """{"n": {grup: haber}, "grup": {grup: {çerçeve: sayı}}, "gunluk": {gün: {çerçeve: sayı}}, "ilk": …}.
    Sayısı 0 olan çerçeveler yazılmaz; "TÜMÜ" grubu bütün kümedir."""
    derli = cerceve_derle(sozluk)
    n: Counter = Counter()
    grup = defaultdict(Counter)
    gun = defaultdict(Counter)
    ilk = {}
    for r in R:
        g = harita.get(r["src"], DIGER)
        g = diger_etiketi if g == DIGER else g
        n[g] += 1
        n[TUM] += 1
        for c in cerceveler_bul(r["url"], derli):
            grup[g][c] += 1
            grup[TUM][c] += 1
            gun[r["date"][:8]][c] += 1
            if c not in ilk:
                ilk[c] = (r["date"], r["src"], unquote(r["url"])[:160])
    return {"n": dict(n), "grup": {g: dict(v) for g, v in grup.items()},
            "gunluk": {d: dict(v) for d, v in sorted(gun.items())}, "ilk": ilk}
