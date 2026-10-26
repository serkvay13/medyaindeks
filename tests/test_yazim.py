"""LLM yazım katmanı: sahte sağlayıcıyla (ağsız) bölüm yazımı, kural denetimi, doğrulama, bütçe ve adaptörler."""
import json
import sys
from types import SimpleNamespace

import pytest

from medya.kanit import KanitKarti
from medya.kanit.anonim import Anonimlestirici
from medya.uzman.saglayici import GeminiSaglayici, OpenAISaglayici, Saglayici, SaglayiciHatasi
from medya.uzman.yazim import ISTEM_DIZINI, bolum_yaz, kural_denetimi, rapor_yaz
from tests.conftest import ROOT

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from llm import butce  # noqa: E402

KR = KanitKarti(tur="haber", kaynak_url="https://ornek.org/kr1", kurum="Örnek Ajans",
                ozet="Saldırgan 19:05'te büyükelçiye ateş açtı; olay yerinde 3 kişi yaralandı.",
                alinti="ateş açtı", kaynak_derecesi="F", bilgi_derecesi="6", olay_tarihi="2016-12-19",
                stabil_id="KR-001", derecesiz=True, erisim_durumu="açıldı", saat="19:05")
RESMI = KanitKarti(tur="resmi_aciklama", kaynak_url="https://ornek.org/bakan", kurum="İçişleri Bakanlığı",
                   ozet="Bakanlık saldırganın bir örgütle bağlantılı olduğunu açıkladı.", kaynak_derecesi="B",
                   bilgi_derecesi="3", stabil_id="K05")
KARTLAR = [KR, RESMI]
HIPOTEZ = {"H1": "Resmî tez", "H2": "Yalnız aktör", "H3a": "Cihatçı ortam"}


class SahteSaglayici(Saglayici):
    ad, model = "sahte", "sahte-1"

    def __init__(self, yanit):
        self.yanit, self.cagrilar = yanit, []

    def tamamla(self, sistem, kullanici, gorev, max_tokens=2000):
        self.cagrilar.append((sistem, kullanici, gorev))
        return self.yanit if isinstance(self.yanit, str) else json.dumps(self.yanit, ensure_ascii=False)


def _yaz(cumleler, anonim=None):
    sag = SahteSaglayici({"cumleler": cumleler})
    return sag, bolum_yaz(sag, {"id": "kronoloji", "baslik": "Kronoloji"}, KARTLAR, HIPOTEZ, anonim)


def test_istem_sabit_dosyada_ve_kurallari_tasir():
    m = (ISTEM_DIZINI / "rapor_yazim.md").read_text(encoding="utf-8")
    for ifade in ("Yalnızca verilen kartlardan yaz", "Gülen cemaati iddiası", "rejim kontrolünde olmayan kaynaklar",
                  "nötr kodlarla", "rolüyle", "Bu rapor ne değildir", "sürümünden", "kurumun iddiasıdır"):
        assert ifade in m, ifade


def test_dogru_cumleler_tutulur_ve_markdown():
    sag, s = _yaz([
        {"tur": "O", "metin": "Saldırgan 19:05'te büyükelçiye ateş açtı.", "kanit": ["KR-001"], "paragraf": 1},
        {"tur": "O", "metin": "İçişleri Bakanlığı saldırganın bir örgütle bağlantılı olduğunu açıkladı.",
         "kanit": ["K05"], "paragraf": 1},
        {"tur": "D", "metin": "H1 ile H2 arasındaki ayrım bu kartlarla belirlenemedi.", "kanit": ["KR-001", "K05"],
         "guven": "belirlenemedi", "paragraf": 2},
        {"tur": "S", "metin": "Saldırganın örgütle iletişimi hangi belgeye dayanıyor?", "kanit": [], "paragraf": 2},
    ])
    assert not s.red, s.red
    md = s.markdown()
    assert md.startswith("**[O]** Saldırgan 19:05'te büyükelçiye ateş açtı [KR-001].")
    assert "**[D]** H1 ile H2" in md and "[KR-001], [K05]." in md and md.rstrip().endswith("dayanıyor?")
    assert md.count("\n\n") == 1                                   # iki paragraf
    paket = json.loads(sag.cagrilar[0][1].split("(JSON):", 1)[1])
    assert {k["id"] for k in paket["kartlar"]} == {"KR-001", "K05"}
    assert "kurum iddiası" in next(k for k in paket["kartlar"] if k["id"] == "K05")["not"]


