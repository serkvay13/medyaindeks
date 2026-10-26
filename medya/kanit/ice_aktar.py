"""Kart dosyası içe aktarıcı: farklı şemalardaki araştırma çıktılarını ortak kanıt modeline (KanitKarti) çevirir.

Desteklenen şemalar (alan adları vaka dosyalarından):

| Şema | Tanıma | Kimlik | Derece | Not |
|---|---|---|---|---|
| `K`  | `{"kartlar": [{"kurum_yayin", "serit", …}]}` | `kanit_id` (K01) | `kaynak_derecesi` + `bilgi_derecesi` | `serit` şerit/tür bilgisidir, sahiplik sınıfı değildir |
| `KR` | `[{"donem", "olay", "saat", …}]` | `"K001"` → `KR-001` | yok → erişim durumu | kronoloji satırı; `celiski` notu taşınır |
| `R`  | `[{"aktor", "ifade_olay", "admiralty", …}]` | `kanit_id` (R01) | `admiralty_kaynak` + `admiralty_bilgi` | aktör ve Türkçe çeviri `ek`'te |
| `RD` | `{"kartlar": [{"olgu", "sinif", "erisim", …}]}` | `kanit_id` (RD01) | `admiralty` (ör. "C3") | |

Her kartta:
- kararlı kimlik (`stabil_id`) korunur; rapor ve doğrulayıcı bu kimlikle atıf yapar;
- Admiralty derecesi yoksa `derecesiz=True` (ACH'de F6 ağırlığı) ve erişim durumu (açıldı / arama özeti /
  bulunamadı / devralındı) taşınır; çelişki notu `celiski` alanına yazılır;
- kaynak sınıfı `medya.kanit.siniflar` kurallarından geçer: "Gülen …" sınıfları "rejim kontrolünde olmayan
  kaynaklar" olur; sahibi değişen yayınların sınıfı yayın tarihine göre düzeltilir (yalnızca sınıf alanı
  sahiplik sınıfı olan şemalarda: KR, R, RD — K'nin `serit` alanı içerik türüdür).

Tarihi ISO olmayan alanlar (ör. "2019-03 (güncelleme 2021-04-02)") uydurulmaz: ISO alan boş kalır, ham değer
`ek["<alan>_ham"]`e yazılır.
"""
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from medya.kanit.kart import ALINTI_AZAMI, OZET_AZAMI, KanitHatasi, KanitKarti
from medya.kanit.siniflar import kurum_temizle, sinif_adlandir, sinif_duzelt

SEMALAR = ("K", "KR", "R", "RD")
# Sınıf alanı yayın sahipliğini anlatan şemalar (sahiplik dönemi düzeltmesi bunlara uygulanır)
VARSAYILAN_SAHIPLIK = {"K": False, "KR": True, "R": True, "RD": True}
_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class IceAktarimHatasi(ValueError):
    pass


@dataclass
class IceAktarimSonucu:
    kartlar: list = field(default_factory=list)          # KanitKarti (dosya sırasıyla)
    uyarilar: list = field(default_factory=list)
    hatalar: list = field(default_factory=list)
    dosyalar: dict = field(default_factory=dict)         # dosya adı -> şema
    hipotezler: dict | None = None                       # hipotezler.json içeriği (varsa)
    ach: dict | None = None                              # ach.json içeriği (varsa)

    def sozluk(self) -> dict[str, KanitKarti]:
        """Görünen (kararlı) kimlik -> kart."""
        return {k.gorunen_id: k for k in self.kartlar}

    def sema(self, ad: str) -> list[KanitKarti]:
        return [k for k in self.kartlar if k.ek.get("_sema") == ad]


# --------------------------------------------------------------------------------
# Şema tanıma
# --------------------------------------------------------------------------------
def sema_tani(veri) -> str | None:
    liste = veri.get("kartlar") if isinstance(veri, dict) else veri
    if not isinstance(liste, list) or not liste or not isinstance(liste[0], dict):
        return None
    ilk = liste[0]
    if {"donem", "olay"} <= set(ilk):
        return "KR"
    if {"aktor", "ifade_olay"} <= set(ilk):
        return "R"
    if {"olgu", "sinif"} <= set(ilk):
        return "RD"
    if {"kurum_yayin", "kaynak_derecesi"} <= set(ilk):
        return "K"
    return None


# --------------------------------------------------------------------------------
# Yardımcılar
# --------------------------------------------------------------------------------
def _tarih(deger, ad: str, ek: dict) -> str:
    s = str(deger or "").strip()
    if not s:
        return ""
    if _ISO.match(s[:10]) and (len(s) == 10 or not s[10:].strip()):
        return s[:10]
    ek[f"{ad}_ham"] = s
    return ""


