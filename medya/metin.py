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
# Sözcükle yazılan sayılar. "bir" (belirsiz tanımlık) ve "altı" (yön sözcüğü) çok anlamlı olduğu için yoktur.
# Katlanmamış (tr_lower) metinde aranır: katlanınca "ön" -> "on" (10) olurdu. "yüz" (surat) de çok anlamlıdır.
SAYI_SOZCUKLERI = {"iki": "2", "üç": "3", "dört": "4", "beş": "5", "yedi": "7", "sekiz": "8", "dokuz": "9",
                   "on": "10", "yirmi": "20", "otuz": "30", "kırk": "40", "elli": "50"}
_SOZCUK_KALIP = re.compile(r"\b(" + "|".join(SAYI_SOZCUKLERI) + r")\b")


def sayi_kanonik(s: str) -> str:
    """"1.000" -> "1000", "3,5" -> "3.5", "007" -> "7"."""
    s = s.strip().rstrip(".,")
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    s = s.replace(",", ".")
    if re.fullmatch(r"\d+", s):
        s = str(int(s))
    return s


def sayilari_bul(text: str, haric: list[tuple[int, int]] | None = None, sozcukler: bool = True) -> list[str]:
    """Kanonik sayı dizgeleri. `haric` aralıkları (tarih konumları) atlanır."""
    f = fold_tr(text)
    haric = haric or []
    out = []
    for m in _SAYI.finditer(f):
        if any(m.start() < b and m.end() > a for a, b in haric):
            continue
        out.append(sayi_kanonik(m.group(0)))
    if sozcukler:
        out += [SAYI_SOZCUKLERI[m.group(1)] for m in _SOZCUK_KALIP.finditer(tr_lower(text))
                if not any(m.start() < b and m.end() > a for a, b in haric)]
    return out
