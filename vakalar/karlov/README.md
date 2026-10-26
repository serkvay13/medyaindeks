# Karlov suikastı — vaka paketi

Rusya'nın Ankara Büyükelçisi Andrey Karlov'a 19 Aralık 2016'da düzenlenen suikastın yeniden üretilebilir
girdileri. Kütüphane kaydı: `../ankara-2016-buyukelci.toml`.

| Dosya | İçerik |
|---|---|
| `vaka.yaml` | vaka ayarı, şema ayarları, rapor künyesi, tablo etiketleri |
| `kartlar/kanitlar.json` | K01–K42 temel kanıt kartları (şema K) |
| `kartlar/kronoloji.json` | KR-001–KR-127 kronoloji satırları (şema KR; ham kimlik `K001` → `KR-001`) |
| `kartlar/rusya_dunya.json` | R01–R69 Rusya ve dünya kartları (şema R) |
| `kartlar/radikallesme_kartlar.json` | RD01–RD56 radikalleşme kartları (şema RD) |
| `kartlar/hipotezler.json`, `kartlar/ach.json` | hipotez ön kaydı ve ilk ACH matrisi |
| `kaynaklar/radikallesme.md` | radikalleşme literatürü özeti ([RAD-A§n], [RAD-B]) |
| `anonimlestirme.json` | özel kişileri rolüyle anma kuralları |
| `gdelt.yaml`, `gdelt/` | GDELT vaka sorgusu ve hesaplanmış istatistikler |
| `ach_matris.yaml`, `celiskiler.yaml` | tanısal kanıt satırları; kaynaklar arası çelişki kayıtları |
| `anlati/` | çevrimdışı mod anlatı metinleri |
| `referans/analiz_v2.md` | eşleşme testlerinin karşılaştırdığı referans rapor |

**Kişi adları:** Kart dosyaları kaynaklarda geçtiği biçimiyle kopyalandı ve özel kişilerin adlarını içerir.
Rapor üretilirken `anonimlestirme.json` kuralları uygulanır; kartların kendisi (birebir alıntı doğrulaması
için) değiştirilmez. Paket herkese açık bir depoya konmadan önce bu durum gözden geçirilmelidir.
