"""Vaka sorgusu: indirilmiş Türkçe GKG satırlarından vakanın haber kümesini çıkarır.

- **Geniş küme:** ad alanlarında (URL, V1/V2 kişiler, kurumlar, alıntılar, tüm adlar, sayfa başlığı) vakanın
  ad kalıbı (`ad_kalibi`, ör. "karlov|karlof|карлов") geçen kayıtlar.
- **Çekirdek küme:** geniş kümeden, URL'si (yüzde kodlaması çözülmüş, Türkçe katlanmış) `url_kalibi`ndeki
  anahtar sözcüklerden birini taşıyan kayıtlar; URL'ye göre tekilleştirilir (ilk görülen tutulur).
- **Site-geneli gürültü uyarısı:** URL kalıbı tek başına (ad alanı şartı olmadan) arşivin tamamında çok daha
  fazla kayıt yakalar (başka büyükelçiler, başka suikastlar). Bu fazlalık sayılır ve en çok katkı veren
  sitelerle raporlanır; çekirdek küme bu yüzden ad alanlarıyla kesiştirilir.
- **Payda:** her gün için arşivdeki bütün Türkçe kayıtların sayısı (normalizasyon).

Kalıplar RE2 uyumludur (yalnızca seçenek ve karakter sınıfı; joker yok). Ham dosyalar büyük olduğu için her
dosyanın çıkarımı tek bir önbellek dosyasına satır olarak eklenir (`data/gdelt/onbellek/<kalıp özeti>.jsonl`;
dosya boyutu değişirse yeniden işlenir); kalıp değişirse önbellek dosyası da değişir. Okuma iş parçacıklarıyla
paraleldir; tarama `en_fazla` ile parçalara bölünebilir ve kaldığı yerden sürer.
"""
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

from medya.metin import fold_tr, sayi_tr

ROOT = Path(__file__).resolve().parents[2]
_SATIR = re.compile(r"\r\n|\r|\n")       # metin kipindeki evrensel satır sonu (referans betikle aynı bölme)
_BASLIK = re.compile(r"<PAGE_TITLE>(.*?)</PAGE_TITLE>")
AD_SUTUNLARI = (4, 11, 12, 13, 22, 23, 26)


