"""GDELT GKG 2.1 ham dosya indirici (15 dakikalık dosyalar; `fetch.sh` mantığının Python karşılığı).

- Akış: `translation` (çeviri akışı, `*.translation.gkg.csv.zip`; İngilizce dışı kaynaklar) ya da `english`
  (`*.gkg.csv.zip`). Dosya listesi GDELT ana listesinden (masterfile) alınabilir ya da zaman damgasından kurulur.
- Süzme: `TranslationInfo` (26. sütun) `srclc:<dil>` içeren satırlar ve/veya alan adı (4. sütun) verilen
  sonekle (`.tr`) biten satırlar tutulur. GCAM sütunu (18.) boyut nedeniyle boşaltılır.
- Paralel: iş parçacığı havuzu. Devam ettirilebilir: `_durum.json` her zaman damgasının sonucunu tutar
  (tamam / bos / yok / hata); yeniden çalıştırmada yalnızca `hata` ve hiç denenmemiş dosyalar indirilir.
  Süzgeçten satır çıkmayan ya da GDELT'te bulunmayan dosya için boş `.tsv` yazılır ve durumu kaydedilir
  ("boş dosya kaydı"): sayım paydası eksik dosyayı sessizce yutmasın.

Ağ çağrısı `getir` parametresiyle değiştirilebilir (testler ağsız çalışır).

    python -m medya gdelt indir --baslangic 2016-12-17 --bitis 2017-01-10 --cikti data/gdelt/karlov/tr
"""
import io
import json
import os
import threading
import time
import urllib.error
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

TABAN = "http://data.gdeltproject.org/gdeltv2"
ANA_LISTE = {"translation": f"{TABAN}/masterfilelist-translation.txt", "english": f"{TABAN}/masterfilelist.txt"}
SUTUN_SAYISI = 27
I_ALAN, I_GCAM, I_CEVIRI = 3, 17, 25


@dataclass
class IndirmeSonucu:
    durum: dict = field(default_factory=dict)       # zaman damgası -> {"durum", "satir"}

    def say(self) -> dict:
        out: dict = {}
        for v in self.durum.values():
            out[v["durum"]] = out.get(v["durum"], 0) + 1
        return out


def zaman_damgalari(baslangic: date | str, bitis: date | str) -> list[str]:
    """Kapalı aralıktaki bütün 15 dakikalık zaman damgaları (UTC, YYYYMMDDHHMMSS)."""
    b = date.fromisoformat(str(baslangic)) if not isinstance(baslangic, date) else baslangic
    s = date.fromisoformat(str(bitis)) if not isinstance(bitis, date) else bitis
    t, son = datetime(b.year, b.month, b.day), datetime(s.year, s.month, s.day, 23, 45)
    out = []
    while t <= son:
        out.append(t.strftime("%Y%m%d%H%M%S"))
        t += timedelta(minutes=15)
    return out


def dosya_url(ts: str, akis: str = "translation") -> str:
    return f"{TABAN}/{ts}.translation.gkg.csv.zip" if akis == "translation" else f"{TABAN}/{ts}.gkg.csv.zip"


def ana_listeden_urller(metin: str, zamanlar: set[str], akis: str = "translation") -> dict[str, str]:
    """Ana liste satırları: "<boyut> <md5> <url>". Yalnızca GKG dosyaları ve istenen zamanlar."""
    out = {}
    sonek = ".translation.gkg.csv.zip" if akis == "translation" else ".gkg.csv.zip"
    for satir in metin.splitlines():
        p = satir.split()
        if len(p) != 3 or not p[2].endswith(sonek):
            continue
        if akis == "english" and p[2].endswith(".translation.gkg.csv.zip"):
            continue
        ts = p[2].rsplit("/", 1)[1][:14]
        if ts in zamanlar:
            out[ts] = p[2]
    return out


