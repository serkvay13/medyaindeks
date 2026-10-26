# Aktör profilleri (katman 2)

Her dosya bir kurumun ya da kamusal rolü olan bir aktörün davranış profilidir. **Özel kişi profili tutulmaz.**

- Her kayıt (çıkar, kırmızı çizgi, tipik hamle, anlatı kalıbı) en az bir kaynak (`url` + `tarih`) taşır.
- Her profilin bir `gozden_gecirme` tarihi vardır; tarihi geçen profil gözden geçirilmeden kullanılmamalıdır.
- `durum = "aktif"` profilde kaynaksız kayıt varsa yükleyici reddeder (`ProfilHatasi`).
- `durum = "taslak"` profiller yüklenir ama **raporlara girmez**. Buradaki örneklerin hepsi taslaktır:
  içerikleri yer tutucudur ve kaynakla doldurulana kadar hiçbir rapora dayanak olamaz.

Denetim: `python -m medya aktor dogrula`