def _kirp(metin: str, azami: int, ad: str, kimlik: str, uyarilar: list) -> str:
    metin = (metin or "").strip()
    if len(metin) <= azami:
        return metin
    uyarilar.append(f"{kimlik}: {ad} {len(metin)} karakter, {azami} karaktere kırpıldı")
    kesik = metin[:azami]
    return kesik.rsplit(" ", 1)[0] if " " in kesik else kesik


def _tur_k(tur: str, serit: str) -> str:
    t = (tur or "").lower()
    s = (serit or "")
    if "resmi" in t or "resmî" in t or s.startswith("resmi"):
        return "resmi_aciklama"
    if "mahkeme" in t or "iddianame" in t or s.startswith("mahkeme"):
        return "mahkeme_kaydi"
    if "düşünce kuruluşu" in t or s == "düşünce kuruluşu":
        return "arastirma_kurumu"
    if "uluslararası kuruluş" in s:
        return "uluslararasi_kurum"
    if any(x in s for x in ("Batı basını", "Arap", "Avrupa basını", "Rus ")):
        return "uluslararasi_basin"
    return "haber"


def _tur_sinif(sinif: str) -> str:
    s = (sinif or "").lower()
    if "uluslararası kuruluş" in s:
        return "uluslararasi_kurum"
    if "kurum" in s or "resmi" in s or "resmî" in s:
        return "resmi_aciklama"
    if "akademik" in s:
        return "arastirma_kurumu"
    if s.startswith(("yabancı", "rus", "rusya")) or "(ru)" in s:
        return "uluslararasi_basin"
    return "haber"


def _yeniden_adlandir(sinif: str, harita: dict | None) -> str:
    for eski, yeni in (harita or {}).items():
        sinif = sinif.replace(eski, yeni)
    return sinif


def _admiralty(kod: str) -> tuple[str, str]:
    kod = (kod or "").strip().upper()
    if re.fullmatch(r"[A-F][1-6]", kod):
        return kod[0], kod[1]
    raise KanitHatasi(f"Admiralty kodu geçersiz: {kod!r}")


# --------------------------------------------------------------------------------
# Şema dönüştürücüleri: ham kayıt -> KanitKarti alanları
# --------------------------------------------------------------------------------
def _k(x: dict, a: dict, u: list) -> dict:
    ek = {"serit": x.get("serit", ""), "devlet_baglantili": bool(x.get("devlet_baglantili")),
          "tur_ham": x.get("tur", ""), "kurum_ham": x.get("kurum_yayin", ""),
          "bilgi_derecesi_gerekcesi": x.get("bilgi_derecesi_gerekcesi", ""),
          "hipotez_iliskisi": x.get("hipotez_iliskisi") or {}}
    kid = str(x["kanit_id"])
    sinif = sinif_adlandir(x.get("serit"))
    duzeltildi = False
    if a.get("sahiplik"):
        sinif, duzeltildi = sinif_duzelt(x.get("kurum_yayin"), x.get("serit"), x.get("yayin_tarihi"))
    return dict(tur=_tur_k(x.get("tur", ""), x.get("serit", "")), kaynak_url=x.get("kaynak_url", ""),
                kurum=kurum_temizle(x.get("kurum_yayin")) or "—",
                ozet=_kirp(x.get("ozet", ""), OZET_AZAMI, "özet", kid, u),
                alinti=_kirp(x.get("alinti", ""), ALINTI_AZAMI, "alıntı", kid, u),
                yayin_tarihi=_tarih(x.get("yayin_tarihi"), "yayin_tarihi", ek),
                olay_tarihi=_tarih(x.get("olay_tarihi"), "olay_tarihi", ek),
                kaynak_derecesi=str(x.get("kaynak_derecesi", "")), bilgi_derecesi=str(x.get("bilgi_derecesi", "")),
                stabil_id=kid, kaynak_sinifi=_yeniden_adlandir(sinif, a.get("yeniden_adlandir")),
                sinif_duzeltildi=duzeltildi, ek=ek)


def _kr_erisim(dogrulama: str) -> str:
    d = dogrulama or ""
    return "açıldı" if "açıldı" in d else ("arama özeti" if "arama" in d else "bulunamadı")


