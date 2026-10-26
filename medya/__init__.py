"""Medya İndeksi — kanıta bağlı OSINT analiz paketi (platform v1).

İki sert kural koda gömülüdür:
1. Uydurma veri yok: rapora giren her cümle kanıt kimliği taşır ve doğrulayıcıdan geçer
   (`medya.dogrulayici`); geçmeyen cümle rapordan çıkarılır ve analiste listelenir.
2. Resmi anlatı olduğu gibi kabul edilmez: resmi açıklama `resmi_aciklama` türünde saklanır ve
   "<kurum> iddiası" olarak gösterilir; her taraf aynı Admiralty (A–F / 1–6) derecelendirmesinden geçer.

LLM ölçmez, anlatır: sayı, tarih, ad ve alıntı yalnızca kanıt kartlarından gelir.
"""
__version__ = "0.1.0"

# GDELT kullanım koşulları: veriyi sunan her çıktıda atıf ve bağlantı zorunludur (README "Kaynak gösterimi").
GDELT_ATTRIBUTION = (
    "Veri kaynağı: [The GDELT Project](https://www.gdeltproject.org/) (GKG 2.1, GQG, GDG, Events 2.0). "
    "GDELT verisi açık ve ücretsizdir; bu rapor GDELT tarafından geliştirilmemiştir."
)
GDELT_ATTRIBUTION_DUZ = (
    "Veri kaynağı: The GDELT Project (https://www.gdeltproject.org/). GDELT verisi açık ve ücretsizdir; "
    "bu çıktı GDELT tarafından geliştirilmemiştir."
)
