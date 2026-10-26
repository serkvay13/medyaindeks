"""Rapor yazım katmanı: bölüm bazlı, sağlayıcıdan bağımsız LLM yazımı + doğrulama.

İlke: **LLM ölçmez, anlatır.** Her bölüm için yalnızca o bölüme seçilmiş kartlar modele verilir; model
`O` / `D` / `S` türlü cümleler yazar; her cümle

1. kural denetiminden (yasak ifadeler, sürüm anlatımı, hipotezin kişiye atfı, kayıtsız hipotez kodu,
   özel kişi adı) ve
2. doğrulayıcıdan (var olmayan kart kimliği, kartta olmayan sayı/tarih/ad, resmî açıklamanın olgu gibi
   yazılması, olgu cümlesinde niyet fiili, değerlendirmede olasılık terimi)

geçer. Geçmeyen cümle **düşürülür** ve nedeniyle raporlanır; geçenler "**[O]** … [KR-001]." biçiminde
Markdown'a dökülür. Sistem istemi sabit dosyadadır: `medya/uzman/istemler/rapor_yazim.md`.
"""
import json
import re
from dataclasses import dataclass, field

from medya.dogrulayici import Cumle, ad_sozlugu, dogrula
from medya.kanit.kart import TURLER, KanitKarti
from medya.metin import fold_tr
from medya.uzman.adimlar import ISTEM_DIZINI, PAKET_ISARETI, _json_blok
from medya.uzman.saglayici import Saglayici

TUR_KODU = {"O": "olgu", "D": "degerlendirme", "S": "acik_soru"}
KOD_TUR = {v: k for k, v in TUR_KODU.items()}

# (katlanmış metinde kalıp, neden)
YASAK_KALIPLAR = [
    (r"gulen cemaati iddia", "\"Gülen cemaati iddiası\" ifadesi yasak; \"rejim kontrolünde olmayan kaynaklar\" kullanılır"),
    (r"gulen hareketine yakin|gulen yanlisi|gulen'e yakin|gulene yakin",
     "sınıf adı \"rejim kontrolünde olmayan kaynaklar\" olmalı"),
    (r"(?<![a-z])surum(?![a-z])|(?<![a-z])surumu|(?<![a-z])surumde|(?<![a-z])surumun|(?<![a-z])surume"
     r"|(?<![a-z])surumden|(?<![a-z])v[0-9](?![0-9a-z])|(onceki|ilk|yeni|bu|son) versiyon",
     "raporda sürüm/versiyon anlatımı yasak"),
    (r"bu rapor ne degildir|raporun ne olmadigi", "\"Bu rapor ne değildir\" bölümü yasak"),
    (r"(analist|yazar|arastirmaci)\w*\s+(\w+\s+)?(hipotez|tez)", "hipotez kişiye/analiste atfedilemez"),
]
_YASAK = [(re.compile(k), n) for k, n in YASAK_KALIPLAR]
# "Ahmet'in tezi", "Bozkurt'un hipotezi": hipotezin bir kişiye atfı
_KISI_TEZI = re.compile(r"[A-ZÇĞİÖŞÜ][a-zçğıöşü]+['’](n?[ıiuü]n)\s+(hipotez|tez)")
_HIPOTEZ_KODU = re.compile(r"(?<![\w-])(H\d{1,2}[a-z]?)(?![\w])")


@dataclass
class BolumSonucu:
    bolum_id: str
    kabul: list = field(default_factory=list)          # Cumle (paragraf numarası Cumle.guven dışında tutulur)
    red: list = field(default_factory=list)            # {"cumle": {...}, "nedenler": [...]}
    paragraflar: dict = field(default_factory=dict)    # cümle id -> paragraf no
    uyarilar: list = field(default_factory=list)
    kart_sayisi: int = 0

    def markdown(self) -> str:
        return cumleleri_md(self.kabul, self.paragraflar)


def kart_gorunumu(k: KanitKarti, anonim=None) -> dict:
    """Modele giden kart görünümü (özel kişiler rolüyle; resmî açıklama kurum iddiası olarak işaretli)."""
    a = anonim or (lambda x: x)
    d = {"id": k.gorunen_id, "tur": TURLER[k.tur], "kaynak": a(k.kurum), "sinif": k.kaynak_sinifi or "—",
         "yayin_tarihi": k.yayin_tarihi or k.ek.get("yayin_tarihi_ham", ""), "olay_tarihi": k.olay_tarihi,
         "derece": k.derece, "ozet": a(k.ozet), "alinti": a(k.alinti)}
    if k.saat:
        d["saat"] = k.saat
    if k.celiski:
        d["celiski_notu"] = a(k.celiski)
    if k.ek.get("aktor"):
        d["aktor"] = a(k.ek["aktor"])
    if k.iddia_mi:
        d["not"] = "resmî açıklama: kurum iddiası olarak aktar"
    if k.derecesiz:
        d["not"] = (d.get("not", "") + "; " if d.get("not") else "") + \
            f"kronoloji kaydı, Admiralty derecesi yok; erişim: {k.erisim_durumu}"
    return d


def kural_denetimi(metin: str, hipotez_kodlari: set[str], anonim=None) -> list[str]:
    """Yazım kurallarının kodla denetlenebilen kısmı. Boş liste = geçti."""
    f = fold_tr(metin)
    nedenler = [n for k, n in _YASAK if k.search(f)]
    if _KISI_TEZI.search(metin):
        nedenler.append("hipotez kişiye/analiste atfedilemez")
    bilinmeyen = sorted({h for h in _HIPOTEZ_KODU.findall(metin) if h not in hipotez_kodlari})
    if hipotez_kodlari and bilinmeyen:
        nedenler.append(f"kayıtlı olmayan hipotez kodu: {', '.join(bilinmeyen)}")
    if anonim is not None and anonim(metin) != metin:
        nedenler.append("özel kişi adıyla anılmış; rolüyle yazılmalı")
    return nedenler


