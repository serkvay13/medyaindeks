"""SENTETİK örnek vaka: testler ve arayüz denemesi için. Gerçek bir olay DEĞİLDİR.

"Kuzey Limanı" kurgusal bir yerdir; kurumlar ve URL'ler yer tutucudur (example.org). Kişi adı yoktur.
"""
from datetime import date, timedelta

from medya.hipotez import Hipotez, KirmiziTakim
from medya.kanit import KanitDeposu, KanitKarti
from medya.vaka import Vaka

VAKA_ID = "ornek-liman"
OLAY_TARIHI = "2025-03-14"


def kartlar() -> dict[str, KanitKarti]:
    d = [
        ("haber_ajans", dict(tur="haber", kaynak_url="https://example.org/ajans/liman-patlama", kurum="Örnek Haber Ajansı",
                             ozet="Kuzey Limanı'ndaki bir depoda 14 Mart 2025'te patlama oldu; 3 kişi yaralandı.",
                             alinti="Depodaki patlamada 3 liman çalışanı yaralandı.", kaynak_derecesi="B",
                             bilgi_derecesi="2", yayin_tarihi="2025-03-14", olay_tarihi="2025-03-14",
                             yayin_grubu="ajans", yayin_grubu_tarihi="2025-01-01",
                             yayin_grubu_dayanak="örnek yayın sicili (sentetik)")),
        ("valilik", dict(tur="resmi_aciklama", kaynak_url="https://example.org/valilik/aciklama-1", kurum="Örnek Valiliği",
                         ozet="Valilik, patlamanın sabotaj sonucu olduğunu ve yasa dışı bir örgütün sorumlu tutulduğunu açıkladı.",
                         alinti="Olay bir sabotaj eylemidir.", kaynak_derecesi="B", bilgi_derecesi="3",
                         yayin_tarihi="2025-03-15", olay_tarihi="2025-03-14")),
        ("muhalif", dict(tur="haber", kaynak_url="https://example.org/bagimsiz/liman-denetim", kurum="Bağımsız Gazete",
                         ozet="Liman işçileri, depoda aylardır güvenlik denetimi yapılmadığını söyledi.",
                         kaynak_derecesi="C", bilgi_derecesi="3", yayin_tarihi="2025-03-16",
                         yayin_grubu="muhalif", yayin_grubu_tarihi="2025-01-01",
                         yayin_grubu_dayanak="örnek yayın sicili (sentetik)")),
        ("mahkeme", dict(tur="mahkeme_kaydi", kaynak_url="https://example.org/mahkeme/iddianame", kurum="Örnek Ağır Ceza Mahkemesi",
                         ozet="İddianamede patlamanın sabotaj olduğuna dair bir bilirkişi raporu yer aldı; savunma raporun eksik olduğunu ileri sürdü.",
                         kaynak_derecesi="A", bilgi_derecesi="2", yayin_tarihi="2025-11-20")),
        ("enstitu", dict(tur="arastirma_kurumu", kaynak_url="https://example.org/enstitu/rapor", kurum="Örnek Liman Güvenliği Enstitüsü",
                         ozet="Enstitü raporu, depoda kimyasal maddelerin uygunsuz depolandığını tespit etti.",
                         kaynak_derecesi="B", bilgi_derecesi="2", yayin_tarihi="2025-06-01")),
        ("yabanci", dict(tur="uluslararasi_basin", kaynak_url="https://example.org/wire/port-blast", kurum="Example Wire",
                         ozet="Patlama, bölgedeki deniz ticareti gerginliğinin arttığı bir haftada yaşandı.",
                         kaynak_derecesi="C", bilgi_derecesi="3", yayin_tarihi="2025-03-17")),
        ("seri", dict(tur="veri_serisi", kaynak_url="https://example.org/istatistik/gemi-trafigi", kurum="Örnek Liman İstatistik Kurumu",
                      ozet="Mart 2025'te limandaki gemi trafiği 120 sefer olarak kaydedildi.", kaynak_derecesi="B",
                      bilgi_derecesi="1", yayin_tarihi="2025-04-02")),
        ("olay_db", dict(tur="olay_kaydi", kaynak_url="https://example.org/olaydb/bolge", kurum="Örnek Olay Veritabanı",
                         ozet="Olaydan önceki 30 günde bölgede 4 silahlı olay kaydedildi.", kaynak_derecesi="C",
                         bilgi_derecesi="2", yayin_tarihi="2025-03-10", olay_tarihi="2025-03-01")),
    ]
    return {ad: KanitKarti(**v) for ad, v in d}


