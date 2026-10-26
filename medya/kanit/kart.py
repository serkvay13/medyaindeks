"""Kanıt kartı: tek bir kaynaktan alınmış, derecelendirilmiş tek bir bilgi.

Derece (Admiralty; cases/sources.py ile aynı ölçek):
  kaynak güvenilirliği A (tam güvenilir) … E (güvenilmez), F (değerlendirilemez)
  bilginin doğruluğu   1 (başka kaynakla teyitli) … 5 (olası değil), 6 (değerlendirilemez)

Simetri: resmi açıklama, iktidara yakın, muhalif ya da yabancı yayın — hepsi aynı ölçekten geçer.
Resmi açıklamalar `resmi_aciklama` türünde saklanır ve her yerde "<kurum> iddiası" olarak gösterilir.
"""
import hashlib
import re
from dataclasses import asdict, dataclass, field, fields
from datetime import date

from medya.metin import tarih_tr

TURLER = {
    "haber": "Haber",
    "resmi_aciklama": "Resmi açıklama",
    "mahkeme_kaydi": "Mahkeme kaydı",
    "arastirma_kurumu": "Araştırma kurumu",
    "uluslararasi_basin": "Uluslararası basın",
    "uluslararasi_kurum": "Uluslararası kurum",
    "veri_serisi": "Veri serisi",
    "olay_kaydi": "Olay kaydı",
    "arsiv": "Arşiv",
}
KAYNAK_DERECELERI = {"A": "tam güvenilir", "B": "genellikle güvenilir", "C": "oldukça güvenilir",
                     "D": "genellikle güvenilmez", "E": "güvenilmez", "F": "değerlendirilemez"}
BILGI_DERECELERI = {"1": "başka kaynakla teyitli", "2": "muhtemelen doğru", "3": "olası",
                    "4": "şüpheli", "5": "olası değil", "6": "değerlendirilemez"}
# İçeriği olgu değil, bir tarafın iddiası olarak gösterilmesi gereken türler
IDDIA_TURLERI = {"resmi_aciklama"}
ALINTI_AZAMI = 300
OZET_AZAMI = 600


class KanitHatasi(ValueError):
    """Kanıt kartı geçersiz."""


def kanit_id_uret(url: str, alinti: str) -> str:
    """URL + alıntıdan kararlı kimlik: aynı kaynak ve aynı alıntı her zaman aynı kimliği verir."""
    taban = (url or "").strip() + "\n" + re.sub(r"\s+", " ", (alinti or "")).strip()
    return "k-" + hashlib.sha256(taban.encode("utf-8")).hexdigest()[:12]


def _iso(d, ad: str, zorunlu: bool = False) -> str:
    if d in (None, ""):
        if zorunlu:
            raise KanitHatasi(f"{ad} zorunlu")
        return ""
    if isinstance(d, date):
        return d.isoformat()
    s = str(d).strip()[:10]
    try:
        date.fromisoformat(s)
    except ValueError as e:
        raise KanitHatasi(f"{ad} YYYY-AA-GG biçiminde olmalı: {d!r}") from e
    return s