@pytest.mark.parametrize("cumle, neden", [
    ({"tur": "O", "metin": "Saldırgan ateş açtı.", "kanit": ["KR-999"]}, "var olmayan kanıt kimliği"),
    ({"tur": "O", "metin": "Olay yerinde 7 kişi yaralandı.", "kanit": ["KR-001"]}, "sayı kanıtta yok: 7"),
    ({"tur": "O", "metin": "Olay yerinde yedi kişi yaralandı.", "kanit": ["KR-001"]}, "sayı kanıtta yok: 7"),
    ({"tur": "O", "metin": "Saldırgan bir örgütle bağlantılıydı.", "kanit": ["K05"]}, "iddia olarak"),
    ({"tur": "O", "metin": "Saldırgan Moskova'da ateş açtı.", "kanit": ["KR-001"]}, "ad kanıtta yok: Moskova"),
    ({"tur": "D", "metin": "Saldırı örgütseldi.", "kanit": ["K05"]}, "Kent"),
    ({"tur": "O", "metin": "Bu bir Gülen cemaati iddiası olarak aktarıldı.", "kanit": ["KR-001"]}, "Gülen cemaati"),
    ({"tur": "O", "metin": "Gülen hareketine yakın yayınlar ateş açtı dedi.", "kanit": ["KR-001"]}, "rejim kontrolünde"),
    ({"tur": "D", "metin": "Raporun önceki sürümünde H1 büyük olasılıkla öndeydi.", "kanit": ["K05"],
      "guven": "büyük olasılıkla"}, "sürüm/versiyon"),
    ({"tur": "D", "metin": "Bozkurt'un tezi H1 olası görünüyor.", "kanit": ["K05"], "guven": "olası"}, "atfedilemez"),
    ({"tur": "D", "metin": "Analistin hipotezi olası.", "kanit": ["K05"], "guven": "olası"}, "atfedilemez"),
    ({"tur": "D", "metin": "H9 olası görünüyor.", "kanit": ["K05"], "guven": "olası"}, "kayıtlı olmayan hipotez"),
    ({"tur": "S", "metin": "Bu rapor ne değildir?", "kanit": []}, "ne değildir"),
    ({"tur": "X", "metin": "Tür yok.", "kanit": []}, "geçersiz cümle türü"),
])
def test_kurala_aykiri_cumle_dusurulur(cumle, neden):
    _, s = _yaz([cumle])
    assert not s.kabul
    assert any(neden in n for r in s.red for n in r["nedenler"]), s.red


def test_ozel_kisi_adi_dusurulur():
    anonim = Anonimlestirici([[r"Tanık Ali Veli", "Bir tanık"]])
    _, s = _yaz([{"tur": "O", "metin": "Tanık Ali Veli ateş açtı dedi.", "kanit": ["KR-001"]}], anonim)
    assert not s.kabul and "rolüyle" in s.red[0]["nedenler"][0]


def test_bozuk_json_raporlanir():
    sag = SahteSaglayici("bu JSON değil")
    s = bolum_yaz(sag, {"id": "b"}, KARTLAR, HIPOTEZ)
    assert not s.kabul and "JSON" in s.red[0]["nedenler"][0]


def test_kural_denetimi_temiz_cumle():
    assert kural_denetimi("H3a büyük olasılıkla öne çıkıyor.", set(HIPOTEZ)) == []
    assert kural_denetimi("Kaynaklar iki versiyon aktarıyor: 19:05 ve 20:15.", set()) == []   # olay versiyonu serbest


# ---------------------------------------------------------------- adaptörler, bütçe, token sayacı
def _sahte_openai(icerik, girdi=120, cikti=40):
    yanit = SimpleNamespace(usage=SimpleNamespace(prompt_tokens=girdi, completion_tokens=cikti),
                            choices=[SimpleNamespace(message=SimpleNamespace(content=icerik))])
    cagrilar = []

    def create(**kw):
        cagrilar.append(kw)
        return yanit
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create))), cagrilar


@pytest.fixture
def defter(tmp_path, monkeypatch):
    monkeypatch.setattr(butce, "DEFTER", tmp_path / "defter.jsonl")
    monkeypatch.setenv("LLM_FIYAT_DOSYASI", str(tmp_path / "yok.toml"))
    return tmp_path