@dataclass
class VakaSorgusu:
    ad_kalibi: str
    url_kalibi: str
    ham_dizin: Path
    onbellek_koku: Path | None = None
    paralel: int = 16

    def __post_init__(self):
        self.ham_dizin = Path(self.ham_dizin)
        self._ad = re.compile(self.ad_kalibi, re.I)
        self._url = re.compile(self.url_kalibi)
        ozet = hashlib.sha256(f"{self.ad_kalibi}\n{self.url_kalibi}".encode()).hexdigest()[:10]
        self.onbellek = Path(self.onbellek_koku or ROOT / "data" / "gdelt" / "onbellek") / f"{ozet}.jsonl"

    @classmethod
    def ayardan(cls, ayar: dict, ham_dizin: str | Path, **ek) -> "VakaSorgusu":
        return cls(ad_kalibi=ayar["ad_kalibi"], url_kalibi=ayar["url_kalibi"], ham_dizin=ham_dizin, **ek)

    # ------------------------------------------------------------------
    def url_eslesir(self, url: str) -> bool:
        return bool(self._url.search(fold_tr(unquote(url or ""))))

    def _satir_kaydi(self, c: list[str]) -> dict:
        ton = c[15].split(",")
        baslik = _BASLIK.search(c[26] if len(c) > 26 else "")
        return {"date": c[1], "src": c[3], "url": c[4], "themes": c[7], "persons": c[11], "orgs": c[13],
                "tone": float(ton[0]) if ton[0] else None,
                "wc": int(ton[6]) if len(ton) > 6 and ton[6] else None, "locs": c[9], "quotes": c[22],
                "allnames": c[23], "title": baslik.group(1) if baslik else ""}

    def dosya_isle(self, yol: Path) -> dict:
        """Tek ham dosyanın çıkarımı: gün başına satır sayısı, geniş küme satırları, URL-yalnız eşleşmeler."""
        metin = yol.read_bytes().decode("utf-8", errors="replace")
        gun: dict[str, int] = {}
        genis, gurultu_site = [], {}
        for satir in _SATIR.split(metin):
            if satir.count("\t") < 26:
                continue
            bas = satir.split("\t", 5)
            d = bas[1][:8]
            gun[d] = gun.get(d, 0) + 1
            if self._ad.search(satir):
                c = satir.split("\t")
                if self._ad.search(" ".join(c[i] if len(c) > i else "" for i in AD_SUTUNLARI)):
                    genis.append(self._satir_kaydi(c))
                    continue
            if self.url_eslesir(bas[4]):
                gurultu_site[bas[3]] = gurultu_site.get(bas[3], 0) + 1
        return {"dosya": yol.name, "boyut": yol.stat().st_size, "gun": gun, "genis": genis,
                "url_yalniz_site": gurultu_site}

    def _onbellek_oku(self) -> dict[str, dict]:
        out = {}
        if self.onbellek.exists():
            with self.onbellek.open(encoding="utf-8") as f:
                for satir in f:
                    if satir.strip():
                        v = json.loads(satir)
                        out[v["dosya"]] = v       # aynı dosya yeniden işlendiyse son kayıt geçerlidir
        return out

    def _bekleyenler(self, kayitli: dict) -> tuple[list[Path], list[Path]]:
        dosyalar = sorted(self.ham_dizin.glob("*.tsv"))
        with ThreadPoolExecutor(max_workers=self.paralel) as ex:
            boyutlar = list(ex.map(lambda y: y.stat().st_size, dosyalar))
        bekleyen = [y for y, b in zip(dosyalar, boyutlar) if kayitli.get(y.name, {}).get("boyut") != b]
        return dosyalar, bekleyen

    def tara(self, en_fazla: int | None = None, ilerleme=None) -> dict:
        """Ham dosyaları işler (önbellekte olanlar atlanır). `en_fazla` ile parça parça çalıştırılabilir.
        Dönüş: {"islenen", "kalan", "toplam"}."""
        self.onbellek.parent.mkdir(parents=True, exist_ok=True)
        dosyalar, bekleyen = self._bekleyenler(self._onbellek_oku())
        secili = bekleyen[:en_fazla] if en_fazla else bekleyen
        n = 0
        with ThreadPoolExecutor(max_workers=self.paralel) as ex, self.onbellek.open("a", encoding="utf-8") as f:
            for v in ex.map(self.dosya_isle, secili):
                f.write(json.dumps(v, ensure_ascii=False) + "\n")
                n += 1
                if ilerleme:
                    ilerleme(v["dosya"])
        return {"islenen": n, "kalan": len(bekleyen) - n, "toplam": len(dosyalar)}

    def sonuc(self) -> "SorguSonucu":
        """Bütün dosyaların çıkarımını birleştirir; önbellekte eksik dosya varsa önce onları işler."""
        self.tara()
        kayitli = self._onbellek_oku()
        dosyalar = sorted(self.ham_dizin.glob("*.tsv"))
        gun: dict[str, int] = {}
        genis, gurultu = [], {}
        bos = 0
        for y in dosyalar:
            v = kayitli[y.name]
            if v["boyut"] == 0:
                bos += 1
            for d, n in v["gun"].items():
                gun[d] = gun.get(d, 0) + n
            genis += v["genis"]
            for s, n in v["url_yalniz_site"].items():
                gurultu[s] = gurultu.get(s, 0) + n
        return SorguSonucu.kur(self, genis, dict(sorted(gun.items())), gurultu, len(dosyalar), bos)


@dataclass
class SorguSonucu:
    genis: list = field(default_factory=list)
    cekirdek: list = field(default_factory=list)       # tekilleştirilmiş, tarih sıralı
    gun_toplam: dict = field(default_factory=dict)      # gün -> arşivdeki Türkçe kayıt
    gurultu_site: dict = field(default_factory=dict)    # URL kalıbı tek başına: site -> kayıt
    dosya_sayisi: int = 0
    bos_dosya: int = 0

    @classmethod
    def kur(cls, sorgu: VakaSorgusu, genis: list, gun_toplam: dict, gurultu: dict, n_dosya: int,
            bos: int) -> "SorguSonucu":
        gorulen, cekirdek = set(), []
        for r in sorted((r for r in genis if sorgu.url_eslesir(r["url"])), key=lambda r: r["date"]):
            if r["url"] in gorulen:
                continue
            gorulen.add(r["url"])
            cekirdek.append(r)
        return cls(genis=genis, cekirdek=cekirdek, gun_toplam=gun_toplam, gurultu_site=gurultu,
                   dosya_sayisi=n_dosya, bos_dosya=bos)

    def gurultu_uyarisi(self, en_cok: int = 10) -> dict:
        """URL kalıbının ad şartı olmadan yakalayacağı fazladan kayıt sayısı ve en çok katkı veren siteler."""
        toplam = sum(self.gurultu_site.values())
        siteler = sorted(self.gurultu_site.items(), key=lambda x: (-x[1], x[0]))[:en_cok]
        oran = toplam / max(len(self.cekirdek), 1)
        return {"url_yalniz_kayit": toplam, "cekirdek": len(self.cekirdek), "oran": round(oran, 2),
                "siteler": siteler,
                "uyari": (f"URL kalıbı tek başına {sayi_tr(toplam)} kayıt daha yakalıyor (çekirdek kümenin "
                          f"{sayi_tr(oran, 1)} katı); "
                          "bunlar büyük olasılıkla başka olaylara ait. Çekirdek küme bu yüzden ad alanlarıyla "
                          "kesiştirildi.") if toplam else ""}