def hipotezler() -> list[Hipotez]:
    return [
        Hipotez("H1", "Patlama, valiliğin açıkladığı gibi yasa dışı bir örgütün sabotajı olabilir.", "resmi_tez",
                destekleyici_gostergeler=["Bilirkişi raporunun bağımsız teyidi"],
                curutucu_gostergeler=["Patlayıcı izine rastlanmaması"]),
        Hipotez("H2", "Patlama, resmi tezde yer almayan başka bir aktörün eylemi olabilir.", "alternatif",
                destekleyici_gostergeler=["Başka bir aktörün üstlenmesi"], curutucu_gostergeler=["Örgüt üyelerinin mahkûmiyeti"]),
        Hipotez("H3", "Patlama, bölgedeki deniz ticareti gerginliğiyle bağlantılı bir dış müdahale olabilir.",
                "dis_konjonktur", destekleyici_gostergeler=["Uluslararası soruşturma bulguları"],
                curutucu_gostergeler=["Gerginlikte olay sonrası değişiklik olmaması"]),
        Hipotez("H4", "Patlama, kimyasal maddelerin uygunsuz depolanmasından kaynaklanan bir kaza olabilir.", "masum",
                destekleyici_gostergeler=["Denetim kayıtlarında eksiklik"], curutucu_gostergeler=["Kasıtlı ateşleme kanıtı"]),
    ]


ACH_DEGERLERI = {
    # kart: {hipotez: değer}
    "valilik": {"H1": "T", "H2": "Ç", "H3": "N", "H4": "Ç"},
    "mahkeme": {"H1": "T", "H2": "N", "H3": "N", "H4": "Ç"},
    "enstitu": {"H1": "Ç", "H2": "N", "H3": "N", "H4": "T"},
    "muhalif": {"H1": "N", "H2": "N", "H3": "N", "H4": "T"},
    "yabanci": {"H1": "N", "H2": "N", "H3": "T", "H4": "N"},
    "olay_db": {"H1": "T", "H2": "T", "H3": "T", "H4": "N"},
}


