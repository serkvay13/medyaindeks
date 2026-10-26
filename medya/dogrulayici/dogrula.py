"""Doğrulayıcı: rapora girecek her cümleyi kanıt kartlarıyla karşılaştırır.

Kurallar (tasarım belgesi, "Rapor motorunda LLM nasıl kullanılır" ve "Uydurma veriyi imkânsız kılmak"):
- olgu: en az bir VAR OLAN kanıt kimliği. Cümledeki her sayı, tarih, tırnak içi alıntı ve büyük harfle
  başlayan ad, atıf yapılan kartların alanlarında (fold_tr ile normalize edilmiş) bulunmalı.
- olgu: niyet fiilleri (kandırdı, amaçladı, planladı, yönlendirdi, gizledi …) yasak. Niyet atfı yalnızca
  ACH sonucunda, değerlendirme cümlesinde ve olasılık diliyle yazılır. Tek istisna: fiil, karttaki alıntıyla
  birebir eşleşen tırnak içindeyse (yani birinin sözü olarak aktarılıyorsa).
- olgu: yalnızca resmi açıklamaya dayanan cümle bir atıf kalıbı taşımalı ("açıkladı", "iddia etti",
  "-e göre" …). Resmi açıklama olgu olarak sunulamaz.
- degerlendirme: en az bir kanıt kimliğine ya da olgu cümlesine dayanmalı; Kent ölçeğinden bir olasılık
  terimi taşımalı. Sayı ve tarihler yine kanıttan gelmeli.
- acik_soru: soru işaretiyle bitmeli; içindeki sayı/tarih/ad vakadaki kanıtlarda geçmeli (soru kılığında
  uydurma olgu sokulamasın).

Geçmeyen cümle rapordan çıkarılır ve gerekçesiyle red listesine yazılır. `kesin_dogrula` tutulan bir cümle
bile geçmezse DogrulamaHatasi yükseltir: rapor bu durumda kurulamaz.
"""
import re
from dataclasses import dataclass, field

from medya.dogrulayici.model import CUMLE_TURLERI, KENT_OLCEGI, Cumle
from medya.kanit.kart import IDDIA_TURLERI, KanitKarti
from medya.metin import fold_tr, normalize, sayilari_bul, tarihleri_bul

# Niyet fiillerinin katlanmış kökleri (kelime başında aranır)
NIYET_KOKLERI = ("kandir", "aldat", "amacla", "amaciyla", "planla", "yonlendir", "gizle", "tezgahla",
                 "kurgula", "manipule", "ortbas", "kasitli", "kasten", "bilerek", "niyetiyle", "kiskirt",
                 "pusu kur", "saklamak ist", "orkestra et")
_NIYET = re.compile(r"\b(" + "|".join(re.escape(k) for k in NIYET_KOKLERI) + r")")

# Resmi açıklamayı iddia olarak çerçeveleyen kalıplar (katlanmış)
ATIF_KALIPLARI = ("acikla", "iddia", "one surdu", "ileri surdu", "belirtti", "bildirdi", "savundu", "dedi",
                  "ifade etti", "duyurdu", "gore", "ifadesiyle", "acikladi", "soyledi", "kaydetti", "aktardi",
                  "ileri suru", "one suru", "beyan")
_ATIF = re.compile(r"\b(" + "|".join(ATIF_KALIPLARI) + r")")

