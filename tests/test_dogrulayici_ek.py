"""Doğrulayıcının kapatılan açıkları: yazıyla yazılmış Türkçe sayılar ve küçük harfle yazılmış adlar."""
from medya.dogrulayici import Cumle, ad_sozlugu, cumle_dogrula
from medya.kanit import KanitKarti
from medya.metin import sayilari_bul, yazili_sayilari_bul

KART = KanitKarti(tur="haber", kaynak_url="https://example.org/a", kurum="Örnek Ajans",
                  ozet="Sergide konuşan büyükelçi Andrey Karlov vuruldu; saldırgan 9,5 saat önce otele girdi. "
                       "Olay yerinde 3 kişi yaralandı.", kaynak_derecesi="B", bilgi_derecesi="2")
DIGER = KanitKarti(tur="haber", kaynak_url="https://example.org/b", kurum="Başka Gazete",
                   ozet="Mahkeme tanık olarak dinlenen Ahmet Yılmaz'ın ifadesini kayda geçirdi; sabah duruşma vardı.",
                   kaynak_derecesi="C", bilgi_derecesi="3")
K = {KART.kanit_id: KART, DIGER.kanit_id: DIGER}


def test_yazili_sayi_obekleri():
    assert sayilari_bul("bir milyon iki yüz bin kişi") == ["1200000"]
    assert sayilari_bul("dokuz buçuk saat") == ["9.5"]
    assert sayilari_bul("on iki sanık, iki bin on altı yılında") == ["12", "2016"]
    assert sayilari_bul("bin iki yüz kişi") == ["1200"]
    assert sayilari_bul("iki buçuk milyon") == ["2500000"]
    assert sayilari_bul("2 bin kişi, 1,5 milyon dolar") == ["2000", "1500000"]
    # çok anlamlı tek sözcükler sayı değildir
    assert sayilari_bul("bir gün altı ay yüz yüze") == []
    assert [d for d, _ in yazili_sayilari_bul("altı yüz")] == ["600"]


def test_yazili_sayi_uydurmasi_reddedilir():
    n = cumle_dogrula(Cumle("olgu", "Saldırıda bin iki yüz kişi yaralandı.", [KART.kanit_id]), K)
    assert any("sayı kanıtta yok: 1200" in x for x in n)
    n = cumle_dogrula(Cumle("olgu", "Saldırgan dokuz buçuk saat önce otele girdi.", [KART.kanit_id]), K)
    assert n == []                       # kartta "9,5" yazıyor
    n = cumle_dogrula(Cumle("olgu", "Saldırgan on bir saat önce otele girdi.", [KART.kanit_id]), K)
    assert any("sayı kanıtta yok: 11" in x for x in n)


def test_kucuk_harfli_ad_reddedilir():
    sozluk = ad_sozlugu(k.dogrulama_metni() for k in K.values())
    assert "yilmaz" in sozluk and "karlov" in sozluk
    assert "sabah" not in sozluk         # kartta küçük harfle de geçiyor: genel sözcük
    n = cumle_dogrula(Cumle("olgu", "Sergide ahmet yılmaz vuruldu.", [KART.kanit_id]), K)
    assert any("küçük harfle" in x and "yılmaz" in x for x in n)
    # atıf yapılan kartta geçen ad küçük harfle yazılsa da kabul edilir
    assert cumle_dogrula(Cumle("olgu", "Sergide büyükelçi karlov vuruldu.", [KART.kanit_id]), K) == []