def baglam_girdisi(k: dict[str, KanitKarti]) -> dict:
    ot = date.fromisoformat(OLAY_TARIHI)
    seri = {}
    for i in range(240, -1, -1):
        g = ot - timedelta(days=i)
        seri[g.isoformat()] = 10 + (i * 7) % 5        # durağan taban
    seri[(ot - timedelta(days=3)).isoformat()] = 60   # olaydan 3 gün önce sıçrama
    return {
        "zaman_cizgisi": [
            {"tarih": "2025-03-01", "serit": "bolgesel_catisma", "metin": "Bölgede silahlı olaylar kaydedildi.",
             "kanit_ids": [k["olay_db"].kanit_id]},
            {"tarih": "2025-03-14", "serit": "guvenlik", "metin": "Kuzey Limanı'ndaki depoda patlama oldu.",
             "kanit_ids": [k["haber_ajans"].kanit_id]},
            {"tarih": "2025-03-15", "serit": "ic_siyaset", "metin": "Örnek Valiliği olayın sabotaj olduğunu açıkladı.",
             "kanit_ids": [k["valilik"].kanit_id]},
            {"tarih": "2025-11-20", "serit": "yargi", "metin": "İddianamede bir bilirkişi raporu yer aldı.",
             "kanit_ids": [k["mahkeme"].kanit_id]},
            {"tarih": "2025-03-20", "serit": "ekonomi", "metin": "Limanda 999 sefer iptal edildi.",   # uydurma: reddedilmeli
             "kanit_ids": [k["haber_ajans"].kanit_id]},
        ],
        "seriler": {"liman haber hacmi (sentetik)": seri},
        "seri_kanitlari": {"liman haber hacmi (sentetik)": [k["seri"].kanit_id]},
        "cui_bono": [
            {"aktor": "Örnek Valiliği",
             "once_hedefler": [],
             "sonra_degisiklikler": [{"metin": "Valilik yasa dışı bir örgütü sorumlu tuttuğunu açıkladı.",
                                      "kanit_ids": [k["valilik"].kanit_id]}]},
        ],
        "iddialar": [
            {"tez": "sabotaj", "kaynak": "Örnek Valiliği", "tarih": "2025-03-15", "kanit_id": k["valilik"].kanit_id,
             "kanit_durumu": "bilirkişi raporu tartışmalı"},
            {"tez": "sabotaj", "kaynak": "Örnek Ağır Ceza Mahkemesi", "tarih": "2025-11-20",
             "kanit_id": k["mahkeme"].kanit_id, "kanit_durumu": "iddianamede"},
            {"tez": "ihmal / uygunsuz depolama", "kaynak": "Bağımsız Gazete", "tarih": "2025-03-16",
             "kanit_id": k["muhalif"].kanit_id, "kanit_durumu": "enstitü raporuyla kısmen teyitli"},
        ],
        "bulgu_tarihi": "2025-06-01",
        "etiketler": ["patlama", "liman", "sabotaj", "ihmal"],
        "erken_isaretler": [
            {"tarih": "2025-03-01", "aktor": "bölgesel silahlı gruplar", "metin": "Bölgede silahlı olaylar kaydedildi.",
             "kanit_ids": [k["olay_db"].kanit_id]},
        ],
        "varsayimlar": [
            {"hipotez_id": "H1", "varsayim": "Bilirkişi raporu bağımsız hazırlandı.", "kanit_ids": [k["mahkeme"].kanit_id],
             "coker_ise": "Resmi tezin ana delili zayıflar.", "durum": "sorgulanabilir"},
            {"hipotez_id": "H4", "varsayim": "Depo denetim kayıtları eksiksizdir.", "kanit_ids": [],
             "coker_ise": "İhmal hipotezi zayıflar."},
        ],
    }


def ornek_kur(depo: KanitDeposu, kok=None, kirmizi_takim: bool = True) -> Vaka:
    v = Vaka(VAKA_ID, kok)
    if not v.var_mi():
        v = Vaka.yeni(VAKA_ID, "Kuzey Limanı patlaması (SENTETİK örnek)",
                      "Kuzey Limanı'ndaki patlamada ne oldu, kim neyi neden anlattı?", OLAY_TARIHI, kok=kok,
                      kapsam={"ajans": 0.9, "muhalif": "yalnızca künye (ek toplama)"},
                      kaliplar=["(?i)\\bkuzey liman"], etiketler=["patlama", "liman", "sabotaj", "ihmal"],
                      kod_kitabi_surumu="yok", veri_anlik_goruntu="2026-10-26 (sentetik)",
                      kapsam_onayi={"onaylayan": "analist (örnek)", "tarih": "2026-10-26"})
    k = kartlar()
    for kart in k.values():
        depo.ekle(kart, vaka_id=v.id)
    m = v.ach()
    if not m.on_kayit:
        m.on_kaydet(hipotezler())
        for ad, hs in ACH_DEGERLERI.items():
            for h, d in hs.items():
                m.degerlendir(k[ad].kanit_id, h, d)
        if kirmizi_takim:
            lider = m.sirala({x.kanit_id: x for x in k.values()})[0]["hipotez_id"]
            m.kirmizi_takim_ekle(KirmiziTakim(lider, [{"arguman": "Öne çıkan hipotezin dayandığı enstitü raporu tek "
                                                                  "bir kurumdan geliyor.", "yanit": "",
                                                      "kanit_ids": [k["enstitu"].kanit_id]}],
                                              "insan: örnek analist"))
        v.ach_kaydet(m)
    if not v.baglam_girdisi():
        v.baglam_girdisi_kaydet(baglam_girdisi(k))
    return v
