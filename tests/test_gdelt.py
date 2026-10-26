"""GDELT modülü: indirici (ağsız), vaka sorgusu, çerçeve sözlüğü (sözcük sınırı), istatistik, göstergeler,
grafikler ve Karlov referans sayılarıyla eşleşme."""
import ast
import io
import json
import os
import zipfile

import pytest

from medya.ayar import yukle
from medya.gdelt import gruplar, vaka_istatistigi
from medya.gdelt.gostergeler import atif_aklama_adaylari, cerceve_eszamanliligi, manset_birligi, sessizlik
from medya.gdelt.indirici import ana_listeden_urller, indir, satir_suz, zaman_damgalari
from medya.gdelt.istatistik import cerceve_derle, cerceveler_bul, istatistik_hesapla, url_tokenleri
from medya.gdelt.sorgu import VakaSorgusu
from tests.conftest import ROOT

KARLOV = ROOT / "vakalar" / "karlov"
AYAR = yukle(KARLOV / "gdelt.yaml")


def _satir(ts="20161219163000", src="ornek.com.tr", url="http://ornek.com.tr/haber", kisiler="", baslik="",
           ton="-2.5,1,3,4,5,6,300", ceviri="srclc:tur;eng:GT"):
    c = [""] * 27
    c[0], c[1], c[2], c[3], c[4] = f"{ts}-1", ts, "1", src, url
    c[11], c[15], c[17], c[25] = kisiler, ton, "GCAM,1,2", ceviri
    c[26] = f"<PAGE_TITLE>{baslik}</PAGE_TITLE>" if baslik else ""
    return "\t".join(c)


# ---------------------------------------------------------------- gruplar
def test_gruplar_app_ile_ayni_alan_adlari():
    agac = ast.parse((ROOT / "app.py").read_text(encoding="utf-8"))
    app = next(ast.literal_eval(d.value) for d in agac.body if isinstance(d, ast.Assign)
               and any(getattr(t, "id", None) == "KEY_OUTLETS" for t in d.targets))
    app_alan = {g: [d for ds in v.values() for d in ds] for g, v in app.items()}
    assert list(app_alan.values()) == list(gruplar.GRUPLAR.values())
    assert "Rejim kontrolünde olmayan kaynaklar" in gruplar.GRUPLAR
    assert not any("Gülen" in g for g in gruplar.GRUPLAR)


# ---------------------------------------------------------------- çerçeve sözlüğü
def test_cerceve_sozcuk_siniri_alt_dize_hatasini_engeller():
    d = cerceve_derle(AYAR["cerceveler"])
    cihat = "Cihatçı (Nusra/El Kaide/IŞİD/cihat)"
    # Eski hata: "dışişleri" içindeki "isis", "saldırısıdır" içindeki "isid" cihatçı sayılıyordu
    assert cihat not in cerceveler_bul("http://x.com/rus-disislerinden-buyukelciye-saldiriyla-ilgili-ilk-aciklama", d)
    assert cihat not in cerceveler_bul("http://x.com/Dışişleri-Bakanlığı-açıklama", d)
    assert cihat not in cerceveler_bul("http://x.com/bu-saldirisidir-dedi", d)
    assert cihat in cerceveler_bul("http://x.com/el-nusra-ustlendi-iddiasi", d)
    assert cihat in cerceveler_bul("http://x.com/IŞİD-saldırısı", d)          # katlama: ışid -> isid
    # ABD kalıbı sözcüğün tamamını ister
    assert "ABD/Batı/CIA/NATO" not in cerceveler_bul("http://x.com/abdullah-bozkurt-yazdi", d)
    assert "ABD/Batı/CIA/NATO" in cerceveler_bul("http://x.com/abd-den-aciklama", d)
    assert "FETÖ/Gülen" in cerceveler_bul("http://x.com/rus-ajansi-FETÖ%27nün-suikasti-olabilir", d)
    assert url_tokenleri("http://a.com/Çağdaş_Sanat?x=1").startswith("-http-a-com-cagdas-sanat-x-1")


