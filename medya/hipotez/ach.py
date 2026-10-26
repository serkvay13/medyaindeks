"""ACH (Analysis of Competing Hypotheses, Heuer 1999).

Ön kayıt: hipotezler kanıta bakılmadan ÖNCE kaydedilir. Kayıt anı ve hipotez kümesinin SHA-256 özeti
saklanır; ilk kanıt bağlandığında küme kilitlenir. Kilitten sonra eklenen hipotez "sonradan eklendi"
olarak işaretlenir (yasak değil, ama okur bunu görür). Kayıtlı kümenin özeti her yüklemede yeniden
hesaplanır; sonradan değiştirilmişse ACHHatasi.

Simetri kuralı: resmi tez her zaman hipotezlerden biridir, asla varsayılan değildir. Hiçbir hipotez
(resmi ya da alternatif) doğru kabul edilmez; sıralama "en az çürütülen" sırasıdır, "doğru" değil.
Resmi tez varsa yanında en az iki rakip hipotez (biri masum ya da yapısal/konjonktürel açıklama) bulunmalıdır.

Matris değerleri: T (tutarlı), Ç (çelişkili), N (nötr / ilgisiz). Sıralama yalnızca ağırlıklı çelişkiye
bakar (Heuer: kanıt bir hipotezi doğrulayamaz, yalnızca çürütebilir). Ağırlık Admiralty derecesinden gelir.
Tanısallık: kanıt tüm hipotezler için aynı değeri alıyorsa ayırt edici değildir (0); farklılaştıkça artar.
"""
import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime

from medya.kanit.kart import KanitKarti

HIPOTEZ_TURLERI = {
    "resmi_tez": "Resmi tez",
    "alternatif": "Alternatif açıklama",
    "yapisal": "Yapısal / jeopolitik açıklama",
    "dis_konjonktur": "Dış konjonktür (bölgesel savaş, büyük güç pazarlığı …)",
    "masum": "Masum açıklama",
    "diger": "Diğer",
}
DEGERLER = {"T": "tutarlı", "Ç": "çelişkili", "N": "nötr"}
_DEGER_ES = {"T": "T", "C": "Ç", "Ç": "Ç", "N": "N", "t": "T", "c": "Ç", "ç": "Ç", "n": "N"}

KAYNAK_AGIRLIK = {"A": 1.0, "B": 0.8, "C": 0.6, "D": 0.4, "E": 0.2, "F": 0.3}
# Bir hipotez bundan az T/Ç değerlendirmesiyle sınanmışsa sıralamadaki yeri güvenilmez sayılır
AZ_KANIT_ESIGI = 2
BILGI_AGIRLIK = {"1": 1.0, "2": 0.8, "3": 0.6, "4": 0.4, "5": 0.2, "6": 0.3}


class ACHHatasi(ValueError):
    pass


def agirlik(kart: KanitKarti) -> float:
    """Admiralty derecesinden kanıt ağırlığı (kaynak × bilgi). F ve 6 "değerlendirilemez" olduğu için
    düşük-orta ağırlık alır; derecelendirilmemiş kanıt güçlü kanıt gibi sayılmasın."""
    return round(KAYNAK_AGIRLIK[kart.kaynak_derecesi] * BILGI_AGIRLIK[kart.bilgi_derecesi], 4)


def _simdi() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class Hipotez:
    id: str
    metin: str
    tur: str = "diger"
    oneren: str = "analist"            # analist | uzman-öneri (LLM) …
    destekleyici_gostergeler: list = field(default_factory=list)
    curutucu_gostergeler: list = field(default_factory=list)
    kayit_zamani: str = ""
    sonradan_eklendi: bool = False

    def __post_init__(self):
        if self.tur not in HIPOTEZ_TURLERI:
            raise ACHHatasi(f"Geçersiz hipotez türü: {self.tur!r} (geçerli: {', '.join(HIPOTEZ_TURLERI)})")
        if not self.id or not self.metin.strip():
            raise ACHHatasi("Hipotezin kimliği ve metni zorunlu")

    def to_dict(self):
        return asdict(self)


