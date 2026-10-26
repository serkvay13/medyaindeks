"""Rapor cümlesi: her cümle türünü söyler ve kanıta bağlanır.

    olgu          — kanıt kartında yazan bir şey; en az bir kanıt kimliği zorunlu
    degerlendirme — analitik çıkarım; kanıta ya da olgu cümlesine dayanır, olasılık terimi taşır
    acik_soru     — kanıtın cevaplayamadığı soru
"""
import json
import uuid
from dataclasses import asdict, dataclass, field

CUMLE_TURLERI = ("olgu", "degerlendirme", "acik_soru")
TUR_ETIKETI = {"olgu": "Olgu", "degerlendirme": "Değerlendirme", "acik_soru": "Açık soru"}

# Kent ölçeği (Sherman Kent, "Words of Estimative Probability") — Türkçe karşılıklar, en yüksekten.
# "belirlenemedi": kanıt yetmiyorsa bunu söylemek raporun doğruluğunun parçasıdır.
KENT_OLCEGI = ("neredeyse kesin", "büyük olasılıkla", "olası", "düşük olasılıkla", "olası değil", "belirlenemedi")


@dataclass
class Cumle:
    tur: str
    metin: str
    kanit_ids: list = field(default_factory=list)
    guven: str = ""                                   # değerlendirmede Kent terimi; olguda boş olabilir
    dayanak: list = field(default_factory=list)       # dayandığı olgu cümlelerinin id'leri
    id: str = ""

    def __post_init__(self):
        self.tur = (self.tur or "").strip()
        self.metin = (self.metin or "").strip()
        self.kanit_ids = [str(k).strip() for k in (self.kanit_ids or []) if str(k).strip()]
        self.dayanak = [str(k).strip() for k in (self.dayanak or []) if str(k).strip()]
        self.guven = (self.guven or "").strip()
        if not self.id:
            self.id = "c-" + uuid.uuid4().hex[:8]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Cumle":
        return cls(tur=d.get("tur", ""), metin=d.get("metin", ""), kanit_ids=d.get("kanit_ids", []),
                   guven=d.get("guven", ""), dayanak=d.get("dayanak", []), id=d.get("id", ""))


def cumleler_from_json(veri) -> list[Cumle]:
    """Model çıktısından cümleler: {"cumleler": [...]} veya düz liste ya da bunların JSON metni."""
    if isinstance(veri, str):
        veri = json.loads(veri)
    if isinstance(veri, dict):
        veri = veri.get("cumleler", [])
    return [Cumle.from_dict(d) for d in veri if isinstance(d, dict)]