def test_cerceve_kalibi_kurallari():
    with pytest.raises(ValueError):
        cerceve_derle({"x": "isis"})                 # '-' ile başlamıyor
    with pytest.raises(ValueError):
        cerceve_derle({"x": "-fet.{1,8}"})           # joker yasak


# ---------------------------------------------------------------- indirici
def _zip(satirlar):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr("x.translation.gkg.csv", "\n".join(satirlar) + "\n")
    return b.getvalue()


def test_zaman_damgalari_ve_suzgec():
    assert len(zaman_damgalari("2016-12-19", "2016-12-19")) == 96
    assert zaman_damgalari("2016-12-19", "2016-12-20")[-1] == "20161220234500"
    s = satir_suz(_satir())
    assert s is not None and s.split("\t")[17] == ""                      # GCAM boşaltıldı
    assert satir_suz(_satir(src="ornek.com", ceviri="srclc:ara")) is None
    assert satir_suz(_satir(src="haber.com.tr", ceviri="srclc:ara")) is not None      # .tr alan adı
    assert satir_suz(_satir(src="haber.com.tr", ceviri="srclc:ara"), alan_soneki=None) is None
    assert satir_suz("kisa\tsatir") is None
    liste = "1 a http://data.gdeltproject.org/gdeltv2/20161219000000.translation.gkg.csv.zip\n" \
            "1 a http://data.gdeltproject.org/gdeltv2/20161219000000.translation.export.CSV.zip\n"
    assert list(ana_listeden_urller(liste, {"20161219000000"})) == ["20161219000000"]


def test_indir_devam_ettirilebilir_ve_bos_dosya_kaydi(tmp_path):
    zamanlar = zaman_damgalari("2016-12-19", "2016-12-19")[:4]
    cagri = []

    def getir(url):
        cagri.append(url)
        if "masterfilelist" in url:
            return b""
        ts = url.rsplit("/", 1)[1][:14]
        if ts == zamanlar[0]:
            return _zip([_satir(ts=ts), _satir(ts=ts, ceviri="srclc:ara")])
        if ts == zamanlar[1]:
            return _zip([_satir(ts=ts, ceviri="srclc:ara")])       # süzgeçten satır çıkmaz → bos
        if ts == zamanlar[2]:
            return None                                             # 404 → yok
        raise RuntimeError("ağ hatası")

    r = indir("2016-12-19", "2016-12-19", tmp_path, paralel=2, getir=getir, alan_soneki=None)
    d = r.durum
    assert d[zamanlar[0]] == {"durum": "tamam", "satir": 1}
    assert d[zamanlar[1]]["durum"] == "bos" and (tmp_path / f"{zamanlar[1]}.tsv").read_text() == ""
    assert d[zamanlar[2]]["durum"] == "yok" and (tmp_path / f"{zamanlar[2]}.tsv").exists()
    assert d[zamanlar[3]]["durum"] == "hata"
    once = len(cagri)
    indir("2016-12-19", "2016-12-19", tmp_path, paralel=2, getir=getir, alan_soneki=None)
    # ikinci çalıştırma yalnızca hatalı/denenmemiş dosyaları ister (+ ana liste)
    yeniden = [u for u in cagri[once:] if "masterfilelist" not in u]
    assert zamanlar[0] not in " ".join(yeniden) and zamanlar[3] in " ".join(yeniden)
    assert json.loads((tmp_path / "_durum.json").read_text())[zamanlar[0]]["durum"] == "tamam"


