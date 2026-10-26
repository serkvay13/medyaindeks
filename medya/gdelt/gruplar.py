"""Yayın grupları (izlenen yayınlar).

`app.py`'deki `KEY_OUTLETS`'in kopyasıdır: app.py içe aktarıldığında arayüzü çalıştırdığı için oradan alınamaz
(medya/metin.py'deki fold_tr ile aynı gerekçe). Tek fark adlandırma kuralıdır: "Gülen hareketine yakın" grubu
burada "Rejim kontrolünde olmayan kaynaklar" adını taşır (medya.kanit.siniflar). Sıra önemlidir: ilk haber
tablosu ve sayımlar bu sırayı izler. tests/test_gdelt.py app.py ile alan adlarının aynı kaldığını denetler.

Liste tarihsizdir: sahibi değişen yayınlar (Hürriyet, CNN Türk: 2018) bugünkü gruplarıyla görünür. Raporlarda
bu sınırlılık yazılır.
"""
from medya.kanit.siniflar import grup_adlandir

_KEY_OUTLETS = {
    "Haber ajansları": {"AA": ["aa.com.tr"], "DHA": ["dha.com.tr"], "İHA": ["iha.com.tr"]},
    "Ana akım": {"Hürriyet": ["hurriyet.com.tr"], "Milliyet": ["milliyet.com.tr"], "Habertürk": ["haberturk.com"],
                 "NTV": ["ntv.com.tr"], "CNN Türk": ["cnnturk.com"], "TRT Haber": ["trthaber.com"],
                 "Sözcü": ["sozcu.com.tr"]},
    "Hükümete yakın": {"Sabah": ["sabah.com.tr"], "Yeni Şafak": ["yenisafak.com", "yenisafak.com.tr"],
                       "Star": ["star.com.tr"], "Akşam": ["aksam.com.tr"], "A Haber": ["ahaber.com.tr"],
                       "Yeni Akit": ["yeniakit.com.tr"]},
    "Muhalif / bağımsız": {"Cumhuriyet": ["cumhuriyet.com.tr"], "BirGün": ["birgun.net"], "Evrensel": ["evrensel.net"],
                           "T24": ["t24.com.tr"], "Halk TV": ["halktv.com.tr"], "Tele1": ["tele1.com.tr"],
                           "Diken": ["diken.com.tr"], "Gazete Duvar": ["gazeteduvar.com.tr"], "Bianet": ["bianet.org"],
                           "Karar": ["karar.com"], "Medyascope": ["medyascope.tv"], "Kısa Dalga": ["kisadalga.net"],
                           "Serbestiyet": ["serbestiyet.com"]},
    "Ulusalcı": {"Aydınlık": ["aydinlik.com.tr", "aydinlikgazete.com"],
                 "Ulusal Kanal": ["ulusalkanal.com.tr", "ulusal.com.tr"], "Odatv": ["odatv.com", "odatv4.com"],
                 "Nefes": ["nefes.com.tr"], "Yeniçağ": ["yenicaggazetesi.com.tr", "yenicaggazetesi.com"]},
    "Kürt siyasetine yakın": {"Özgür Gündem": ["ozgur-gundem.com", "ozgurgundem.com"],
                              "Mezopotamya Ajansı": ["mezopotamyaajansi.com"]},
    "Gülen hareketine yakın": {"Samanyoluhaber": ["samanyoluhaber.com", "shaber3.com"], "TR724": ["tr724.com"],
                               "Bold Medya": ["boldmedya.com"]},
    "Yabancı yayınların Türkçe servisleri": {"BBC Türkçe": ["bbc.com"], "DW Türkçe": ["dw.com"],
                                             "Euronews": ["euronews.com"],
                                             "Sputnik": ["sputniknews.com.tr", "sputniknews.com", "anlatilaninotesi.com.tr"],
                                             "Amerika'nın Sesi": ["amerikaninsesi.com"]},
}

# grup -> alan adları (sıra korunur)
GRUPLAR: dict[str, list[str]] = {grup_adlandir(g): [d for ds in yayinlar.values() for d in ds]
                                 for g, yayinlar in _KEY_OUTLETS.items()}
YAYIN_ADLARI: dict[str, str] = {d: ad for yayinlar in _KEY_OUTLETS.values() for ad, ds in yayinlar.items() for d in ds}
DIGER = "Diğer"


def alan_grubu_haritasi(gruplar: dict | None = None) -> dict[str, str]:
    """alan adı -> grup (sıra: grupların ve alan adlarının tanım sırası)."""
    return {d: g for g, ds in (gruplar or GRUPLAR).items() for d in ds}


def grup_bul(alan: str, harita: dict | None = None) -> str:
    return (harita or alan_grubu_haritasi()).get(alan, DIGER)
