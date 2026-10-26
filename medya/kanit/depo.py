"""Kanıt deposu (DuckDB). Yol `MEDYA_KANIT_DB` ortam değişkeniyle değiştirilebilir;
varsayılan `data/store/kanit.duckdb` (git dışı)."""
import json
import os
from pathlib import Path

import duckdb

from medya.kanit.kart import KanitHatasi, KanitKarti

ROOT = Path(__file__).resolve().parents[2]

_SEMA = """
CREATE TABLE IF NOT EXISTS kanit (
    kanit_id VARCHAR PRIMARY KEY,
    tur VARCHAR NOT NULL,
    kaynak_url VARCHAR NOT NULL,
    kurum VARCHAR NOT NULL,
    yayin_grubu VARCHAR, yayin_grubu_tarihi VARCHAR, yayin_grubu_dayanak VARCHAR,
    yayin_tarihi VARCHAR, olay_tarihi VARCHAR,
    ozet VARCHAR NOT NULL,
    alinti VARCHAR,
    kaynak_derecesi VARCHAR NOT NULL,
    bilgi_derecesi VARCHAR NOT NULL,
    erisim_tarihi VARCHAR, arsiv_url VARCHAR,
    etiketler VARCHAR            -- JSON listesi
);
CREATE TABLE IF NOT EXISTS kanit_vaka (
    vaka_id VARCHAR NOT NULL,
    kanit_id VARCHAR NOT NULL,
    alt_soru VARCHAR DEFAULT '',  -- derinleştirme sorusuyla eklendiyse sorunun kimliği
    PRIMARY KEY (vaka_id, kanit_id)
);
"""
# İçe aktarılan kart dosyalarının alanları (sonradan eklendi; eski depolara ALTER ile eklenir)
_EK_KOLONLAR = {"stabil_id": "VARCHAR", "erisim_durumu": "VARCHAR", "celiski": "VARCHAR", "kaynak_sinifi": "VARCHAR",
                "sinif_duzeltildi": "BOOLEAN", "derecesiz": "BOOLEAN", "saat": "VARCHAR", "donem": "VARCHAR",
                "ek": "VARCHAR"}
_JSON_KOLONLAR = ("etiketler", "ek")
_KOLONLAR = ["kanit_id", "tur", "kaynak_url", "kurum", "yayin_grubu", "yayin_grubu_tarihi", "yayin_grubu_dayanak",
             "yayin_tarihi", "olay_tarihi", "ozet", "alinti", "kaynak_derecesi", "bilgi_derecesi", "erisim_tarihi",
             "arsiv_url", "etiketler"] + list(_EK_KOLONLAR)


def varsayilan_yol() -> Path:
    return Path(os.environ.get("MEDYA_KANIT_DB", ROOT / "data" / "store" / "kanit.duckdb"))


