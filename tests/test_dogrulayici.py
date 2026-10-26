import pytest

from medya.dogrulayici import Cumle, DogrulamaHatasi, cumle_dogrula, dogrula, kesin_dogrula
from medya.kanit import KanitKarti

HABER = KanitKarti(tur="haber", kaynak_url="https://example.org/olay", kurum="Örnek Ajans",
                   ozet="Ankara'da 19 Aralık 2016'da bir sergi açılışında silahlı saldırı oldu; 3 kişi yaralandı.",
                   alinti="Saldırgan olay yerinde etkisiz hâle getirildi.", kaynak_derecesi="B", bilgi_derecesi="2",
                   yayin_tarihi="2016-12-19")
RESMI = KanitKarti(tur="resmi_aciklama", kaynak_url="https://example.org/bakanlik", kurum="Örnek Bakanlığı",
                   ozet="Bakanlık, saldırganın bir örgütle bağlantılı olduğunu açıkladı.", kaynak_derecesi="B",
                   bilgi_derecesi="3", yayin_tarihi="2016-12-20")
K = {HABER.kanit_id: HABER, RESMI.kanit_id: RESMI}
H, R = HABER.kanit_id, RESMI.kanit_id


def neden(c):
    return cumle_dogrula(c, K)


def test_dogru_cumle_kabul():
    assert neden(Cumle("olgu", "Ankara'da 19.12.2016 tarihinde silahlı saldırı oldu; 3 kişi yaralandı.", [H])) == []
    assert neden(Cumle("olgu", "Örnek Ajans, saldırının 19 Aralık 2016'da olduğunu aktardı.", [H])) == []


def test_uydurma_sayi_reddedilir():
    n = neden(Cumle("olgu", "Saldırıda 12 kişi yaralandı.", [H]))
    assert any("sayı kanıtta yok: 12" in x for x in n)


def test_uydurma_tarih_reddedilir():
    n = neden(Cumle("olgu", "Saldırı 21 Aralık 2016'da oldu.", [H]))
    assert any("tarih kanıtta yok" in x for x in n)
    n = neden(Cumle("olgu", "Saldırı 20.12.2016 tarihinde oldu.", [H]))
    assert any("tarih kanıtta yok" in x for x in n)


def test_uydurma_ad_reddedilir():
    n = neden(Cumle("olgu", "Saldırgan İzmir'de yakalandı.", [H]))
    assert any("ad kanıtta yok: İzmir" in x for x in n)


def test_niyet_fiili_olguda_yasak():
    n = neden(Cumle("olgu", "Örnek Ajans kamuoyunu yönlendirdi.", [H]))
    assert any("niyet atfı yasak" in x for x in n)
    n = neden(Cumle("olgu", "Saldırgan saldırıyı planladı.", [H]))
    assert any("niyet atfı yasak" in x for x in n)


def test_niyet_fiili_degerlendirmede_olasilik_diliyle_serbest():
    c = Cumle("degerlendirme", "Saldırının önceden planlandığı olası görünüyor.", [H], guven="olası")
    assert neden(c) == []


def test_resmi_aciklama_olgu_gibi_yazilamaz():
    assert any("iddia olarak" in x for x in neden(Cumle("olgu", "Saldırgan bir örgütle bağlantılıydı.", [R])))
    assert neden(Cumle("olgu", "Örnek Bakanlığı, saldırganın bir örgütle bağlantılı olduğunu açıkladı.", [R])) == []


def test_kanitsiz_ve_var_olmayan_kimlik():
    assert neden(Cumle("olgu", "Saldırı oldu.", []))
    assert any("var olmayan" in x for x in neden(Cumle("olgu", "Saldırı oldu.", ["k-yok"])))


def test_alinti_birebir_olmali():
    assert neden(Cumle("olgu", "Ajansa göre “Saldırgan olay yerinde etkisiz hâle getirildi.”", [H])) == []
    assert any("alıntı kanıtta yok" in x
               for x in neden(Cumle("olgu", "Ajansa göre “Saldırgan kaçtı.”", [H])))


def test_degerlendirme_kent_terimi_ve_dayanak():
    assert any("Kent" in x for x in neden(Cumle("degerlendirme", "Saldırı örgütseldi.", [R])))
    assert any("dayanmalı" in x for x in neden(Cumle("degerlendirme", "Saldırı olası olarak örgütseldi.", [])))
    # olgu cümlesine dayanan değerlendirme
    o = Cumle("olgu", "Ankara'da silahlı saldırı oldu.", [H], id="o1")
    d = Cumle("degerlendirme", "Saldırının örgütsel olması belirlenemedi.", [], guven="belirlenemedi", dayanak=["o1"])
    s = dogrula([d, o], K)
    assert s.temiz and len(s.kabul) == 2


def test_acik_soru():
    assert neden(Cumle("acik_soru", "Saldırganın Ankara'daki temasları kimlerdi?")) == []
    assert any("soru işaretiyle" in x for x in neden(Cumle("acik_soru", "Temaslar bilinmiyor.")))
    assert any("ad kanıtta yok" in x for x in neden(Cumle("acik_soru", "Saldırgan Moskova'ya gitti mi?")))


def test_kesin_dogrula_kilit():
    iyi = [Cumle("olgu", "Ankara'da silahlı saldırı oldu.", [H])]
    kesin_dogrula(iyi, K)
    with pytest.raises(DogrulamaHatasi):
        kesin_dogrula(iyi + [Cumle("olgu", "Saldırıda 40 kişi öldü.", [H])], K)


def test_red_listesi_nedenleriyle():
    s = dogrula([Cumle("olgu", "Ankara'da saldırı oldu.", [H]), Cumle("olgu", "İstanbul'da 7 kişi öldü.", [H])], K)
    assert len(s.kabul) == 1 and len(s.red) == 1
    assert len(s.red[0].nedenler) >= 2
