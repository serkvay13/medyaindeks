"""Offline sağlayıcının deterministik şablonları. Dünya bilgisi kullanmaz: yalnızca girdi paketindeki
yapılandırılmış alanlardan (vaka tanımı, kart özetleri, ACH sıralaması) cümle kurar."""
from medya.metin import tarih_tr


def hipotez_uret(paket: dict) -> dict:
    v = paket.get("vaka", {})
    ad = v.get("ad") or "olay"
    resmi = v.get("resmi_tez") or "Resmi açıklamalarda öne sürülen tez doğrudur."
    sorgu = ad
    return {"etiket": "öneri — kanıt aranacak", "hipotezler": [
        {"id": "Ö1", "tur": "resmi_tez", "metin": resmi,
         "destekleyen_kanit": ["İddianame ve gerekçeli kararda tezi destekleyen deliller"],
         "curuten_kanit": ["Bağımsız kaynaklarda resmi kronolojiyle çelişen kayıtlar"],
         "kaynak_turleri": ["mahkeme_kaydi", "resmi_aciklama", "haber"],
         "arama_sorgulari": [f"{sorgu} iddianame", f"{sorgu} gerekçeli karar"]},
        {"id": "Ö2", "tur": "alternatif", "metin": "Olay, resmi tezde yer almayan başka bir aktör ya da ağ "
                                                   "tarafından gerçekleştirilmiş olabilir.",
         "destekleyen_kanit": ["Resmi tezde açıklanmayan temas ya da lojistik izleri"],
         "curuten_kanit": ["Mahkemede sınanmış ve çelişkisiz delil zinciri"],
         "kaynak_turleri": ["uluslararasi_basin", "arastirma_kurumu", "mahkeme_kaydi"],
         "arama_sorgulari": [f"{sorgu} alternative explanation", f"{sorgu} soruşturma çelişki"]},
        {"id": "Ö3", "tur": "yapisal", "metin": "Olay, bölgesel savaş dinamiklerinin ve silahlı gruplar "
                                                "üzerindeki askeri baskının bir yansıması olabilir.",
         "destekleyen_kanit": ["Aynı haftalarda bölgesel çatışma yoğunluğunda kırılma"],
         "curuten_kanit": ["Çatışma verisinde olay öncesi olağandışı değişim olmaması"],
         "kaynak_turleri": ["olay_kaydi", "arastirma_kurumu", "veri_serisi"],
         "arama_sorgulari": [f"{sorgu} bölgesel çatışma", "ACLED UCDP olay yoğunluğu"]},
        {"id": "Ö4", "tur": "dis_konjonktur", "metin": "Olayın zamanlaması, büyük güçler arası pazarlık ve "
                                                       "diplomatik takvimle ilişkili olabilir.",
         "destekleyen_kanit": ["Olay öncesi diplomatik görüşmelerde dönüm noktası"],
         "curuten_kanit": ["Diplomatik süreçte olay sonrası değişiklik olmaması"],
         "kaynak_turleri": ["uluslararasi_basin", "uluslararasi_kurum", "resmi_aciklama"],
         "arama_sorgulari": [f"{sorgu} diplomacy timeline"]},
        {"id": "Ö5", "tur": "masum", "metin": "Olay, örgütsel bağı olmayan bireysel bir eylem olabilir; "
                                              "güvenlik zafiyeti gibi kurumsal ihmaller rol oynamış olabilir.",
         "destekleyen_kanit": ["Failin önceki temaslarına dair bağımsız kayıt bulunmaması"],
         "curuten_kanit": ["Örgütsel talimat ya da finansman belgesi"],
         "kaynak_turleri": ["mahkeme_kaydi", "haber", "arastirma_kurumu"],
         "arama_sorgulari": [f"{sorgu} güvenlik zafiyeti"]},
    ]}


def _olgu_metni(k: dict) -> str:
    kurum, ozet = k["kurum"], k["ozet"].rstrip(".")
    if k["tur"] == "resmi_aciklama":
        return f"{kurum} açıklamasına göre (iddia): {ozet}."
    if k["tur"] == "mahkeme_kaydi":
        return f"{kurum} kaydına göre: {ozet}."
    if k["tur"] == "veri_serisi":
        return f"{kurum} verisine göre: {ozet}."
    if k.get("yayin_tarihi"):
        return f"{kurum} ({tarih_tr(k['yayin_tarihi'])}) aktardı: {ozet}."
    return f"{kurum} aktardı: {ozet}."