def set_ozeti(hipotezler: list[Hipotez]) -> str:
    """Kümenin SHA-256 özeti: kimlik, metin ve tür (zaman ve göstergeler hariç; içerik kilitlenir)."""
    cekirdek = sorted(({"id": h.id, "metin": h.metin.strip(), "tur": h.tur} for h in hipotezler),
                      key=lambda x: x["id"])
    return hashlib.sha256(json.dumps(cekirdek, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


@dataclass
class KirmiziTakim:
    """Şeytanın avukatı: öne çıkan hipotezi çürütmeye çalışan ayrı geçiş (insan ya da ayrı LLM oturumu)."""
    hipotez_id: str
    karsi_argumanlar: list            # [{"arguman": str, "yanit": str, "kanit_ids": [..]}]
    yapan: str                        # "insan: <rol>" | "llm-ayri-oturum: <model>"
    zaman: str = ""

    def to_dict(self):
        return asdict(self)


class ACHMatrisi:
    def __init__(self):
        self.hipotezler: dict[str, Hipotez] = {}
        self.on_kayit: dict = {}               # {"zaman", "ozet", "ids"}
        self.kilit_zamani: str = ""            # ilk kanıt bağlandığı an
        self.hucreler: dict[tuple[str, str], dict] = {}   # (kanit_id, hipotez_id) -> {"deger","gerekce","zaman"}
        self.kirmizi_takim: list[KirmiziTakim] = []

    # ---------------------------------------------------------------- ön kayıt
    def on_kaydet(self, hipotezler: list[Hipotez]) -> str:
        if self.on_kayit:
            raise ACHHatasi("Hipotez kümesi zaten ön kayıtlı; yeni hipotezi `ekle` ile ekleyin "
                            "(sonradan eklendi olarak işaretlenir)")
        if self.hucreler:
            raise ACHHatasi("Kanıt bağlandıktan sonra ön kayıt yapılamaz")
        ids = [h.id for h in hipotezler]
        if len(set(ids)) != len(ids):
            raise ACHHatasi("Hipotez kimlikleri benzersiz olmalı")
        self._simetri_denetimi(hipotezler)
        zaman = _simdi()
        for h in hipotezler:
            h.kayit_zamani = h.kayit_zamani or zaman
            h.sonradan_eklendi = False
            self.hipotezler[h.id] = h
        self.on_kayit = {"zaman": zaman, "ozet": set_ozeti(hipotezler), "ids": ids}
        return self.on_kayit["ozet"]

    @staticmethod
    def _simetri_denetimi(hipotezler: list[Hipotez]):
        if len(hipotezler) < 2:
            raise ACHHatasi("ACH en az iki rakip hipotez ister; tek hipotez sınanamaz")
        resmi = [h for h in hipotezler if h.tur == "resmi_tez"]
        if resmi:
            digerleri = [h for h in hipotezler if h.tur != "resmi_tez"]
            if len(digerleri) < 2:
                raise ACHHatasi("Resmi tez varsayılan olamaz: yanında en az iki rakip hipotez olmalı")
            if not any(h.tur in ("masum", "yapisal", "dis_konjonktur", "alternatif") for h in digerleri):
                raise ACHHatasi("Resmi tezin yanında en az bir alternatif/yapısal/masum açıklama olmalı")

    def ekle(self, h: Hipotez) -> Hipotez:
        """Ön kayıttan sonra hipotez ekler. Kilitten (ilk kanıt bağlama) sonra eklenen 'sonradan eklendi'dir."""
        if not self.on_kayit:
            raise ACHHatasi("Önce hipotez kümesi ön kaydedilmeli (on_kaydet)")
        if h.id in self.hipotezler:
            raise ACHHatasi(f"{h.id} zaten var")
        h.kayit_zamani = _simdi()
        h.sonradan_eklendi = bool(self.kilit_zamani)
        self.hipotezler[h.id] = h
        return h

    def butunluk_denetimi(self) -> None:
        """Ön kayıtlı hipotezlerin metni/türü değiştirilmiş mi?"""
        if not self.on_kayit:
            return
        ilk = [self.hipotezler[i] for i in self.on_kayit["ids"] if i in self.hipotezler]
        if len(ilk) != len(self.on_kayit["ids"]) or set_ozeti(ilk) != self.on_kayit["ozet"]:
            raise ACHHatasi("Ön kayıtlı hipotez kümesi değiştirilmiş: özet uyuşmuyor. Hipotezler veriye "
                            "bakıldıktan sonra yeniden yazılamaz; yeni hipotez ekleyin.")

    # ---------------------------------------------------------------- matris
    def degerlendir(self, kanit_id: str, hipotez_id: str, deger: str, gerekce: str = "") -> None:
        if not self.on_kayit:
            raise ACHHatasi("Hipotezler kanıttan önce kaydedilmeli: önce on_kaydet")
        if hipotez_id not in self.hipotezler:
            raise ACHHatasi(f"Bilinmeyen hipotez: {hipotez_id}")
        d = _DEGER_ES.get(str(deger).strip())
        if not d:
            raise ACHHatasi(f"Geçersiz değer {deger!r}: T, Ç (C) ya da N")
        if not self.kilit_zamani:
            self.kilit_zamani = _simdi()
        self.hucreler[(kanit_id, hipotez_id)] = {"deger": d, "gerekce": gerekce, "zaman": _simdi()}

    def kanit_idleri(self) -> list[str]:
        return sorted({k for k, _ in self.hucreler})

    def deger(self, kanit_id: str, hipotez_id: str) -> str:
        return self.hucreler.get((kanit_id, hipotez_id), {}).get("deger", "N")

    def tanisallik(self, kanit_id: str) -> float:
        """0 = tüm hipotezlerde aynı (ayırt etmez) … 1'e yakın = güçlü ayırt edici."""
        hs = list(self.hipotezler)
        if len(hs) < 2:
            return 0.0
        degerler = [self.deger(kanit_id, h) for h in hs]
        en_cok = max(degerler.count(v) for v in set(degerler))
        return round(1 - en_cok / len(hs), 4) if en_cok < len(hs) else 0.0

    def sirala(self, kartlar: dict[str, KanitKarti]) -> list[dict]:
        """En az çürütülenden en çok çürütülene. Kartı depoda olmayan kanıt sayılmaz (uyarıyla)."""
        self.butunluk_denetimi()
        sonuc = []
        for hid, h in self.hipotezler.items():
            celiski = tutarli = 0.0
            n_c = n_t = 0
            for kid in self.kanit_idleri():
                if kid not in kartlar:
                    continue
                w = agirlik(kartlar[kid])
                d = self.deger(kid, hid)
                tani = self.tanisallik(kid)
                if d == "Ç":
                    celiski += w
                    n_c += 1
                elif d == "T":
                    tutarli += w * tani      # tanısal olmayan "tutarlı" kanıt hiçbir şey söylemez
                    n_t += 1
            sonuc.append({"hipotez_id": hid, "metin": h.metin, "tur": h.tur,
                          "agirlikli_celiski": round(celiski, 4), "celisen_kanit": n_c,
                          "tanisal_tutarlilik": round(tutarli, 4), "tutarli_kanit": n_t,
                          # Az kanıtla sınanmış hipotez "az çürütülmüş" görünür; bu bir kapsam sorunudur
                          "az_kanit": (n_c + n_t) < AZ_KANIT_ESIGI,
                          "sonradan_eklendi": h.sonradan_eklendi})
        # Eşitlikte tür değil kimlik sırası: resmi tez hiçbir zaman eşitlik bozucu değildir
        sonuc.sort(key=lambda r: (r["agirlikli_celiski"], -r["tanisal_tutarlilik"], r["hipotez_id"]))
        for i, r in enumerate(sonuc, 1):
            r["sira"] = i
        return sonuc

    def eksik_kanitlar(self, kartlar: dict[str, KanitKarti]) -> list[str]:
        return [k for k in self.kanit_idleri() if k not in kartlar]

    def guven_onerisi(self, kartlar: dict[str, KanitKarti]) -> str:
        """Analiste öneri (karar değil): kanıt az ya da fark küçükse 'belirlenemedi'."""
        s = self.sirala(kartlar)
        n_kanit = len([k for k in self.kanit_idleri() if k in kartlar])
        if len(s) < 2 or n_kanit < 5 or s[0]["az_kanit"]:
            return "belirlenemedi"
        fark = s[1]["agirlikli_celiski"] - s[0]["agirlikli_celiski"]
        if fark >= 1.5:
            return "büyük olasılıkla"
        if fark >= 0.6:
            return "olası"
        return "belirlenemedi"

    def kirmizi_takim_ekle(self, kt: KirmiziTakim) -> None:
        if kt.hipotez_id not in self.hipotezler:
            raise ACHHatasi(f"Bilinmeyen hipotez: {kt.hipotez_id}")
        if not kt.karsi_argumanlar:
            raise ACHHatasi("Kırmızı takım kaydı en az bir karşı argüman içermeli")
        kt.zaman = kt.zaman or _simdi()
        self.kirmizi_takim.append(kt)

    def onde_gelen_icin_kirmizi_takim(self, kartlar) -> KirmiziTakim | None:
        s = self.sirala(kartlar)
        if not s:
            return None
        lider = s[0]["hipotez_id"]
        return next((k for k in reversed(self.kirmizi_takim) if k.hipotez_id == lider), None)

    def izlenecek_gostergeler(self) -> list[dict]:
        out = []
        for h in self.hipotezler.values():
            out += [{"hipotez_id": h.id, "yon": "destekler", "gosterge": g} for g in h.destekleyici_gostergeler]
            out += [{"hipotez_id": h.id, "yon": "çürütür", "gosterge": g} for g in h.curutucu_gostergeler]
        return out

    # ---------------------------------------------------------------- kalıcılık
    def to_dict(self) -> dict:
        return {"hipotezler": [h.to_dict() for h in self.hipotezler.values()], "on_kayit": self.on_kayit,
                "kilit_zamani": self.kilit_zamani,
                "hucreler": [{"kanit_id": k, "hipotez_id": h, **v} for (k, h), v in self.hucreler.items()],
                "kirmizi_takim": [k.to_dict() for k in self.kirmizi_takim]}

    @classmethod
    def from_dict(cls, d: dict) -> "ACHMatrisi":
        m = cls()
        for h in d.get("hipotezler", []):
            m.hipotezler[h["id"]] = Hipotez(**h)
        m.on_kayit = d.get("on_kayit", {})
        m.kilit_zamani = d.get("kilit_zamani", "")
        for c in d.get("hucreler", []):
            m.hucreler[(c["kanit_id"], c["hipotez_id"])] = {"deger": c["deger"], "gerekce": c.get("gerekce", ""),
                                                            "zaman": c.get("zaman", "")}
        m.kirmizi_takim = [KirmiziTakim(**k) for k in d.get("kirmizi_takim", [])]
        m.butunluk_denetimi()
        return m

    def matris_markdown(self, kartlar: dict[str, KanitKarti]) -> str:
        hs = list(self.hipotezler)
        if not hs:
            return "_Hipotez kaydı yok._"
        bas = "| Kanıt | Derece | Ağırlık | Tanısallık | " + " | ".join(hs) + " |"
        ayr = "|---|---|---|---|" + "---|" * len(hs)
        satirlar = [bas, ayr]
        for kid in self.kanit_idleri():
            k = kartlar.get(kid)
            der = k.derece if k else "—"
            w = f"{agirlik(k):.2f}" if k else "kart yok"
            satirlar.append(f"| `{kid}` | {der} | {w} | {self.tanisallik(kid):.2f} | "
                            + " | ".join(self.deger(kid, h) for h in hs) + " |")
        return "\n".join(satirlar)
