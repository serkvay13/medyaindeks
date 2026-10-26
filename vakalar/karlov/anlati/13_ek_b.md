
## B.1 GDELT yeniden kurulumu {.unnumbered}

- **Kaynak:** The GDELT Project, Global Knowledge Graph 2.1, çeviri akışı (`*.translation.gkg.csv.zip`), 15 dakikalık dosyalar, 17.12.2016 00:00 – 10.01.2017 23:45 UTC; 2.400 dosya, 8'i boş [GDELT-istatistik].
- **Filtre:** `TranslationInfo` sütununda `srclc:tur` bulunan kayıtlar (Türkçe kaynak); GCAM sütunu boyut nedeniyle atıldı (`fetch.sh`). Pencere içinde Türkçe kaynaklı toplam kayıt: 606.455.
- **Çekirdek küme:** URL'sinde *karlov / büyükelçi / suikast / altıntaş / mevlüt* geçen kayıtlar; URL'ye göre tekilleştirme sonrası 4.185 haber, 211 site (`stats_core.py`).
- **Yayın grupları:** Ayrı bir medya indeksi çalışmasının KEY_OUTLETS listesi; liste tarihsizdir (sınırlılık: Bölüm 3).
- **Zaman:** GDELT `DATE` alanı UTC'dir ve dosyanın tarama zamanını gösterir; TSİ = UTC + 3. Saatlik eğri bu çevrimle çizildi [GDELT-ek].
- **Ton:** GDELT `V2Tone` alanının ilk bileşeni (olumlu – olumsuz sözcük yüzdesi); makine çevirisi üzerinde hesaplanır.
- **Çerçeve sözlüğü (URL slug'ı üzerinde, küçük harf, URL-çözülmüş):** FETÖ/Gülen (`fetö|feto|gülen|gulen|fetullah|fethullah`); cihatçı (`nusra|el-kaide|cihat|cihad|ışid|isid|deaş|daeş|isis|selefi`); Halep/Suriye (`halep|suriye|aleppo`); provokasyon (`provokas`); güvenlik açığı (`güvenlik zaafı|koruma|zafiyet|ihmal|güvenlik açığı`); Nurettin Yıldız/Sosyal Doku (`nurettin|nureddin|sosyal-doku`); Samanyolu dizisi (`samanyolu|nizama|stv`); ABD/Batı (`abd|cia|amerika|nato|batı` sözcük olarak).
- **Düzeltme:** İlk sayımda alt dize eşleşmeleri yanlış pozitif üretti (ör. "dışişleri" ve "saldırısıdır" içindeki "isid"; ilk "cihatçı" URL bu yüzden bir Dışişleri haberiydi). `cerceve_duzeltilmis.json` bu hataları ayıklanmış sayımları içerir ve raporda kanonik değer olarak kullanıldı [GDELT-istatistik].
- **Duyarlılık testi :** Sözcük sınırına dayalı bağımsız bir yeniden sayımda cihatçı çerçeve tümü 44, hükümete yakın 3, muhalif/bağımsız 13; FETÖ/Gülen 217 (aynı) çıktı; Samanyolu sayısı sözlüğe göre 51–57 arasında değişiyor [GDELT-ek]. **[D]** Ana bulgu (hükümete yakın yayınlarda FETÖ çerçevesinin cihatçı çerçeveye yaklaşık 15 kat baskınlığı) sözlük değişikliklerine karşı dayanıklıdır.
- **Bilinen kör noktalar:** "Cemaat" sözcüğü FETÖ/Gülen sözlüğünde yoktur (rejim kontrolünde olmayan kaynakların kullandığı terim); başlığa taşınmayan çerçeveler sayılmaz; GDELT 2019 öncesi başlık tutmaz.
- **Atıf:** Bu çalışmadaki tüm medya istatistikleri The GDELT Project verisinden türetilmiştir (https://www.gdeltproject.org).

## B.2 Admiralty derecelendirmesi {.unnumbered}

Kaynak güvenilirliği (A–F) kurumun geçmişine ve vakadaki konumuna göre; bilgi doğruluğu (1–6) başka kaynaklarla teyit durumuna göre verildi. Resmî açıklamalar kurum iddiası olarak derecelendirildi; Türk, Rus ve hükümetten bağımsız kaynaklara aynı ölçüt uygulandı. Yazarın vakada kişisel çıkar çatışması olduğu durumlarda bu, kart notunda belirtildi ve kaynak harfi en fazla C olarak tutuldu.

## B.3 ACH {.unnumbered}

Heuer yöntemi; T/Ç/N işaretleme; ağırlık = kaynak × bilgi katsayısı; sıralama ağırlıklı tutarsızlığa göre; mekanik sonuç analist yargısıyla düzeltildi ve düzeltmenin gerekçesi Bölüm 8'de açıkça yazıldı. Olasılık aralıkları analitik yargıdır.

## B.4 Kronoloji ve saat dilimi {.unnumbered}

Olay günü satırları TSİ'dir; AiF, RBC ve Kremlin saatleri MSK'dir ve Aralık 2016'da TSİ ile aynıdır. Rus canlı akış saatleri haberin akışa düştüğü anı gösterir.