@dataclass
class KanitKarti:
    tur: str
    kaynak_url: str
    kurum: str                      # yayın ya da kurum adı
    ozet: str                       # kısa açıklama (kendi cümlemizle)
    kaynak_derecesi: str            # A–F
    bilgi_derecesi: str             # 1–6
    alinti: str = ""                # en çok 300 karakter, birebir
    yayin_tarihi: str = ""          # kaynağın yayın tarihi (ISO)
    olay_tarihi: str = ""           # anlatılan olayın tarihi (ISO)
    yayin_grubu: str = ""           # yayın çizgisi grubu …
    yayin_grubu_tarihi: str = ""    # … şu tarihteki …
    yayin_grubu_dayanak: str = ""   # … şu dayanağa göre
    erisim_tarihi: str = ""
    arsiv_url: str = ""
    etiketler: list = field(default_factory=list)   # ör. "bolum:6", "hipotez:H2"
    kanit_id: str = ""

    def __post_init__(self):
        self.tur = (self.tur or "").strip()
        if self.tur not in TURLER:
            raise KanitHatasi(f"Geçersiz kanıt türü: {self.tur!r} (geçerli: {', '.join(TURLER)})")
        if not (self.kaynak_url or "").strip():
            raise KanitHatasi("kaynak_url zorunlu: kaynaksız kanıt kartı olmaz")
        if not (self.kurum or "").strip():
            raise KanitHatasi("kurum/yayın zorunlu")
        if not (self.ozet or "").strip():
            raise KanitHatasi("özet zorunlu")
        if len(self.ozet) > OZET_AZAMI:
            raise KanitHatasi(f"özet en çok {OZET_AZAMI} karakter olmalı (şu an {len(self.ozet)})")
        self.alinti = (self.alinti or "").strip()
        if len(self.alinti) > ALINTI_AZAMI:
            raise KanitHatasi(f"alıntı en çok {ALINTI_AZAMI} karakter olmalı (şu an {len(self.alinti)}); "
                              "telifli metin dışarı aktarılmaz")
        self.kaynak_derecesi = str(self.kaynak_derecesi).strip().upper()
        self.bilgi_derecesi = str(self.bilgi_derecesi).strip()
        if self.kaynak_derecesi not in KAYNAK_DERECELERI:
            raise KanitHatasi(f"Kaynak derecesi A–F olmalı: {self.kaynak_derecesi!r}")
        if self.bilgi_derecesi not in BILGI_DERECELERI:
            raise KanitHatasi(f"Bilgi derecesi 1–6 olmalı: {self.bilgi_derecesi!r}")
        self.yayin_tarihi = _iso(self.yayin_tarihi, "yayin_tarihi")
        self.olay_tarihi = _iso(self.olay_tarihi, "olay_tarihi")
        self.erisim_tarihi = _iso(self.erisim_tarihi or date.today(), "erisim_tarihi")
        self.yayin_grubu_tarihi = _iso(self.yayin_grubu_tarihi, "yayin_grubu_tarihi")
        if self.yayin_grubu and not (self.yayin_grubu_tarihi and self.yayin_grubu_dayanak):
            raise KanitHatasi("Yayın grubu tarihsiz ve dayanaksız yazılamaz: yayin_grubu_tarihi ve "
                              "yayin_grubu_dayanak gerekli (yayın sicili ilkesi)")
        self.etiketler = list(self.etiketler or [])
        beklenen = kanit_id_uret(self.kaynak_url, self.alinti or self.ozet)
        if self.kanit_id and self.kanit_id != beklenen:
            raise KanitHatasi(f"kanit_id içerikle uyuşmuyor ({self.kanit_id} ≠ {beklenen})")
        self.kanit_id = beklenen

    # ------------------------------------------------------------------
    @property
    def derece(self) -> str:
        return f"{self.kaynak_derecesi}{self.bilgi_derecesi}"

    @property
    def iddia_mi(self) -> bool:
        return self.tur in IDDIA_TURLERI

    def baslik(self) -> str:
        """Kartın gösterim başlığı. Resmi açıklama olgu olarak değil, kurumun iddiası olarak görünür."""
        if self.iddia_mi:
            return f"{self.kurum} iddiası"
        return f"{self.kurum} · {TURLER[self.tur]}"

    def grup_metni(self) -> str:
        if not self.yayin_grubu:
            return "grup atanmadı"
        return f"{self.yayin_grubu} ({tarih_tr(self.yayin_grubu_tarihi)} itibarıyla, dayanak: {self.yayin_grubu_dayanak})"

    def dogrulama_metni(self) -> str:
        """Doğrulayıcının sayı, tarih, ad ve alıntı aradığı alanlar (URL bilerek dışarıda: içindeki rakamlar
        uydurma sayıyı geçirebilirdi)."""
        return " \n ".join(x for x in (self.kurum, self.ozet, self.alinti, self.yayin_tarihi, self.olay_tarihi,
                                       self.yayin_grubu) if x)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "KanitKarti":
        adlar = {f.name for f in fields(cls)}
        bilinmeyen = set(d) - adlar
        if bilinmeyen:
            raise KanitHatasi(f"Bilinmeyen alan(lar): {', '.join(sorted(bilinmeyen))}")
        return cls(**{k: v for k, v in d.items() if k in adlar})

    def markdown(self) -> str:
        satir = f"- `{self.kanit_id}` **{self.baslik()}** — {self.derece} " \
                f"({KAYNAK_DERECELERI[self.kaynak_derecesi]} / {BILGI_DERECELERI[self.bilgi_derecesi]})"
        tarih = ", ".join(x for x in (f"yayın {tarih_tr(self.yayin_tarihi)}" if self.yayin_tarihi else "",
                                      f"olay {tarih_tr(self.olay_tarihi)}" if self.olay_tarihi else "") if x)
        satir += f"  \n  {self.ozet}"
        if self.alinti:
            satir += f"  \n  > “{self.alinti}”"
        satir += f"  \n  [{self.kaynak_url}]({self.kaynak_url})"
        if self.arsiv_url:
            satir += f" · [arşiv]({self.arsiv_url})"
        if tarih:
            satir += f" · {tarih}"
        satir += f" · erişim {tarih_tr(self.erisim_tarihi)} · {self.grup_metni()}"
        return satir