def test_anahtar_yoksa_net_hata(monkeypatch, defter):
    for ad in ("OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"):
        monkeypatch.delenv(ad, raising=False)
    with pytest.raises(SaglayiciHatasi, match="OPENAI_API_KEY"):
        OpenAISaglayici().tamamla("s", "k", "g")
    with pytest.raises(SaglayiciHatasi, match="GEMINI_API_KEY"):
        GeminiSaglayici().tamamla("s", "k", "g")


def test_fiyatsiz_model_izinsiz_cagrilmaz_ve_uyarir(monkeypatch, defter):
    monkeypatch.delenv("MEDYA_FIYATSIZ_IZIN", raising=False)
    istemci, cagrilar = _sahte_openai("{}")
    with pytest.raises(SaglayiciHatasi, match="fiyat tanımlı değil"):
        OpenAISaglayici(model="gpt-x", istemci=istemci).tamamla("s", "k", "g")
    assert not cagrilar                                            # ağ çağrısı yapılmadı


def test_rapor_yaz_openai_adaptoru_token_sayaci(monkeypatch, defter):
    monkeypatch.setenv("MEDYA_FIYATSIZ_IZIN", "1")
    yanit = json.dumps({"cumleler": [{"tur": "O", "metin": "Saldırgan 19:05'te büyükelçiye ateş açtı.",
                                      "kanit": ["KR-001"]}]}, ensure_ascii=False)
    istemci, cagrilar = _sahte_openai(yanit)
    sayac = butce.TokenSayaci(tavan_token=10_000)
    sag = OpenAISaglayici(model="gpt-x", istemci=istemci)
    s = rapor_yaz(sag, [{"id": "a", "baslik": "A"}, {"id": "b", "baslik": "B"}], lambda b: KARTLAR, HIPOTEZ,
                  tum_kartlar=KARTLAR, sayac=sayac)
    assert len(cagrilar) == 2 and cagrilar[0]["messages"][0]["role"] == "system"
    assert all(len(b.kabul) == 1 for b in s.bolumler.values())
    assert s.sayac["toplam_token"] == 320 and s.sayac["fiyatsiz_modeller"] == ["gpt-x"]
    assert len(butce.kayitlar()) == 2 and butce.kayitlar()[0]["etiket"].endswith("-fiyatsiz")


def test_fiyat_yapilandirma_dosyasindan_ve_tavan(monkeypatch, tmp_path, defter):
    f = tmp_path / "fiyat.toml"
    f.write_text('[modeller."gpt-x"]\ngirdi = 1.0\ncikti = 2.0\n', encoding="utf-8")
    monkeypatch.setenv("LLM_FIYAT_DOSYASI", str(f))
    assert butce.fiyat_var_mi("gpt-x") and butce.maliyet("gpt-x", girdi=1_000_000, cikti=500_000) == 2.0
    sayac = butce.TokenSayaci(tavan_usd=0.0001)
    istemci, cagrilar = _sahte_openai("{}")
    with pytest.raises(butce.ButceAsimi):
        OpenAISaglayici(model="gpt-x", istemci=istemci, sayac=sayac).tamamla("s" * 400, "k", "g", max_tokens=1000)
    assert not cagrilar
    with pytest.raises(butce.ButceAsimi):
        butce.TokenSayaci(tavan_token=10).on_denetim("gpt-x", 5, 10)
    # varsayılan fiyat dosyası depoda boş gelir: Claude dışı model fiyatsız
    monkeypatch.setenv("LLM_FIYAT_DOSYASI", str(ROOT / "llm" / "fiyatlar.toml"))
    assert butce.fiyat_dosyasi_oku() == {} and butce.fiyat_uyarisi("gpt-5-mini")


def test_gemini_adaptoru(monkeypatch, defter):
    monkeypatch.setenv("MEDYA_FIYATSIZ_IZIN", "1")
    yanit = SimpleNamespace(text='{"cumleler": []}',
                            usage_metadata=SimpleNamespace(prompt_token_count=10, candidates_token_count=5))
    istemci = SimpleNamespace(models=SimpleNamespace(generate_content=lambda **kw: yanit))
    sayac = butce.TokenSayaci()
    assert GeminiSaglayici(model="gem-x", istemci=istemci, sayac=sayac).tamamla("s", "k", "g") == '{"cumleler": []}'
    assert sayac.toplam_token == 15