def _kr(x: dict, a: dict, u: list) -> dict:
    ham_id = str(x["id"])
    kid = "KR-" + ham_id[1:] if re.fullmatch(r"K\d{3}", ham_id) else ham_id
    ek = {"id_ham": ham_id, "sinif_ham": x.get("kaynak_sinifi"), "sinif_notu": x.get("sinif_notu"),
          "saat_turu": x.get("saat_turu", ""), "not_": x.get("not_"), "dogrulama": x.get("dogrulama", ""),
          "yayin_ham": x.get("yayin")}
    if a.get("sahiplik", True):
        sinif, duzeltildi = sinif_duzelt(x.get("yayin"), x.get("kaynak_sinifi"), x.get("yayin_tarihi"))
    else:
        sinif, duzeltildi = sinif_adlandir(x.get("kaynak_sinifi")), False
    sinif = _yeniden_adlandir(sinif, a.get("yeniden_adlandir"))
    return dict(tur=_tur_sinif(x.get("kaynak_sinifi")), kaynak_url=x.get("kaynak_url") or "",
                kurum=(x.get("yayin") or "").strip() or "—",
                ozet=_kirp(x.get("olay", ""), OZET_AZAMI, "özet", kid, u),
                alinti=_kirp(x.get("alinti") or "", ALINTI_AZAMI, "alıntı", kid, u),
                yayin_tarihi=_tarih(x.get("yayin_tarihi"), "yayin_tarihi", ek),
                olay_tarihi=_tarih(x.get("tarih"), "olay_tarihi", ek), kaynak_derecesi="F", bilgi_derecesi="6",
                derecesiz=True, erisim_durumu=_kr_erisim(x.get("dogrulama")), celiski=x.get("celiski") or "",
                stabil_id=kid, kaynak_sinifi=sinif, sinif_duzeltildi=duzeltildi, saat=x.get("saat") or "",
                donem=x.get("donem") or "", ek=ek)


def _r(x: dict, a: dict, u: list) -> dict:
    kid = str(x["kanit_id"])
    ek = {"aktor": x.get("aktor", ""), "tema": x.get("tema", ""), "alinti_tr": x.get("alinti_tr", ""),
          "admiralty_gerekce": x.get("admiralty_gerekce", ""), "dogrulama": x.get("dogrulama", ""),
          "sinif_ham": x.get("kaynak_sinifi", "")}
    if a.get("sahiplik", True):
        sinif, duzeltildi = sinif_duzelt(x.get("yayin"), x.get("kaynak_sinifi"), x.get("yayin_tarihi"))
    else:
        sinif, duzeltildi = sinif_adlandir(x.get("kaynak_sinifi")), False
    ks, bd = (x.get("admiralty_kaynak"), x.get("admiralty_bilgi")) if x.get("admiralty_kaynak") \
        else _admiralty(x.get("admiralty"))
    return dict(tur=_tur_sinif(x.get("kaynak_sinifi")), kaynak_url=x.get("kaynak_url", ""),
                kurum=(x.get("yayin") or "").strip() or "—",
                ozet=_kirp(x.get("ifade_olay", ""), OZET_AZAMI, "özet", kid, u),
                alinti=_kirp(x.get("alinti_orijinal", ""), ALINTI_AZAMI, "alıntı", kid, u),
                yayin_tarihi=_tarih(x.get("yayin_tarihi"), "yayin_tarihi", ek),
                olay_tarihi=_tarih(x.get("tarih"), "olay_tarihi", ek), kaynak_derecesi=str(ks), bilgi_derecesi=str(bd),
                erisim_durumu="açıldı" if "açıldı" in (x.get("dogrulama") or "") else "arama özeti",
                stabil_id=kid, kaynak_sinifi=_yeniden_adlandir(sinif, a.get("yeniden_adlandir")),
                sinif_duzeltildi=duzeltildi, ek=ek)


def _rd_erisim(erisim: str) -> str:
    e = erisim or ""
    if e.startswith("fetch"):
        return "açıldı"
    return "arama özeti" if "arama" in e else "devralındı"


