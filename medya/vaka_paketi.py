"""Vaka paketi: depoda sürümlenen, bir vakanın yeniden üretilebilir girdileri (`vakalar/<vaka>/`).

    vakalar/<vaka>/vaka.yaml            vaka ayarı (ad, olay tarihi, rapor künyesi, şema ayarları, tablo etiketleri)
    vakalar/<vaka>/kartlar/*.json       araştırma kart dosyaları (K/KR/R/RD şemaları; medya.kanit.ice_aktar)
    vakalar/<vaka>/kartlar/hipotezler.json, ach.json
    vakalar/<vaka>/anonimlestirme.json  özel kişileri rolüyle anma kuralları
    vakalar/<vaka>/gdelt.yaml           GDELT vaka sorgusu: tarih aralığı, kalıplar, çerçeve sözlüğü
    vakalar/<vaka>/gdelt/               hesaplanmış GDELT istatistikleri (ham veri depoda yoktur)
    vakalar/<vaka>/ach_matris.yaml      tanısal kanıt satırları (E01…) ve ağırlık ölçeği
    vakalar/<vaka>/celiskiler.yaml      kaynaklar arası çelişki kayıtları
    vakalar/<vaka>/anlati/*.md          çevrimdışı mod anlatı metinleri (yer tutuculu)

Çalışma alanı (`medya.vaka.Vaka`, git dışı) ile karıştırılmamalı: paket girdidir, çalışma alanı durumdur.
"""
from functools import cached_property
from pathlib import Path

from medya.ayar import ilk_bulunan, yukle
from medya.kanit.anonim import Anonimlestirici
from medya.kanit.ice_aktar import IceAktarimSonucu, klasor_ice_aktar

ROOT = Path(__file__).resolve().parents[1]
PAKET_KOKU = ROOT / "vakalar"


class PaketHatasi(ValueError):
    pass


class VakaPaketi:
    def __init__(self, vaka_id: str, kok: str | Path | None = None):
        self.id = vaka_id
        self.dizin = Path(kok or PAKET_KOKU) / vaka_id
        yol = ilk_bulunan(self.dizin, "vaka")
        if not yol:
            raise PaketHatasi(f"Vaka paketi bulunamadı: {self.dizin} (vaka.yaml yok)")
        self.ayar = yukle(yol)

    # ------------------------------------------------------------------
    def yol(self, *parca) -> Path:
        return self.dizin.joinpath(*parca)

    def alt_ayar(self, ad: str, varsayilan=None):
        p = ilk_bulunan(self.dizin, ad)
        return yukle(p) if p else ({} if varsayilan is None else varsayilan)

    @cached_property
    def ice_aktarim(self) -> IceAktarimSonucu:
        return klasor_ice_aktar(self.yol(self.ayar.get("kart_klasoru", "kartlar")), self.ayar.get("sema_ayarlari"))

    @property
    def kartlar(self) -> dict:
        return self.ice_aktarim.sozluk()

    @cached_property
    def anonim(self) -> Anonimlestirici:
        return Anonimlestirici.dosyadan(self.yol("anonimlestirme.json"))

    @property
    def olay_tarihi(self) -> str:
        return str(self.ayar["olay_tarihi"])

    def anlati(self, ad: str) -> str | None:
        p = self.yol("anlati", f"{ad}.md")
        return p.read_text(encoding="utf-8") if p.exists() else None


def paketler(kok: str | Path | None = None) -> list[str]:
    k = Path(kok or PAKET_KOKU)
    return sorted(p.parent.name for p in k.glob("*/vaka.yaml"))


# --------------------------------------------------------------------------------
def vakaya_aktar(klasor: str | Path, vaka_id: str, depo, kok_calisma=None, ayar: dict | None = None) -> dict:
    """Kart klasörünü çalışma alanındaki bir vakaya aktarır (`python -m medya vaka-ice-aktar`).

    - Ayar: `ayar` verilmişse o; yoksa klasörün üstünde ya da içinde `vaka.yaml` varsa (paket yapısı) okunur;
      yoksa varsayılanlar.
    - Vaka çalışma alanında yoksa oluşturulur (olay tarihi ayardan ya da kartlardan gelmezse hata).
    - hipotezler.json varsa ve vaka henüz ön kayıtlı değilse ön kayıt yapılır — kartlar depoya
      bağlanmadan ÖNCE (hipotez önce, kanıt sonra).
    - Kartlar kararlı kimlikleriyle kanıt deposuna eklenir ve vakaya bağlanır.
    """
    import json

    from medya.hipotez.kayit import matrise_kaydet
    from medya.vaka import Vaka

    klasor = Path(klasor)
    if ayar is None:
        ayar_yolu = ilk_bulunan(klasor, "vaka") or ilk_bulunan(klasor.parent, "vaka")
        ayar = yukle(ayar_yolu) if ayar_yolu else {}
    if ayar.get("kart_klasoru") and (klasor / ayar["kart_klasoru"]).is_dir():
        klasor = klasor / ayar["kart_klasoru"]
    sonuc = klasor_ice_aktar(klasor, ayar.get("sema_ayarlari"))
    v = Vaka(vaka_id, kok_calisma)
    if not v.var_mi():
        olay = ayar.get("olay_tarihi")
        if not olay:
            raise PaketHatasi("Olay tarihi bilinmiyor: vaka.yaml'a olay_tarihi yazın ya da önce `vaka yeni` ile "
                              "vakayı oluşturun")
        v = Vaka.yeni(vaka_id, ayar.get("ad") or vaka_id, ayar.get("soru") or "", str(olay), kok=kok_calisma,
                      kaynak_paketi=str(ayar_yolu.parent) if ayar_yolu else str(klasor))
    on_kayit = None
    if sonuc.hipotezler:
        m = v.ach()
        if not m.on_kayit:
            m = matrise_kaydet(sonuc.hipotezler, ayar.get("hipotez_turleri"), m)
            v.ach_kaydet(m)
            on_kayit = m.on_kayit
    eklenen = sum(depo.ekle(k, vaka_id=vaka_id) for k in sonuc.kartlar)
    (v.dizin / "kartlar_normal.json").write_text(
        json.dumps({"vaka_id": vaka_id, "kartlar": [k.to_dict() for k in sonuc.kartlar]}, ensure_ascii=False,
                   indent=1), encoding="utf-8")
    return {"vaka": vaka_id, "kart": len(sonuc.kartlar), "yeni_kart": eklenen, "dosyalar": sonuc.dosyalar,
            "hatalar": sonuc.hatalar, "uyarilar": sonuc.uyarilar, "on_kayit": on_kayit}