# ---------------------------------------------------------------- sorgu + istatistik + göstergeler
@pytest.fixture
def ornek_ham(tmp_path):
    d = tmp_path / "tr"
    d.mkdir()
    (d / "20161219163000.tsv").write_text("\n".join([
        _satir(src="hurriyet.com.tr", url="http://hurriyet.com.tr/rus-buyukelcisi-karlov-vuruldu-1"),
        _satir(src="star.com.tr", url="http://star.com.tr/rus-ajansi-fetonun-suikasti-olabilir-2",
               kisiler="Andrey Karlov,10"),
        _satir(src="yeniakit.com.tr", url="http://yeniakit.com.tr/rus-ajansi-fetonun-suikasti-olabilir-3",
               baslik="Karlov"),
        _satir(src="baska.com", url="http://baska.com/fransa-buyukelcisi-suikast"),        # URL-yalnız gürültü
        _satir(src="hurriyet.com.tr", url="http://hurriyet.com.tr/rus-buyukelcisi-karlov-vuruldu-1"),  # kopya
    ]) + "\n", encoding="utf-8")
    (d / "20161219164500.tsv").write_text("\n".join([
        _satir(ts="20161219164500", src=s, url=f"http://{s}/el-nusra-karlov-suikastini-ustlendi-iddiasi-{i}")
        for i, s in enumerate(["sabah.com.tr", "aksam.com.tr", "cumhuriyet.com.tr"])]) + "\n", encoding="utf-8")
    (d / "20161219170000.tsv").write_text("", encoding="utf-8")
    return d


def test_vaka_sorgusu_ve_istatistik(ornek_ham, tmp_path):
    q = VakaSorgusu.ayardan(AYAR, ornek_ham, onbellek_koku=tmp_path / "ob")
    assert q.tara(en_fazla=1) == {"islenen": 1, "kalan": 2, "toplam": 3}
    s = q.sonuc()
    assert len(s.genis) == 7 and len(s.cekirdek) == 6 and s.bos_dosya == 1
    assert s.gun_toplam == {"20161219": 8}
    assert s.gurultu_site == {"baska.com": 1} and "1 kayıt daha" in s.gurultu_uyarisi()["uyari"]
    ist = istatistik_hesapla(s, AYAR)
    assert ist["gunluk"]["20161219"] == {"haber": 6, "tum": 8, "pay_yuzde": 75.0}
    assert ist["saatlik_yerel"] == {"20161219 19": 6}                   # UTC 16:xx → TSİ 19:xx
    assert list(ist["izlenen_yayin_ilk_haber_utc"])[0] == "hurriyet.com.tr"
    c = ist["cerceve"]
    assert c["n"]["TÜMÜ"] == 6 and c["grup"]["Hükümete yakın"]["FETÖ/Gülen"] == 2
    assert c["grup"]["TÜMÜ"]["Cihatçı (Nusra/El Kaide/IŞİD/cihat)"] == 3
    # göstergeler
    adaylar = atif_aklama_adaylari(s.cekirdek, AYAR["cerceveler"], AYAR["gostergeler"]["atif_kaliplari"])
    assert {a["site"] for a in adaylar if a["cerceve"] == "FETÖ/Gülen"} == {"star.com.tr", "yeniakit.com.tr"}
    es = cerceve_eszamanliligi(s.cekirdek, AYAR["cerceveler"], asgari_site=3)
    assert es and es[0]["cerceve"].startswith("Cihatçı") and es[0]["site_sayisi"] == 3
    mb = manset_birligi(s.cekirdek, asgari_site=2)
    assert mb[0]["site_sayisi"] == 3 and ["star.com.tr", "yeniakit.com.tr"] in [x["siteler"] for x in mb]
    ss = sessizlik(c, asgari_toplam=1, asgari_grup=1, esik_oran=0.5)
    assert any(x["grup"] == "Ana akım" and x["gozlenen"] == 0 for x in ss)


def test_grafikler_png(ornek_ham, tmp_path):
    from medya.gdelt.grafik import gunluk_grafik, saatlik_grafik
    s = VakaSorgusu.ayardan(AYAR, ornek_ham, onbellek_koku=tmp_path / "ob").sonuc()
    ist = istatistik_hesapla(s, AYAR)
    for p in (gunluk_grafik(ist, tmp_path / "g.png"), saatlik_grafik(ist, tmp_path / "s.png")):
        assert p.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


