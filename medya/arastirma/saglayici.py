"""Arama sağlayıcıları (soyut arayüz + iki uygulama).

- `WebAramaSaglayici`: JSON döndüren bir web arama uç noktası (ör. SearxNG `?q=…&format=json` ya da eşdeğeri).
  Adres `MEDYA_ARAMA_URL` (içinde `{q}` ve isteğe bağlı `{dil}`), anahtar `MEDYA_ARAMA_ANAHTAR` ortam
  değişkeninden okunur; koda yazılmaz. Sonuçlar KART DEĞİLDİR: "arama özeti" erişimli aday kayıtlardır ve
  analist ya da harici ajan sayfayı açıp kartlaştırmadan rapora girmez.
- `ManuelSaglayici` ("manuel / harici ajan" modu): görevleri kart şemalarıyla birlikte `gorevler.json` olarak
  yazar; dışarıda doldurulan kart dosyaları (`<dizin>/kartlar/*.json`) içe aktarıcıyla geri alınır.
"""
import json
import os
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from medya.kanit.ice_aktar import IceAktarimSonucu, klasor_ice_aktar


@dataclass
class AramaSonucu:
    baslik: str
    url: str
    ozet: str
    dil: str = ""
    gorev_id: str = ""

    def to_dict(self):
        return {"baslik": self.baslik, "url": self.url, "ozet": self.ozet, "dil": self.dil, "gorev_id": self.gorev_id,
                "erisim": "arama özeti"}


class AramaSaglayici:
    ad = "temel"

    def ara(self, sorgu: str, dil: str = "tr", en_fazla: int = 10) -> list[AramaSonucu]:
        raise NotImplementedError

    def gorevleri_calistir(self, gorevler: list[dict], en_fazla: int = 10) -> dict[str, list[dict]]:
        out = {}
        for g in gorevler:
            if g.get("tur") != "arama":
                continue
            out[g["id"]] = [dict(s.to_dict(), gorev_id=g["id"]) for s in self.ara(g["sorgu"], g.get("dil", "tr"), en_fazla)]
        return out


class WebAramaSaglayici(AramaSaglayici):
    ad = "web"

    def __init__(self, url_sablonu: str | None = None, anahtar: str | None = None, getir=None):
        self.url_sablonu = url_sablonu or os.environ.get("MEDYA_ARAMA_URL", "")
        self.anahtar = anahtar if anahtar is not None else os.environ.get("MEDYA_ARAMA_ANAHTAR", "")
        self._getir = getir

    def _http(self, url: str) -> dict:
        istek = urllib.request.Request(url, headers={"Accept": "application/json",
                                                     **({"Authorization": f"Bearer {self.anahtar}"} if self.anahtar else {})})
        with urllib.request.urlopen(istek, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))

    def ara(self, sorgu, dil="tr", en_fazla=10):
        if not self.url_sablonu:
            raise RuntimeError("Web araması yapılandırılmadı: MEDYA_ARAMA_URL ortam değişkenini tanımlayın "
                               "(ör. https://arama.ornek/search?q={q}&format=json&language={dil}) ya da manuel modu kullanın")
        url = self.url_sablonu.replace("{q}", urllib.parse.quote(sorgu)).replace("{dil}", dil)
        veri = (self._getir or self._http)(url)
        sonuclar = veri.get("results", veri.get("sonuclar", [])) if isinstance(veri, dict) else veri
        out = []
        for x in sonuclar[:en_fazla]:
            out.append(AramaSonucu(baslik=x.get("title") or x.get("baslik", ""), url=x.get("url", ""),
                                   ozet=x.get("content") or x.get("snippet") or x.get("ozet", ""), dil=dil))
        return out


class ManuelSaglayici(AramaSaglayici):
    """Harici ajan / analist modu: görev dosyası yazar, doldurulan kartları geri alır."""
    ad = "manuel"

    def __init__(self, dizin: str | Path):
        self.dizin = Path(dizin)

    def ara(self, sorgu, dil="tr", en_fazla=10):
        return []          # arama dışarıda yapılır

    def gorevleri_yaz(self, gorevler: list[dict], vaka_id: str = "", talimat: str = "") -> Path:
        self.dizin.mkdir(parents=True, exist_ok=True)
        (self.dizin / "kartlar").mkdir(exist_ok=True)
        veri = {"vaka": vaka_id, "talimat": talimat or (
            "Her görev için kaynağı aç, bulguyu görevin kart şemasıyla tek olgu = tek kart olarak yaz. Alıntı "
            "birebir ve en çok 300 karakter; resmî açıklama kurum iddiasıdır; özel kişiler rolüyle; derece ve erişim "
            "durumunu doldur; kaynaklar arası çelişkiyi 'celiski' alanına yaz. Kartları <dizin>/kartlar/ altına şema "
            "başına bir JSON dosyası olarak koy (K: {\"kartlar\": [...]}, KR: [...], R: [...], RD: {\"kartlar\": [...]})."),
            "gorevler": gorevler}
        yol = self.dizin / "gorevler.json"
        yol.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
        return yol

    def sonuclari_al(self, sema_ayarlari: dict | None = None) -> IceAktarimSonucu:
        return klasor_ice_aktar(self.dizin / "kartlar", sema_ayarlari)