_KENT = [fold_tr(k) for k in KENT_OLCEGI]
# Tırnak içi alıntılar: “…”, "…", «…», ‘…’. Düz tek tırnak Türkçe kesme işareti olduğu için alınmaz.
_TIRNAK = re.compile(r"“([^”]{2,})”|\"([^\"]{2,})\"|«([^»]{2,})»|‘([^’]{2,})’")
# Büyük harfle başlayan sözcükler (Türkçe büyük harfler dahil); kesme işaretinden sonraki ek atılır
_AD = re.compile(r"(?<![\w])([A-ZÇĞİÖŞÜÂÎÛ][A-Za-zÇĞİÖŞÜÂÎÛçğıöşüâîû0-9\-]*)(?:['’][a-zçğıöşüâîû]+)?")
# Cümle başında büyük harfle yazılmış ama ad olmayan yaygın sözcükler (katlanmış)
CUMLE_BASI_SOZCUKLER = frozenset("""
bu bir o su ancak ama fakat ayrica ote yandan buna gore bununla birlikte olay olaydan olayin olayla
resmi resmî mevcut kayitli kayitlarda kanit kanitlar kanitlara mahkeme savcilik dava davada karar kararda
saldiri saldirinin saldirgan saldirganin hipotez hipotezi hipotezin hipotezler hipotezlerden en ilk son
sonra once oncesinde sonrasinda ayni aynı hangi neden nicin nasil kim kimin ne ne zaman nerede hic hicbir
iddia iddiaya iddianame iddianameye rapor raporda veri veriler verilere yetkililer yetkili haber haberde
haberler haberlerde basin basinda medya medyada ana akim bagimsiz uluslararasi kaynak kaynaklar kaynaklara
eldeki elde dis ic yerel bolgesel kamuoyu kamuoyunda tum butun cogu bazi baska diger her hem ya veya
cunku ozellikle yalnizca sadece henuz halen zaten belki muhtemelen eger yine de dolayisiyla bunun
neredeyse buyuk olasi olasilikla dusuk belirlenemedi gostergeler gosterge izlenecek acik soru turk
""".split())


@dataclass
class Red:
    cumle: Cumle
    nedenler: list

    def to_dict(self) -> dict:
        return {"cumle": self.cumle.to_dict(), "nedenler": list(self.nedenler)}

    @classmethod
    def from_dict(cls, d: dict) -> "Red":
        return cls(Cumle.from_dict(d["cumle"]), list(d["nedenler"]))


@dataclass
class DogrulamaSonucu:
    kabul: list = field(default_factory=list)
    red: list = field(default_factory=list)

    @property
    def temiz(self) -> bool:
        return not self.red


class DogrulamaHatasi(RuntimeError):
    """Tutulan cümlelerden en az biri doğrulayıcıdan geçmiyor: rapor kurulamaz."""


# --------------------------------------------------------------------------------
def _tarih_kumesi(metin: str) -> set:
    return {t for t, _ in tarihleri_bul(metin)}


def _tarih_eslesir(t: tuple, kume: set) -> bool:
    """Cümledeki tarih (yıl, ay, gün) kartlardaki bir tarihle uyuşuyor mu? Eksik bileşenler (yılsız
    "19 Aralık", günsüz "Aralık 2016") bilinen bileşenleriyle eşleşir."""
    y, a, g = t
    for (ky, ka, kg) in kume:
        if ka != a:
            continue
        if y is not None and ky is not None and y != ky:
            continue
        if y is not None and ky is None:
            continue
        if g is not None and kg is not None and g != kg:
            continue
        if g is not None and kg is None:
            continue
        return True
    return False


def _sayi_kumesi(metin: str) -> set:
    tarihler = tarihleri_bul(metin)
    kume = set(sayilari_bul(metin, haric=[s for _, s in tarihler]))
    kume |= {str(t[0]) for t, _ in tarihler if t[0]}   # tarihlerin yılları da sayı olarak anılabilir
    return kume


