"""Özel kişileri rolüyle anma (anonimleştirme).

Kamusal rolü olmayan kişiler (tanıklar, yaralılar, akrabalar, dosyada adı geçen diğer özel kişiler) raporda
adıyla değil rolüyle anılır. Kurallar vaka paketinde (`vakalar/<vaka>/anonimlestirme.json`) sıralı
`[kalıp, yerine]` çiftleri olarak tutulur; sıra önemlidir (uzun/özgül kalıp önce).

Kurallar rapora giden metne (tablo hücreleri, modele giden kart görünümü) uygulanır; kanıt kartının kendisi
değişmez, çünkü birebir alıntı doğrulaması özgün metne karşı yapılır.
"""
import json
import re
from pathlib import Path


class Anonimlestirici:
    def __init__(self, kurallar: list | None = None):
        self.kurallar = [(re.compile(k), y) for k, y in (kurallar or [])]

    @classmethod
    def dosyadan(cls, yol: str | Path | None) -> "Anonimlestirici":
        if not yol or not Path(yol).exists():
            return cls([])
        veri = json.loads(Path(yol).read_text(encoding="utf-8"))
        return cls(veri.get("kurallar", veri) if isinstance(veri, dict) else veri)

    def __call__(self, metin: str | None) -> str | None:
        if not metin:
            return metin
        for k, y in self.kurallar:
            metin = k.sub(y, metin)
        return metin

    def __len__(self):
        return len(self.kurallar)