# ---------------------------------------------------------------- Karlov referans eşleşmesi
REF = KARLOV / "referans" / "gdelt"


def _karlov_karsilastir(ist):
    S = json.loads((REF / "stats_core.json").read_text(encoding="utf-8"))
    C = json.loads((REF / "cerceve_duzeltilmis.json").read_text(encoding="utf-8"))
    X = json.loads((REF / "gdelt_ek_saatlik.json").read_text(encoding="utf-8"))
    c = ist["cerceve"]
    # Kullanıcının sabitlediği sayılar
    assert c["grup"]["TÜMÜ"]["FETÖ/Gülen"] == 217
    assert ist["tekil_url"] == 4185 and ist["tekil_site"] == 211
    assert c["n"]["Hükümete yakın"] == 322 and c["grup"]["Hükümete yakın"]["FETÖ/Gülen"] == 44
    assert c["grup"]["Hükümete yakın"]["Cihatçı (Nusra/El Kaide/IŞİD/cihat)"] == 3
    assert c["n"]["Muhalif / bağımsız"] == 276
    assert c["grup"]["Muhalif / bağımsız"]["FETÖ/Gülen"] == 14
    assert c["grup"]["Muhalif / bağımsız"]["Cihatçı (Nusra/El Kaide/IŞİD/cihat)"] == 14
    # Referans dosyalarla birebir
    assert c["n"] == C["n"] and c["grup"] == C["grup"] and c["gunluk"] == C["gunluk"]
    assert {k: (v["haber"], v["tum"], v["pay_yuzde"]) for k, v in ist["gunluk"].items()} == \
        {k: (v["karlov"], v["tum"], v["pay_%"]) for k, v in S["gunluk"].items()}
    for k in ("toplam_kayit", "tekil_url", "tekil_site", "turkce_toplam_kayit_pencere", "ton_tum", "ort_kelime",
              "izlenen_yayin_ilk_haber_utc", "izlenen_yayin_sayi", "grup"):
        assert ist[k] == S[k], k
    assert {g: list(v) for g, v in ist["ton_grup"].items()} == S["ton_grup"]
    assert [list(x) for x in ist["ayni_slug_cok_site"]] == S["ayni_slug_cok_site"]
    assert [list(x) for x in ist["site_top40"]] == S["site_top40"]
    assert all(ist["saatlik_utc"][k] == v for k, v in S["saatlik_utc_19_20"].items())
    assert all(ist["saatlik_yerel"][k] == v for k, v in X["saatlik_TSI"].items())
    assert ist["dosya_sayisi"] == 2400 and ist["bos_dosya"] == 8


def test_karlov_kayitli_istatistik_referansla_eslesir():
    """Depodaki hesaplanmış istatistik (ham veri gerektirmez) referans sayılarla birebir."""
    _karlov_karsilastir(json.loads((KARLOV / "gdelt" / "istatistik.json").read_text(encoding="utf-8")))


def test_karlov_ham_veriden_yeniden_hesap():
    """Ham veriden baştan hesap (ham veri yoksa atlanır; ilk çalıştırma büyük veride uzun sürer)."""
    from medya.gdelt import ham_dizin
    d = ham_dizin(AYAR, "karlov")
    if not d.is_dir() or not any(d.glob("*.tsv")):
        pytest.skip(f"GDELT ham verisi yok: {d}")
    ist, _ = vaka_istatistigi(AYAR, "karlov")
    _karlov_karsilastir(ist)
    g = ist["gostergeler"]
    assert {a["site"] for a in g["atif_aklama"] if a["cerceve"] == "FETÖ/Gülen"} == {"star.com.tr", "yeniakit.com.tr"}
    assert any(x["dosya_utc"] == "20161227184500" and x["cerceve"] == "Samanyolu dizisi" and x["site_sayisi"] == 4
               for x in g["cerceve_eszamanliligi"])
