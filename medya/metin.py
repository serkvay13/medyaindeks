"""Türkçe metin yardımcıları: katlama, küçültme, tarih ve sayı ayrıştırma.

`fold_tr` ve `tr_lower` app.py'deki tanımların birebir kopyasıdır. app.py içe aktarıldığında arayüzü
çalıştırdığı için oradan alınamaz; davranış aynı kalmalıdır (tests/test_metin.py denetler).
Düz `.lower()` kullanılmaz: Türkçede "I"/"İ" yanlış küçülür.

Kalıplar kelime başı sınırı kullanır ve joker (`.{1,8}`) içermez. Doğrulayıcının kalıpları yalnızca
Python tarafında çalışır; arama kalıpları (topic_patterns) gibi BigQuery'ye gitmez.
"""
import re
from datetime import date

TR_FOLD = str.maketrans({
    "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u", "â": "a", "î": "i", "û": "u",
    "Ç": "c", "Ğ": "g", "İ": "i", "I": "i", "Ö": "o", "Ş": "s", "Ü": "u", "Â": "a", "Î": "i", "Û": "u",
})


def fold_tr(text: str) -> str:
    """Türkçe karakterleri ASCII'ye indirip küçük harfe çevirir (eşleştirme için)."""
    return (text or "").translate(TR_FOLD).lower()


def tr_lower(text: str) -> str:
    return (text or "").replace("I", "ı").replace("İ", "i").lower()


def tr_capitalize(text: str) -> str:
    """İlk harfi Türkçe kurala göre büyütür ("i" -> "İ")."""
    if not text:
        return text
    ilk = {"i": "İ", "ı": "I"}.get(text[0], text[0].upper())
    return ilk + text[1:]


def normalize(text: str) -> str:
    """Katlanmış, tırnak ve boşlukları sadeleştirilmiş metin (karşılaştırma için)."""
    t = fold_tr(text)
    t = re.sub(r"[“”«»„\"‘’`´]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# --------------------------------------------------------------------------------
# TARİHLER
# --------------------------------------------------------------------------------
TR_AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim",
            "Kasım", "Aralık"]
_AY_NO = {fold_tr(a): i + 1 for i, a in enumerate(TR_AYLAR)}
_AY_KALIP = "|".join(sorted(_AY_NO, key=len, reverse=True))

