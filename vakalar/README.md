# Vaka kütüphanesi

Tamamlanan her vaka; etiketleri, ilk atıfları ve nihai sonucuyla buraya girer. Bağlam protokolünün 5. adımı
(tarihsel benzerler) ve **ilk atıf isabet sicili** (`medya.vaka.ilk_atif_isabet_sicili`) bu dosyalardan beslenir.

Kurallar:
- Yalnızca kamusal rolü olan kişi ve kurumlar; özel kişiler adıyla değil rolüyle yazılır. Sanık adları yazılmaz.
- Her olgu bir kaynak (url + tarih) taşır. Kaynaksız alan `TODO` olarak bırakılır, uydurulmaz.
- `nihai_sonuc.durum`: `devam` | `kismen_kesinlesti` | `kesinlesti` | `belirsiz`. İsabet sicili yalnızca
  `kesinlesti` vakaları sayar.
- `ilk_atiflar[].nihai_ile_uyum`: `tutarli` | `kismen` | `celisik` | `belirsiz`. Bu alan, nihai sonuç kesinleştikten
  sonra analist tarafından doldurulur.

Biçim:

```toml
id = "…"
ad = "…"
durum = "taslak" | "tamam"
olay_tarihi = "YYYY-AA-GG"
yer = "…"
etiketler = ["…"]

[[ilk_atiflar]]
kaynak = "…"            # yayın, kurum ya da yetkilinin rolü
kaynak_turu = "resmi_aciklama" | "haber" | …
tarih = "YYYY-AA-GG"
atif = "…"
url = "…"
nihai_ile_uyum = "belirsiz"

[nihai_sonuc]
durum = "…"
ozet = "…"
tarih = "YYYY-AA-GG"

[[kaynaklar]]
url = "…"
tarih = "YYYY-AA-GG"
not = "…"
```
