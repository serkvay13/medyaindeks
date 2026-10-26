"""Tepki fonksiyonları (katman 1): GDELT olay verisi benzeri tablodan koşullu olasılık.

Soru: A, B'ye karşı Y sınıfı bir eylem yaptıktan sonraki N gün içinde B'nin A'ya karşı X sınıfı eylem
yapma olasılığı, B'nin herhangi bir günü izleyen N günde bunu yapma taban oranından farklı mı?

    P(X | Y) = (B'nin N gün içinde X yaptığı tetik günleri) / (tetik günü sayısı)
    taban    = (B'nin N gün içinde X yaptığı takvim günleri) / (takvim günü sayısı)

Her sonuç n ve Wilson %95 güven aralığı taşır; n olmadan sonuç yoktur. n < 20 "yetersiz" işaretlenir.
Bu bir ilişki ölçüsüdür, nedensellik değildir; GDELT olay kodlaması otomatik ve gürültülüdür
(tasarım belgesi: "eğilim için kullanılır, tek olay kanıtı olarak değil").

Beklenen kolonlar (ad eşlemesiyle değiştirilebilir): tarih, aktor1, aktor2, ve sınıf kolonu
(QuadClass ya da EventRootCode); isteğe bağlı GoldsteinScale.
"""
from dataclasses import asdict, dataclass
from math import sqrt

import pandas as pd

YETERSIZ_N = 20


def wilson(basari: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson skor aralığı (oran için %95 GA). n = 0 ise (0, 1)."""
    if n <= 0:
        return (0.0, 1.0)
    p = basari / n
    payda = 1 + z * z / n
    merkez = (p + z * z / (2 * n)) / payda
    yari = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / payda
    return (round(max(0.0, merkez - yari), 4), round(min(1.0, merkez + yari), 4))


@dataclass
class TepkiSonucu:
    a: str
    b: str
    tetik_sinif: str
    tepki_sinif: str
    n_gun: int
    n: int                    # tetik günü sayısı
    basari: int
    oran: float | None
    ga: tuple
    n_taban: int
    basari_taban: int
    taban_oran: float | None
    ga_taban: tuple
    oran_farki: float | None  # oran / taban (lift)
    goldstein_ort: float | None
    yetersiz: bool
    not_: str = ""

    def to_dict(self):
        return asdict(self)

    def __str__(self):
        if self.oran is None:
            return f"n={self.n}: tetik yok, oran hesaplanamadı"
        y = " — YETERSİZ ÖRNEKLEM (n<20)" if self.yetersiz else ""
        return (f"P({self.b}→{self.a}: {self.tepki_sinif} ≤{self.n_gun} gün | {self.a}→{self.b}: {self.tetik_sinif}) = "
                f"{self.oran:.2f} [%95 GA {self.ga[0]:.2f}–{self.ga[1]:.2f}], n={self.n}; taban {self.taban_oran:.2f} "
                f"[{self.ga_taban[0]:.2f}–{self.ga_taban[1]:.2f}], n={self.n_taban}{y}")


def tepki_olasiligi(df: pd.DataFrame, a: str, b: str, tetik_sinif, tepki_sinif, n_gun: int = 7,
                    sinif_kolonu: str = "QuadClass", tarih="tarih", aktor1="aktor1", aktor2="aktor2",
                    goldstein="GoldsteinScale") -> TepkiSonucu:
    d = df[[c for c in (tarih, aktor1, aktor2, sinif_kolonu, goldstein) if c in df.columns]].copy()
    d[tarih] = pd.to_datetime(d[tarih]).dt.normalize()
    sinif = d[sinif_kolonu].astype(str)
    tetik_gunleri = sorted(set(d.loc[(d[aktor1] == a) & (d[aktor2] == b) & (sinif == str(tetik_sinif)), tarih]))
    tepki_mask = (d[aktor1] == b) & (d[aktor2] == a) & (sinif == str(tepki_sinif))
    tepki_gunleri = pd.DatetimeIndex(sorted(set(d.loc[tepki_mask, tarih])))

    def izleyen(gun) -> bool:
        if not len(tepki_gunleri):
            return False
        bas, son = gun + pd.Timedelta(days=1), gun + pd.Timedelta(days=n_gun)
        return bool(((tepki_gunleri >= bas) & (tepki_gunleri <= son)).any())

    basari = sum(izleyen(g) for g in tetik_gunleri)
    n = len(tetik_gunleri)
    # Taban: kayıt döneminin her takvim günü (son N gün hariç: izleme penceresi dolmaz)
    ilk, son = d[tarih].min(), d[tarih].max() - pd.Timedelta(days=n_gun)
    takvim = pd.date_range(ilk, son, freq="D") if pd.notna(ilk) and son >= ilk else pd.DatetimeIndex([])
    basari_t = sum(izleyen(g) for g in takvim)
    n_t = len(takvim)
    oran = basari / n if n else None
    taban = basari_t / n_t if n_t else None
    gold = None
    if goldstein in d.columns and tepki_mask.any():
        gold = round(float(d.loc[tepki_mask, goldstein].mean()), 3)
    return TepkiSonucu(a=a, b=b, tetik_sinif=str(tetik_sinif), tepki_sinif=str(tepki_sinif), n_gun=n_gun, n=n,
                       basari=basari, oran=None if oran is None else round(oran, 4), ga=wilson(basari, n),
                       n_taban=n_t, basari_taban=basari_t, taban_oran=None if taban is None else round(taban, 4),
                       ga_taban=wilson(basari_t, n_t),
                       oran_farki=round(oran / taban, 3) if oran is not None and taban else None,
                       goldstein_ort=gold, yetersiz=n < YETERSIZ_N,
                       not_="İlişki ölçüsüdür, nedensellik değildir; GDELT olay kodlaması otomatik ve gürültülüdür.")
