"""Vaka raporunun yapısı (referans rapor biçimi).

Her bölüm: kimlik, başlık (vaka ayarı `rapor.basliklar` ile değiştirilebilir), numarasız mı, LLM yazım katmanına
gidip gitmeyeceği, kart seçimi ve bölümün içine koddan yerleştirilen deterministik parçalar (yer tutucular).

Deterministik parçalar (koddan): kapak, kaynak tabanı tablosu, kronoloji tabloları (4 alt dönem), çelişki
tablosu, GDELT tabloları ve grafikleri, ACH matrisi, kart dizini (Ek A). Anlatı: LLM katmanı ya da vaka
paketindeki hazır metin (`vakalar/<vaka>/anlati/<sira>_<kimlik>.md`; "çevrimdışı mod").

Yer tutucular: {{KAYNAK_TABANI}} {{KRONOLOJI:0..3}} {{CELISKI_TABLOSU}} {{GDELT_GUNLUK}} {{GDELT_ILK_HABER}}
{{GDELT_CERCEVE}} {{GDELT_TON}} {{GRAFIK:gunluk}} {{GRAFIK:saatlik}} {{ACH_MATRISI}} {{KART_DIZINI}}
"""

# kimlik, varsayılan başlık, numarasız, llm, kart seçimi, deterministik parçalar (LLM modunda bölüm sonuna eklenir)
BOLUMLER = [
    {"id": "kaynak_tabani", "baslik": "Kaynak tabanı ve okuma kılavuzu", "numarasiz": True, "llm": False,
     "parcalar": [("Kaynak tabanı özeti", "{{KAYNAK_TABANI}}")]},
    {"id": "yonetici_ozeti", "baslik": "Yönetici özeti", "llm": True, "secim": {"semalar": ["K", "KR", "R", "RD"],
                                                                                  "azami": 60},
     "amac": "Cevabın kısası: olay, fail süreci, medya çerçevelemesi, aktörler ve güncel hipotez sıralaması."},
    {"id": "kronoloji", "baslik": "Dakika dakika kronoloji", "llm": True, "secim": {"semalar": ["KR"]},
     "amac": "Dört alt dönemde (olay öncesi, olay günü, sonraki günler, yargı) ne zaman ne oldu; çelişkiler.",
     "parcalar": [("Olay öncesi", "{{KRONOLOJI:0}}"), ("Olay günü", "{{KRONOLOJI:1}}"),
                  ("Sonraki günler", "{{KRONOLOJI:2}}"), ("Yargı ve sonrası", "{{KRONOLOJI:3}}"),
                  ("Kaynaklar arası çelişkiler", "{{CELISKI_TABLOSU}}")]},
    {"id": "medya", "baslik": "Medya nasıl anlattı: GDELT istatistikleri", "llm": True,
     "secim": {"semalar": ["GDELT"]},
     "amac": "Kimin ne anlattığı (hacim, ilk haber, çerçeveler, ton) ve üç manipülasyon göstergesi; doğruluk ölçülmez.",
     "parcalar": [("Hacim", "![Günlük hacim ve Türkçe arşivdeki pay. Kaynak: The GDELT Project.]({{GRAFIK:gunluk}})"
                            "\n\n{{GDELT_GUNLUK}}"),
                  ("Saatlik eğri", "![Saatlik hacim, yerel saat. Kaynak: The GDELT Project.]({{GRAFIK:saatlik}})"),
                  ("İlk haber zamanları", "{{GDELT_ILK_HABER}}"), ("Çerçeve sayımları", "{{GDELT_CERCEVE}}"),
                  ("Ton", "{{GDELT_TON}}")]},
    {"id": "aktorler", "baslik": "Diğer aktörler", "llm": True, "secim": {"semalar": ["R"]},
     "amac": "Diğer devletlerin ve kurumların tepkileri, kendi soruşturmaları, mağdur yakınlarının açıklamaları."},
    {"id": "kavram", "baslik": "Kavram", "llm": True, "secim": {"semalar": ["RAD"]},
     "amac": "Raporda kullanılan kavramın akademik tanımı, modelleri ve göstergeleri."},
    {"id": "vaka_sureci", "baslik": "Failin süreci", "llm": True, "secim": {"semalar": ["RD"]},
     "amac": "Kavramın bu vakadaki süreci: yaşam öyküsü, çevre, dijital iz, tanıklıklar (özel kişiler rolüyle)."},
    {"id": "baglam", "baslik": "Bağlam ve \"neden şimdi?\"", "llm": True, "secim": {"semalar": ["K", "R"], "azami": 50},
     "amac": "Olayın kesiştiği süreçler; zamanlama; nedensellik iddiası olmadan."},
    {"id": "hipotezler", "baslik": "Hipotezler ve rakip hipotezler analizi (ACH)", "llm": True,
     "secim": {"semalar": ["ACH", "K"], "azami": 70},
     "amac": "Ön kayıtlı hipotezler, kanıt–hipotez matrisi, güncel değerlendirme, şeytanın avukatı.",
     "parcalar": [("Kanıt–hipotez matrisi", "{{ACH_MATRISI}}")]},
    {"id": "kim_kazandi", "baslik": "Kim kazandı? Anlatıların işlevi", "llm": True,
     "secim": {"semalar": ["K", "R"], "azami": 50},
     "amac": "Anlatıların işlevleri simetrik biçimde: resmî anlatı ve karşı anlatılar aynı ölçütle. "
             "Kazanmak kasıt kanıtı değildir."},
    {"id": "acik_sorular", "baslik": "Açık sorular", "llm": True, "secim": {"semalar": ["KR", "K", "RD"], "azami": 60,
                                                                           "celiskili_once": True},
     "amac": "Mevcut kamuya açık kanıtla yanıtlanamayan sorular ve hangi belgeyle kapanacakları."},
    {"id": "kaynak_elestirisi", "baslik": "Kaynak eleştirisi ve veri boşlukları", "llm": True,
     "secim": {"semalar": ["K", "KR", "R", "RD"], "azami": 60},
     "amac": "Kaynak tabanının sınırları, erişim durumu, çıkar çatışmaları, sınıflandırma tutarsızlıkları."},
    {"id": "ek_a", "baslik": "Ek A: Kanıt kartı dizini", "numarasiz": True, "llm": False,
     "parcalar": [("", "{{KART_DIZINI}}")]},
    {"id": "ek_b", "baslik": "Ek B: Yöntem", "numarasiz": True, "llm": False},
]
BOLUM = {b["id"]: b for b in BOLUMLER}

# Yer tutucu -> div sınıfı (stil dosyasındaki tablo biçimleri bu sınıflara bağlıdır)
DIV_SINIFI = {"KRONOLOJI:0": "tbl-kr_a", "KRONOLOJI:1": "tbl-kr_b", "KRONOLOJI:2": "tbl-kr_c",
              "KRONOLOJI:3": "tbl-kr_d", "GDELT_GUNLUK": "tbl-g_daily", "GDELT_ILK_HABER": "tbl-g_first",
              "GDELT_CERCEVE": "tbl-g_frames", "GDELT_TON": "tbl-g_tone", "ACH_MATRISI": "tbl-ach",
              "KART_DIZINI": "tbl-eka"}


def baslik(bolum_id: str, ayar: dict | None = None) -> str:
    b = BOLUM[bolum_id]
    metin = ((ayar or {}).get("rapor", {}).get("basliklar", {}) or {}).get(bolum_id, b["baslik"])
    return f"# {metin}" + (" {.unnumbered}" if b.get("numarasiz") else "")


def dosya_adi(bolum_id: str) -> str:
    return f"{[b['id'] for b in BOLUMLER].index(bolum_id):02d}_{bolum_id}"
