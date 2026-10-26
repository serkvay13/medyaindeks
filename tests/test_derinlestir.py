import json

from medya.derinlestir import soru_ekle, soru_isle
from medya.kanit import KanitKarti
from medya.rapor import markdown_uret, rapor_uret
from medya.uzman import OfflineSaglayici


def _ilk_surum(v, depo):
    r = rapor_uret(v, depo, OfflineSaglayici())
    v.rapor_yaz(r, markdown_uret(r, depo.vaka_sozluk(v.id)))
    return r


def test_soru_ekle_kimlik_zaman_plan(ornek, depo):
    v, _ = ornek
    s = soru_ekle(v, "Olaydan önceki haftalarda bölgede ne değişti?", OfflineSaglayici(), depo)
    assert s["id"] == "S1" and s["zaman"] and s["durum"] == "plan_hazir"
    assert s["plan"]["etiket"] == "öneri — kanıt aranacak"
    assert s["plan"]["alt_hipotezler"] and s["plan"]["kaynaklar_sorgular"]
    assert v.sorular()[0]["id"] == "S1"
    assert soru_ekle(v, "İkinci bir ek soru metni?", OfflineSaglayici(), depo)["id"] == "S2"


def test_soru_isle_yeni_surum_eski_korunur(ornek, depo):
    v, k = ornek
    _ilk_surum(v, depo)
    v1_md = (v.dizin / "raporlar" / "v1.md").read_text(encoding="utf-8")
    s = soru_ekle(v, "Bölgedeki deniz ticareti gerginliği olayla ilişkili mi?", OfflineSaglayici(), depo)
    yeni = KanitKarti(tur="uluslararasi_kurum", kaynak_url="https://example.org/kurum/deniz-raporu",
                      kurum="Örnek Denizcilik Örgütü",
                      ozet="Örgüt raporu, Mart 2025'te bölgede deniz ticaretine yönelik 2 olay kaydetti.",
                      kaynak_derecesi="B", bilgi_derecesi="2", yayin_tarihi="2025-05-01")
    r2 = soru_isle(v, s["id"], depo, OfflineSaglayici(), [yeni])
    assert r2["surum"] == 2 and r2["onceki_surum"] == 1 and r2["durum"] == "taslak"
    assert v.rapor_surumleri() == [1, 2]
    assert (v.dizin / "raporlar" / "v1.md").read_text(encoding="utf-8") == v1_md   # eski sürüm değişmedi
    ek = next(b for b in r2["bolumler"] if b["no"] == "E1")
    assert ek["baslik"] == "Ek soru 1" and any(yeni.kanit_id in c["kanit_ids"] for c in ek["cumleler"])
    assert any("Yeni bölüm: Ek soru 1" in d for d in r2["degisiklikler"])
    assert any(yeni.kanit_id in d for d in r2["degisiklikler"])
    assert depo.alt_soru_haritasi(v.id)[yeni.kanit_id] == "S1"
    assert v.sorular()[0]["durum"] == "islendi" and v.sorular()[0]["rapor_surumu"] == 2
    assert "Değişiklik günlüğü" in (v.dizin / "raporlar" / "v2.md").read_text(encoding="utf-8")


def test_soru_isle_onceki_cumleleri_yeniden_dogrular(ornek, depo):
    """Önceki sürümden alınan (yeniden yazılmayan) bölümlerin cümleleri de doğrulanır: önceki sürüme elle
    sokulmuş uydurma cümle yeni sürüme taşınmaz."""
    v, k = ornek
    _ilk_surum(v, depo)
    yol = v.dizin / "raporlar" / "v1.json"
    r1 = json.loads(yol.read_text(encoding="utf-8"))
    b10 = next(b for b in r1["bolumler"] if b["no"] == 10)
    b10["cumleler"].append({"tur": "olgu", "metin": "Mahkeme 9 sanığa ceza verdi.",
                            "kanit_ids": [k["mahkeme"].kanit_id], "guven": "", "dayanak": [], "id": "elle"})
    yol.write_text(json.dumps(r1, ensure_ascii=False), encoding="utf-8")
    s = soru_ekle(v, "Valiliğin açıklaması zamanla değişti mi?", OfflineSaglayici({"arastirma_plani": {
        "etkilenen_bolumler": [6]}}), depo)
    r2 = soru_isle(v, s["id"], depo, OfflineSaglayici())
    b10_yeni = next(b for b in r2["bolumler"] if b["no"] == 10)
    assert all(c["id"] != "elle" for c in b10_yeni["cumleler"])
    assert any(x["cumle"]["id"] == "elle" for x in r2["reddedilenler"])
