"""Aktör profilleri (aktorler/*.toml).

Her kayıt (çıkar, kırmızı çizgi, tipik hamle, anlatı kalıbı) en az bir kaynak (url + tarih) taşımalıdır ve
profilin bir gözden geçirme tarihi olmalıdır. `durum = "aktif"` profilde kaynaksız kayıt bulunursa yükleyici
ProfilHatasi yükseltir. `durum = "taslak"` profiller yüklenir ama raporlara girmez (`raporlanabilir=False`).

Yalnızca kurumlar ve kamusal rolü olan aktörler profillenir; özel kişi profili tutulmaz.

Biçim:
    aktor = "…"          # kurum adı
    tur = "devlet_kurumu" | "uluslararasi_kurum" | "silahli_grup" | "siyasi_parti" | "yabanci_devlet" | "medya" | "diger"
    durum = "taslak" | "aktif"
    gozden_gecirme = "YYYY-AA-GG"
    [[cikarlar]]           metin = "…"; kaynaklar = [{url = "…", tarih = "YYYY-AA-GG"}]
    [[kirmizi_cizgiler]]   …
    [[tipik_hamleler]]     …
    [[anlati_kaliplari]]   …
"""
import tomllib
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AKTOR_DIZINI = ROOT / "aktorler"
AKTOR_TURLERI = ("devlet_kurumu", "uluslararasi_kurum", "silahli_grup", "siyasi_parti", "yabanci_devlet", "medya",
                 "diger")
KAYIT_ALANLARI = ("cikarlar", "kirmizi_cizgiler", "tipik_hamleler", "anlati_kaliplari")


class ProfilHatasi(ValueError):
    pass


@dataclass
class AktorProfili:
    aktor: str
    tur: str
    durum: str
    gozden_gecirme: str
    kayitlar: dict = field(default_factory=dict)    # alan -> [{"metin", "kaynaklar": [{"url","tarih"}]}]
    dosya: str = ""
    kaynaksiz: list = field(default_factory=list)   # taslakta kaynaksız kayıtlar (bilgi için)

    @property
    def raporlanabilir(self) -> bool:
        return self.durum == "aktif" and not self.kaynaksiz

    def gozden_gecirme_gecti(self, bugun: date | None = None) -> bool:
        return date.fromisoformat(self.gozden_gecirme) < (bugun or date.today())


def _kaynak_gecerli(k) -> bool:
    if not isinstance(k, dict):
        return False
    url, tarih = str(k.get("url", "")).strip(), str(k.get("tarih", "")).strip()
    if not url.startswith(("http://", "https://")) or not tarih:
        return False
    try:
        date.fromisoformat(tarih[:10])
    except ValueError:
        return False
    return True


def profil_yukle(yol: str | Path) -> AktorProfili:
    yol = Path(yol)
    d = tomllib.loads(yol.read_text(encoding="utf-8"))
    for alan in ("aktor", "tur", "durum", "gozden_gecirme"):
        if not str(d.get(alan, "")).strip():
            raise ProfilHatasi(f"{yol.name}: '{alan}' zorunlu")
    if d["tur"] not in AKTOR_TURLERI:
        raise ProfilHatasi(f"{yol.name}: geçersiz tür {d['tur']!r}")
    if d["durum"] not in ("taslak", "aktif"):
        raise ProfilHatasi(f"{yol.name}: durum 'taslak' ya da 'aktif' olmalı")
    try:
        date.fromisoformat(str(d["gozden_gecirme"])[:10])
    except ValueError as e:
        raise ProfilHatasi(f"{yol.name}: gozden_gecirme YYYY-AA-GG olmalı") from e
    kayitlar, kaynaksiz = {}, []
    for alan in KAYIT_ALANLARI:
        kayitlar[alan] = []
        for i, k in enumerate(d.get(alan, []) or []):
            metin = str(k.get("metin", "")).strip()
            if not metin:
                raise ProfilHatasi(f"{yol.name}: {alan}[{i}] metinsiz")
            kaynaklar = [x for x in (k.get("kaynaklar") or []) if _kaynak_gecerli(x)]
            if not kaynaklar:
                if d["durum"] == "aktif":
                    raise ProfilHatasi(f"{yol.name}: {alan}[{i}] kaynaksız (url + tarih zorunlu): {metin[:60]}")
                kaynaksiz.append(f"{alan}[{i}]")
            kayitlar[alan].append({"metin": metin, "kaynaklar": kaynaklar})
    return AktorProfili(aktor=d["aktor"], tur=d["tur"], durum=d["durum"],
                        gozden_gecirme=str(d["gozden_gecirme"])[:10], kayitlar=kayitlar, dosya=str(yol),
                        kaynaksiz=kaynaksiz)


def profilleri_yukle(dizin: str | Path | None = None, yalniz_raporlanabilir: bool = False) -> list[AktorProfili]:
    dizin = Path(dizin) if dizin else AKTOR_DIZINI
    out = [profil_yukle(p) for p in sorted(dizin.glob("*.toml"))]
    return [p for p in out if p.raporlanabilir] if yalniz_raporlanabilir else out