class KanitDeposu:
    def __init__(self, yol: str | Path | None = None):
        self.yol = str(yol) if yol is not None else str(varsayilan_yol())
        if self.yol != ":memory:":
            Path(self.yol).parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(self.yol)
        self.con.execute(_SEMA)
        for ad, tip in _EK_KOLONLAR.items():
            self.con.execute(f"ALTER TABLE kanit ADD COLUMN IF NOT EXISTS {ad} {tip}")

    def kapat(self):
        self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.kapat()

    # ------------------------------------------------------------------
    def ekle(self, kart: KanitKarti, vaka_id: str | None = None, alt_soru: str = "") -> bool:
        """Kartı ekler (aynı kimlik varsa içeriği değiştirmez). Vaka verilirse vakaya bağlar.
        Yeni kart eklendiyse True."""
        var = self.con.execute("SELECT 1 FROM kanit WHERE kanit_id = ?", [kart.kanit_id]).fetchone()
        if not var:
            d = kart.to_dict()
            for k in _JSON_KOLONLAR:
                d[k] = json.dumps(d[k], ensure_ascii=False)
            self.con.execute(f"INSERT INTO kanit ({', '.join(_KOLONLAR)}) VALUES ({', '.join('?' * len(_KOLONLAR))})",
                             [d[k] for k in _KOLONLAR])
        if vaka_id:
            self.con.execute("INSERT INTO kanit_vaka (vaka_id, kanit_id, alt_soru) VALUES (?, ?, ?) "
                             "ON CONFLICT DO NOTHING", [vaka_id, kart.kanit_id, alt_soru or ""])
        return not var

    def _kart(self, satir) -> KanitKarti:
        d = dict(zip(_KOLONLAR, satir))
        d["etiketler"] = json.loads(d["etiketler"] or "[]")
        d["ek"] = json.loads(d["ek"] or "{}")
        d = {k: (v if v is not None else "") for k, v in d.items()}
        d["sinif_duzeltildi"] = bool(d["sinif_duzeltildi"])
        d["derecesiz"] = bool(d["derecesiz"])
        return KanitKarti.from_dict(d)

    def getir(self, kanit_id: str) -> KanitKarti | None:
        r = self.con.execute(f"SELECT {', '.join(_KOLONLAR)} FROM kanit WHERE kanit_id = ?", [kanit_id]).fetchone()
        return self._kart(r) if r else None

    def var_mi(self, kanit_id: str) -> bool:
        return bool(self.con.execute("SELECT 1 FROM kanit WHERE kanit_id = ?", [kanit_id]).fetchone())

    def vaka_kartlari(self, vaka_id: str, alt_soru: str | None = None) -> list[KanitKarti]:
        sql = (f"SELECT {', '.join('k.' + c for c in _KOLONLAR)} FROM kanit k JOIN kanit_vaka v USING (kanit_id) "
               "WHERE v.vaka_id = ?")
        par = [vaka_id]
        if alt_soru is not None:
            sql += " AND v.alt_soru = ?"
            par.append(alt_soru)
        sql += " ORDER BY k.olay_tarihi, k.yayin_tarihi, k.kanit_id"
        return [self._kart(r) for r in self.con.execute(sql, par).fetchall()]

    def vaka_sozluk(self, vaka_id: str, gorunen: bool = False) -> dict[str, KanitKarti]:
        """Kimlik -> kart. `gorunen=True` ise anahtar kararlı kimliktir (KR-001); raporda atıf böyle yapılır."""
        return {(k.gorunen_id if gorunen else k.kanit_id): k for k in self.vaka_kartlari(vaka_id)}

    def alt_soru_haritasi(self, vaka_id: str) -> dict[str, str]:
        return dict(self.con.execute("SELECT kanit_id, alt_soru FROM kanit_vaka WHERE vaka_id = ?",
                                     [vaka_id]).fetchall())

    # ------------------------------------------------------------------
    def disa_aktar(self, vaka_id: str, yol: str | Path) -> int:
        kartlar = self.vaka_kartlari(vaka_id)
        harita = self.alt_soru_haritasi(vaka_id)
        veri = {"vaka_id": vaka_id, "kartlar": [{**k.to_dict(), "_alt_soru": harita.get(k.kanit_id, "")}
                                                for k in kartlar]}
        Path(yol).write_text(json.dumps(veri, ensure_ascii=False, indent=2), encoding="utf-8")
        return len(kartlar)

    def ice_aktar(self, yol: str | Path, vaka_id: str | None = None) -> tuple[int, list[str]]:
        """JSON'dan kart yükler: {"kartlar": [...]} ya da düz liste. Geçersiz kartlar eklenmez,
        nedenleriyle döner. (eklenen sayısı, hatalar)"""
        veri = json.loads(Path(yol).read_text(encoding="utf-8"))
        liste = veri["kartlar"] if isinstance(veri, dict) else veri
        vaka_id = vaka_id or (veri.get("vaka_id") if isinstance(veri, dict) else None)
        n, hatalar = 0, []
        for i, d in enumerate(liste):
            d = dict(d)
            alt = d.pop("_alt_soru", "")
            try:
                kart = KanitKarti.from_dict(d)
            except (KanitHatasi, TypeError) as e:
                hatalar.append(f"#{i + 1}: {e}")
                continue
            n += self.ekle(kart, vaka_id=vaka_id, alt_soru=alt)
        return n, hatalar