# Katlanmış metin üzerinde çalışır. Sıra önemlidir: uzun biçimler önce.
_TARIH_KALIPLARI = [
    ("gun_ay_yil", re.compile(rf"\b(\d{{1,2}})\s+({_AY_KALIP})\s+(\d{{4}})\b")),
    ("iso", re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")),
    ("noktali", re.compile(r"\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b")),
    ("ay_yil", re.compile(rf"\b({_AY_KALIP})\s+(\d{{4}})\b")),
    ("gun_ay", re.compile(rf"\b(\d{{1,2}})\s+({_AY_KALIP})\b")),
]


def tarihleri_bul(text: str) -> list[tuple[tuple, tuple[int, int]]]:
    """Metindeki tarihleri bulur. Her öğe ((yil|None, ay, gun|None), (baş, son)) biçimindedir.
    Konumlar katlanmış metin üzerindedir (fold_tr uzunluğu korur)."""
    f = fold_tr(text)
    out, dolu = [], []

    def cakisir(s, e):
        return any(s < b and e > a for a, b in dolu)

    for ad, kalip in _TARIH_KALIPLARI:
        for m in kalip.finditer(f):
            if cakisir(*m.span()):
                continue
            g = m.groups()
            try:
                if ad == "gun_ay_yil":
                    t = (int(g[2]), _AY_NO[g[1]], int(g[0]))
                elif ad == "iso":
                    t = (int(g[0]), int(g[1]), int(g[2]))
                elif ad == "noktali":
                    t = (int(g[2]), int(g[1]), int(g[0]))
                elif ad == "ay_yil":
                    t = (int(g[1]), _AY_NO[g[0]], None)
                else:
                    t = (None, _AY_NO[g[1]], int(g[0]))
                if t[2] is not None and t[0] is not None:
                    date(t[0], t[1], t[2])   # geçersiz tarihleri (31.02) ele
                elif not 1 <= t[1] <= 12:
                    continue
            except (ValueError, KeyError):
                continue
            out.append((t, m.span()))
            dolu.append(m.span())
    return out


def tarih_tr(d) -> str:
    """ISO tarih veya date -> "19 Aralık 2016"."""
    if not d:
        return ""
    if isinstance(d, str):
        d = date.fromisoformat(d[:10])
    return f"{d.day} {TR_AYLAR[d.month - 1]} {d.year}"


# --------------------------------------------------------------------------------
# SAYILAR
# --------------------------------------------------------------------------------
# Rakamla yazılmış sayı: önünde harf/rakam olmayan (H1, A2 gibi kimlikler sayı sayılmaz)
_SAYI = re.compile(r"(?<![\w.,])\d+(?:[.,]\d+)*")
# Sözcükle yazılan sayılar. Tek başına "bir" (belirsiz tanımlık), "altı" (yön sözcüğü) ve "yüz" (surat) çok
# anlamlı olduğu için sayı sayılmaz; ancak bir sayı öbeğinin içinde ("bir milyon", "altı yüz") sayılır.
# Katlanmamış (tr_lower) metinde aranır: katlanınca "ön" -> "on" (10) olurdu.
SAYI_SOZCUKLERI = {"iki": "2", "üç": "3", "dört": "4", "beş": "5", "yedi": "7", "sekiz": "8", "dokuz": "9",
                   "on": "10", "yirmi": "20", "otuz": "30", "kırk": "40", "elli": "50", "altmış": "60",
                   "yetmiş": "70", "seksen": "80", "doksan": "90", "bin": "1000", "milyon": "1000000",
                   "milyar": "1000000000"}
_SOZCUK_KALIP = re.compile(r"(?<![\wçğıöşü])(" + "|".join(sorted(SAYI_SOZCUKLERI, key=len, reverse=True))
                           + r")(?![\wçğıöşü])")
BIRLER = {"bir": 1, "iki": 2, "üç": 3, "dört": 4, "beş": 5, "altı": 6, "yedi": 7, "sekiz": 8, "dokuz": 9}
ONLAR = {"on": 10, "yirmi": 20, "otuz": 30, "kırk": 40, "elli": 50, "altmış": 60, "yetmiş": 70, "seksen": 80,
         "doksan": 90}
BUYUK_CARPANLAR = {"bin": 1000, "milyon": 10 ** 6, "milyar": 10 ** 9, "trilyon": 10 ** 12}
_SAYI_SOZCUK_TUMU = set(BIRLER) | set(ONLAR) | set(BUYUK_CARPANLAR) | {"yüz", "buçuk"}
_KELIME = re.compile(r"[a-zçğıöşüâîû]+")


def _kanonik_deger(v: float) -> str:
    if float(v).is_integer():
        return str(int(v))
    return f"{v:.6f}".rstrip("0").rstrip(".")


def _obek_degeri(sozcukler: list[str]) -> float | None:
    """Türkçe sayı öbeğinin değeri ("bir milyon iki yüz bin" -> 1200000, "dokuz buçuk" -> 9.5).
    Dilbilgisine uymayan öbek (ör. "bir iki", "on yirmi") None döner."""
    toplam, simdiki = 0.0, 0.0
    onceki = None          # son sözcüğün sınıfı: birler | onlar | yuz | buyuk | bucuk
    for s in sozcukler:
        if s in BIRLER:
            if onceki == "birler" or onceki == "bucuk":
                return None
            simdiki += BIRLER[s]
            onceki = "birler"
        elif s in ONLAR:
            if onceki in ("onlar", "birler", "bucuk"):
                return None
            simdiki += ONLAR[s]
            onceki = "onlar"
        elif s == "yüz":
            if onceki in ("yuz", "onlar", "bucuk") or simdiki >= 100:
                return None
            simdiki = (simdiki or 1) * 100
            onceki = "yuz"
        elif s in BUYUK_CARPANLAR:
            if onceki == "buyuk" and BUYUK_CARPANLAR[s] >= 1000:
                return None
            toplam += (simdiki or 1) * BUYUK_CARPANLAR[s]
            simdiki = 0.0
            onceki = "buyuk"
        elif s == "buçuk":
            if onceki is None or onceki == "bucuk":
                return None
            if onceki == "buyuk":
                toplam += 0.5 * max(c for c in BUYUK_CARPANLAR.values() if toplam >= c)
            else:
                simdiki += 0.5
            onceki = "bucuk"
    return toplam + simdiki


def yazili_sayilari_bul(text: str) -> list[tuple[str, tuple[int, int]]]:
    """Yazıyla yazılmış sayı öbekleri: [(kanonik değer, (baş, son)), ...]. Konumlar tr_lower metin
    üzerindedir (uzunluk korunur). Tek sözcüklük çok anlamlı biçimler (bir, altı, yüz) alınmaz; "buçuk"
    tek başına sayı değildir."""
    t = tr_lower(text)
    kelimeler = [(m.group(0), m.span()) for m in _KELIME.finditer(t)]
    out, i = [], 0
    while i < len(kelimeler):
        if kelimeler[i][0] not in _SAYI_SOZCUK_TUMU or kelimeler[i][0] == "buçuk":
            i += 1
            continue
        j = i
        # öbek: aralarında yalnızca boşluk olan ardışık sayı sözcükleri
        while j + 1 < len(kelimeler) and kelimeler[j + 1][0] in _SAYI_SOZCUK_TUMU \
                and t[kelimeler[j][1][1]:kelimeler[j + 1][1][0]].strip() == "":
            j += 1
        sozcukler = [k for k, _ in kelimeler[i:j + 1]]
        span = (kelimeler[i][1][0], kelimeler[j][1][1])
        if len(sozcukler) == 1:
            s = sozcukler[0]
            if s in SAYI_SOZCUKLERI:
                out.append((SAYI_SOZCUKLERI[s], span))
        else:
            v = _obek_degeri(sozcukler)
            if v is not None:
                out.append((_kanonik_deger(v), span))
            else:   # öbek kurulamadı: tek tek bilinen sözcükler
                for k, sp in kelimeler[i:j + 1]:
                    if k in SAYI_SOZCUKLERI:
                        out.append((SAYI_SOZCUKLERI[k], sp))
        i = j + 1
    return out


def sayi_kanonik(s: str) -> str:
    """"1.000" -> "1000", "3,5" -> "3.5", "007" -> "7"."""
    s = s.strip().rstrip(".,")
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    s = s.replace(",", ".")
    if re.fullmatch(r"\d+", s):
        s = str(int(s))
    return s


_RAKAM_CARPAN = re.compile(r"\s+(bin|milyon|milyar|trilyon)(?![\wçğıöşü])")


def sayilari_bul(text: str, haric: list[tuple[int, int]] | None = None, sozcukler: bool = True,
                 genis: bool = False) -> list[str]:
    """Kanonik sayı dizgeleri. `haric` aralıkları (tarih konumları) atlanır.

    "2 bin", "1,5 milyon" gibi rakam + çarpan biçimleri birleşik değer verir (2000, 1500000). `genis=True`
    (kanıt tarafı) ise rakamın kendisini de ekler: kartta "2 bin" yazıyorsa cümledeki "2" de "2000" de geçer.
    """
    f = fold_tr(text)
    t = tr_lower(text)
    haric = haric or []
    out = []
    for m in _SAYI.finditer(f):
        if any(m.start() < b and m.end() > a for a, b in haric):
            continue
        ham = sayi_kanonik(m.group(0))
        c = _RAKAM_CARPAN.match(t, m.end())
        if c:
            try:
                birlesik = _kanonik_deger(float(ham) * BUYUK_CARPANLAR[c.group(1)])
            except ValueError:
                birlesik = None
            if birlesik:
                out.append(birlesik)
                if genis:
                    out.append(ham)
                continue
        out.append(ham)
    if sozcukler:
        for deger, (s, e) in yazili_sayilari_bul(text):
            if any(s < b and e > a for a, b in haric):
                continue
            # rakamdan sonra gelen çarpan ("2 bin") yukarıda birleşik sayıldı
            if t[s:e] in BUYUK_CARPANLAR and re.search(r"\d\s+$", t[:s]):
                continue
            out.append(deger)
    return out


def sayi_tr(deger, ondalik: int | None = None) -> str:
    """Türkçe sayı yazımı: binlik ayırıcı nokta, ondalık ayırıcı virgül (1.429 · 3,42)."""
    s = f"{deger:,}" if ondalik is None else f"{deger:,.{ondalik}f}"
    return s.replace(",", "\0").replace(".", ",").replace("\0", ".")