def _ad_bulunur(ad: str, korpus_f: str) -> bool:
    """Ad katlanmış korpusta kelime başı olarak geçiyor mu? Türkçe çekim ekleri için cümledeki sözcüğün
    sonundan en çok 4 harf kırpılarak (kök en az 4 harf ve sözcüğün %70'i kalacak biçimde) yeniden denenir."""
    a = fold_tr(ad)
    en_kisa = max(min(max(4, -(-len(a) * 7 // 10)), len(a)), len(a) - 4)
    for n in range(len(a), en_kisa - 1, -1):
        if re.search(r"(?<![a-z0-9])" + re.escape(a[:n]), korpus_f):
            return True
    return False


def _adlar(metin: str) -> list[str]:
    """Büyük harfli ad adayları; cümle başındaki yaygın sözcükler ve tek harfler atlanır."""
    out = []
    for m in _AD.finditer(metin):
        ad = m.group(1)
        if len(ad) < 2:
            continue
        onceki = metin[:m.start()].rstrip()
        cumle_basi = not onceki or onceki[-1] in ".!?:;—–-(\n"
        if cumle_basi and fold_tr(ad) in CUMLE_BASI_SOZCUKLER:
            continue
        out.append(ad)
    return out


def _tirnaklar(metin: str) -> list[tuple[str, tuple[int, int]]]:
    return [(next(g for g in m.groups() if g), m.span()) for m in _TIRNAK.finditer(metin)]


def _icerik_denetimi(c: Cumle, korpus: str, ad_korpusu: str, nedenler: list) -> list[tuple[int, int]]:
    """Sayı/tarih/alıntı/ad denetimi. Doğrulanmış alıntıların konumlarını döner."""
    korpus_n = normalize(korpus)
    korpus_f = fold_tr(korpus)
    ad_f = fold_tr(ad_korpusu)
    metin = c.metin

    # 1) Alıntılar: birebir (normalize edilmiş) geçmeli
    gecerli_tirnak = []
    for alinti, span in _tirnaklar(metin):
        if normalize(alinti) and normalize(alinti) in korpus_n:
            gecerli_tirnak.append(span)
        else:
            nedenler.append(f"alıntı kanıtta yok: “{alinti}”")
    # Alıntı içindeki ad/sayılar ayrıca aranmaz (alıntı zaten birebir doğrulandı)
    maske = list(metin)
    for s, e in gecerli_tirnak:
        for i in range(s, e):
            maske[i] = " "
    acik = "".join(maske)

    # 2) Tarihler
    kart_tarihleri = _tarih_kumesi(korpus)
    tarihler = tarihleri_bul(acik)
    for t, _ in tarihler:
        if not _tarih_eslesir(t, kart_tarihleri):
            y, a, g = t
            nedenler.append(f"tarih kanıtta yok: {'.'.join(str(x) for x in (g, a, y) if x is not None)}")

    # 3) Sayılar (tarihlerin içindekiler hariç)
    kart_sayilari = _sayi_kumesi(korpus)
    for s in sayilari_bul(acik, haric=[sp for _, sp in tarihler]):
        if s not in kart_sayilari:
            nedenler.append(f"sayı kanıtta yok: {s}")

    # 4) Adlar
    tarih_aylari = {fold_tr(x) for x in ("Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
                                         "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık")}
    for ad in _adlar(acik):
        if fold_tr(ad) in tarih_aylari:
            continue
        if not (_ad_bulunur(ad, korpus_f) or (ad_f and _ad_bulunur(ad, ad_f))):
            nedenler.append(f"ad kanıtta yok: {ad}")
    return gecerli_tirnak


def cumle_dogrula(c: Cumle, kartlar: dict[str, KanitKarti], olgular: dict[str, Cumle] | None = None,
                  ek_adlar: str = "") -> list[str]:
    """Tek cümlenin red nedenleri (boş liste = geçti).

    kartlar: vakanın tüm kanıt kartları (kimlik -> kart)
    olgular: aynı rapordaki kabul edilmiş olgu cümleleri (değerlendirmenin dayanağı için)
    ek_adlar: değerlendirme ve açık sorularda adların aranabileceği ek metin (ör. önceden kayıtlı
              hipotez metinleri). Sayı ve tarihler için KULLANILMAZ.
    """
    olgular = olgular or {}
    nedenler: list[str] = []
    if c.tur not in CUMLE_TURLERI:
        return [f"geçersiz cümle türü: {c.tur!r}"]
    if not c.metin:
        return ["boş cümle"]

    bilinmeyen = [k for k in c.kanit_ids if k not in kartlar]
    if bilinmeyen:
        nedenler.append(f"var olmayan kanıt kimliği: {', '.join(bilinmeyen)}")
    atif = [kartlar[k] for k in c.kanit_ids if k in kartlar]

    if c.tur == "olgu":
        if not atif:
            nedenler.append("olgu cümlesi en az bir geçerli kanıt kimliği taşımalı")
            return nedenler
        korpus = "\n".join(k.dogrulama_metni() for k in atif)
        tirnaklar = _icerik_denetimi(c, korpus, "", nedenler)
        # Niyet fiili: doğrulanmış alıntının içinde değilse yasak
        maske = list(fold_tr(c.metin))
        for s, e in tirnaklar:
            for i in range(s, e):
                maske[i] = " "
        m = _NIYET.search("".join(maske))
        if m:
            nedenler.append(f"olgu cümlesinde niyet atfı yasak: “{c.metin[m.start():m.end() + 6].strip()}…” "
                            "(niyet yalnızca ACH sonucunda, değerlendirme olarak ve olasılık diliyle yazılır)")
        if all(k.tur in IDDIA_TURLERI for k in atif) and not _ATIF.search(fold_tr(c.metin)):
            nedenler.append("yalnızca resmi açıklamaya dayanan cümle olgu gibi yazılmış; "
                            "\"<kurum> açıkladı / iddia etti / -e göre\" biçiminde iddia olarak aktarılmalı")

    elif c.tur == "degerlendirme":
        dayanak_olgu = [olgular[d] for d in c.dayanak if d in olgular]
        eksik = [d for d in c.dayanak if d not in olgular]
        if eksik:
            nedenler.append(f"dayanak olgu cümlesi bulunamadı: {', '.join(eksik)}")
        if not atif and not dayanak_olgu:
            nedenler.append("değerlendirme en az bir kanıta ya da olgu cümlesine dayanmalı")
        f = fold_tr(c.metin)
        if not any(k in f for k in _KENT):
            nedenler.append("değerlendirme Kent ölçeğinden bir olasılık terimi taşımalı "
                            f"({', '.join(KENT_OLCEGI)})")
        if c.guven and fold_tr(c.guven) not in _KENT:
            nedenler.append(f"güven alanı Kent ölçeğinde değil: {c.guven!r}")
        kartlar_hepsi = atif + [kartlar[k] for o in dayanak_olgu for k in o.kanit_ids if k in kartlar]
        korpus = "\n".join([k.dogrulama_metni() for k in kartlar_hepsi] + [o.metin for o in dayanak_olgu])
        _icerik_denetimi(c, korpus, ek_adlar, nedenler)

    else:  # acik_soru
        if not c.metin.rstrip().endswith("?"):
            nedenler.append("açık soru soru işaretiyle bitmeli")
        havuz = atif or list(kartlar.values())
        korpus = "\n".join(k.dogrulama_metni() for k in havuz)
        _icerik_denetimi(c, korpus, ek_adlar, nedenler)
    return nedenler


def dogrula(cumleler: list[Cumle], kartlar: dict[str, KanitKarti], ek_adlar: str = "",
            onceki_olgular: dict[str, Cumle] | None = None) -> DogrulamaSonucu:
    """Cümleleri sırayla doğrular. Önce olgular (değerlendirmeler onlara dayanabilsin)."""
    sonuc = DogrulamaSonucu()
    olgular = dict(onceki_olgular or {})
    for c in [x for x in cumleler if x.tur == "olgu"]:
        n = cumle_dogrula(c, kartlar, olgular, ek_adlar)
        if n:
            sonuc.red.append(Red(c, n))
        else:
            olgular[c.id] = c
    for c in cumleler:
        if c.tur == "olgu":
            continue
        n = cumle_dogrula(c, kartlar, olgular, ek_adlar)
        if n:
            sonuc.red.append(Red(c, n))
    reddedilen = {r.cumle.id for r in sonuc.red}
    sonuc.kabul = [c for c in cumleler if c.id not in reddedilen]
    return sonuc


def kesin_dogrula(cumleler: list[Cumle], kartlar: dict[str, KanitKarti], ek_adlar: str = "",
                  onceki_olgular: dict[str, Cumle] | None = None) -> None:
    """Tutulan cümlelerin hepsi geçmeli; biri bile geçmezse rapor kurulmaz."""
    s = dogrula(cumleler, kartlar, ek_adlar, onceki_olgular)
    if s.red:
        ozet = "; ".join(f"{r.cumle.id}: {', '.join(r.nedenler)}" for r in s.red[:5])
        raise DogrulamaHatasi(f"{len(s.red)} cümle doğrulayıcıdan geçmedi, rapor kurulamaz: {ozet}")
