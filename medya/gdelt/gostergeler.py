"""Üç manipülasyon göstergesi (aday üretir, hüküm vermez).

Her gösterge bir **örüntüdür**, kasıt kanıtı değildir; her biri masum açıklamasıyla birlikte raporlanır.

1. **Sessizlik:** bir çerçevenin belirli bir yayın grubunda, kümenin genelindeki payına göre beklenenden çok az
   (ya da hiç) görünmemesi. Beklenen = çerçevenin genel payı × grubun haber sayısı. Beklenen değer küçükse
   (< 1) sonuç "zayıf" işaretlenir.
2. **Eşzamanlı söylem / manşet birliği:** aynı URL sonu (slug) ya da aynı çerçeve, aynı 15 dakikalık GDELT
   dosyasında en az N farklı sitede. Masum açıklama: ajans metninin yeniden yayımı (Türk medyasında olağan).
3. **Atıf aklama adayı:** bir çerçevenin kümede ilk göründüğü dosyadaki URL'lerin yabancı bir kaynağa atıf
   kalıbı taşıması (ör. "-rus-ajansi-"). Masum açıklama: yabancı kaynak bu ihtimali gerçekten dile getirmiş
   olabilir; metin açılmadan ayırt edilemez.
"""
from collections import defaultdict

from medya.gdelt.gruplar import DIGER, alan_grubu_haritasi
from medya.gdelt.istatistik import TUM, cerceve_derle, cerceveler_bul, slug, url_tokenleri

MASUM = {
    "sessizlik": "URL'ye dayalı sayım başlığa taşınmayan çerçeveyi kaçırır; GDELT grubu eksik taramış olabilir; "
                 "grup gündemi başka bir konuya ayırmış olabilir.",
    "manset_birligi": "Aynı ajans metninin (AA, DHA, İHA) birden çok sitede yeniden yayımı olağan bir mekanizmadır; "
                      "tek başına merkezi koordinasyon kanıtı değildir.",
    "cerceve_eszamanliligi": "Aynı anda düşen bir ajans haberi ya da resmî açıklama birçok sitenin aynı çerçeveyi "
                             "aynı dilimde kullanmasını açıklayabilir.",
    "atif_aklama": "Yabancı kaynak bu ihtimali gerçekten dile getirmiş olabilir (konuk yorumcu, muhabir); haber metni "
                   "ve özgün kaynak açılmadan ayırt edilemez.",
}


def sessizlik(cerceve: dict, asgari_toplam: int = 5, asgari_grup: int = 50, esik_oran: float = 0.25) -> list[dict]:
    """cerceve: istatistik["cerceve"] ({"n", "grup"}). Gözlenen/beklenen oranı eşiğin altındaki grup×çerçeve."""
    n_tum = cerceve["n"].get(TUM, 0)
    out = []
    if not n_tum:
        return out
    for c, toplam in cerceve["grup"].get(TUM, {}).items():
        if toplam < asgari_toplam:
            continue
        pay = toplam / n_tum
        for g, n_g in cerceve["n"].items():
            if g == TUM or n_g < asgari_grup:
                continue
            gozlenen = cerceve["grup"].get(g, {}).get(c, 0)
            beklenen = pay * n_g
            oran = gozlenen / beklenen if beklenen else 0.0
            if oran < esik_oran:
                out.append({"gosterge": "sessizlik", "cerceve": c, "grup": g, "n_grup": n_g, "gozlenen": gozlenen,
                            "beklenen": round(beklenen, 2), "oran": round(oran, 2), "zayif": beklenen < 1,
                            "masum_aciklama": MASUM["sessizlik"]})
    return sorted(out, key=lambda x: (x["oran"], -x["beklenen"], x["cerceve"], x["grup"]))


def manset_birligi(cekirdek: list, asgari_site: int = 3, asgari_slug: int = 25) -> list[dict]:
    """Aynı slug, aynı 15 dakikalık dosyada ≥ asgari_site farklı sitede."""
    kume = defaultdict(set)
    for r in cekirdek:
        s = slug(r["url"])
        if len(s) > asgari_slug:
            kume[(r["date"], s)].add(r["src"])
    out = [{"gosterge": "manset_birligi", "dosya_utc": ts, "slug": s, "site_sayisi": len(v), "siteler": sorted(v),
            "masum_aciklama": MASUM["manset_birligi"]} for (ts, s), v in kume.items() if len(v) >= asgari_site]
    return sorted(out, key=lambda x: (-x["site_sayisi"], x["dosya_utc"], x["slug"]))


def cerceve_eszamanliligi(cekirdek: list, sozluk: dict, asgari_site: int = 3) -> list[dict]:
    """Aynı çerçeve, aynı 15 dakikalık dosyada ≥ asgari_site farklı sitede."""
    derli = cerceve_derle(sozluk)
    kume = defaultdict(set)
    url = defaultdict(list)
    for r in cekirdek:
        for c in cerceveler_bul(r["url"], derli):
            kume[(r["date"], c)].add(r["src"])
            url[(r["date"], c)].append(r["url"])
    out = [{"gosterge": "cerceve_eszamanliligi", "dosya_utc": ts, "cerceve": c, "site_sayisi": len(v),
            "siteler": sorted(v), "url_sayisi": len(url[(ts, c)]), "masum_aciklama": MASUM["cerceve_eszamanliligi"]}
           for (ts, c), v in kume.items() if len(v) >= asgari_site]
    return sorted(out, key=lambda x: (x["dosya_utc"], x["cerceve"]))


def atif_aklama_adaylari(cekirdek: list, sozluk: dict, kaliplar: list[str]) -> list[dict]:
    """Her çerçevenin ilk göründüğü dosyadaki URL'lerden yabancı kaynağa atıf kalıbı taşıyanlar."""
    derli = cerceve_derle(sozluk)
    ilk_dosya: dict[str, str] = {}
    for r in cekirdek:                      # çekirdek tarih sıralı
        for c in cerceveler_bul(r["url"], derli):
            ilk_dosya.setdefault(c, r["date"])
    out = []
    for c, ts in ilk_dosya.items():
        for r in cekirdek:
            if r["date"] != ts or c not in cerceveler_bul(r["url"], derli):
                continue
            t = url_tokenleri(r["url"]) + "-"
            eslesen = [k for k in kaliplar if (k if k.endswith("-") else k + "-") in t]
            if eslesen:
                out.append({"gosterge": "atif_aklama", "cerceve": c, "ilk_dosya_utc": ts, "site": r["src"],
                            "url": r["url"], "atif_kalibi": eslesen, "masum_aciklama": MASUM["atif_aklama"]})
    return out


def hepsi(ist: dict, cekirdek: list, ayar: dict) -> dict:
    g = ayar.get("gostergeler", {})
    sozluk = ayar.get("cerceveler", {})
    return {"sessizlik": sessizlik(ist["cerceve"], **g.get("sessizlik", {})),
            "manset_birligi": manset_birligi(cekirdek, g.get("eszamanli", {}).get("asgari_site", 3)),
            "cerceve_eszamanliligi": cerceve_eszamanliligi(cekirdek, sozluk,
                                                           g.get("eszamanli", {}).get("asgari_site", 3)),
            "atif_aklama": atif_aklama_adaylari(cekirdek, sozluk, g.get("atif_kaliplari", [])),
            "not": "Göstergeler örüntü adayıdır; kasıt kanıtı değildir. Her biri masum açıklamasıyla okunur."}


__all__ = ["sessizlik", "manset_birligi", "cerceve_eszamanliligi", "atif_aklama_adaylari", "hepsi", "MASUM",
           "DIGER", "alan_grubu_haritasi"]