def bolum_yaz(paket: dict) -> dict:
    kartlar = paket.get("kartlar", [])
    cumleler = [{"tur": "olgu", "metin": _olgu_metni(k), "kanit_ids": [k["kanit_id"]], "guven": ""}
                for k in kartlar[:8]]
    ach = paket.get("ach") or {}
    sira = ach.get("siralama") or []
    kart_ids = {k["kanit_id"] for k in kartlar}
    ach_ids = [k for k in ach.get("kanit_ids", []) if k in kart_ids]
    if len(sira) >= 2 and ach_ids:
        g = ach.get("guven_onerisi") or "belirlenemedi"
        cumleler.append({"tur": "degerlendirme", "kanit_ids": ach_ids, "guven": g,
                         "metin": f"Kayıtlı kanıtlarla en az çürütülen hipotez {sira[0]['hipotez_id']}; "
                                  f"bu sıralamanın güven düzeyi: {g}."})
        if sira[0].get("az_kanit"):
            cumleler.append({"tur": "degerlendirme", "kanit_ids": ach_ids, "guven": "belirlenemedi",
                             "metin": f"{sira[0]['hipotez_id']} az kanıtla sınandığı için öne çıkması kanıt "
                                      f"kapsamının darlığını yansıtabilir; güven düzeyi: belirlenemedi."})
        for r in sira:
            if r.get("celisen_kanit", 0) == 0 and r.get("tutarli_kanit", 0) == 0:
                cumleler.append({"tur": "acik_soru", "kanit_ids": [],
                                 "metin": f"{r['hipotez_id']} hipotezini doğrudan destekleyen ya da çürüten "
                                          f"bağımsız bir kanıt var mı?"})
    if kartlar and all(k["tur"] == "resmi_aciklama" for k in kartlar):
        cumleler.append({"tur": "acik_soru", "kanit_ids": [],
                         "metin": "Resmi açıklamalardaki iddiaları bağımsız olarak doğrulayan bir kaynak var mı?"})
    if not kartlar:
        cumleler.append({"tur": "acik_soru", "kanit_ids": [],
                         "metin": "Bu bölümün sorusunu cevaplayacak kanıt henüz toplanmadı; hangi kaynaklar aranmalı?"})
    return {"cumleler": cumleler}


def arastirma_plani(paket: dict) -> dict:
    s = paket.get("ek_soru", {}).get("metin", "")
    return {"etiket": "öneri — kanıt aranacak",
            "alt_hipotezler": [
                {"id": "A1", "metin": f"Sorunun ima ettiği ilişki kanıtla gösterilebilir: {s}",
                 "destekler": "Belgeyle kurulmuş, tarihli bağlantı", "curutur": "Bağlantıyı dışlayan kayıt"},
                {"id": "A2", "metin": "Görünen ilişki tesadüfi zamanlama ya da ortak bir üçüncü etkenden "
                                      "kaynaklanıyor olabilir (masum/yapısal açıklama).",
                 "destekler": "Aynı örüntünün olaysız dönemlerde de görülmesi",
                 "curutur": "Örüntünün yalnızca olay penceresinde görülmesi"}],
            "kanit_ihtiyaclari": [{"aciklama": "Soruyla ilgili birincil belge", "kaynak_turu": "mahkeme_kaydi"},
                                  {"aciklama": "Bağımsız dış kaynak değerlendirmesi", "kaynak_turu": "arastirma_kurumu"},
                                  {"aciklama": "Uluslararası basında aynı dönem", "kaynak_turu": "uluslararasi_basin"}],
            "kaynaklar_sorgular": [{"kaynak_turu": "haber", "sorgu": s[:120]},
                                   {"kaynak_turu": "arsiv", "sorgu": "Wayback Machine: ilgili haberlerin ilk sürümleri"}],
            "etkilenen_bolumler": [2, 3, 12]}


def kirmizi_takim(paket: dict) -> dict:
    kartlar = paket.get("kartlar", [])
    zayif = [k for k in kartlar if k["derece"][0] in "DEF" or k["derece"][1] in "456"]
    out = [{"arguman": "Öne çıkan hipotezin dayandığı kanıtların bir kısmı düşük dereceli ya da "
                       "değerlendirilemez; bağımsız teyit aranmalı.", "kanit_ids": [k["kanit_id"] for k in zayif]}]
    out.append({"arguman": "Rakip hipotezleri destekleyebilecek kaynak türleri (uluslararası basın, araştırma "
                           "kurumları) henüz yeterince taranmamış olabilir.", "kanit_ids": []})
    return {"karsi_argumanlar": out}