def _http_getir(url: str, deneme: int = 3, zaman_asimi: int = 120) -> bytes | None:
    """İçerik; GDELT'te dosya yoksa (404) None. Geçici hatalarda üç kez dener."""
    son_hata = None
    for i in range(deneme):
        try:
            with urllib.request.urlopen(url, timeout=zaman_asimi) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            son_hata = e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            son_hata = e
        time.sleep(1 + 2 * i)
    raise RuntimeError(f"{url}: {son_hata}")


def satir_suz(satir: str, dil: str | None = "tur", alan_soneki: str | None = ".tr") -> str | None:
    """Tek GKG satırı: süzgeçten geçerse GCAM'ı boşaltılmış satır, geçmezse None."""
    c = satir.rstrip("\n").rstrip("\r").split("\t")
    if len(c) < SUTUN_SAYISI:
        return None
    dil_tutar = bool(dil) and f"srclc:{dil}" in c[I_CEVIRI]
    alan_tutar = bool(alan_soneki) and c[I_ALAN].lower().endswith(alan_soneki)
    if not (dil_tutar or alan_tutar):
        return None
    c[I_GCAM] = ""
    return "\t".join(c)


def zip_suz(icerik: bytes, dil: str | None = "tur", alan_soneki: str | None = ".tr") -> list[str]:
    with zipfile.ZipFile(io.BytesIO(icerik)) as z:
        ad = z.namelist()[0]
        with z.open(ad) as f:
            metin = io.TextIOWrapper(f, encoding="utf-8", errors="replace")
            return [s for s in (satir_suz(x, dil, alan_soneki) for x in metin) if s is not None]


def indir(baslangic, bitis, cikti: str | Path, akis: str = "translation", dil: str | None = "tur",
          alan_soneki: str | None = ".tr", paralel: int = 8, ana_liste: bool = True, getir=None,
          ilerleme=None) -> IndirmeSonucu:
    """Aralıktaki dosyaları indirip süzer; `<cikti>/<ts>.tsv` yazar. Devam ettirilebilir."""
    getir = getir or _http_getir
    cikti = Path(cikti)
    cikti.mkdir(parents=True, exist_ok=True)
    durum_yolu = cikti / "_durum.json"
    durum = json.loads(durum_yolu.read_text(encoding="utf-8")) if durum_yolu.exists() else {}
    zamanlar = zaman_damgalari(baslangic, bitis)
    urller = {ts: dosya_url(ts, akis) for ts in zamanlar}
    if ana_liste:
        try:
            liste = getir(ANA_LISTE[akis])
            if liste:
                urller.update(ana_listeden_urller(liste.decode("utf-8", "replace"), set(zamanlar), akis))
        except RuntimeError:
            pass   # ana liste alınamazsa adlar zaman damgasından kurulur
    yapilacak = [ts for ts in zamanlar if durum.get(ts, {}).get("durum") not in ("tamam", "bos", "yok")]
    kilit = threading.Lock()

    def _is(ts):
        hedef = cikti / f"{ts}.tsv"
        try:
            icerik = getir(urller[ts])
            if icerik is None:
                satirlar, d = [], "yok"
            else:
                satirlar = zip_suz(icerik, dil, alan_soneki)
                d = "tamam" if satirlar else "bos"
            gecici = hedef.with_suffix(".tsv.tmp")
            gecici.write_text("".join(s + "\n" for s in satirlar), encoding="utf-8")
            os.replace(gecici, hedef)
            sonuc = {"durum": d, "satir": len(satirlar)}
        except Exception as e:   # tek dosyanın hatası tüm indirmeyi durdurmaz; sonraki çalıştırmada denenir
            sonuc = {"durum": "hata", "satir": 0, "hata": str(e)[:300]}
        with kilit:
            durum[ts] = sonuc
            if ilerleme:
                ilerleme(ts, sonuc)
        return sonuc

    with ThreadPoolExecutor(max_workers=max(1, paralel)) as ex:
        list(ex.map(_is, yapilacak))
    durum_yolu.write_text(json.dumps(dict(sorted(durum.items())), ensure_ascii=False, indent=0), encoding="utf-8")
    return IndirmeSonucu({ts: durum[ts] for ts in zamanlar if ts in durum})