def cumleleri_md(cumleler: list[Cumle], paragraflar: dict | None = None) -> str:
    """"**[O]** metin [K1], [K2]." biçimi; paragraf numarasına göre gruplanır."""
    paragraflar = paragraflar or {}
    gruplar: dict = {}
    for c in cumleler:
        gruplar.setdefault(paragraflar.get(c.id, 0), []).append(c)
    out = []
    for _, cs in sorted(gruplar.items(), key=lambda x: x[0]):
        parca = []
        for c in cs:
            metin = c.metin.rstrip()
            son = metin[-1] if metin and metin[-1] in ".?!" else "."
            govde = metin[:-1] if metin and metin[-1] in ".?!" else metin
            atif = (" " + ", ".join(f"[{k}]" for k in c.kanit_ids)) if c.kanit_ids else ""
            parca.append(f"**[{KOD_TUR[c.tur]}]** {govde}{atif}{son}")
        out.append(" ".join(parca))
    return "\n\n".join(out)


def bolum_yaz(saglayici: Saglayici, bolum: dict, kartlar: list[KanitKarti], hipotezler: dict | None = None,
              anonim=None, ad_sozlugu_metni=None, max_tokens: int = 4000) -> BolumSonucu:
    """bolum: {"id", "baslik", "amac", "alt_basliklar"}; hipotezler: {"H1": "metin", …}.
    Doğrulama yalnızca bu bölümün kartlarına karşı yapılır: model görmediği karta dayanamaz."""
    hipotezler = hipotezler or {}
    sistem = (ISTEM_DIZINI / "rapor_yazim.md").read_text(encoding="utf-8")
    paket = {"bolum": bolum, "hipotezler": hipotezler, "kartlar": [kart_gorunumu(k, anonim) for k in kartlar]}
    ham = saglayici.tamamla(sistem, f"{PAKET_ISARETI}\n{json.dumps(paket, ensure_ascii=False)}",
                            f"yazim-{bolum.get('id', '')}", max_tokens=max_tokens)
    sonuc = BolumSonucu(bolum_id=str(bolum.get("id", "")), kart_sayisi=len(kartlar))
    veri = _json_blok(ham)
    if not isinstance(veri, dict) or not isinstance(veri.get("cumleler"), list):
        sonuc.red.append({"cumle": {"tur": "", "metin": (ham or "")[:300]}, "nedenler": ["model JSON döndürmedi"]})
        return sonuc
    sozluk = {k.gorunen_id: k for k in kartlar}
    adlar = ad_sozlugu(ad_sozlugu_metni) if ad_sozlugu_metni is not None else None
    adaylar = []
    for i, x in enumerate(veri["cumleler"], 1):
        if not isinstance(x, dict):
            continue
        kod = str(x.get("tur", "")).strip().upper()[:1]
        metin = str(x.get("metin", "")).strip()
        c = Cumle(TUR_KODU.get(kod, kod), metin, x.get("kanit") or x.get("kanit_ids") or [],
                  guven=str(x.get("guven", "")), id=f"{sonuc.bolum_id}-{i}")
        if kod not in TUR_KODU:
            sonuc.red.append({"cumle": c.to_dict(), "nedenler": [f"geçersiz cümle türü: {x.get('tur')!r} (O/D/S)"]})
            continue
        n = kural_denetimi(metin, set(hipotezler), anonim)
        if n:
            sonuc.red.append({"cumle": c.to_dict(), "nedenler": n})
            continue
        try:
            sonuc.paragraflar[c.id] = int(x.get("paragraf", 0) or 0)
        except (TypeError, ValueError):
            sonuc.paragraflar[c.id] = 0
        adaylar.append(c)
    d = dogrula(adaylar, sozluk, ek_adlar="\n".join(f"{h} {m}" for h, m in hipotezler.items()), sozluk=adlar)
    sonuc.kabul = d.kabul
    sonuc.red += [r.to_dict() for r in d.red]
    return sonuc


@dataclass
class YazimSonucu:
    bolumler: dict = field(default_factory=dict)       # bolum_id -> BolumSonucu
    sayac: dict = field(default_factory=dict)

    @property
    def red_sayisi(self) -> int:
        return sum(len(b.red) for b in self.bolumler.values())

    def red_listesi(self) -> list[dict]:
        return [{"bolum": bid, **r} for bid, b in self.bolumler.items() for r in b.red]


def rapor_yaz(saglayici: Saglayici, bolumler: list[dict], kart_secici, hipotezler: dict | None = None,
              anonim=None, tum_kartlar: list[KanitKarti] | None = None, sayac=None) -> YazimSonucu:
    """Her bölüm için `kart_secici(bolum) -> list[KanitKarti]` ile kartları seçer ve yazdırır.
    Küçük harfli ad denetimi için vakanın bütün kartları (`tum_kartlar`) sözlük olarak kullanılır."""
    if sayac is not None and getattr(saglayici, "sayac", None) is None:
        saglayici.sayac = sayac
    metinler = [k.dogrulama_metni() for k in (tum_kartlar or [])] if tum_kartlar else None
    out = YazimSonucu()
    for b in bolumler:
        out.bolumler[str(b["id"])] = bolum_yaz(saglayici, b, kart_secici(b), hipotezler, anonim, metinler)
    if sayac is not None:
        out.sayac = sayac.ozet()
    return out
