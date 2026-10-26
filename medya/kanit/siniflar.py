"""Kaynak sınıfı normalizasyonu.

İki kural her yerde uygulanır:

1. **Adlandırma:** "Gülen hareketine yakın", "Gülen yanlısı/sürgün" gibi sınıflar her yerde
   "rejim kontrolünde olmayan kaynaklar" olarak yazılır. Bu yayınlar hükümetin denetimi dışındadır; bu,
   iddialarını otomatik olarak doğru kılmaz — her iddia ayrıca derecelendirilir.
2. **Sahiplik dönemi:** Yayın grubu sınıfı tarihsiz değildir. Sahibi değişen yayınların (Hürriyet,
   Hürriyet Daily News, CNN Türk: 2016'da Doğan Grubu, 2018'de Demirören) sınıfı yayın tarihine göre
   düzeltilir ve `sinif_duzeltildi` işaretlenir (raporda † ile gösterilir).

Kurallar veri olarak tutulur; vaka ayarı (`vakalar/<vaka>/vaka.yaml`, `sahiplik_donemleri`) kendi
listesini verebilir.
"""
import re

from medya.metin import fold_tr

REJIM_DISI = "rejim kontrolünde olmayan kaynaklar"
REJIM_DISI_GRUP = "Rejim kontrolünde olmayan kaynaklar"   # yayın grubu adı (büyük harfle)

# Sınıf metninde bu kök geçerse sınıf REJIM_DISI olur (katlanmış metinde aranır)
_GULEN = re.compile(r"(?<![a-z])gulen")

# Yazım birliği: aynı anlama gelen sınıf adları
ETIKET_DUZELTME = {
    "TR hükümet yanlısı basın": "hükümete yakın yayın",
}

# Sahiplik dönemleri. yil_oncesi: bu yıldan önce; yil: tam bu yıl; yil_sonrasi: bu yıldan sonra.
SAHIPLIK_DONEMLERI = [
    {
        "kalip": r"^(Hürriyet|HDN|CNN Türk)",
        "haric": r"Diken",
        "donemler": [
            {"yil_oncesi": 2018, "sinif": "yurt içi ana akım (Doğan dönemi)"},
            {"yil": 2018, "sinif": "yurt içi ana akım/hükümete yakın (2018 geçiş yılı)"},
            {"yil_sonrasi": 2018, "sinif": "hükümete yakın yayın (Demirören dönemi)"},
        ],
    },
]
# Ham sınıf zaten dönemi söylüyorsa (ör. "Doğan grubu dönemi") yeniden düzeltilmez
_DONEM_BELIRTILMIS = re.compile(r"dogan|demiroren")


def sinif_adlandir(sinif: str | None) -> str:
    """Adlandırma kuralı + yazım birliği. Boş sınıf boş döner."""
    s = (sinif or "").strip()
    if not s:
        return ""
    if _GULEN.search(fold_tr(s)):
        return REJIM_DISI
    return ETIKET_DUZELTME.get(s, s)


def grup_adlandir(grup: str) -> str:
    """Yayın grubu adı (büyük harfli) için aynı kural: "Gülen hareketine yakın" → "Rejim kontrolünde …"."""
    return REJIM_DISI_GRUP if _GULEN.search(fold_tr(grup or "")) else grup


def _yil(tarih: str | None) -> int | None:
    m = re.match(r"(\d{4})", (tarih or "").strip())
    return int(m.group(1)) if m else None


def sinif_duzelt(yayin: str | None, sinif: str | None, tarih: str | None,
                 kurallar: list | None = None) -> tuple[str, bool]:
    """(düzeltilmiş sınıf, düzeltildi mi). Önce sahiplik dönemi (yayın adı + yayın yılı), sonra adlandırma.

    >>> sinif_duzelt("Hürriyet", "yurt içi muhalif/bağımsız", "2016-12-20")
    ('yurt içi ana akım (Doğan dönemi)', True)
    """
    y = (yayin or "").strip()
    ham = (sinif or "").strip()
    if not _DONEM_BELIRTILMIS.search(fold_tr(ham)):
        yil = _yil(tarih)
        for kural in (kurallar if kurallar is not None else SAHIPLIK_DONEMLERI):
            if not re.search(kural["kalip"], y) or (kural.get("haric") and re.search(kural["haric"], y)):
                continue
            if yil is None:
                break
            for d in kural["donemler"]:
                if ("yil_oncesi" in d and yil < d["yil_oncesi"]) or ("yil" in d and yil == d["yil"]) or \
                        ("yil_sonrasi" in d and yil > d["yil_sonrasi"]):
                    return d["sinif"], True
            break
    return sinif_adlandir(ham), False


def kurum_temizle(kurum: str | None) -> str:
    """Kurum/yayın adındaki konum etiketlerini ayıklar: "(Gülen hareketine yakın …)", "(hükümet yanlısı)".
    Konum bilgisi kaynak sınıfında tutulur; ad alanı yalnızca yayının adıdır."""
    s = re.sub(r"\s*\((Gülen[^)]*|hükümet yanlısı)\)", "", kurum or "")
    s = re.sub(r"\(Gülen'e yakın; ", "(", s)
    return s.strip()