def _rd(x: dict, a: dict, u: list) -> dict:
    kid = str(x["kanit_id"])
    ek = {"tema": x.get("tema", ""), "erisim_ham": x.get("erisim", ""), "teyit": x.get("teyit", ""),
          "admiralty_gerekce": x.get("admiralty_gerekce", ""), "sinif_ham": x.get("sinif", "")}
    if a.get("sahiplik", True):
        sinif, duzeltildi = sinif_duzelt(x.get("yayin"), x.get("sinif"), x.get("yayin_tarihi"))
    else:
        sinif, duzeltildi = sinif_adlandir(x.get("sinif")), False
    ks, bd = _admiralty(x.get("admiralty"))
    return dict(tur=_tur_sinif(x.get("sinif")), kaynak_url=x.get("url", ""), kurum=(x.get("yayin") or "").strip() or "—",
                ozet=_kirp(x.get("olgu", ""), OZET_AZAMI, "özet", kid, u),
                alinti=_kirp(x.get("alinti", ""), ALINTI_AZAMI, "alıntı", kid, u),
                yayin_tarihi=_tarih(x.get("yayin_tarihi"), "yayin_tarihi", ek),
                olay_tarihi=_tarih(x.get("olay_tarihi"), "olay_tarihi", ek), kaynak_derecesi=ks, bilgi_derecesi=bd,
                erisim_durumu=_rd_erisim(x.get("erisim")), stabil_id=kid,
                kaynak_sinifi=_yeniden_adlandir(sinif, a.get("yeniden_adlandir")), sinif_duzeltildi=duzeltildi, ek=ek)


_DONUSTURUCU = {"K": _k, "KR": _kr, "R": _r, "RD": _rd}


# --------------------------------------------------------------------------------
def kayitlari_donustur(veri, sema: str, dosya: str = "", ayar: dict | None = None) -> IceAktarimSonucu:
    """Tek dosyanın içeriğini karta çevirir. `ayar`: {"sahiplik": bool, "yeniden_adlandir": {eski: yeni}}."""
    if sema not in _DONUSTURUCU:
        raise IceAktarimHatasi(f"Bilinmeyen şema: {sema}")
    a = {"sahiplik": VARSAYILAN_SAHIPLIK[sema], **(ayar or {})}
    liste = veri.get("kartlar") if isinstance(veri, dict) else veri
    sonuc = IceAktarimSonucu(dosyalar={dosya: sema})
    for i, x in enumerate(liste or []):
        kimlik = str(x.get("kanit_id") or x.get("id") or f"#{i + 1}")
        try:
            alanlar = _DONUSTURUCU[sema](x, a, sonuc.uyarilar)
            alanlar["ek"] = {**alanlar["ek"], "_sema": sema, "_dosya": dosya, "_sira": i}
            sonuc.kartlar.append(KanitKarti(**alanlar))
        except (KanitHatasi, KeyError, TypeError) as e:
            sonuc.hatalar.append(f"{dosya} {kimlik}: {e}")
    return sonuc


def dosya_ice_aktar(yol: str | Path, ayarlar: dict | None = None, sema: str | None = None) -> IceAktarimSonucu:
    yol = Path(yol)
    veri = json.loads(yol.read_text(encoding="utf-8"))
    sema = sema or sema_tani(veri)
    if not sema:
        raise IceAktarimHatasi(f"{yol.name}: şema tanınamadı (beklenen: {', '.join(SEMALAR)})")
    return kayitlari_donustur(veri, sema, yol.name, (ayarlar or {}).get(sema))


def klasor_ice_aktar(klasor: str | Path, ayarlar: dict | None = None) -> IceAktarimSonucu:
    """Klasördeki bütün kart dosyalarını içe aktarır. hipotezler.json ve ach.json ayrıca okunur.
    Aynı kararlı kimlik iki kez gelirse ikincisi hata olarak raporlanır (kimlik çakışması)."""
    klasor = Path(klasor)
    if not klasor.is_dir():
        raise IceAktarimHatasi(f"Klasör bulunamadı: {klasor}")
    toplam = IceAktarimSonucu()
    gorulen: dict[str, str] = {}
    for yol in sorted(klasor.glob("*.json")):
        veri = json.loads(yol.read_text(encoding="utf-8"))
        if yol.name == "hipotezler.json" or (isinstance(veri, dict) and "hipotezler" in veri and "kartlar" not in veri):
            toplam.hipotezler = veri
            continue
        if yol.name == "ach.json" or (isinstance(veri, dict) and "matris" in veri):
            toplam.ach = veri
            continue
        sema = sema_tani(veri)
        if not sema:
            toplam.uyarilar.append(f"{yol.name}: kart şeması tanınmadı, atlandı")
            continue
        s = kayitlari_donustur(veri, sema, yol.name, (ayarlar or {}).get(sema))
        for k in s.kartlar:
            if k.gorunen_id in gorulen:
                toplam.hatalar.append(f"{yol.name} {k.gorunen_id}: kimlik çakışması ({gorulen[k.gorunen_id]} dosyasında da var)")
                continue
            gorulen[k.gorunen_id] = yol.name
            toplam.kartlar.append(k)
        toplam.uyarilar += s.uyarilar
        toplam.hatalar += s.hatalar
        toplam.dosyalar[yol.name] = sema
    return toplam
