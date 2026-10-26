<div class="cover">
<div class="draft">TASLAK — İNSAN ONAYI BEKLİYOR</div>
<p class="kicker">Açık kaynak istihbarat (OSINT) analizi</p>
<h1 class="title">Andrey Karlov Suikastı<br/>Ankara, 19 Aralık 2016</h1>
<p class="subtitle">Dakika dakika kronoloji, medya çerçevelemesinin nicel analizi, Rusya ve uluslararası tepkiler, failin radikalleşme süreci ve rakip hipotezlerin kanıtla sınanması</p>
<table class="covermeta">
<tr><td>Hazırlanma</td><td>26 Ekim 2026 (Europe/Brussels)</td></tr>
<tr><td>Kaynak tabanı</td><td>294 kanıt kartı/satırı (K 42 · KR 127 · R 69 · RD 56) + GDELT GKG 2.1 yeniden kurulumu (4.185 haber, 211 site)</td></tr>
<tr><td>Hipotezler</td><td>Ön kayıtlı: H1, H2, H3a, H3b, H4, H5a (kanıt toplamadan önce zaman damgalı)</td></tr>
<tr><td>Durum</td><td>Taslak; yargısal bulgu değildir; insan editör onayı olmadan dağıtılmamalıdır</td></tr>
</table>
<p class="gdelt">Medya verisi: <b>The GDELT Project</b> (https://www.gdeltproject.org) — Global Knowledge Graph 2.1, çeviri akışı (translation GKG), Türkçe kaynaklı kayıtlar, 17.12.2016–10.01.2017. GDELT verisinin kullanımı kaynak gösterimini zorunlu kılar; bu raporda GDELT'ten türetilen her sayı [GDELT-istatistik] veya [GDELT-ek] etiketiyle işaretlidir.</p>
</div>

# Kaynak tabanı ve okuma kılavuzu {.unnumbered}

## Kaynak tabanı özeti {.unnumbered}

| Dosya | Kart/satır | Sınıf dağılımı (kaynak sınıfı) | Derece / erişim |
|---|---|---|---|
| `kanitlar.json` (K01–K42) | 42 | Mahkeme/iddianame aktarımı 9 · Batı basını 7 · TR hükümete yakın 4 · TR ana akım 3 · Arap/Körfez basını 3 · düşünce kuruluşu 3 · resmî-TR 2 · resmî-RU 2 · TR devlet basını 2 · rejim kontrolünde olmayan kaynaklar 2 · Rus devlet basını 1 · Rus basını 1 · Avrupa basını 1 · uluslararası kuruluş 1 · TR muhalefet 1; devlet bağlantılı 15/42 | Kaynak: A 5 · B 12 · C 20 · D 5. Bilgi: 1→3 · 2→15 · 3→15 · 4→8 · 5→1 |
| `kronoloji.json` (KR-001–KR-127) | 127 (54'ü olay günü) | TR devlet medyası 30 · yabancı bağımsız medya 28 · Rus devlet medyası 21 · TR hükümete yakın 15 · TR ana akım (Doğan dönemi) 11 · TR muhalif/bağımsız 9 · resmî kurum 6 · rejim kontrolünde olmayan kaynaklar 5 · 2018 geçiş yılı 1 · sınıfsız 1 | Açıldı 119 · yalnızca arama özeti 7 · bulunamadı 1; çelişki notlu 49 |
| `rusya_dunya.json` (R01–R69) | 69 | Rus devlet medyası 15 · Rus resmî kurum 11 · Rus bağımsız medya 10 · yabancı bağımsız medya 12 · Rusya'da hükümete yakın yayın 8 · akademik 4 · uluslararası kuruluş 3 · TR devlet medyası 2 · TR resmî 1 · TR yayın 1 · ABD resmî 1 · İran devlet medyası 1 | A 17 · B 47 · C 5; bilgi 1→42 · 2→21 · 3→4 · 5→2; açıldı 56 · arama özeti 13 |
| `radikallesme_kartlar.json` (RD01–RD56) | 56 | TR devlet medyası 16 · rejim kontrolünde olmayan kaynaklar 13 · TR muhalif/bağımsız 11 · TR hükümete yakın 7 · TR ana akım (Doğan dönemi) 5 · yabancı bağımsız 2 · diğer 2 | A 2 · B 16 · C 33 · D 5; açıldı 37 · arama özeti 17 · temel kartlardan 2 |
| GDELT GKG 2.1 yeniden kurulumu | 2.400 adet 15 dakikalık dosya (8'i boş); Türkçe kaynaklı 606.455 kayıt; çekirdek küme 4.185 haber, 211 site | Yayın grupları: hükümete yakın 322 · muhalif/bağımsız 276 · ana akım 257 · yabancı yayınların Türkçe servisleri 176 · ulusalcı 111 · haber ajansları 101 · rejim kontrolünde olmayan kaynaklar 11 · diğer (yerel/portal) 2.931 | URL düzeyinde sayım; bkz. Ek B |

*Not:* "Rejim kontrolünde olmayan kaynaklar" ifadesi bu raporda TR724, Turkish Minute, Nordic Monitor, Stockholm Center for Freedom (SCF) ve Samanyolu Haber gibi Türkiye hükümetinin denetimi dışında, çoğunlukla yurt dışından yayın yapan yayın organları için kullanılır. Bu yayınlar hükümetten bağımsızdır; bu bağımsızlık onların iddialarını otomatik olarak doğru kılmaz, her iddia teyit durumuna göre ayrıca derecelendirilir. Hürriyet, Hürriyet Daily News ve CNN Türk 2016'da Doğan Grubu'ndaydı ve 2018'de el değiştirdi; girdi dosyalarında bu yayınların bir kısmı "muhalif/bağımsız" olarak kodlanmıştı, bu raporda yayın tarihine göre "ana akım (Doğan dönemi)" ya da "hükümete yakın (Demirören dönemi)" olarak düzeltildi (Ek A'da † işaretli).

## Okuma kılavuzu {.unnumbered}

**Cümle türleri.** Her madde ya da cümle, başındaki işaretle türünü belirtir:

| İşaret | Tür | Anlamı |
|---|---|---|
| **[O]** | Olgu | Bir kaynağın aktardığı bilgi. Resmî açıklamalar "kurum iddiası" olarak yazılır; bir kurumun bir şey söylemiş olması olgudur, söylediğinin doğru olması ayrıca değerlendirilir. |
| **[D]** | Değerlendirme | Analitik yargı. Nedensellik ve niyet içeren her değerlendirme aşağıdaki olasılık sözcükleriyle yazılır. |
| **[S]** | Açık soru | Mevcut kamuya açık kanıtla yanıtlanamayan konu. Bölüm 10'da hangi belgeyle kapanacağı belirtilir. |

**Kimlik etiketleri.** [K..] temel kanıt kartı · [KR-...] kronoloji satırı · [R..] Rusya/dünya kartı · [RD..] radikalleşme kartı · [GDELT-istatistik] girdi dosyalarındaki GDELT istatistiği (`stats_core.json`, `cerceve_duzeltilmis.json`) · [GDELT-ek] aynı ham GDELT kayıtlarından yapılan URL düzeyi ek kontrol (`work/karlov_v2/gdelt_ek.json`) · [RAD-A§n] radikalleşme literatürü özeti (`radikallesme.md`, Parça A, n. alt bölüm) · [RAD-B] aynı dosyanın Parça B künyesi ve kaynak eleştirisi · [ACH] ACH yöntem dosyası. "(arama özeti)" ibaresi, kaynağın sayfası açılmadan yalnızca arama sonucu özetinden alındığını gösterir; bu bilgiler ihtiyatla kullanılır.

**Admiralty (NATO) ölçeği.** Her kart iki boyutta derecelendirilir:

| Kaynak güvenilirliği | | Bilginin doğruluğu | |
|---|---|---|---|
| A | Tamamen güvenilir | 1 | Başka kaynaklarca teyitli |
| B | Genellikle güvenilir | 2 | Muhtemelen doğru |
| C | Oldukça güvenilir | 3 | Olası |
| D | Genellikle güvenilir değil / taraflı | 4 | Şüpheli |
| E | Güvenilmez | 5 | Olasılık dışı |
| F | Değerlendirilemez | 6 | Değerlendirilemez |

**Olasılık sözcükleri.** neredeyse kesin (≥%90) · muhtemel / büyük olasılıkla (%60–89) · olası (%35–59) · düşük olasılık (%15–34) · olası değil (%5–14) · çok düşük (<%5).

**Kişiler.** Fail ve kamu figürleri (bakanlar, sözcüler, mahkûm edilen ya da firari olarak aranan baş sanıklar, gazeteciler, vaizler) adıyla; failin akrabaları, tanıklar, yaralılar ve dosyada adı geçen diğer özel kişiler rolüyle anılır. Hipotezler hiçbir kişiye atfedilmez; yalnızca nötr kodlarla (H1…H5a) anılır.

**Saatler.** Aksi belirtilmedikçe saatler Türkiye saatidir (TSİ, UTC+3). Aralık 2016'da Moskova saati (MSK) de UTC+3 olduğundan Rus kaynaklarındaki saatler TSİ ile aynıdır [KR-030]. GDELT dosya zamanları UTC'dir; metinde TSİ'ye çevrilmiştir.


# Yönetici özeti

1. **[O]** Rusya'nın Ankara Büyükelçisi Andrey Karlov, 19 Aralık 2016 akşamı Ankara Çağdaş Sanat Merkezi'ndeki sergi açılışında konuşurken arkadan vuruldu; İçişleri Bakanlığı'nın resmî saati 19:05'tir [KR-017], [KR-018], [KR-019]. **[O]** Fail, 2,5 yıldır Ankara Çevik Kuvvet'te görevli 22 yaşındaki polis Mevlüt Mert Altıntaş'tır; X-ray'den geçmeden polis kimliğini göstererek içeri girdi [KR-038], [KR-014], [RD01]. **[O]** Bakanlık iddiasına göre Karlov'da 19:53'te hastanede hayati bulgu yoktu [KR-034]. **[O]** Fail çatışmada öldürüldü; çatışmanın süresi kaynaklarda 15 dakika (BBC) ile 25 dakika (Lenta.ru, Karlov'un yerde kaldığı süre) arasında değişiyor [KR-027], [KR-028].

2. **[O]** Fail ateş ettikten sonra bozuk Arapçayla bir cihat biatı dizesi okudu ve Türkçe "Halep'i unutmayın, Suriye'yi unutmayın" diye bağırdı; bu kısım video kaydındadır [RD55], [K01], [KR-024], [KR-023]. **[D]** Sözlerin söylendiği neredeyse kesindir; onların gerçek bir inancı mı yoksa planlı bir "hedef şaşırtma"yı mı yansıttığı, hipotezleri ayıran temel yorum sorusudur.

3. **[O]** Failin Selefi-cihatçı yönde bilişsel radikalleşmesine dair kanıt geniş bir kaynak tabanına dayanıyor: saldırıdan bir gün önce bir tanığa bıraktığı valizde Seyyid Kutub, Hasan el-Benna, Nurettin Yıldız ve Abdulkadir Şen kitapları [RD27]; Şubat 2016'da indirilip 18 Aralık 2016'da silinen bir El Kaide videosu [RD38]; Ağustos–Aralık 2016 arasında Halis Bayancuk, Awlaki ve Kouachi kardeşler aramaları [RD39]; iki ayrı tanığın aktardığı Suriye'ye gitme isteği [RD33], [RD34]; 2014–2016 arasında Nurettin Yıldız/Sosyal Doku sohbetlerine düzenli katılım [RD11], [RD13], [RD16]. **[D]** "Dizüstünde cihatçı içerik yok" okuması [K21] yanlıştır: Rus heyetinin bulgusu yalnızca *silinmiş* dosyalarla ilgiliydi; silinmemiş dosyalarda cihatçı içerik vardı [RD40], [RD38].

4. **[O]** İlk resmî metin olan Dışişleri Bakanlığı'nın 327 sayılı açıklaması hiçbir örgüt adı vermedi [KR-047], [K12]. **[O]** Aynı gece bir AKP milletvekili, Suriye bağlantısını "çok düşük ihtimal" sayarak eleme yoluyla FETÖ'yü işaret etti [K05]; Ankara Büyükşehir Belediye Başkanı da Twitter'da olası bir Gülen bağlantısını ima etti ve BBC'ye göre ilk günlerde ortaya atılan bağlantıların hiçbiri kanıtlanmadı [K04], [KR-060]. **[O]** Cumhurbaşkanı 21 Aralık'ta failin "FETÖ terör örgütüne mensup" olduğunu söyledi [KR-082], [K08]. **[O]** GDELT verisinde URL'sinde FETÖ/Gülen geçen ilk haberler 19 Aralık 22:00 TSİ'de, Star ve Yeni Akit'te, "Rus ajansı: FETÖ'nün suikasti olabilir" başlığıyla çıktı [GDELT-istatistik], [GDELT-ek]. **[D]** Siyasi atıf, kamuya açıklanmış herhangi bir soruşturma bulgusundan önce geldi; bu neredeyse kesindir.

5. **[O]** Rusya'nın resmî tarafı FETÖ tezini ne onayladı ne reddetti: Putin olay gecesi "provokasyon" dedi ve "katilin elini kimin yönlendirdiğini öğrenmeliyiz" diye ekledi [R02], [R04]; Kremlin 21 Aralık'ta "sonuç çıkarmakta acele etmeyin" dedi [R18]; Rusya Dışişleri 2021 kararından "memnuniyet" duyduğunu söylerken azmettiriciler hakkında "kapsamlı bilgi" beklediğini ve sorumluluğun bir kısmını Suriye konusunda medyada "olumsuz atmosfer yaratan çevrelere" yükledi [R42], [KR-116]. **[D]** Türk medyasında FETÖ çerçevesinin ilk kez bir Rus kaynağına atıfla girmesi, o saatlerde Rus resmî tarafının bu tezi dile getirdiğine dair hiçbir kart bulunmaması nedeniyle, bir "çerçeve ithali / atıf aklama" örneği olabilir (olası; kanıtlanmamış).

6. **[O]** Yargı süreci: iddianame Kasım 2018'de 28 şüpheli hakkında sunuldu [KR-106]; 9 Mart 2021'de üç sanığa ikişer, iki sanığa birer kez ağırlaştırılmış müebbet verildi, altı sanık beraat etti [KR-114], [K28]; Yargıtay 2023'te 13 sanıktan 12'sinin cezasını onadı [KR-119], [K29]. **[O]** Gerekçeli karar, Altıntaş'ın FETÖ'nün "renklendirme" talimatıyla Sosyal Doku'ya sızdığını ve Şahin Söğüt'ün 9 Aralık 2016'da ona talimat verdiğini kabul etti [RD43], [RD44]. **[D]** Kararın dayandığı iletişim içerikleri kamuya açık değil; failin kendisinin ByLock kullanmadığı belirlendi [RD46]; bu nedenle mahkeme bulgusu açık kaynaklarla bağımsız olarak sınanamıyor.

7. **[O]** Savcılık kaynaklı habere göre failin Gmail yazışmaları, fail öldükten yaklaşık 2,5 saat sonra silindi [KR-099], [K20]; başka bir aktarıma göre Gmail ve Facebook yazışmaları "suikast saatlerinde" VPN/sanal bilgisayar üzerinden silindi [KR-100]. **[D]** Bu bulgu doğruysa "tamamen yalnız fail" (H2) hipotezini ciddi biçimde zayıflatır; silen kişinin kim olduğu ve hangi çevreye ait olduğu bilinmiyor.

8. **[O]** Medya çerçevelemesi yayın grubuna göre keskin biçimde ayrıştı: hükümete yakın yayınların 322 haberinde URL'de FETÖ/Gülen 44, cihatçı terimler 3 kez geçti (yaklaşık 15 kat); muhalif/bağımsız yayınların 276 haberinde 14'e 14; ana akımın 257 haberinde 5'e 0 [GDELT-istatistik]. **[O]** Nurettin Yıldız/Sosyal Doku hattı tüm çekirdek kümede yalnızca 5 URL'de, yalnızca 24 Aralık'ta geçti; 27–28 Aralık'ta ise "suikast Samanyolu TV'de işlenmiş" başlıklı 51 URL'lik eşzamanlı bir haber dalgası oluştu [GDELT-istatistik]. **[D]** Bu ayrışma bir medya hegemonyası örüntüsüyle uyumludur; tek başına hiçbir hipotezin doğruluğu hakkında kanıt değildir.

9. **[D]** Güncel hipotez sıralaması: H3a (Türkiye'deki İslamcı-cihatçı ortamda radikalleşme, örgütsel emir yok) **muhtemel** (≈%55–70); H5a (Gülen çevresiyle erken temas + İslamcı çevrede dönüşüm + Halep tetikleyicisi + kimliği belirsiz yardımcı) **olası** (≈%35–50); H1 (resmî tez: FETÖ organizasyonu) **düşük olasılık–olası sınırında** (≈%20–35); H3b (cihatçı ağ yönlendirmesi) **olası değil** (≈%5–15); H2 (saf yalnız aktör) **olası değil** (≈%5–10); H4 (üçüncü devlet provokasyonu) **çok düşük** (<%5). Hipotezler birbirini dışlamaz; aralıkların toplamı 100 değildir.


11. **[S]** Sonucu değiştirebilecek en kritik belirsizlikler: Söğüt–Altıntaş iletişiminin içeriği [K22], [RD44]; Gmail silme işleminin hangi cihaz ve IP'den yapıldığı [KR-099]; failin telefonunun ikinci 16 haneli şifresinin hiç çözülüp çözülmediği [KR-105]; Rusya Soruşturma Komitesi'nin kendi dosyasının içeriği [R41], [R39]; iddianamenin ve gerekçeli kararın tam metni [KR-106].

12. **[O]** 2026'da dosya yeniden gündeme geldi: MİT, firari sanık Cemal Karaata'nın Kanada'da "Salih Ada" adıyla yaşadığını açıkladı [KR-121], Rus devlet ajansı Kanada sicilinde eski adının açıkça yazdığını bildirdi [KR-123]; MİT, Nordic Monitor kurucusu gazeteci Abdullah Bozkurt hakkında suç duyurusunda bulundu [KR-124], [KR-125], [K38]. **[O]** GDELT verisi, "suikastçının Abdullah Bozkurt'un evinde kaldığı" iddiasının 19–20 Aralık 2016 gecesi hükümete yakın sitelerde zaten dolaşımda olduğunu gösteriyor [GDELT-ek]. **[D]** Bu, 2026 iddiasını "9,5 yıl sonra ilk kez ortaya atılan" bir iddia olarak niteleyen değerlendirmeyi [RD53] kısmen düzeltir: ev iddiası 2016'dan, "radikalleştirme ve yönlendirme" suçlaması ise 2026'dan kalmadır.

# Dakika dakika kronoloji

Bu bölüm `kronoloji.json` dosyasındaki 127 satırın tamamını dört döneme ayırarak verir. Tablolardaki her satır bir **[O]** olgu satırıdır: kaynağın aktardığı bilgidir, doğruluğu "Erişim / çelişki" sütunu ve aşağıdaki çelişki kutusuyla birlikte okunmalıdır. Olay sütunundaki "iddianame" ibaresi, bilginin bir kurum iddiası olduğunu gösterir.

## Olay öncesi (2014 – 18 Aralık 2016)

**[O]** İddianameye göre Samanyolu TV'deki bir dizinin 30 Aralık 2014'te yayımlanan 89. bölümünde resim sergisindeki bir büyükelçiye suikast girişimi canlandırıldı [KR-001]. **[O]** İddianameye göre ilk girişim 27 Haziran 2016'daki AK Parti büyükelçiler iftarında planlandı ve Karlov yurt dışında olduğu için gerçekleşmedi [KR-002], [K24]. **[O]** Bir habere göre fail 4 Ekim 2016'da FETÖ şüphesiyle açığa alındı ve 16 Kasım'da göreve iade edildi [KR-003]; Emniyet ise 21 Aralık 2016'da açığa alınma iddiasını yalanladı [RD49]. **[O]** İddianameye göre fail 14 Aralık'ta otel rezervasyonu yaptı, sergi açılışının ertelenmesi üzerine 15 Aralık 23:21'de rezervasyonu 19–20 Aralık olarak değiştirdi [KR-004], [KR-006]. **[O]** Sergi 16 Aralık'ta açıldı ve tanıklara göre fail o gün sergiyi dolaştı (keşif şüphesi) [KR-007], [RD07].

<div class="tbl-kr_a">

| KR | Tarih | Saat (TSİ) | Olay | Kaynak · sınıf | Erişim / çelişki |
|---|---|---|---|---|---|
| KR-001 | 2014-12-30 | — | İddianameye göre Samanyolu TV'deki 'Nizama Adanmış Ruhlar' dizisinin 89. bölümünde resim sergisindeki bir büyükelçiye suikast girişimi canlandırıldı (iddianame iddiası). | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-002 | 2016-06-27 | — | İddianameye göre ilk suikast girişimi: AK Parti büyükelçiler iftarına Altıntaş koruma polisi olarak sızacaktı; Karlov yurt dışında olduğu için katılmadı (iddianame iddiası). | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-003 | 2016-10-04 | — | Altıntaş'ın FETÖ şüphesiyle 4 Ekim'de açığa alındığı, 16 Kasım'da göreve iade edildiği bildirildi. | Hürriyet Daily News · yurt içi ana akım (Doğan dönemi)† | açıldı · ⚠ çelişki notu |
| KR-004 | 2016-12-14 | 21:54 ve 22:16 | İddianameye göre Altıntaş otelden 16 Aralık giriş, 1 gece konaklama için rezervasyon yaptı. | Anadolu Ajansı · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-005 | 2016-12-14 | — | Cumhuriyet: Altıntaş ÇSM'ye 300 metre yakındaki oteli arayarak rezervasyon yaptırdı. | Cumhuriyet · yurt içi muhalif/bağımsız | açıldı · ⚠ çelişki notu |
| KR-006 | 2016-12-15 | 23:21 | İddianameye göre sergi açılışının ertelenmesi üzerine rezervasyon 19 Aralık giriş/20 Aralık çıkış olarak değiştirildi. | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-007 | 2016-12-16 | — | Sergi 16 Aralık'ta açıldı; tanıklara göre Altıntaş o gün sergiye gelip dolaştı (keşif şüphesi). Resmi açılış Büyükelçilikçe 19 Aralık'a alındı. | Cumhuriyet · yurt içi muhalif/bağımsız | açıldı · ⚠ çelişki notu |
| KR-008 | 2016-12-18 | — | 2016 basınına göre Altıntaş saldırıdan bir gün önce otelin 214 numaralı odasına yerleşti. | Hürriyet · yurt içi ana akım (Doğan dönemi)† | açıldı · ⚠ çelişki notu |

</div>

Kronoloji dosyası dışındaki kartlardan olay öncesine ait önemli bağlam satırları:

| Tarih | Olay | Tür | Kart |
|---|---|---|---|
| 27.06.2016 | Erdoğan'ın Putin'e mektubu; normalleşmenin başlangıcı (Kremlin aktarımı) | [O] | [K18] |
| 16–17.07.2016 | Fail senelik izin kullandı; izni sonradan FETÖ'den tutuklanan bir şube müdürü verdi; abla aynı günlerde bir düğün için İzmir'de olduğunu söylüyor | [O] | [RD51] |
| 25.08.2016 | Teknik rapora göre Halis Bayancuk araması (rejim kontrolünde olmayan kaynak aktarımı) | [O] | [RD39] |
| 05.09.2016 | Bir derneğe para gönderdiği ve dernek yöneticisiyle iki kez görüştüğü iddiası (tek kaynak) | [O] | [RD36] |
| 08.10.2016 | İstanbul'da Selefi yazar Abdulkadir Şen'le görüştüğü iddiası (tek kaynak) | [O] | [RD37] |
| 18–19.10.2016 | Erdoğan: Putin'le Fetih eş-Şam'ın Halep'ten çıkarılması konusunda anlaştık | [O] | [K16] |
| 15.11.2016 sonrası | İddianameye göre hatsız telefon ve Wi-Fi üzerinden Söğüt'le iletişim | [O] kurum iddiası | [K22] |
| Kasım sonu 2016 | Kız arkadaşına "Şahadet istiyorum" yazışması (savcılık kaynaklı) | [O] | [RD41] |
| 09.12.2016 | Gerekçeli karara göre Söğüt'ün talimat verdiği gün; iddianameye göre Söğüt'ün telefonu failin evine 256 m mesafede sinyal verdi | [O] kurum iddiası | [RD44], [K22] |
| 12–15.12.2016 | Ebu Basir el-Hindi (12.12) ve Awlaki (15.12) aramaları | [O] | [RD39] |
| 13.12.2016 | Ankara'da Rus Büyükelçiliği önünde hükümete yakın STK'ların protestosu | [O] | [K41] |
| 14.12.2016 | Tanığa göre İHH'nin "Halep'e Yol Aç" konvoyu davetini izin planı nedeniyle reddetti | [O] | [RD34] |
| 15.12.2016 | Doğu Halep tahliyesi başladı (22 Aralık'ta tamamlandı, ≈35.000 kişi) | [O] | [K14] |
| 17.12.2016 | İHH konvoyu sınırda "Rusya Suriye'den defol" protestosuna dönüştü | [O] | [K15] |
| 18.12.2016 | Kitap valizini bir tanığa bıraktı; El Kaide videosu ortak dizüstünde silindi; Kouachi kardeşler ve Bhutto suikastı aramaları | [O] | [RD27], [RD38], [RD39] |

## 19 Aralık 2016: olay günü (54 satır)

**[O]** Olay günü satırları 12:15'te otele girişle başlar [KR-009] ve Rusya Soruşturma Komitesi'nin 23:53'teki resmî duyurusuyla kapanır [KR-059]. **[O]** Rus canlı akışlarındaki (AiF, RBC) saatler haberin akışa düştüğü anı gösterir, olayın kendisini değil [KR-030], [KR-049]. **[O]** Türk televizyonları 19:14 (FOX) ile 19:21 (Show) arasında yayına girdi [KR-029]; GDELT'teki ilk haber dosyası 19:30 TSİ tarihlidir [GDELT-istatistik].

<div class="tbl-kr_b">

| KR | Tarih | Saat (TSİ) | Olay | Kaynak · sınıf | Erişim / çelişki |
|---|---|---|---|---|---|
| KR-009 | 2016-12-19 | 12:15 | İddianameye göre Altıntaş otele geldi, bir gecelik ücreti kredi kartıyla ödedi, 204 numaralı odaya yerleşti. | Anadolu Ajansı · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-010 | 2016-12-19 | 16:10 | Kuru temizlemeye verilen takım elbise Altıntaş'a teslim edildi (iddianame). | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-011 | 2016-12-19 | 17:30 civarı | Altıntaş otelden çıktı (2016 basını). | Hürriyet · yurt içi ana akım (Doğan dönemi)† | açıldı · ⚠ çelişki notu |
| KR-012 | 2016-12-19 | 18:30 | Sergi açılışı 18.30'da başladı; Altıntaş otelden yürüyerek ÇSM'ye geldi. | Cumhuriyet · yurt içi muhalif/bağımsız | açıldı |
| KR-013 | 2016-12-19 | — | Otelde tıraş olup takım elbise ve kravatla yaya olarak ÇSM'ye geçti. | Hürriyet · yurt içi ana akım (Doğan dönemi)† | açıldı |
| KR-014 | 2016-12-19 | — | Girişte X-Ray'den geçmeyen Altıntaş özel güvenlikçe uyarıldı; polis kimliğini göstererek içeri girdi (Çankaya Belediyesi açıklaması). | Hürriyet · yurt içi ana akım (Doğan dönemi)† | açıldı · ⚠ çelişki notu |
| KR-015 | 2016-12-19 | — | Livemint/AFP: Altıntaş üç şarjör ve ceplerinde toplam 75 mermiyle geldi. | Livemint (AFP) · yabancı bağımsız medya | **arama özeti** · ⚠ çelişki notu |
| KR-016 | 2016-12-19 | 19:00 (plan) | İddianame/soruşturmaya göre TRT'nin sergiden 3G ile canlı yayın yaptığı incelendi; iddianame bunu 'habercilikle açıklanamaz' buldu. | İstiklal · hükümete yakın yayın | açıldı |
| KR-017 | 2016-12-19 | 19:05 civarı | Karlov konuşma yaparken arkadan ateş açıldı (İçişleri Bakanı Soylu'nun resmi saati). | Anadolu Ajansı · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-018 | 2016-12-19 | 19:05 (16:05 GMT) | BBC: saldırı yerel saatle 19:05 civarı; 11 atış, 9'u büyükelçiye, 2'si havaya. | BBC News · yabancı bağımsız medya | açıldı |
| KR-019 | 2016-12-19 | 19:05 | DW Türkçe Soylu açıklamasını aktarıyor: 19:05 saldırı, 19:53 hastanede hayati bulgu yok. | DW Türkçe · yabancı bağımsız medya | açıldı |
| KR-020 | 2016-12-19 | — | Lenta.ru: Karlov kürsüde konuşmaya başladıktan 'bir dakikadan kısa' süre sonra vuruldu; tanıklar 8 atış saydı. | Lenta.ru · yabancı bağımsız medya | açıldı · ⚠ çelişki notu |
| KR-021 | 2016-12-19 | — | AP: Karlov sergide birkaç dakikadır konuşuyordu; hastaneye kaldırıldı ve öldü (AP fotoğraf altı). | AP Images Blog · yabancı bağımsız medya | açıldı · ⚠ çelişki notu |
| KR-022 | 2016-12-19 | — | AP foto muhabiri Burhan Özbilici'nin anlatımı: en az 8 atış; saldırgan cesedin çevresinde dolaşıp fotoğrafları kırdı, Arapça ve Türkçe bağırdı. | The Guardian (AP, Burhan Özbilici) · yabancı bağımsız medya | açıldı |
| KR-023 | 2016-12-19 | — | Özbilici: saldırgan 'Allahu ekber' ve Halep hakkında bağırdı, cesedin çevresinde dolaşarak duvardaki fotoğrafları kırdı. | AP Images Blog (Burhan Özbilici) · yabancı bağımsız medya | açıldı |
| KR-024 | 2016-12-19 | — | Sloganlar: 'Halep'i unutmayın, Suriye'yi unutmayın... Sadece ölüm beni durdurur. Biz Halep'te ölüyoruz, sen burada öleceksin.' | Lenta.ru · yabancı bağımsız medya | açıldı |
| KR-025 | 2016-12-19 | — | Hürriyet: Adli Tıp tutanağına göre 11 el ateş, 9 isabet; silah Canik 9x19; trafik polisleri JFK Caddesi'nde ilk müdahaleyi yaptı; teslim ol çağrısına 'sağ çıkmaya gelmedim' yanıtı (iddia). | Hürriyet · yurt içi ana akım (Doğan dönemi)† | açıldı · ⚠ çelişki notu |
| KR-026 | 2016-12-19 | — | Soylu: Çankaya Polis Merkezi ekipleri müdahale etti, çatışma sürerken gelen Özel Harekât saldırganı etkisiz hale getirdi. | Anadolu Ajansı · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-027 | 2016-12-19 | — | BBC: saldırgan teslim olmayı reddetti, polisle yaklaşık 15 dakika çatıştıktan sonra öldürüldü. | BBC News · yabancı bağımsız medya | açıldı · ⚠ çelişki notu |
| KR-028 | 2016-12-19 | — | Lenta.ru: Özel harekât gelip saldırganı öldürdüğünde Karlov 25 dakikadır yerde yatıyordu. | Lenta.ru · yabancı bağımsız medya | açıldı |
| KR-029 | 2016-12-19 | 19:14–19:21 | TV'lerin yayına giriş saatleri: FOX 19.14, ATV 19.15, Kanal D 19.17, Star 19.19, Show 19.21. İlk kare fotoğraf bir Hürriyet muhabiri'a ait. | Milliyet (Sina Koloğlu) · hükümete yakın yayın | açıldı |
| KR-030 | 2016-12-19 | 19:20 | Türk medyası büyükelçiye silahlı saldırıyı duyurdu (AiF canlı akışı). | Argumenty i Fakty · Rus devlet medyası | açıldı |
| KR-031 | 2016-12-19 | 19:24 | Spektr (Daily Sabah'a atfen): büyükelçi yaralandı, hastaneye kaldırıldı, en az 5 kez ateş edildi. | Spektr.press · rejim kontrolünde olmayan kaynaklar | açıldı · ⚠ çelişki notu |
| KR-032 | 2016-12-19 | 19:28 | AiF: saldırı 'Türklerin gözüyle Rusya' sergisi açılışında, Karlov konuşurken oldu. | Argumenty i Fakty · Rus devlet medyası | açıldı · ⚠ çelişki notu |
| KR-033 | 2016-12-19 | 19:49 | Rusya Dışişleri doğruladı: Zaharova büyükelçinin ateşli silahla yaralandığını söyledi. | Argumenty i Fakty · Rus devlet medyası | açıldı |
| KR-034 | 2016-12-19 | 19:53 | Soylu: Güven Hastanesi'nde 19.53'te hayati bulgu olmadığı tespit edildi, canlandırmaya yanıt alınamadı. | Anadolu Ajansı · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-035 | 2016-12-19 | 20:10 | Türk medyası saldırganın polisçe etkisiz hale getirildiğini duyurdu. | Argumenty i Fakty · Rus devlet medyası | açıldı |
| KR-036 | 2016-12-19 | 20:24 | RIA: Zaharova Karlov'un öldüğünü açıkladı; MİD olayı terör eylemi sayıyor; 'Terörizm geçmeyecek'. | RIA Novosti · Rus devlet medyası | açıldı · ⚠ çelişki notu |
| KR-037 | 2016-12-19 | 20:27 | TASS: Moskova cinayeti terör eylemi olarak nitelendirdi (Zaharova); Türkiye titiz soruşturma sözü verdi. | TASS · Rus devlet medyası | açıldı · ⚠ çelişki notu |
| KR-038 | 2016-12-19 | — | Soylu Güven Hastanesi önünde failin kimliğini açıkladı: 24.06.1994 Söke doğumlu, 2,5 yıldır Ankara Çevik Kuvvet'te görevli Mevlüt Mert Altıntaş. | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-039 | 2016-12-19 | — | Soylu: yaralılar üç yaralı (biri taburcu; biri Arnavutluk doğumlu TC vatandaşı). | Anadolu Ajansı · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-040 | 2016-12-19 | — | Soylu: Dışişleri Bakanı Çavuşoğlu Rusya'daydı; ertesi gün Moskova'da önemli toplantı vardı. | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-041 | 2016-12-19 | 21:05 | Rusya'ya taziyeler gelmeye başladı (Mogherini, Boris Johnson, ABD, Almanya, BM). | Argumenty i Fakty · Rus devlet medyası | açıldı |
| KR-042 | 2016-12-19 | 21:29 | RTÜK: Başbakanlığın 19.12.2016 tarih ve 4368 sayılı yazısıyla geçici yayın yasağı; resmi açıklamalar dışında haber/görüntü yasak. | Timeturk · hükümete yakın yayın | **arama özeti** · ⚠ çelişki notu |
| KR-043 | 2016-12-19 | — | AA: RTÜK, Başbakanlık tarafından geçici yayın kısıtlaması getirildiğini duyurdu. | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-044 | 2016-12-19 | 21:35 | AiF: Rusya Soruşturma Komitesi (SK) 'uluslararası korunan kişiye saldırı' maddesinden dava açtı. | Argumenty i Fakty · Rus devlet medyası | açıldı · ⚠ çelişki notu |
| KR-045 | 2016-12-19 | 21:50 | Failin adı (Mevlüt Mert Altıntaş) ilk kez medyada. | Argumenty i Fakty · Rus devlet medyası | açıldı |
| KR-046 | 2016-12-19 | 21:59 | Türk medyası: savcılık failin evinde arama başlattı. | Argumenty i Fakty · Rus devlet medyası | açıldı |
| KR-047 | 2016-12-19 | — | Dışişleri Bakanlığı No:327 basın açıklaması: 'Bu saldırının Türk-Rus dostluğuna gölge düşürmesine izin vermeyeceğiz.' | T.C. Dışişleri Bakanlığı · devlet kurumu/resmi | açıldı |
| KR-048 | 2016-12-19 | 22:14 | Türkiye İçişleri Bakanlığı failin polis olduğunu doğruladı (RIA'ya atfen). | Argumenty i Fakty · Rus devlet medyası | açıldı |
| KR-049 | 2016-12-19 | 22:42 | CNN Türk (isimsiz kaynak): failin Cebhetü'n-Nusra ile bağlantılı olabileceği. | RBC · yabancı bağımsız medya | açıldı |
| KR-050 | 2016-12-19 | 22:45 | Kremlin: Putin, Lavrov, Narışkin ve Bortnikov ile toplantı; 'provokasyon', 'haydutlar bunu hissedecek'. | Kremlin (Rusya Devlet Başkanlığı) · devlet kurumu/resmi | açıldı · ⚠ çelişki notu |
| KR-051 | 2016-12-19 | 22:47 | Anadolu'ya atfen: Erdoğan Putin'i telefonla bilgilendirdi. (İbrahim Kalın'ın açıklaması BBC Rusça'da.) | Argumenty i Fakty · Rus devlet medyası | açıldı · ⚠ çelişki notu |
| KR-052 | 2016-12-19 | — | BBC Rusça: Cumhurbaşkanlığı Sözcüsü Kalın, Erdoğan'ın Putin'i arayıp bilgilendirdiğini söyledi (CNN Türk'e atfen). | BBC Rusça · yabancı bağımsız medya | açıldı |
| KR-053 | 2016-12-19 | — | Erdoğan ulusa video mesaj: Putin'le görüştü, 'provokasyon', iki ülke de 'bu tuzağa düşmeyecek'. | RFE/RL · yabancı bağımsız medya | açıldı |
| KR-054 | 2016-12-19 | 22:55 | RBC, Soylu'ya atfen yaralıları sıraladı; bir yaralı taburcu, ikisi kol ve bacaktan tedavide. | RBC · yabancı bağımsız medya | açıldı |
| KR-055 | 2016-12-19 | 22:58 | Peskov: Rusya Türkiye'ye soruşturma ekibi gönderecek. | RBC · yabancı bağımsız medya | açıldı |
| KR-056 | 2016-12-19 | 23:02 | RBC özeti: CNN Türk'e göre failin evinde arama; kız kardeşi ve annesi gözaltında. Fail 2014'te İzmir polis okulunu bitirmiş, kimlikle girmiş. | RBC · yabancı bağımsız medya | açıldı |
| KR-057 | 2016-12-19 | 23:28 | BM Güvenlik Konseyi cinayeti terör eylemi olarak tanıdı. | RBC · yabancı bağımsız medya | açıldı · ⚠ çelişki notu |
| KR-058 | 2016-12-19 | 23:39 | Putin-Erdoğan telefonunda soruşturma ekibi gönderilmesi ve diplomatik misyonların korunmasının artırılması kararlaştırıldı. | Argumenty i Fakty · Rus devlet medyası | açıldı |
| KR-059 | 2016-12-19 | 23:53 | Rusya Soruşturma Komitesi resmi duyurusu: cinayetle ilgili ceza davası açıldı (resmi site zaman damgası 23:53:43). | Rusya Soruşturma Komitesi (sledcom.ru) · devlet kurumu/resmi | açıldı |
| KR-060 | 2016-12-19 | — | BBC: Ankara Büyükşehir Belediye Başkanı Melih Gökçek Twitter'da failin Gülen hareketiyle bağlantısı olabileceğini yazdı; Gülenciler bağlantıyı reddetti. | BBC News · yabancı bağımsız medya | açıldı |
| KR-061 | 2016-12-19 | — | Söke'deki aile (anne, baba, kız kardeş) evlerinde hemen gözaltına alındı. | BBC News · yabancı bağımsız medya | açıldı |
| KR-062 | 2016-12-19 | — | Ankara Valiliği'nin olay gecesine ait yazılı açıklaması: bulunamadı. | — · — | **bulunamadı** |

</div>

**[O]** GDELT ek kontrolü, RTÜK yayın yasağına ilişkin ilk URL'nin (CNN Türk, "rtukten-andrey-karlov-suikastine-yayin-yasagi") 17:30 UTC dosyasında, yani en geç 20:30 TSİ'de bulunduğunu gösteriyor [GDELT-ek]. **[D]** KR-042'deki 21:29 saati bir sayfanın zaman damgasıdır; yasak haberinin en geç 20:30'da dolaşımda olduğu büyük olasılıkla doğrudur.

**[D]** Olay günü dizisinden çıkan analitik gözlemler: (1) failin otel, kıyafet ve giriş hazırlığı gün içinde saatlere yayılmış, planlı bir davranıştır [KR-009], [KR-010], [KR-013]; bu, anlık bir öfke patlaması okumasını neredeyse kesin olarak dışlar. (2) Olay gecesi Rus tarafı iki saat içinde terör nitelemesi yaptı [KR-036], [KR-037], dört saat içinde güvenlik kurulunu topladı [KR-050] ve beş saat içinde ceza davası açtı [KR-059]; Türk tarafının ilk yazılı metni ise örgüt adı vermedi [KR-047]. (3) Ankara Valiliği'nin olay gecesine ait yazılı açıklaması bulunamadı [KR-062].

## 20–31 Aralık 2016

**[O]** 20 Aralık'ta Rus soruşturma ekibi Ankara'ya indi [KR-070], [KR-071], Moskova'da üçlü toplantı yapıldı [KR-077] ve Çavuşoğlu Kerry'ye "Türkiye de Rusya da saldırının arkasında FETÖ'nün olduğunu biliyor" dedi [KR-078]. **[O]** 21 Aralık'ta sahte bir üstlenme bildirisi dolaşıma girdi ve aynı gün yalanlandı [KR-080], [KR-081], [KR-084]. **[O]** 24 Aralık'ta failin Nurettin Yıldız sohbetlerine katıldığı haberleri çıktı [KR-091], [KR-092]; 26 Aralık'ta mahkeme soruşturma süresince yayın yasağı getirdi [KR-094].

<div class="tbl-kr_c">

| KR | Tarih | Saat (TSİ) | Olay | Kaynak · sınıf | Erişim / çelişki |
|---|---|---|---|---|---|
| KR-063 | 2016-12-20 | 00:12 / 00:23 | Çavuşoğlu-Lavrov telefon görüşmesi; Çavuşoğlu cinayeti kınadı. | Argumenty i Fakty · Rus devlet medyası | açıldı · ⚠ çelişki notu |
| KR-064 | 2016-12-20 | 00:23 / 00:54 | Başbakan Yıldırım, Medvedev'e soruşturmayı kişisel kontrolüne alacağını söyledi. | RBC · yabancı bağımsız medya | açıldı · ⚠ çelişki notu |
| KR-065 | 2016-12-20 | 00:35 | SK davayı RF CK m.361/3 (uluslararası terör eylemi) kapsamında nitelendirdi. | Argumenty i Fakty · Rus devlet medyası | açıldı |
| KR-066 | 2016-12-20 | 00:58 | TASS: 5 kişi gözaltında (öncesinde yalnızca anne ve kız kardeş bildirilmişti). | TASS · Rus devlet medyası | açıldı · ⚠ çelişki notu |
| KR-067 | 2016-12-20 | 01:39 | Fethullah Gülen cinayeti 'korkunç bir terör eylemi' olarak kınadı. | Argumenty i Fakty · Rus devlet medyası | açıldı |
| KR-068 | 2016-12-20 | ~05:49 (06:49'da 'yaklaşık bir saat önce') | TASS (kaynak): Rus soruşturma ekibi özel uçakla Moskova'dan Ankara'ya hareket etti. | TASS · Rus devlet medyası | **arama özeti** |
| KR-069 | 2016-12-20 | — | Peskov: 18 kişilik ekip (SK, MİD, 'özel servis' temsilcileri) Türkiye'ye uçtu; Putin-Erdoğan görüşmesinde kararlaştırılmıştı. | BBC Rusça · yabancı bağımsız medya | açıldı |
| KR-070 | 2016-12-20 | 11:00 | Rus uzman ekip özel uçakla Esenboğa'ya indi, Keçiören Adli Tıp'ta otopsiye girdi (Odatv). | Odatv · yurt içi muhalif/bağımsız | **arama özeti** |
| KR-071 | 2016-12-20 | 12:20 (haber) | AA/Hürriyet: yaklaşık 18 kişilik heyet (savcı, 2 güvenlik ataşesi, Acil Durum Bakanlığı, adli tıp, psikologlar) Esenboğa'ya indi. | Hürriyet (AA) · yurt içi ana akım (Doğan dönemi)† | açıldı · ⚠ çelişki notu |
| KR-072 | 2016-12-20 | — | Karlov ve Altıntaş'ın cesetleri Keçiören Adli Tıp'a götürüldü; Rus heyet otopsiye katıldı. | Cumhuriyet · yurt içi muhalif/bağımsız | açıldı |
| KR-073 | 2016-12-20 | 07:27 (haber) | Hürriyet: otel rezervasyonu 14 Aralık'ta (AA'ya göre), 214 nolu oda; otel odası mühürlendi; fail rapor alarak işe gitmemişti. | Hürriyet · yurt içi ana akım (Doğan dönemi)† | açıldı · ⚠ çelişki notu |
| KR-074 | 2016-12-20 | öğleden sonra | Esenboğa'da devlet töreni; tören Türkeş, Soylu ve Dışişleri Bakan Yardımcısı Ahmet Yıldız'ın katılımıyla yapıldı, naaş Moskova'ya uğurlandı. | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-075 | 2016-12-20 | — | Türkeş: 'Karlov'u öldürmediler, tarihe gömdüler... Türk-Rus dostluğunun ölümsüz sembolü oldu.' | Anadolu Ajansı (EN) · devlet medyası (TR) | **arama özeti** |
| KR-076 | 2016-12-20 | geç saat | Naaş Moskova Vnukovo'ya ulaştı; Lavrov ve Çavuşoğlu karşıladı. Naaşı, Rus soruşturma ekibini getiren uçak taşıdı. | Anadolu Ajansı (EN) · devlet medyası (TR) | açıldı |
| KR-077 | 2016-12-20 | — | Moskova'da Türkiye-Rusya-İran dışişleri bakanları üçlü toplantısı; Suriye'de siyasi süreç için ortak bildiri. | T.C. Dışişleri Bakanlığı · devlet kurumu/resmi | açıldı |
| KR-078 | 2016-12-20 | — | Çavuşoğlu, Kerry'ye telefonda 'Türkiye de Rusya da saldırının arkasında FETÖ'nün olduğunu biliyor' dedi. | BBC Türkçe · yabancı bağımsız medya | açıldı · ⚠ çelişki notu |
| KR-079 | 2016-12-21 | — | Altıntaş'ın Keçiören Adli Tıp'taki otopsisi tamamlandı; 15 günlük teslim süresi başladı. | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-080 | 2016-12-21 | — | TASS (Al-Youm Al-Sabea'ya atfen): Ceyşü'l-Fetih koalisyonu cinayeti üstlendi; Haber 7'ye göre şüpheli sayısı 13'e çıktı. | TASS (EN) · Rus devlet medyası | açıldı · ⚠ çelişki notu |
| KR-081 | 2016-12-21 | — | Ceyşü'l-Fetih sözcüsü Hüsam eş-Şafii üstlenme metninin sahte ve 'amatör' olduğunu söyledi. | Daily Sabah · hükümete yakın yayın | açıldı |
| KR-082 | 2016-12-21 | 18:32 | Erdoğan: 'FETÖ terör örgütüne mensup, gizlememize gerek yok.' | Milliyet (DHA) · hükümete yakın yayın | açıldı |
| KR-083 | 2016-12-21 | — | Nordic Monitor (2020): bir müteahhit/dernek yöneticisi 21 Aralık'taki ifadesinde faili tanımadığını söyledi; telefon/banka kayıtları aksini gösteriyor. | Nordic Monitor · rejim kontrolünde olmayan kaynaklar | açıldı |
| KR-084 | 2016-12-22 | 00:27 | Rusdialog (SITE Intelligence'a atfen): üstlenme açıklaması sahte, yazım ve imla grubun resmi bildirilerinden farklı. | Rusdialog.ru · yabancı bağımsız medya | açıldı |
| KR-085 | 2016-12-22 | 12:15 (MSK) | Moskova'da Dışişleri binasında veda töreni; Putin katıldı. | Kremlin · devlet kurumu/resmi | açıldı |
| KR-086 | 2016-12-22 | — | AA: failin telefonu incelendi; aktif görüştüğü 8 kişinin (5 polis, emniyet amiri ve yardımcısı dahil) ByLock kullandığı belirlendi. | Anadolu Ajansı (Rusça) · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-087 | 2016-12-22 | — | Hürriyet: istihbaratçılar 22 yaşındaki polisin büyükelçinin programını nasıl öğrendiğini sorguluyor; 'El Nusra süsü' tezi. | Hürriyet · yurt içi ana akım (Doğan dönemi)† | açıldı |
| KR-088 | 2016-12-22 | — | Star (Ulusal Kanal aktarımı): failin evinde 'ABD ve Rusya'nın sonu yakındır. Artık kıyam vaktidir' yazan not bulundu. | Ulusal Kanal (Star'a atfen) · yurt içi muhalif/bağımsız | **arama özeti** |
| KR-089 | 2016-12-23 | — | Habertürk: iPhone'un 4 haneli şifresi Türkiye'de kırılamadı, Rusya'nın desteğiyle kırılmaya çalışılacak. | Habertürk · hükümete yakın yayın | açıldı |
| KR-090 | 2016-12-23 | 22:30 (MSK) | Kremlin: Erdoğan, Putin'i soruşturmanın seyri hakkında bilgilendirdi. | Kremlin · devlet kurumu/resmi | açıldı |
| KR-091 | 2016-12-24 | 11:15 (Diken) | Hürriyet (Diken aktarımı): Altıntaş, ev arkadaşları bir avukat ve bir polis ile Nurettin Yıldız'ın Hacı Bayram'daki sohbetlerine katılıyordu. | Diken · yurt içi muhalif/bağımsız | açıldı |
| KR-092 | 2016-12-24 | — | Turkish Minute: hükümet Gülen bağını öne sürerken failin Erdoğan yanlısı vaiz Yıldız'ın sohbetlerine katıldığı ortaya çıktı. | Turkish Minute · rejim kontrolünde olmayan kaynaklar | açıldı · ⚠ çelişki notu |
| KR-093 | 2016-12-24 | 18:17 | Sabah: 2 gün sorgulanıp serbest bırakılan anne-baba cenazeyi istemedi; dayı: 'kimsesizler mezarlığına gömün'. | Sabah · hükümete yakın yayın | açıldı · ⚠ çelişki notu |
| KR-094 | 2016-12-26 | — | Ankara 7. Sulh Ceza Hakimliği, Başsavcılık Anayasal Suçlar Bürosu talebiyle soruşturma tamamlanana kadar yayın yasağı getirdi. | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-095 | 2016-12-30 | — | RTÜK, vurulma anını ve sloganları canlı yayınlayan 5 kanala yaptırım uyguladı. | Anadolu Ajansı · devlet medyası (TR) | açıldı |

</div>

## 2017–2026: yargı ve sonrası

**[O]** Bu dönemin ana hatları: Ocak 2017'de beş kişi tutuklandı [KR-096] ve fail kimsesizler mezarlığına gömüldü [KR-098]; Nisan 2018'de Gülen dahil sekiz kişi hakkında yakalama kararı çıktı [KR-104]; Kasım 2018'de iddianame sunuldu [KR-106]; Mart 2021'de karar açıklandı [KR-114]; Şubat 2022'de istinaf [KR-117], Haziran 2023'te Yargıtay onaması geldi [KR-119]; 2026'da MİT'in iki açıklaması dosyayı yeniden gündeme taşıdı [KR-121], [KR-124].

<div class="tbl-kr_d">

| KR | Tarih | Saat (TSİ) | Olay | Kaynak · sınıf | Erişim / çelişki |
|---|---|---|---|---|---|
| KR-096 | 2017-01-07 | 18:07 (MSK, haber) | İzmir Başsavcılığı: 4'ü failin meslektaşı polis, 1'i Gülen bağlantılı 5 kişi tutuklandı. | Interfax · yabancı bağımsız medya | açıldı |
| KR-097 | 2017-01-12 | — | AA: cenaze 24 gündür morgda; ailesi 15 günlük sürede teslim almadı, kimsesizler mezarlığı işlemi başladı. | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-098 | 2017-01-13 | — | Fail Altıntaş belediye ekiplerince Ankara'da kimsesizler mezarlığına gömüldü. | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-099 | 2017-01-29 | — | Milliyet: savcılık, Gmail yazışmalarının suikasttan ~2,5 saat sonra (fail ölüyken) silindiğini tespit etti; Google'dan döküm istendi. | Milliyet · hükümete yakın yayın | açıldı |
| KR-100 | 2017-12-18 | — | Soruşturma bulgusu: Gmail ve Facebook yazışmaları suikast saatlerinde VPN/sanal bilgisayar üzerinden silindi. | Hürriyet Daily News · yurt içi ana akım (Doğan dönemi)† | açıldı · ⚠ çelişki notu |
| KR-101 | 2017-12-18 | — | İstiklal: 33 kişinin ifadesi alındı, 4 kişi tutuklandı; iCloud yedeklerine erişildi; Apple şifre talebine olumlu yanıt vermedi. | İstiklal · hükümete yakın yayın | açıldı |
| KR-102 | 2017-12-20 | — | HDN: İsrailli firma 20 bin dolar isteyip garanti vermeyince görüşme kesildi; bir Hint şirketi telefonu açacak. | Hürriyet Daily News · yurt içi ana akım (Doğan dönemi)† | açıldı · ⚠ çelişki notu |
| KR-103 | 2018-03-09 | — | HDN (Hürriyet): Rus istihbarat ekibi de telefonu kıramadı; Aralık 2017'de bir sabit diskteki dosyalar Rus istihbaratınca açılmıştı. | Hürriyet Daily News · yurt içi ana akım/hükümete yakın (2018 geçiş yılı)† | açıldı |
| KR-104 | 2018-04-02 | — | Ankara 2. Sulh Ceza Hakimliği, Gülen dahil 8 kişi (Tekalan, Karaata, Özkan, Uslu, Sevinç, Tokay, Alsancak) hakkında yakalama kararı verdi. | Anadolu Ajansı (EN) · devlet medyası (TR) | açıldı |
| KR-105 | 2018-04-17 | 04:46 (haber) | Habertürk: 20 bin dolara anlaşılan İngiltere'den gelen Çinli uzman 16 haneli ikinci şifreyi çözemedi; iCloud şifresiyle yazışma ve maillere ulaşıldı. | Habertürk · hükümete yakın yayın | açıldı · ⚠ çelişki notu |
| KR-106 | 2018-11-23 | — | AA (yargı kaynakları): Gülen dahil 28 şüpheli hakkındaki iddianame Ankara mahkemesine sunuldu. | Anadolu Ajansı (EN) · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-107 | 2018-11-23 | — | AA Arapça (TürkPress): iddianame 609 sayfa; olay 'Türk-Rus ilişkilerine yönelik provokasyon'. | TürkPress (AA Arapça aktarımı) · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-108 | 2018-11-25 | — | BirGün: 609 sayfalık iddianamede STV dizisinin 89. bölümündeki suikast sahnesi delil olarak yer aldı. | BirGün · yurt içi muhalif/bağımsız | **arama özeti** |
| KR-109 | 2018-12-07 | — | Ankara 2. Ağır Ceza iddianameyi kabul etti; ilk duruşma 8 Ocak 2019. İddianameye göre cinayet başta Haziran'da planlanmıştı. | Anadolu Ajansı (EN) · devlet medyası (TR) | açıldı |
| KR-110 | 2019-01-08 | — | Dava başladı; iddianame 16 sanığı 'terör amaçlı tasarlayarak öldürme', 12'sini örgüt üyeliğiyle suçluyor. | DW · yabancı bağımsız medya | açıldı · ⚠ çelişki notu |
| KR-111 | 2019-01-15 | — | TR724: failin 2014'ten itibaren Sosyal Doku Vakfı/Nurettin Yıldız çevresiyle irtibatı; iddianamedeki bir tanığın anlatımı. | TR724 · rejim kontrolünde olmayan kaynaklar | açıldı |
| KR-112 | 2020-03-05 | — | Savcı esas hakkındaki mütalaada 8 sanık için birden fazla ağırlaştırılmış müebbet istedi. | Hürriyet Daily News · hükümete yakın yayın (Demirören dönemi)† | açıldı |
| KR-113 | 2020-12-19 | — | BBC Rusça: dul eş Marina Karlova: 'Bu dava asla çözülmeyecek... bir günah keçisi bulacaklar.' | BBC Rusça · yabancı bağımsız medya | açıldı |
| KR-114 | 2021-03-09 | 16:49 (Hürriyet haber) | Karar: Söğüt, Yılmaz, Kılınçarslan 2'şer kez; Kötüce ve Akalın birer kez ağırlaştırılmış müebbet (+15 yıl); 6 beraat; Karaata dahil firarilerin dosyası ayrıldı. | Anadolu Ajansı · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-115 | 2021-03-09 | — | BBC Rusça: 5 müebbet, 6 kişiye 5-9 yıl, 28 sanıktan 6'sı beraat. | BBC Rusça · yabancı bağımsız medya | açıldı · ⚠ çelişki notu |
| KR-116 | 2021-03-09 | 19:21 (MSK, haber) | Rusya Dışişleri: azmettiricilere dair 'kapsamlı bilgi' bekliyoruz; sorumluluk saldırı öncesi medyada 'olumsuz atmosfer yaratan çevrelerde'. | Kommersant · yabancı bağımsız medya | açıldı |
| KR-117 | 2022-02-11 | — | Ankara BAM 19. Ceza Dairesi 13 sanığın mahkûmiyetini istinafta onadı. | Anadolu Ajansı · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-118 | 2022-12-18 | — | AA iddianame özeti: bilgiyi 'mahrem imam' eski BTK çalışanı Şahin Söğüt sağladı; suikasttan 10 gün önce Keçiören'de talimatı iletti; fail 'hedef şaşırtmak' için terör sitelerine girdi. | Anadolu Ajansı · devlet medyası (TR) | açıldı · ⚠ çelişki notu |
| KR-119 | 2023-06-23 | — | Yargıtay 3. Ceza Dairesi 13 sanıktan 12'sinin cezasını onadı; organizatör Özkan'ın 3 yıl 9 ay cezası delil yetersizliğinden bozuldu. | Anadolu Ajansı · devlet medyası (TR) | açıldı |
| KR-120 | 2023-08-13/15 | — | Söğüt'ün eşi (9 yıl ceza almış, kaçak) İstanbul Beylikdüzü'nde Pazar günü yakalandı; polis Salı (15 Ağustos) duyurdu. | Daily Sabah · hükümete yakın yayın | açıldı · ⚠ çelişki notu |
| KR-121 | 2026-01-16 | 14:04 | MİT: kırmızı bültenle aranan Cemal Karaata, 'Salih Ada' adıyla Kanada Waterloo'da psikoterapist olarak yaşıyor; masrafları örgütçe karşılanıyor. | DHA · hükümete yakın yayın | açıldı |
| KR-122 | 2026-01-16 | 15:59 | HDN (güvenlik kaynakları): Karaata'nın isim değişikliğinin başlıca nedeni Rusya tarafından kaçırılma korkusu; Kanada güvenlik birimleriyle temas. | Hürriyet Daily News · hükümete yakın yayın (Demirören dönemi)† | açıldı |
| KR-123 | 2026-01-16 | 19:50 (MSK) | RIA (Kanada sicilleri): Karaata 'Salih Ada' adıyla Eylül 2022'den beri Ontario'da lisanslı psikoterapist; sicilde eski adı yazıyor. | RIA Novosti · Rus devlet medyası | açıldı · ⚠ çelişki notu |
| KR-124 | 2026-05-01 | 14:10 (Daily Sabah) | MİT, İsveç'teki Abdullah Bozkurt (Nordic Monitor kurucusu) hakkında Ankara Başsavcılığına suç duyurusu; Bozkurt'u suikastı 'yönlendirmek' ve dezenformasyonla suçluyor. | Daily Sabah · hükümete yakın yayın | açıldı · ⚠ çelişki notu |
| KR-125 | 2026-05-01 | 08:51 (T24) | T24 (Sabah'tan): suç duyurusu Bozkurt'un sitesindeki yayınları 'iftira' ve 'devlet kurumlarını aşağılama' olarak niteliyor. | T24 · yurt içi muhalif/bağımsız | açıldı |
| KR-126 | 2026-05-07 | — | Nordic Monitor (Bozkurt): hükümet El Kaide bağlantılı ağları gizledi; Rusya duruşmalara gözlemci göndermeyi bıraktı, kendi soruşturmasıyla 'gerçek failleri' belirledi. | Nordic Monitor · rejim kontrolünde olmayan kaynaklar | açıldı |
| KR-127 | 2026-07-06 | 18:36 (MSK) | RIA (Sabah'a atfen): suikast çok katmanlı bir istihbarat operasyonunun parçasıydı; senaryo 2 yıl önce dizide gösterilmişti. | RIA Novosti · Rus devlet medyası | açıldı |

</div>

## Kaynaklar arası çelişkiler {.unnumbered}

<div class="box">

**Kaynaklar arası saat, sayı ve ayrıntı çelişkileri.** Her satır bir **[O]** olgudur (kaynakların ne dediği); son sütun **[D]** değerlendirmedir.

| Konu | Versiyonlar | Kart | Değerlendirme |
|---|---|---|---|
| Saldırı saati | 19:05 (Soylu, BBC "16:05 GMT", DW) · 20:15 (Türkçe ve İngilizce Vikipedi bilgi kutusu) | [KR-017], [KR-018], [KR-019] | 19:05 neredeyse kesin; 20:15 birincil kaynaklarla çelişen hatalı değer |
| Otel odası ve giriş günü | 214 no'lu oda, 18 Aralık (2016 basını) · 204 no'lu oda, 19 Aralık 12:15 (iddianame, AA 2022) · aynı Hürriyet sayfasında "dün (19 Aralık) gelen" | [KR-008], [KR-009], [KR-073], [RD45] | Çözülemedi; iddianame versiyonu daha ayrıntılı, 2016 basını daha erken |
| Rezervasyon süresi | 2 günlük (2016 basını) · 1 gecelik (iddianame) | [KR-004] | Rezervasyon değişikliği iki versiyonu da açıklayabilir (olası) |
| Otelden çıkış | 17:00 (AA 2022) · 17:30 (Hürriyet) · 18:30'a bağlanan anlatım (Cumhuriyet) | [KR-011], [KR-012] | 17:00–17:30 aralığı muhtemel |
| Atış sayısı | En az 5 (ilk haber) · 8 (tanıklar, AP "en az 8") · 11 atış, 9 isabet (Adli Tıp/kamera, BBC) · 15–20 (Rusça Vikipedi, birincil teyit yok) | [KR-031], [KR-020], [KR-022], [KR-025], [KR-018] | 11 atış, 9 isabet muhtemel |
| Şarjör / mermi | Üç şarjör ve 75 mermi (AFP, arama özeti) · silahtaki ile birlikte iki şarjör (Hürriyet) | [KR-015] | Çözülemedi |
| Konuşma süresi | "Bir dakikadan kısa" (Lenta.ru) · "birkaç dakikadır" (AP) | [KR-020], [KR-021] | Çözülemedi |
| Müdahale süresi | ≈15 dk çatışma (BBC) · Karlov 25 dk yerde (Lenta.ru) · ≈20 dk, 19:27'de öldürüldü (Rusça Vikipedi, teyitsiz) | [KR-027], [KR-028] | 15–25 dk aralığı; failin öldürülme saatine dair resmî kaynak yok [KR-035] |
| İlk müdahale eden birim | Çankaya Polis Merkezi (Soylu) · JFK Caddesi trafik polisleri (Hürriyet) | [KR-026] | İki versiyon birbirini dışlamayabilir |
| Ölüm yeri | Hastanede 19:53 (Soylu) · saldırgan öldürülene kadar tahliye edilmedi (Rus MİD, Lenta) · ambulansta kalp masajı (RIA/NTV) | [KR-034], [KR-021] | Ölüm anı belirsiz |
| Rus ceza davasının maddesi | m.360 (korunan kişiye saldırı; AiF, Interfax arama özeti) · m.361/3 (uluslararası terör; SK sitesi) · iki madde birlikte (BBC) | [KR-044], [KR-065], [R14], [R15], [R17] | Önce 360, sonra 361/3 eklenmiş olması muhtemel |
| Gözaltı sayısı | 5 (TASS/NTV) · 6 (Reuters, Vikipedi aktarımı) · 13 şüpheli (Haber 7'ye atfen TASS) | [KR-066], [KR-080] | Sayılar farklı anlara ait olabilir |
| Ailenin serbest bırakılması | 2 gün sorgulama (Sabah) · 22 Aralık (TR Vikipedi, kaynaksız) · "bir gün" (EN Vikipedi) | [KR-093] | Çözülemedi |
| Gmail silme anı | Suikasttan ≈2,5 saat sonra (Milliyet) · "suikast saatlerinde" (HDN) | [KR-099], [KR-100] | İkisi de savcılık kaynaklı; kesin saat açık soru |
| Telefon şifresi | 4 haneli şifre Türkiye'de kırılamadı (Habertürk 2016) · Rus ekibi de kıramadı (HDN 2018) · Çinli uzman 16 haneli ikinci şifreyi çözemedi (Habertürk 2018) · "Rusya açtı" (IBTimes, sonra düzeltildi, arama özeti) | [KR-089], [KR-103], [KR-105] | Şifrenin çözüldüğüne dair açılabilen kaynak yok |
| Telefon açma ücreti | 20 bin dolar: İsrailli firma (HDN) · İngiliz firma/Çinli uzman (Habertürk) | [KR-102], [KR-105] | Çözülemedi |
| Telefon verileri | 8 kişinin ByLock kullandığı "telefon incelemesinden" (AA) · telefon şifresi kırılamadı | [KR-086], [RD50] | Verinin HTS/iCloud kaynaklı olması olası [KR-101] |
| İddianame | 609 sayfa (AA Arapça, BirGün) · 607 sayfa (arama özeti) · sunuluş 22 Kasım (Nordic Monitor) / 23 Kasım (AA) | [KR-106], [KR-107], [KR-108] | 609 muhtemel |
| 2021 karar sayıları | Üç sanığa ikişer müebbet (AA/Hürriyet) · "ikisine" (BBC Rusça) · 6 beraat (AA) / 5 beraat (Rusça Vikipedi) · firari 9 | [KR-114], [KR-115], [K28] | AA versiyonu muhtemel |
| Yargıtay | 13 sanıktan 12'si onandı (AA) · "12 sanık mahkûm" (Daily Sabah) | [KR-119], [KR-120] | AA versiyonu muhtemel |
| Talimat zinciri | Söğüt (AA 2022) · Salih Yılmaz ve Ahmet Kılınçarslan da "ileten" olarak anılıyor | [KR-118], [K27] | Zincirin halkaları kaynaklara göre değişiyor |
| Açığa alınma | 4 Ekim'de açığa alındı, 16 Kasım'da iade (HDN) · darbe sonrası ihraç edilmişti (ilk Rus haberleri) · Emniyet yalanladı, ihraç listelerinde yok · BBC "doğrulanmamış" | [KR-003], [RD49], [K03], [K32] | Çözülemedi; resmî yazı metni yok |
| Dershane | Söke'deki Körfez dershanesinde hazırlandı (AA, arama özeti) · anne ve abla yalanlıyor | [RD06], [RD02], [RD05] | AA iddiası zayıf (C4) |
| Sergi adı | "Gezgin Gözüyle Kaliningrad'dan Kamçatka'ya Rusya" (AA/Soylu) ve Rusça/İngilizce farklı çeviriler | [KR-032] | Çeviri farkı |
| Yasak saati | 21:29 (Timeturk sayfa damgası) · en geç 20:30 (CNN Türk URL'si, GDELT) | [KR-042], [GDELT-ek] | 20:30 veya öncesi muhtemel |
| Karaata'nın adı | "İsim değiştirerek kayıtlardan kaçtı" (MİT/HDN) · Kanada sicilinde eski adı açıkça yazıyor (RIA) | [KR-122], [KR-123] | İki kurum anlatısı çelişiyor |

</div>


# Medya nasıl anlattı: GDELT istatistikleri

## Veri, kapsam ve okuma kuralı

**[O]** Bu bölümdeki sayılar, GDELT Global Knowledge Graph 2.1'in çeviri akışındaki ham 15 dakikalık dosyalardan yeniden kuruldu: 17 Aralık 2016–10 Ocak 2017 arasındaki 2.400 dosyadan (8'i boş) Türkçe kaynaklı 606.455 kayıt, bunların içinden URL'sinde *karlov / büyükelçi / suikast / altıntaş / mevlüt* geçen 4.185 tekil haber (211 site) "çekirdek küme" olarak alındı [GDELT-istatistik]. **[O]** Yayın grupları, ayrı bir medya indeksi çalışmasındaki KEY_OUTLETS listesinden atandı; 2.931 haber hiçbir izlenen gruba girmeyen yerel site ve portallara aittir [GDELT-istatistik]. **[O]** GDELT'in 2019 öncesi kayıtları başlık tutmadığı için çerçeve sayımları haber metninden değil URL'deki sözcüklerden (slug) yapıldı; bu kaba bir ölçümdür (yöntem: Ek B).

**[D]** Okuma kuralı: Bu bölüm *kimin ne anlattığını* ölçer, *neyin doğru olduğunu* ölçmez. Bir çerçevenin baskınlığı, o çerçevenin doğru ya da yanlış olduğunun kanıtı değildir. Nedensellik iddiası yapılmaz.

## Hacim: iki günlük patlama, hızlı sönümlenme

![Günlük hacim ve Türkçe arşivdeki pay. Kaynak: The GDELT Project; hesaplama: GDELT-istatistik.](../../../work/karlov_v2/gdelt_gunluk.png)

**[O]** Çekirdek küme 19 Aralık'ta 933 habere (o günkü Türkçe GDELT kayıtlarının %3,42'si), 20 Aralık'ta 1.429 habere (%5,18) ulaştı; 21 Aralık'ta 465'e (%1,68), 23 Aralık'ta 167'ye (%0,67), 29 Aralık'ta 14'e (%0,05) düştü [GDELT-istatistik]. **[O]** Ocak başındaki küçük sıçramalar 3 Ocak (75), 7 Ocak (53), 9 Ocak (52) ve 10 Ocak (51) günlerindedir [GDELT-istatistik]; URL örnekleri 7 Ocak'ta tutuklama haberlerini [KR-096], 9–10 Ocak'ta ise sergi salonuna ve sokağa Karlov adının verilmesini içeriyor [GDELT-ek], [R36]. **[D]** Haber ilgisinin yarı ömrü kısadır: ilk iki gün toplam hacmin yarıdan fazlasını oluşturuyor (933 + 1.429 = 2.362 / 4.185). Bu, ilk 48 saatte kurulan çerçevenin kamuoyu algısında belirleyici olmasının büyük olasılıkla yapısal nedenidir.

<div class="tbl-g_daily">

| Gün | Çekirdek küme (haber) | Türkçe GKG toplam kayıt | Pay (%) |
|---|---|---|---|
| 17.12.2016 | 0 | 21.255 | 0,0 |
| 18.12.2016 | 0 | 17.600 | 0,0 |
| 19.12.2016 | 933 | 27.262 | 3,42 |
| 20.12.2016 | 1429 | 27.564 | 5,18 |
| 21.12.2016 | 465 | 27.670 | 1,68 |
| 22.12.2016 | 449 | 27.123 | 1,66 |
| 23.12.2016 | 167 | 25.107 | 0,67 |
| 24.12.2016 | 157 | 18.892 | 0,83 |
| 25.12.2016 | 61 | 16.724 | 0,36 |
| 26.12.2016 | 88 | 25.551 | 0,34 |
| 27.12.2016 | 77 | 26.704 | 0,29 |
| 28.12.2016 | 49 | 26.965 | 0,18 |
| 29.12.2016 | 14 | 28.339 | 0,05 |
| 30.12.2016 | 9 | 26.436 | 0,03 |
| 31.12.2016 | 7 | 19.782 | 0,04 |
| 01.01.2017 | 15 | 17.232 | 0,09 |
| 02.01.2017 | 2 | 24.867 | 0,01 |
| 03.01.2017 | 75 | 26.393 | 0,28 |
| 04.01.2017 | 21 | 26.847 | 0,08 |
| 05.01.2017 | 7 | 27.157 | 0,03 |
| 06.01.2017 | 2 | 27.789 | 0,01 |
| 07.01.2017 | 53 | 20.391 | 0,26 |
| 08.01.2017 | 2 | 17.555 | 0,01 |
| 09.01.2017 | 52 | 27.733 | 0,19 |
| 10.01.2017 | 51 | 27.517 | 0,19 |

</div>

## Saatlik eğri (Türkiye saati)

![Saatlik hacim, Türkiye saati. Kaynak: The GDELT Project; hesaplama: GDELT-ek.](../../../work/karlov_v2/gdelt_saatlik.png)

**[O]** GDELT saatleri UTC'dir; Türkiye saati UTC+3'tür [GDELT-istatistik]. **[O]** Saldırıdan (19:05) sonraki ilk GDELT dosyası 19:30 TSİ tarihlidir ve 3 haber içerir; ilk tam saatte (19:00–20:00 TSİ) 19, sonraki saatlerde 113, 128 ve 22:00–23:00 TSİ'de 186 haber vardır; bu, olay gecesinin zirvesidir [GDELT-ek]. **[O]** Hacim gece 06:00 TSİ'de 5 habere iner, 20 Aralık 12:00–13:00'te 152 ile ikinci zirveye çıkar [GDELT-ek]. **[D]** İkinci zirve, sabah yayımlanan resmî açıklamalar ve Esenboğa'daki tören [KR-074] ile aynı zaman dilimine denk geliyor; zaman örtüşmesi nedensellik kanıtı değildir.

## Yayınların ilk haber zamanları

**[O]** İzlenen yayınlar içinde ilk GDELT dosyasında yer alan Hürriyet'tir (16:30 UTC = 19:30 TSİ); Sözcü, Star, Habertürk, Yeni Akit ve Yeniçağ 19:45 TSİ dosyasındadır [GDELT-istatistik]. **[O]** Anadolu Ajansı 20:15, TRT Haber ve A Haber 21:00, Sputnik Türkçe 21:30 TSİ dosyasında ilk kez görünüyor [GDELT-istatistik].

<div class="tbl-g_first">

| Yayın | Grup (KEY_OUTLETS) | İlk GDELT dosyası (UTC) | TSİ | Çekirdek kümede haber |
|---|---|---|---|---|
| hurriyet.com.tr | Ana akım | 19.12 16:30 | 19.12 19:30 | 34 |
| sozcu.com.tr | Ana akım | 19.12 16:45 | 19.12 19:45 | 57 |
| star.com.tr | Hükümete yakın | 19.12 16:45 | 19.12 19:45 | 89 |
| haberturk.com | Ana akım | 19.12 16:45 | 19.12 19:45 | 48 |
| yeniakit.com.tr | Hükümete yakın | 19.12 16:45 | 19.12 19:45 | 71 |
| yenicaggazetesi.com.tr | Ulusalcı | 19.12 16:45 | 19.12 19:45 | 14 |
| shaber3.com | Rejim kontrolünde olmayan kaynaklar | 19.12 17:00 | 19.12 20:00 | 11 |
| yenisafak.com | Hükümete yakın | 19.12 17:00 | 19.12 20:00 | 54 |
| odatv.com | Ulusalcı | 19.12 17:00 | 19.12 20:00 | 22 |
| t24.com.tr | Muhalif / bağımsız | 19.12 17:00 | 19.12 20:00 | 84 |
| birgun.net | Muhalif / bağımsız | 19.12 17:00 | 19.12 20:00 | 44 |
| aksam.com.tr | Hükümete yakın | 19.12 17:15 | 19.12 20:15 | 39 |
| aa.com.tr | Haber ajansları | 19.12 17:15 | 19.12 20:15 | 48 |
| cumhuriyet.com.tr | Muhalif / bağımsız | 19.12 17:15 | 19.12 20:15 | 103 |
| cnnturk.com | Ana akım | 19.12 17:30 | 19.12 20:30 | 42 |
| dha.com.tr | Haber ajansları | 19.12 17:30 | 19.12 20:30 | 29 |
| ntv.com.tr | Ana akım | 19.12 17:45 | 19.12 20:45 | 20 |
| ulusalkanal.com.tr | Ulusalcı | 19.12 17:45 | 19.12 20:45 | 75 |
| iha.com.tr | Haber ajansları | 19.12 17:45 | 19.12 20:45 | 24 |
| sabah.com.tr | Hükümete yakın | 19.12 17:45 | 19.12 20:45 | 39 |
| ahaber.com.tr | Hükümete yakın | 19.12 18:00 | 19.12 21:00 | 30 |
| trthaber.com | Ana akım | 19.12 18:00 | 19.12 21:00 | 25 |
| dw.com | Yabancı yayınların Türkçe servisleri | 19.12 18:15 | 19.12 21:15 | 4 |
| sputniknews.com | Yabancı yayınların Türkçe servisleri | 19.12 18:30 | 19.12 21:30 | 172 |
| evrensel.net | Muhalif / bağımsız | 19.12 19:00 | 19.12 22:00 | 36 |
| milliyet.com.tr | Ana akım | 19.12 19:30 | 19.12 22:30 | 31 |
| bianet.org | Muhalif / bağımsız | 19.12 20:30 | 19.12 23:30 | 7 |
| karar.com | Muhalif / bağımsız | 20.12 02:45 | 20.12 05:45 | 1 |
| diken.com.tr | Muhalif / bağımsız | 21.12 17:30 | 21.12 20:30 | 1 |

</div>

**[D]** Bu zamanlar yayın anı değil, GDELT'in haberi taradığı 15 dakikalık dosyanın zamanıdır; bir yayının listede geç görünmesi geç yayın yaptığını değil, GDELT'in onu geç ya da eksik taradığını da gösterebilir. **[O]** Örneğin Diken çekirdek kümede yalnızca 1 haberle, Karar 1 haberle görünüyor [GDELT-istatistik]; oysa Diken'in 24 Aralık'ta failin Nurettin Yıldız sohbetlerine katıldığını yazan haberi kartlarda mevcuttur [KR-091], [RD11]. **[D]** Bu, GDELT kapsamının küçük ve bağımsız yayınlarda eksik olduğunun somut bir örneğidir.

## Çerçeve sayımları: kim neyi URL'ye taşıdı?

<div class="tbl-g_frames">

| Grup | n | FETÖ/ Gülen | Cihatçı | Halep/ Suriye | ABD/ Batı | Provo- kasyon | Güvenlik açığı | Samanyolu dizisi | N. Yıldız/ Sosyal Doku | FETÖ : cihatçı |
|---|---|---|---|---|---|---|---|---|---|---|
| Hükümete yakın | 322 | 44 | 3 | 4 | 10 | 3 | 4 | 4 | 0 | 44:3 (≈14,7×) |
| Muhalif / bağımsız | 276 | 14 | 14 | 8 | 8 | 1 | 4 | 0 | 2 | 14:14 (≈1,0×) |
| Ana akım | 257 | 5 | 0 | 5 | 3 | 0 | 1 | 5 | 0 | 5:0 (cihatçı 0) |
| Yabancı yayınların Türkçe servisleri | 176 | 6 | 2 | 6 | 11 | 2 | 2 | 1 | 0 | 6:2 (≈3,0×) |
| Ulusalcı | 111 | 4 | 1 | 1 | 0 | 0 | 2 | 0 | 0 | 4:1 (≈4,0×) |
| Haber ajansları | 101 | 4 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 4:0 (cihatçı 0) |
| Rejim kontrolünde olmayan kaynaklar | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0:0 (cihatçı 0) |
| Diğer (yerel/portal) | 2931 | 140 | 26 | 26 | 70 | 10 | 24 | 40 | 3 | 140:26 (≈5,4×) |
| TÜMÜ | 4185 | 217 | 46 | 51 | 103 | 17 | 37 | 51 | 5 | 217:46 (≈4,7×) |

</div>

*Kaynak: The GDELT Project; sözlük ve düzeltme: Ek B. "Rejim kontrolünde olmayan kaynaklar" grubunda yalnızca 11 haber (shaber3.com) vardır.*

**[O]** Hükümete yakın yayınların 322 haberinin 44'ünde (%13,7) URL'de FETÖ/Gülen terimleri, 3'ünde (%0,9) cihatçı terimler geçiyor; oran yaklaşık 15'e 1'dir [GDELT-istatistik]. **[O]** Bu üç cihatçı URL'nin üçü de 21 Aralık tarihlidir ve sahte üstlenme bildirisiyle ilgilidir; biri "suikasti El Nusra yaptı yalanı neyi amaçlıyor" biçimindedir [GDELT-ek]. **[O]** Muhalif/bağımsız grupta oran 14'e 14'tür; bu grupta bir URL iki çerçeveyi birlikte taşıyor: "Karlov'un katili FETÖ ise bela eden sizsiniz, El Nusra ise her türlü desteği veren de sizsiniz" [GDELT-istatistik], [GDELT-ek]. **[O]** Ana akım grubunda FETÖ 5, cihatçı 0, Samanyolu dizisi 5 URL'dir [GDELT-istatistik].

**[O]** "Yabancı yayınların Türkçe servisleri" grubunun 176 haberinin 172'si Sputnik Türkçe'ye, 4'ü DW'ye aittir [GDELT-istatistik]. **[D]** Bu grup fiilen Rus devlet medyasının Türkçe servisini temsil ediyor; bu grubun 6'ya 2 FETÖ:cihatçı oranı ve 11 ABD/Batı URL'si Rus devlet medyasının Türkçe yayın çizgisini yansıtıyor, Batılı yayınların Türkçe servislerini değil.

**[D]** Değerlendirme: Hükümete yakın yayınlarda FETÖ çerçevesinin cihatçı çerçeveye yaklaşık 15 kat baskın olması, failin sözlerinin açıkça cihatçı olduğu [RD55] bir olayda dikkat çekicidir. Muhalif/bağımsız yayınlarda iki çerçevenin dengeli olması, çerçeve seçiminin olgulardan çok yayın grubunun konumuyla ilişkili olduğunu düşündürüyor (muhtemel). **[O]** Aynı dönemde Sabah, Nusra sloganını başlığa taşıyan Hürriyet'i, Cumhuriyet'i ve BirGün'ü "FETÖ'nün algı operasyonuna hizmet" etmekle suçladı [K36]. **[D]** Bu, cihatçı çerçeveyi kullanmanın hükümete yakın medya ekosisteminde bir maliyeti olduğuna işaret ediyor ve sayısal ayrışmanın bir kısmını büyük olasılıkla açıklıyor.

## FETÖ çerçevesi nasıl girdi: "Rus ajansı" atfı

**[O]** URL'sinde FETÖ/Gülen geçen ilk haberler 19 Aralık 19:00 UTC (22:00 TSİ) dosyasında, Star ve Yeni Akit'te "Rus ajansı: FETÖ'nün suikasti olabilir" başlığıyla yer aldı; 19:30 UTC'de (22:30 TSİ) "Rusya devlet televizyonu: suikastta FETÖ parmağı" başlıklı haberler geldi [GDELT-istatistik], [GDELT-ek]. **[O]** Aynı gece 23:15 TSİ'de "suikast talimatı Gülen'den" ve "FETÖ üyesi grubun suikasti", 01:00 TSİ'de "suikastçının 15 Temmuz'da izne yollanması" ve "suikasti 3 gün önce FETÖ'cü Bozkurt yazmış", 02:00 TSİ'de "suikastçı FETÖ'cü Abdullah Bozkurt'un evinde kalıyormuş" başlıklı URL'ler dolaşıma girdi [GDELT-ek].

**[O]** Aynı saatlerde Rus resmî ve yarı resmî kaynakların söyledikleri: Zaharova 20:24–20:27'de olayı terör eylemi olarak nitelendirdi [KR-036], [KR-037], [R01]; Putin 22:45'te "provokasyon" dedi ve yönlendiricinin bulunması gerektiğini söyledi, ama kimseyi adlandırmadı [KR-050], [R02], [R04], [K11]; Federasyon Konseyi'nden Klintseviç IŞİD, Kürt grupları ve "büyük olasılıkla NATO istihbaratı"nı [R08], Jirinovski Batı'yı [R13], Puşkov Halep konusundaki Batı medyası "histerisini" [R12], Kosaçev ise "planlı terör ya da yalnız bir manyak" ihtimalini [R10] işaret etti. **[O]** Rus basını ertesi gün ağırlıkla "normalleşmeyi bozmak isteyen üçüncü bir güç" çerçevesini kullandı [R43]. **[O]** Kremlin, Türkiye'nin "Rusya da FETÖ olduğunu biliyor" açıklamasından sonra, 21 Aralık'ta "sonuç çıkarmakta acele etmeyin" dedi [R18], [KR-078].

**[D]** Bu çalışmadaki 69 Rusya/dünya kartının hiçbiri, 19 Aralık gecesi bir Rus devlet ajansının ya da devlet televizyonunun saldırıyı FETÖ'ye atfettiğini göstermiyor. Buna karşın Türk hükümete yakın medyasında FETÖ çerçevesi ilk kez bir Rus kaynağına atıfla girdi. Bu durum bir **"çerçeve ithali" ya da "atıf aklama"** ihtimaline işaret ediyor: yurt içinde üretilen bir çerçevenin, dışarıdan bir kaynağa atfedilerek ek inandırıcılık kazanması (olası; kanıtlanmamış). **[D]** Alternatif açıklama da eşit derecede açık tutulmalıdır: bir Rus yayın organında konuk bir yorumcu ya da muhabir bu ihtimali gerçekten dile getirmiş olabilir ve Türk yayınları bunu "Rus ajansı" diye aktarmış olabilir (olası). **[S]** Hangi Rus ajansının ya da kanalının, kimin ağzından ve hangi ifadeyle böyle bir şey söylediği, bu haberlerin metinleri açılmadığı için bilinmiyor; bkz. Bölüm 10, soru 6.

**[O]** URL'sinde cihatçı terim geçen ilk gerçek haber, 19 Aralık 21:00 UTC (20 Aralık 00:00 TSİ) dosyasında bir yerel sitede, hükümete yakın köşe yazarı Abdulkadir Selvi'ye atfen "Rus büyükelçiyi vuran saldırgan bir El Nusracı olabilir" biçimindedir [GDELT-ek]. **[O]** Selvi'nin 20 Aralık tarihli yazısı ise saldırıyı "FETÖ suikast hücresi" olarak çerçeveledi ve Arapça sözleri "El Kaide/Nusra imajı yaratma çabası" olarak niteledi [K06]. **[D]** URL metni açılmadığı için kesin değildir; ancak doğruysa, aynı yorumcunun çerçevesinin 24 saat içinde cihatçı ihtimalden FETÖ tezine kaydığını gösterir ve ekosistemin genel yönelimiyle örtüşür (olası).

**[D]** Genel değerlendirme: Olaydan yaklaşık üç ila yedi saat sonra hükümete yakın web ekosisteminde resmî anlatının sonraki yıllarda iddianameye girecek temel unsurları (Gülen talimatı, 15 Temmuz izni, "FETÖ'cü gazeteci" bağlantısı) zaten kurulmuştu [GDELT-ek], [K26], [RD51]. Bu sırada açıklanmış tek resmî bilgi failin kimliğiydi [KR-038] ve Dışişleri'nin yazılı metni örgüt adı vermiyordu [KR-047]. Çerçevenin delilden önce geldiği neredeyse kesindir; bu, çerçevenin yanlış olduğunu göstermez, çıpalama riskinin yüksek olduğunu gösterir.

## Nurettin Yıldız hattının görece sessizliği

**[O]** URL'sinde Nurettin (Nureddin) Yıldız ya da Sosyal Doku geçen haber sayısı tüm çekirdek kümede 5'tir; hepsi 24 Aralık tarihlidir ve sol.org.tr, haberdar.com ve Cumhuriyet'e aittir; hükümete yakın ve ana akım gruplarda bu sayı 0'dır [GDELT-istatistik], [GDELT-ek]. **[O]** Bu beş URL'den biri vaizin "Ahrar'uş Şam liderine mektup yazdığının ortaya çıktığını" söylüyor (metin açılmadı) [GDELT-ek]. **[O]** Aynı olgu, yani failin Yıldız sohbetlerine katılımı, sonradan iddianame, gerekçeli karar ve birden fazla bağımsız kaynakta kabul edildi [RD11], [RD13], [RD43], [K27]. **[D]** Bir olgunun hem resmî hem bağımsız kaynaklarda teyit edilmesine rağmen hükümete yakın yayınlarda URL düzeyinde hiç görünmemesi, büyük olasılıkla bir gündem seçimi (agenda-setting) örüntüsüdür. Bu sayım URL'ye dayandığı için, Yıldız'ı başlığa değil metne taşıyan haberleri kaçırır (bkz. Ek B).

## 27–28 Aralık "Samanyolu dizisi" dalgası

**[O]** 27 Aralık 18:45 UTC (21:45 TSİ) dosyasında dört siteden altı URL, neredeyse aynı başlıkla ("Rus Büyükelçi Karlov'a suikast Samanyolu TV'de işlenmiş") birlikte göründü; İHA ve Sabah 22:00 TSİ dosyasında yer aldı [GDELT-istatistik], [GDELT-ek]. **[O]** Dalga yaklaşık 20 saat sürdü (son URL 28 Aralık 17:45 TSİ) ve 51 URL'ye ulaştı: 27 Aralık'ta 39, 28 Aralık'ta 12 [GDELT-istatistik]. **[O]** 27 Aralık'taki 77 haberin 39'u (%51) bu konuyu işliyor [GDELT-istatistik]. **[O]** Dalga, mahkemenin soruşturma süresince yayın yasağı getirmesinin [KR-094] ertesi akşamına denk geliyor. **[O]** Aynı dizi bölümü iki yıl sonra iddianamede delil olarak yer aldı [KR-001], [KR-108]; 2026'da Rus devlet ajansı da "senaryo iki yıl önce dizide gösterilmişti" ifadesini aktardı [KR-127], [R48].

**[D]** URL'lerin aynı dosyada, aynı başlıkla ve kısa aralıkla çoğalması büyük olasılıkla tek bir ajans kaynağından dağıtılan bir metnin yeniden yayımlanmasıdır (manşet birliği / kopya haber göstergesi). Ajans dağıtımı Türk medyasında olağan bir mekanizmadır; bu örüntü tek başına merkezi bir koordinasyonun kanıtı değildir. **[D]** Dikkat çekici olan, yayın yasağının hemen ardından gündemin yarısını bu konunun doldurması ve medyada önce dolaşan bir anlatının sonradan iddianamede delil statüsü kazanmasıdır (anlatı–delil döngüsü ihtimali; olası). **[O]** 28 Aralık'ta Sputnik Türkçe'de URL'sinde "trt-samanyolu-karlov-sahne" geçen bir haber var [GDELT-ek]. **[S]** Bu haberin TRT'de benzer bir sahneye mi işaret ettiği, metin açılmadığı için bilinmiyor.

## Yayın yasakları ve hacim

**[O]** Olay akşamı Başbakanlık yazısıyla RTÜK geçici yayın yasağı getirdi; yasak, resmî açıklamalar dışında haber ve görüntüyü kapsıyordu [KR-042], [KR-043]. **[O]** Yasak haberi en geç 20:30 TSİ'de web'de dolaşımdaydı; çevrimiçi hacim ise yasaktan sonra arttı ve 22:00–23:00 TSİ'de zirveye ulaştı [GDELT-ek]. **[O]** 26 Aralık akşamı Ankara 7. Sulh Ceza Hakimliği soruşturma süresince yayın yasağı getirdi [KR-094]; RTÜK 30 Aralık'ta saldırı anını canlı yayınlayan beş kanala yaptırım uyguladı [KR-095]. **[O]** Günlük hacim 23–25 Aralık'ta zaten 167, 157 ve 61 habere inmişti; 26 Aralık'ta 88, 27 Aralık'ta 77 (yarısı Samanyolu dalgası), 28 Aralık'ta 49, 29 Aralık'ta 14 habere düştü [GDELT-istatistik].

**[D]** Mahkeme yasağından sonra hacmin düştüğü bir olgudur; bu düşüşün ne kadarının yasaktan, ne kadarının haber ilgisinin doğal sönümlenmesinden kaynaklandığı bu veriyle ayrıştırılamaz. **[D]** Yasak sonrasında kalan hacmin önemli bir kısmının resmî tezle uyumlu bir konuya (Samanyolu dizisi) ayrılması, yasağın soruşturma ayrıntılarını sınırlarken iddia niteliğindeki bazı içeriklerin dolaşımını engellemediğini düşündürüyor (olası).

## Ton

<div class="tbl-g_tone">

| Grup | Ortalama ton | Medyan ton | n |
|---|---|---|---|
| Yabancı yayınların Türkçe servisleri | -3,78 | -3,49 | 176 |
| Hükümete yakın | -3,31 | -2,7 | 322 |
| Diğer | -3,3 | -3,21 | 2931 |
| Rejim kontrolünde olmayan kaynaklar | -2,74 | -0,49 | 11 |
| Muhalif / bağımsız | -2,71 | -2,17 | 276 |
| Ulusalcı | -2,64 | -2,51 | 111 |
| Ana akım | -2,47 | -2,27 | 257 |
| Haber ajansları | -1,35 | -1,37 | 101 |
| **Tümü** | -3,16 | — | 4185 |

</div>

**[O]** GDELT'in ton ölçüsü, metindeki olumlu ve olumsuz sözcük yüzdeleri farkıdır; tüm çekirdek kümenin ortalaması −3,16'dır [GDELT-istatistik]. **[O]** En az olumsuz grup haber ajanslarıdır (−1,35); en olumsuz grup Sputnik ağırlıklı yabancı Türkçe servislerdir (−3,78); hükümete yakın grup −3,31, muhalif/bağımsız −2,71, ana akım −2,47'dir [GDELT-istatistik]. **[D]** Ajansların daha nötr tonu, olgu bildiren kısa haber biçimiyle tutarlıdır (muhtemel). Ton farkları küçük ve makine çevirisinden geçmiş metin üzerinde hesaplandığı için, gruplar arasında ideolojik bir sonuç çıkarmaya elverişli değildir. Rejim kontrolünde olmayan kaynaklar grubunun medyan tonu (−0,49) 11 haberle hesaplandığı için anlamsızdır.

## Sınırlılıklar

1. **[O]** Grup listesi (KEY_OUTLETS) tarihsizdir; Hürriyet ve CNN Türk 2016'da Doğan Grubu'ndaydı ve 2018'de el değiştirdi [GDELT-istatistik], [RD04]. **[D]** 2016 için "ana akım" sınıfı kabaca doğrudur, ama listenin bugünkü sahiplik yapısını 2016'ya yansıtma riski vardır.
2. **[O]** "Rejim kontrolünde olmayan kaynaklar" grubunda yalnızca 11 haber (shaber3.com) var; bu yayınların çoğu Temmuz 2016 KHK'larıyla kapatılmıştı [GDELT-istatistik]. **[D]** Bu grup için çerçeve ve ton sonuçları **eksik veridir**; grubun anlatısı GDELT'ten okunamaz. **[O]** Ayrıca bu grubun URL'lerinde "cemaat" sözcüğü geçiyor ("rus-elci-suikastinde-cemaatin-rolu-var-mi", "rus-basini-altintas-cemaat-baglantisi-dezenformasyona-benziyor") [GDELT-ek]; sözlük "cemaat"i FETÖ/Gülen çerçevesine dahil etmediği için bu grubun çerçeve sayısı 0 görünüyor.
3. **[D]** URL'den çerçeve saymak kaba bir ölçümdür: başlığa taşınmayan çerçeveleri kaçırır, alt dize eşleşmelerinde yanlış pozitif üretebilir (ör. "dışişleri" içindeki "isid"); düzeltilmiş sözlük ve duyarlılık testi Ek B'dedir.
4. **[D]** GDELT tüm siteleri taramaz ve tarama zamanı yayın zamanı değildir; küçük ve bağımsız yayınlar (Diken, Karar) eksik temsil ediliyor.
5. **[D]** Makine çevirisi ton ve ad çıkarımını bozar; GDELT'in Türkçe adları İngilizceye çevirmesi (ör. "Religious Ceremonies Manly" = Mevlüt Mert) ad sayımlarını kullanışsız kılıyor [GDELT-istatistik].
6. **[D]** Sosyal medya, televizyon ve basılı gazete bu ölçüme dahil değildir.

# Rusya ve diğer aktörler

## Rusya'nın tutumunun evrimi

| Tarih | Aktör | Ne dedi (kurum iddiası) | Kart |
|---|---|---|---|
| 19.12.2016 | Maria Zaharova (MİD sözcüsü) | "Olanı terör eylemi olarak nitelendiriyoruz… Katiller cezalandırılacak"; konu BM Güvenlik Konseyi'ne taşınacak | [R01], [KR-036], [KR-037] |
| 19.12.2016 | Vladimir Putin | Suç, normalleşmeyi ve Suriye barış sürecini sabote etmeye yönelik bir "provokasyon"; "haydutlar bunu hissedecek"; "katilin elini kimin yönlendirdiğini öğrenmeliyiz"; Viyana Sözleşmesi uyarınca güvenlik güvencesi | [R02], [R03], [R04], [KR-050] |
| 19.12.2016 | Sergey Lavrov | "Elverişsiz araçlarla güdülen bir amaç. Geçmeyecek… Asıl olan, bu suçun arkasında kimin durduğunu anlamak" | [R05] |
| 19.12.2016 | Ramzan Kadırov | "Doğrudan ya da dolaylı ilgisi olan herkesin" cezalandırılması | [R06] |
| 19.12.2016 | Klintseviç · Kosaçev · Slutskiy · Puşkov · Jirinovski | Sırasıyla: NATO istihbaratı ihtimali; planlı terör ya da yalnız manyak; ilişkiyi bozma girişimleri başarısız olacak; Halep "histerisi" ve bilgi savaşı; Batı Rus-Türk dostluğundan korkuyor | [R08], [R10], [R11], [R12], [R13] |
| 20.12.2016 | Peskov | 18 kişilik ekip (SK, MİD, özel servisler) Türkiye'ye uçtu | [R16], [R17], [KR-069] |
| 20.12.2016 | Lavrov · Zaharova | Organizatörler toplantıyı engelleyemedi; Karlov Suriyeli muhalefetle temas kuruyordu ve bu suikasta "ayrı bir boyut" katıyor | [R26], [R25] (arama özeti), [R24] |
| 21.12.2016 | Peskov | FETÖ atfı sorulunca: ortak ekibin sonuçlarını bekleyin, "acele etmeyin"; diplomatların güvenliği ev sahibi ülkenin sorumluluğu, olay Ankara'nın prestijine darbe | [R18], [R19] |
| 22.12.2016 | Kadırov | Suikastı "adalet" diye niteleyen bir ABD gazetesi yazısını "terörün kamuoyu önünde desteklenmesi" olarak kınadı | [R07] (arama özeti, C2) |
| 21.12.2016 | Klintseviç | ABD dahil NATO servislerinin "parmağını" görüyor, "kanıtlamak zor" | [R09] (arama özeti, C5) |
| 23.12.2016 | Putin (yıllık basın toplantısı) | "Rusya'ya ve Rus-Türk ilişkilerine suikast"; "yıkıcı unsurların Türkiye'nin devlet yapılarına, kolluğuna ve ordusuna sızması derin bir nitelik taşıyor"; kimseyi suçlamadığını ekledi; ilişkiler engellenmeyecek | [R20], [R21] |
| 27.12.2016 | Zaharova | Batı'nın Suriye konusundaki "amaçlı Rusya karşıtı propagandası" suikasta yol açan etkenlerden biri | [R23] |
| 09.03.2017 | Peskov | Putin–Erdoğan görüşmesinde soruşturmanın seyri ele alınacak | [R30] |
| 11.01.2019 | Zaharova | Tüm sorumluların cezalandırılmasını bekliyoruz; Rus müfettişler Türk materyallerini kendi soruşturmalarında inceliyor | [R40] |
| 24.07.2019 | Aleksandr Bastrıkin (SK Başkanı) | Hazırlık koşulları ve güzergâh belirlendi; "başka sorular da var, konuşmak için erken" | [R41] |
| 09.03.2021 | Rusya Dışişleri | Karardan "memnuniyet"; azmettiriciler ve organizatörler hakkında "kapsamlı bilgi" bekleniyor; sorumluluğun önemli kısmı medyada olumsuz atmosfer yaratan "belirli çevrelerde" | [R42], [KR-116] |
| 19.12.2021 | Rusya Dışişleri / Lavrov | "Sorular hâlâ duruyor"; Rusya bunu cezasız bırakmayacak | [R39] (arama özeti) |

**[D]** Rusya'nın tutumu dört aşamada okunabilir: (1) olay gecesi hızlı terör nitelemesi ve adlandırmasız "provokasyon" çerçevesi [R01], [R02]; (2) ilk hafta Türkiye'nin FETÖ atfına mesafe, güvenlik sorumluluğunun Ankara'ya hatırlatılması ve "sızma" teması [R18], [R19], [R20]; (3) 2017–2019 arasında ortak soruşturmanın diplomatik gündemde tutulması [R30], [R40], [R41]; (4) 2021 sonrasında kararın kabulü ama dosyanın "azmettirenler" sorusuyla açık tutulması [R42], [R39]. **[D]** Putin'in 23 Aralık'taki "yıkıcı unsurların sızması" ifadesi hem Türk resmî tezinin "devlete sızmış yapı" anlatısıyla hem de genel bir güvenlik zafiyeti eleştirisiyle uyumlu okunabilir; Putin kimseyi adıyla suçlamadığını açıkça söyledi [R20]. Bu belirsizlik büyük olasılıkla bilinçlidir.

## Rusya Soruşturma Komitesi soruşturması

- **[O]** SK olay gecesi önce Ceza Kanunu'nun 360. maddesi (uluslararası korunan kişiye saldırı) kapsamında dava açtığını duyurdu (Interfax, arama özeti; AiF 21:35) [R14], [KR-044]; ardından davayı 361/3. madde (ölümle sonuçlanan uluslararası terör eylemi) kapsamında yeniden nitelendirdi; resmî sitedeki duyuru 23:53 tarihlidir [R15], [KR-059], [KR-065]. **[O]** SK'ya göre saldırganın sözleri Rusya'nın uluslararası terörle mücadeledeki tutumuna tepkiyle bağlantılıydı [R15].
- **[O]** Putin–Erdoğan telefon görüşmesinde ortak soruşturma ekibi kararlaştırıldı [KR-058]; savcı, güvenlik ataşeleri, adli tıp uzmanları ve psikologlardan oluşan yaklaşık 18 kişilik heyet 20 Aralık'ta Esenboğa'ya indi ve Keçiören Adli Tıp'taki otopsiye katıldı [R16], [KR-070], [KR-071], [KR-072]. **[O]** Heyetin bileşimi kaynaklarda farklı tarif ediliyor [KR-071].
- **[O]** Failin iPhone'unun 4 haneli şifresi Türkiye'de kırılamadı ve Rusya'nın desteğinin isteneceği bildirildi [KR-089]; 2018'de Rus istihbarat ekibinin de telefonu kıramadığı, ancak Aralık 2017'de bir sabit diskteki dosyaların Rus istihbaratınca açıldığı aktarıldı [KR-103].
- **[O]** Savcılık kaynaklı habere göre Rus heyeti silinmiş dosyalarda "Fetullah Gülen" adlı 2, "Hizmet" adlı 690, "FETÖ" adlı 4, "Nur Cemaati" adlı 1 dosya buldu; El Kaide, Nusra ve DEAŞ adlarıyla aradı ve silinmiş dosyalarda bu adlarla dosya bulamadı [RD40]. **[D]** "Hizmet" sözcüğü Türkçede genel anlamlıdır; 690 dosyanın içeriği bilinmiyor. Silinmemiş dosyalarda cihatçı içerik bulunduğu ayrıca bildirildi [RD38], [RD39]. Bu nedenle bulgu "dizüstünde cihatçı içerik yok" biçiminde okunamaz; K21'in tek başına okunması bu yüzden yanıltıcıdır.
- **[O]** SK Başkanı Bastrıkin 2019'da Türkiye'deki işlemlerle failin rapor alması, otel rezervasyonu ve kimlikle aramasız giriş dahil hazırlık koşullarının belirlendiğini, "başka sorular" olduğunu ama konuşmak için erken olduğunu söyledi [R41]. **[O]** Karlov'un eşi 2018'de soruşturmayı Rusya SK'nin yürüttüğünü ve kendisini bilgilendirdiğini, ama haberlerin çoğunu internetten öğrendiğini söyledi [R53].
- **[O]** Rejim kontrolünde olmayan bir kaynak (Nordic Monitor, 2026), Rusya'nın duruşmalara gözlemci göndermeyi bıraktığını ve kendi soruşturmasıyla "gerçek failleri" belirlediğini yazdı [KR-126]. **[O]** Bu iddiayı teyit eden bir Rus resmî kaynağı bulunamadı [KR-126]. **[O]** Yazar, 2026'da MİT suç duyurusunun hedefidir; bu bir çıkar çatışmasıdır [KR-124].

## Rusya'nın FETÖ tezine yaklaşımı: ne onay ne ret

**[O]** Türk Dışişleri Bakanı 20 Aralık'ta ABD'li mevkidaşına "Türkiye de Rusya da saldırının arkasında FETÖ'nün olduğunu biliyor" dedi [KR-078], [K07]. **[O]** Kremlin ertesi gün sonuç çıkarmakta acele edilmemesi gerektiğini söyledi [R18], [K10]. **[O]** Bir Rus akademisyen 2018'de Rus tarafının Gülen'in suikastın arkasında olduğuna "pek inanmadığını" ve olasılığın "sıfıra yaklaştığını" söyledi; bu bir resmî görüş değil, uzman yorumudur (C3) [R46]. **[O]** Devlet kontrolündeki NTV 2023'te Gülen'in "ABD istihbaratının çatısı altında" saklandığını aktararak suikastı ABD'ye bağlayan bir çerçeve kurdu (C5) [R47]. **[O]** RIA Novosti 2026'da Türk mahkemesinin başka bir davadaki gerekçesine dayanan Sabah haberini yorumsuz aktardı [R48], [KR-127].

**[D]** Rusya'nın resmî tutumu on yıl boyunca aynı dengeyi korudu: Türk yargısının kararını kabul etti, FETÖ'yü azmettirici olarak açıkça adlandırmadı, "azmettirenler" sorusunu açık tuttu ve sorumluluğun bir kısmını Suriye konusundaki medya atmosferine bağladı [R42], [R23], [R12]. **[D]** Bu son vurgu, saldırının bir ideolojik iklimden beslendiği okumasıyla (H3a) Türkiye'nin resmî tezinden daha uyumludur; ancak Rusya'nın resmî açıklamaları da diplomatik çıkarla şekillenen kurum iddialarıdır ve aynı ihtiyatla okunmalıdır.

## Rus medyasının çerçeveleri: devlet ve bağımsız

- **[O]** BBC Monitoring'e göre Rus basını suikastı ağırlıkla normalleşmeyi bozma girişimi olarak okudu; Komsomolskaya Pravda'da "üçüncü güç" teması, Izvestia'da Halep kaynaklı düşmanca atmosfer yorumu öne çıktı [R43].
- **[O]** BBC Rusça'nın sosyal medya analizine göre suikastı Suriye kampanyasıyla ilişkilendirenler ağırlıkla muhaliflerdi; hükümet yanlısı blogcular Batı'yı ve isimsiz Rusya düşmanlarını suçladı [R44].
- **[O]** The Atlantic'teki bir analize göre Batı haberlerinin ilk satırlarındaki "Halep'i unutma" motivasyonu Rus devlet medyasında "göze batacak şekilde yoktu" (arama özeti, B3) [R45].
- **[O]** Lenta.ru ve RBC gibi Rus kaynakları ilk saatlerde failin darbe sonrası polislikten ihraç edildiğini yazdı; İçişleri Bakanı ise failin "halen görevde" olduğunu söyledi [KR-003], [KR-038].
- **[D]** Rus devlet medyasının Halep motivasyonunu geri planda tutması, Rusya'nın Suriye politikasının bir saldırıya gerekçe olarak sunulmasından kaçınma çıkarıyla tutarlıdır (muhtemel). Bu, Türk hükümete yakın medyasının cihatçı çerçeveyi geri planda tutmasıyla yapısal bir benzerlik gösteriyor: iki ülkenin devlete yakın medyası da kendi hükümetinin Suriye politikasını sorgulatacak çerçeveden uzak durdu (olası).

## Marina Karlova'nın açıklamaları

**[O]** Karlov'un eşi Marina Karlova, suikasttan sonra Türk ve Rus basınına birçok kez konuştu ve 2019'da Uluslararası Andrey Karlov Vakfı'nın başkanı olarak anıldı [R55]. Açıklamaları kronolojik sırayla:

- **[O]** Haziran 2017, Türk basınına ilk açıklaması: Türkiye'ye ve Türk halkına kin beslemediğini, katillerin amacının iki halkı düşman etmek olduğunu, yöneticilerin bu tuzağa düşmediğini söyledi [R50].
- **[O]** Kasım 2017, RT: Ankara'ya veda için döndüğünde sıradan Türklerin "hepsi ağladı, sarıldı, bazıları elimi bile öptü ve hepsi özür diledi" [R51].
- **[O]** Aralık 2018, RIA: "Andrey'in başına gelen trajedinin Türklerle hiçbir ilgisi yok, bu uluslararası teröristlerin işi. Katil… zombileştirilmiş, etkilenebilir bir çocuk" [R52]; failin bıraktığı notta "ABD ve Rusya kötülüktür" yazdığını, karar öncesi sanıkların gözlerine bakmak istediğini söyledi [R53].
- **[O]** Ocak 2019: davanın açılış duruşmasında cinayetin Rusya–Türkiye ilişkilerine zarar vermeyi amaçladığını söyledi (beyanın biçimi belirsiz, arama özeti) [R60].
- **[O]** Kasım 2019, Sputnik: yaşananların Türk halkının değil uluslararası terörizmin suçu olduğunu, altı ay evden çıkamadığını ve vakıf çalışmalarıyla hayata döndüğünü anlattı [R55].
- **[O]** Aralık 2020, BBC Rusça: "Bu davanın asla aydınlatılmayacağından eminim… Er ya da geç bir günah keçisi bulacaklar ya da yalnız bir terörist olduğunu söyleyecekler" [R56], [KR-113]. Aynı röportajda saldırıdan en az dört ay önce tehditler olduğunu, eşinin arabada "yat dersem soru sorma, yere yat" dediğini, sonradan tehditlerin varlığının söylendiği halde "nedense kimsenin tepki vermediğini" ve galeride metal dedektörden geçirilmeden içeri alındıklarını anlattı (B2) [R57].
- **[O]** Mart 2021, karar sonrası: yargılamayı takip etmediğini, bunun manevi olarak ağır geldiğini söyledi [R58].
- **[O]** Mart 2023, NTV: ya bazı sinyaller olduğunu ya da her gün gerilen siyasi ortamın, Türk basınındaki sert Rusya karşıtı yayınların etkili olduğunu düşündüğünü söyledi [R59].
- **[O]** Bir Rus yayını, eşinin İzvestia'ya katili "etkilenebilir bir zombi çocuk" ve "çok yalnız bir insan" olarak tarif ettiğini aktardı (arama özeti) [RD32].

**[D]** Marina Karlova'nın açıklamaları hiçbir hipotezi tam olarak desteklemiyor: "uluslararası teröristler" ve "zombileştirilmiş çocuk" ifadeleri bir dış yönlendirme ya da ideolojik etkilenme okumasına; "günah keçisi ya da yalnız terörist" ifadesi ise resmî kapanışa duyulan güvensizliğe işaret ediyor. Önceden gelen tehditlere tepki verilmediği yönündeki anlatımı (B2, tek tanık), koruma zafiyeti sorusunu (Bölüm 10) güçlendiriyor. **[O]** Oğlunun kamuya açık bir açıklamasına rastlanmadı [R54].

## Anma politikası

**[O]** Karlov'a ölümünden sonra "Rusya Federasyonu Kahramanı" unvanı verildi (kararname 20.12.2016) [R33]; 22 Aralık'ta Moskova'da Dışişleri binasındaki veda törenine Putin katıldı [R34], [KR-085]. **[O]** Ankara'da Rus Büyükelçiliği'nin bulunduğu sokağa belediye meclisinin oybirliğiyle Karlov'un adı verildi; girişim Çavuşoğlu'nundu [R36]. **[O]** Moskova'da bir geçide ve okuduğu okula adı verildi [R35]; büyükelçilik bahçesine MİD çalışanlarının bağışlarıyla bronz büst dikildi ve büyükelçilik okuluna adı verildi (arama özeti) [R37]; birinci yıl dönümünde Moskova'da anma plaketi açıldı [R38]. **[O]** Rusya'nın yeni Ankara Büyükelçisi birinci yıl dönümünde Karlov'a en iyi anıtın "TürkAkım boru hattının kilometreleri, Akkuyu NGS'nin reaktörleri" olacağını söyledi [R31]. **[O]** Esenboğa'daki törende Türk bakan "Karlov'u öldürmediler, tarihe gömdüler… Türk-Rus dostluğunun ölümsüz sembolü oldu" dedi (arama özeti) [KR-075].

**[D]** Her iki devletin anma pratiği, Karlov'u ikili ilişkinin sembolüne dönüştürdü; anma, ilişkiyi kurumsallaştırmanın bir aracı olarak işledi (muhtemel). Bu çerçevede suikastın faili ve azmettiricisi sorusu anmanın merkezinde değil.

## Türkiye–Rusya ilişkisine etkisi

**[O]** Suikastın ertesi günü Moskova'daki Türkiye–Rusya–İran üçlü toplantısı iptal edilmedi; "Moskova Bildirgesi" Suriye'de askerî çözüm olmadığını ve üç ülkenin garantörlüğe hazır olduğunu açıkladı [R27], [KR-077], [K13]. **[O]** Ocak 2017'de Astana görüşmeleri başladı [R28]. **[O]** Eylül 2017'de Türkiye'nin S-400 için Rusya'ya peşinat ödediği açıklandı (arama özeti) [R29]. **[O]** Putin, 23 Aralık 2016'da suikastın ilişkilerin gelişmesine engel olmayacağını söyledi [R21]. **[O]** Çavuşoğlu 2021'de "Türkiye ve Rusya bu tuzağa düşmedi" dedi [R32]. **[O]** Gülen dahil sekiz kişi hakkındaki yakalama kararının Putin'in Türkiye ziyaretinden bir gün önce çıktığı bildirildi (Reuters, arama özeti) [KR-104].

**[D]** Suikastın ilişkiyi bozmadığı neredeyse kesindir. İlişkinin suikasttan sonra Suriye diplomasisi ve savunma alanında derinleştiği olgularla tutarlıdır; derinleşmenin suikast *nedeniyle* mi yoksa suikasta *rağmen* mi olduğu, mevcut kartlarla ayırt edilemez. **[D]** Yakalama kararının zamanlaması (kaynak arama özeti) yargı adımlarının diplomatik takvimle örtüştüğünü düşündürüyor; bu tek örnekten bir örüntü çıkarılamaz.

## ABD, AB, BM, NATO, İran, Suriye ve cihatçı gruplar

| Aktör | Tepki (kurum iddiası) | Kart |
|---|---|---|
| Donald Trump (seçilmiş başkan) | Karlov "radikal İslamcı bir terörist" tarafından öldürüldü (yazılı açıklama) | [R61] |
| ABD Dışişleri (Kerry) | Kınadı; soruşturmada yardıma hazır | [R62] |
| ABD Dışişleri sözcüsü (Kirby) | Motivasyon henüz bilinmiyor; ABD'nin işin içinde olduğu iması "absolutely ridiculous" | [K09] |
| Beyaz Saray | "Kabul edilemez"; terörle mücadelede Rusya ve Türkiye ile birlik | [R63] |
| NATO Genel Sekreteri | "Böyle iğrenç bir eylemin hiçbir gerekçesi olamaz" | [R64], [R63] |
| BM Genel Sekreteri ve Güvenlik Konseyi | Terör eylemi olarak kınadı; failler, organizatörler, finansörler ve sponsorların adalete teslimi; Viyana Sözleşmesi | [R65], [KR-057] |
| AB (Mogherini) | En güçlü biçimde kınadı | [R66] |
| AGİT Daimi Konseyi | "Ölümcül terör saldırısı" (arama özeti) | [R69] |
| İran Dışişleri | "Tekfirci" grupların işi; ülkeler arasında çatışma yaratma amacı | [R67] |
| Suriye (Esad yönetimi) | "Terörist ve korkakça" saldırı | [R68] |
| Fethullah Gülen | "Korkunç bir terör eylemi" olarak kınadı | [KR-067] |
| Ceyş el-Fetih / Cebhet Fetih eş-Şam | Üstlenme metni sahte ve "amatör"; ancak suikast Halep'teki Rus "katliamına" karşı bölge insanlarının "doğal tepkisi" | [R49], [K34], [K35], [KR-081], [KR-084] |

**[D]** Uluslararası aktörlerin çerçeveleri, her birinin kendi Suriye konumunu yansıtıyor: ABD'nin seçilmiş başkanı ve İran cihatçı/tekfirci bir faili işaret etti [R61], [R67]; Rusya adlandırmasız "provokasyon" çerçevesini seçti [R02]; Türkiye FETÖ'yü işaret etti [K08]. Hiçbir uluslararası kuruluş fail ya da azmettirici adlandırmadı [R65], [R66], [R69]. **[O]** Sahte üstlenme bildirisi Mısır ve Irak medyası üzerinden TASS'a ulaştı; İtalyan basınına göre İran'ın ISNA'sı da yaydı (arama özeti) [KR-080], [K34]. **[S]** Bildirinin ilk kaynağı bilinmiyor.


# Kavram: radikalleşme

Bu bölüm, failin süreci değerlendirilmeden önce kullanılacak kavramsal araçları özetler. Kaynaklar `radikallesme.md` Parça A'dadır; erişim işaretleri korunmuştur: [kayıt] = yayıncı ya da DOI kaydı doğrulandı, tam metin okunmadı; [arama özeti] = yalnızca arama sonucu özetinden.

## Tanım tartışması

- **[O]** "Radikalleşme" kavramı 2004–2005 Madrid ve Londra saldırılarından sonra politika diline yerleşti ve tanımı hâlâ tartışmalıdır [RAD-A§1]. **[O]** Peter Neumann (2013, *International Affairs* 89(4)) bilişsel radikalleşme (aşırı inançlar) ile davranışsal radikalleşme (aşırı eylem) arasında ayrım yapar ve tanım farklılıklarının kaynağını bu belirsizlikte görür [RAD-A§1] [kayıt].
- **[O]** Randy Borum (2011, *Journal of Strategic Security* 4(4)) radikal inancın terörün zorunlu öncülü olmadığını vurgular; terörizme katılımı farklı kişilerde farklı işleyen süreçler bütünü olarak görür ve toplumsal hareket kuramı, sosyal psikoloji ve din değiştirme kuramını önerir [RAD-A§1] [kayıt].
- **[O]** Alex P. Schmid (2013, ICCT) "radikalizm" ile "aşırıcılık" arasında ayrım yapar ve radikalleşmenin mikro (birey), mezo (radikal çevre) ve makro (radikalleşen kamuoyu ve siyaset) düzeylerde incelenmesini önerir [RAD-A§1] [kayıt].
- **[D]** Bu vaka için ayrımın önemi şudur: failin *ne düşündüğü* (bilişsel) ile *eylemi kimin tetiklediği ya da yönlendirdiği* (davranışsal) ayrı sorulardır ve farklı kanıt türleri gerektirir.

## Başlıca modeller

| Model | Temel fikir | Bu vakada aranacak işaret | Kaynak |
|---|---|---|---|
| Moghaddam, "terörizme giden merdiven" (2005) | Altı katlı, daralan merdiven: adaletsizlik algısı → seçenek arayışı → öfke → ahlaki bağlılık → biz/onlar → eylem | Mağduriyet dili, kategorik düşman algısı | [RAD-A§2] [arama özeti] |
| McCauley ve Moskalenko (2008; 2017) | 12 mekanizma (kişisel ve grup mağduriyeti, kaygan yokuş, sevgi/bağlılık, grup kutuplaşması, şehitlik); görüş piramidi ile eylem piramidi ayrımı | Grup mağduriyeti (Halep), şehitlik dili, aktivizmden eyleme geçiş | [RAD-A§2] [kayıt] |
| Wiktorowicz, "bilişsel açılma" (2005) | Kriz → dini arayış → çerçeve hizalanması → sosyalleşme; "kutsal otorite" ve küçük çalışma halkaları | Ardışık dini grup arayışı, bir vaize bağlanma | [RAD-A§2], [RAD-A§4] [kayıt] |
| Sageman, "bunch of guys" (2004; 2008) | Arkadaşlık bağlarıyla örgütlenen küçük gruplar; ahlaki öfke, küresel savaş çerçevesi, ağ mobilizasyonu | Akran ağı, ortak ev, birlikte grup değiştirme | [RAD-A§2] [kayıt] |
| Kruglanski, "önem arayışı" (2014; 2022) | İhtiyaç (needs) + anlatı (narratives) + ağ (networks) = "3N"; önem kaybı ya da önem kazanma fırsatı | Yalnızlık, statü arayışı, şehitlik yoluyla önem | [RAD-A§2] [kayıt] |
| Della Porta (2013) | Hareket–karşı hareket–devlet etkileşimi; tırmanan polislik, ideolojik kapsülleşme | Devlet tasfiyeleri ve kapalı grup dinamiği | [RAD-A§2] [kayıt] |

## Çevrimiçi ve çevrimdışı radikalleşme

**[O]** RAND'ın 15 vakalık çalışması internetin propagandaya erişimi ve "yankı odası" etkisini artırdığını, ancak yüz yüze temasın yerini aldığı varsayımını desteklemediğini buldu (von Behr vd., 2013) [RAD-A§3] [kayıt]. **[O]** İngiltere'de mahkûm 223 terörist üzerine yapılan nicel çalışmaya göre internet büyük ölçüde kolaylaştırıcıdır; birçok kişi inancını değiştirmek için değil pekiştirmek için çevrimiçine girer (Gill, Corner, Conway vd., 2017) [RAD-A§3] [kayıt]. **[D]** Bu vakada çevrimiçi izler (El Kaide videosu, aramalar) ile çevrimdışı izler (sohbet halkaları, kitaplar, tanıklar) birlikte bulunuyor; literatür ikisini rakip değil tamamlayıcı süreçler olarak görmeyi öneriyor.

## Din eğitimi, sohbet halkaları ve "kutsal otorite"

**[O]** Wiktorowicz'e göre dini aşırıcılığa katılımın kilit unsuru kutsal otoritenin güvenilirliği ve küçük çalışma halkalarındaki "kültürlenme"dir [RAD-A§4]. **[O]** Türkiye örneklerinde gayriresmî dini mekânlar öne çıkar: Adıyaman'daki "İslam Çay Ocağı" (SETA 2016, arama özeti) ve Uluslararası Kriz Grubu'nun aktardığı, devlet imamının vaazlarını reddedip cumaya gitmeyi bırakan "Cumasızlar" (ICG 2020) [RAD-A§4].

## "Yalnız aktör" tartışması

**[O]** Gill, Horgan ve Deckert (2014) 119 yalnız aktör teröristi inceledi; tek tip profil bulmadılar, çoğunun bir grup ya da hareketle gözlemlenebilir faaliyeti vardı ve niyet sıklıkla çevreye "sızdırılmıştı" [RAD-A§5] [kayıt]. **[O]** Schuurman ve arkadaşları (2019) "yalnız kurt" tipolojisinin terk edilmesini savunur; radikal çevrelerle bağlar hem güdünün hem kapasitenin oluşmasında kritiktir [RAD-A§5] [kayıt]. **[D]** Bu bulgu, H2 ("saf yalnız aktör") ile H3a ("ortamda radikalleşmiş, örgütsel emir yok") arasındaki ayrımı keskinleştirir: eylemde yalnız olmak, radikalleşmede yalnız olmak anlamına gelmez.

## Türkiye bağlamı

- **[O]** ICG'ye göre IŞİD topraklarına giden Türk vatandaşı sayısının tahminleri 5.000 ile 9.000 arasında değişiyor; 2013–2014'te ailelerin bildirimlerine rağmen yetkililerin pek bir şey yapmadığı aktarılıyor [RAD-A§6].
- **[O]** CTC Sentinel'e göre Türk güvenlik kurumları tarihsel olarak PKK'ya odaklıydı ve IŞİD ağlarını agresif biçimde dağıtmaya ancak 2015 yazında başladı [RAD-A§6]. **[O]** 15 Temmuz 2016'dan sonra önceliğin FETÖ'ye de kaydığı ICG'nin terim notundan ve Polis Akademisi literatüründen izlenebiliyor; Polis Akademisi'nin 2017 raporu dört radikalleşme türü sayıyor: etnik (PKK), din istismarına dayalı (DEAŞ/El Kaide), "sahte-mehdilik temelli" (FETÖ) ve sol-ideolojik (arama özeti) [RAD-A§6].
- **[O]** Adıyaman'daki Dokumacı ağı 2015'teki Diyarbakır, Suruç ve Ankara Garı saldırılarıyla ilişkilendirildi [RAD-A§6].
- **[O]** Bu çalışmada Ankara'daki Hacı Bayram çevresini cihatçı bir merkez olarak inceleyen akademik bir çalışma bulunamadı; Hacı Bayram bu vakada yalnızca Nurettin Yıldız vaazlarının yapıldığı yer olarak geçiyor [RAD-A§6].

## Neden önemli ve hangi göstergelerle izlenir

**[D]** Radikalleşme bir süreç olarak anlaşılırsa müdahale fırsatları görünür hale gelir; Gill vd. (2014) ve Schuurman vd. (2019) yalnız aktörlerin bile çoğunlukla gözlemlenebilir ve sızdırılmış davranışlar sergilediğini gösteriyor [RAD-A§7]. **[O]** Literatürden çıkan yedi izleme göstergesi: (1) ana akım dini otoriteden kopuş, (2) kapalı sohbet halkalarına yoğunlaşma, (3) çatışma bölgesine gitme isteği ve bağış, (4) şehitlik ve önem dili, (5) cihatçı içerik ve kitap edinimi, (6) niyet sızıntısı ve veda davranışları, (7) meslekten ayrılma isteği ve operasyonel hazırlık [RAD-A§7]. Bu göstergeler Bölüm 6'da failin süreciyle tek tek eşleştirilmiştir.

# Failin radikalleşme süreci

**[O]** Bu bölümün dayandığı 56 kartın 37'si açılan sayfadan, 17'si yalnızca arama özetinden alındı, 2'si temel kanıt kartlarından alındı; iddianame, gerekçeli karar, MASAK ve Emniyet yazılarının birincil metni hiçbir kartta doğrudan açılmadı [RAD-B]. **[D]** Bu nedenle aşağıdaki her "iddianameye göre" ifadesi bir basın aktarımıdır ve kurum iddiası olarak okunmalıdır.

## Yaşam öyküsü ve aile

- **[O]** İçişleri Bakanı'nın açıkladığı kimliğe göre fail 24 Haziran 1994 Söke doğumlu, Söke Cumhuriyet Anadolu Lisesi ve İzmir Rüştü Ünsal Polis Meslek Yüksekokulu mezunu, 2,5 yıldır Ankara Çevik Kuvvet'te görevliydi [RD01], [KR-038].
- **[O]** Abla, ailenin polis okulunu "ucuz ve garantili" olduğu için seçtiğini, kardeşinin çocukken cuma ve teravihe gittiğini, günde beş vakit namaza polis okulunda başladığını anlattı [RD04]. **[O]** Baba, emniyet ifadesinde oğlunun polis olduktan sonra "ibadetlerine daha düşkün olmaya, içine kapanmaya ve sessizleşmeye" başladığını söyledi [RD03]. **[O]** Bir akraba değişimin "son iki-iki buçuk yılda, mesleğe girdikten sonra" olduğunu, denize girmemeye ve televizyon açtırmamaya başladığını anlattı [RD09].
- **[O]** Reuters'a göre baba, oğlunun bildiği kadarıyla hiçbir terör örgütüne, dini ağa ya da gruba üye olmadığını söyledi (arama özeti) [RD10]. **[O]** Failin dayısı "aile olarak FETÖ'ye karşıyız" dedi (arama özeti) [RD08].
- **[O]** Anne ifadesine göre fail olay günü saat 16:30'da annesini arayıp "Allah'a emanet ol, hakkını helal et" dedi [RD02]. **[D]** Bu, literatürdeki "veda davranışı" göstergesine uyuyor (muhtemel) [RAD-A§7].
- **[O]** Dershane konusunda kaynaklar çelişiyor: AA, failin Söke'de 2014'te kapatılan FETÖ'ye ait Körfez Dershanesi'nde hazırlandığının "bildirildiğini" yazdı (arama özeti, C4) [RD06]; anne ve abla bunu yalanladı [RD02], [RD05]. **[O]** Eğitim masraflarını firari bir işadamının karşıladığı iddiası (D4) abla tarafından yalanlandı [RD07], [RD05].
- **[O]** Aile olay gecesi Söke'de gözaltına alındı [KR-061]; anne-baba cenazeyi teslim almadı ve fail kimsesizler mezarlığına gömüldü [KR-093], [KR-097], [KR-098].

## Polis okulu dönemi (2012–2014) ve Gülen çevresi iddiaları

- **[O]** İddianamedeki bir şüpheli beyanına göre fail, "Hamza" kod adlı bir kişinin evinde Gülen videoları izliyordu ve 17–25 Aralık sonrasında da bu eve gidip geliyordu [RD18]. **[O]** Bu şüpheli duruşmada ifadesini "baskı altında" verdiğini söyleyerek geri aldı (arama özeti) [RD18].
- **[O]** Polis okulundan arkadaşı olan bir sanık savcıya, 17–25 Aralık öncesinde örgüt sohbetlerine birkaç kez katıldığını ve failin de geldiğini, sonrasını bilmediğini söyledi [RD19]. **[O]** Sınıf komiseri ikisini uyardığını ve 17–25 Aralık sonrasında "ilişkilerini kestiklerini iddia ettiklerini" aktardı [RD20]. **[O]** Bir tanık failin ikinci sınıftan itibaren sınıf kütüphanesindeki Gülen kitaplarını okuduğunu [RD21], başka bir tanık failin "Fetullah Gülen cemaati sohbetlerine de gitmiştim" dediğini aktardı [RD22].
- **[O]** Bir hükümete yakın gazete, failin ve arkadaşının polis okulu sınavını yakın puanla ve yanlışları aynı şıkla geçtiğini yazdı; kaynak "savcılık kaynakları"dır (arama özeti, D4) [RD25].
- **[D]** Polis okulu dönemine ait Gülen çevresi temasının tüm kaynakları 15 Temmuz sonrası ortamda alınmış ifadelerdir; en az bir ifade mahkemede geri alındı ve tanıkların bir kısmı aynı dosyada sanıktır [RD18], [RD19]. Erken bir temasın varlığı olası; ancak temasın içeriği ve derinliği belirsiz, sürdüğüne dair bağımsız kanıt yok. Tanıkların ikisi de 17–25 Aralık 2013 sonrasında bir kopuştan söz ediyor [RD19], [RD20].

## Ankara dönemi: sohbet halkaları, Nurettin Yıldız ve Sosyal Doku (2014–2016)

- **[O]** Hürriyet'in 24 Aralık 2016 haberine göre fail, iki ev arkadaşıyla (biri avukat, biri polis) Etlik ve Batıkent'te bir evde ve Hacı Bayram Camii'nde Nurettin Yıldız'ın sohbetlerine katılıyordu [RD11], [KR-091]. **[O]** İddianameye göre fail 2014'te Sosyal Doku Ankara Gönüllüleri'ne dahil oldu, 2015'te Twitter üzerinden İsmailağa çevresinin Ankara uzantısından kişilerle ve bir dernek mensubuyla irtibat kurdu [RD13]; ajandasında Yıldız sohbetlerine dair notlar vardı [RD14]. **[O]** 2018 tarihli bilirkişi raporuna göre bir USB bellekte Yıldız sohbet dosyaları ile Çeçen ve Hamas marşları bulundu [RD15].
- **[O]** Bir tanık, failin Ekim–Kasım 2014 temasından sonra Hacı Bayram'daki sohbete geldiğini ve Aralık 2014'ten itibaren polis okulundan arkadaşıyla programlara "aksatmadan" katıldığını aktardı (arama özeti) [RD16], [KR-111]. **[O]** İHH çalışanı bir tanık failin Yıldız'ın vaazlarında görüldüğünü kabul etti; bu bilgi ifade tutanağı görüntüsüyle yayımlandı, ancak yayının yazarı vakada MİT suç duyurusunun hedefidir (çıkar çatışması) [RD17].
- **[O]** Sosyal Doku Vakfı, Yıldız'ın Hacı Bayram vaazlarının halka açık olduğunu ve iki yıl önce yapıldığını, haberlerin "algı operasyonu" olduğunu açıkladı; açıklama katılımı reddetmiyor (arama özeti, D3) [RD12].
- **[O]** İddianame ve gerekçeli karar bu katılımı kabul etti ve "renklendirme" olarak yorumladı: karara göre fail 17–25 Aralık sonrası talimatla dini gruplara sızdı, Sosyal Doku içinde "saklandı" ve FETÖ'ye bilgi aktardı [RD43], [RD52], [K27]. **[O]** İçişleri Bakanı 24 Aralık 2016'da failin hayatındaki radikal İslamcı izlerin Gülen bağlantısını gizleme çabası olduğunu savundu (arama özeti) [RD56].
- **[D]** Sohbet halkalarına katılım, bu dosyada **devlet ve devlet dışı kaynakların aynı olguda buluştuğu** nadir noktalardan biridir (güçlü, çok kaynaklı). Kaynaklar olgu üzerinde değil, yorum üzerinde ayrışıyor: aynı davranış resmî anlatıda "örtü", diğer anlatıda "arayış" olarak okunuyor [KR-092].

## Kitaplar: iki yönlü haberler ayrı ayrı

**"FETÖ kitapları" yönündeki haberler**

- **[O]** AA, 20 Aralık 2016'da failin Keçiören'deki evinde "FETÖ ve El Kaide'ye ilişkin kitaplar bulunduğunu" yazdı; kitap adı vermedi (C3) [RD29].
- **[O]** İddianame aktarımına göre evde Risale-i Nur kitapları vardı; bazıları kullanılmıştı ve Meyve Risalesi'nde altı çizili yerler bulunuyordu [RD28]. **[O]** Risale-i Nur Said Nursi'nin eseridir, Gülen'in değil; açılan kaynaklarda evden Gülen'e ait bir kitap adı listelenmiyor [RD28]. Gülen kitapları yalnızca polis okulu sınıf kütüphanesi bağlamında, bir tanık beyanında geçiyor [RD21].

**Cihatçı/Selefi yöndeki haberler**

- **[O]** İddianameye göre fail, saldırıdan bir gün önce "taşınacağı" gerekçesiyle bir tanığa bir kitap valizi bıraktı: Seyyid Kutub'un *Fî Zılâli'l-Kur'an*'ı (16 cilt), Hasan el-Benna, Nurettin Yıldız kitapları ve Abdulkadir Şen'in Suriye kitabı; aynı tanığa WhatsApp'tan "şu özel harekat netleşmedi, ocak gibi başlayacak" yazdı [RD27]. **[O]** Savcılık bu teslimi "hedef şaşırtmak amacıyla" yapılmış olarak niteledi [RD27].
- **[O]** Evde Yahya Konuk imzalı yabancı savaşçı ve cihat kitapları da bulundu; iddianameye göre bunlarda okunma izi yoktu [RD28].
- **[O]** Rejim kontrolünde olmayan bir kaynağa göre satış faturaları, failin Awlaki'nin *Cihadı Desteklemenin 44 Yolu* kitabını sipariş ettiğini ve olay günü diğer cihatçı kitaplarla bir arkadaşa bağışladığını gösteriyor (C3) [RD30]. **[O]** Bu kitap iddianamedeki valiz listesinde geçmiyor ve teslim tarihi farklı (olay günü / 18 Aralık) [RD30], [RD27].

**Çelişen "tek kitap" iddiası**

- **[O]** Karar gazetesi 22 Aralık 2016'da, savcılığın evde "bulunan tek dini kitap" ve el yazısı notun dikkatleri başka yöne çevirmek için hazırlanmış olabileceğini değerlendirdiğini yazdı (C3) [RD31]. **[O]** Bu "tek kitap" iddiası sonraki iddianame listeleriyle çelişiyor [RD31], [RD27], [RD28].
- **[O]** El yazısı notta "ABD ve Rusya'nın sonu yakındır. Artık kıyam vaktidir. Beldelerimizde güveni hissetmedikçe sizler beldelerinizde güvende olmayacaksınız" yazdığı aktarıldı [RD31], [KR-088]; Karlov'un eşi de nottan söz etti [R53], [RD32].

**[D]** Kitap kanıtı yön bakımından asimetrik: Selefi-cihatçı eserler adlarıyla, tarih ve teslim bağlamıyla listeleniyor; "FETÖ kitapları" ifadesi ise adsız kalıyor ve evde Gülen eseri listelenmiyor. Bu asimetri H3a lehine bir göstergedir (muhtemel). Resmî yorum (planlı "mizansen") bu göstergeyi açıklayabilir, ama ek bir varsayım gerektirir: Şubat 2016'da indirilen bir videonun ve on ay boyunca süren aramaların da mizansenin parçası olması [RD38], [RD39].

## Bağışlar ve İHH

- **[O]** Rejim kontrolünde olmayan bir kaynağın yayımladığı MASAK raporu görüntülerine göre fail Ocak 2015–Temmuz 2016 arasında İHH hesaplarına 11 havale yaptı (C2) [RD35]; temel kanıt kartına göre toplam tutar 1.584,13 TL'dir [K33]. **[O]** Bu bilgi Türk resmî kaynaklarında teyit edilmedi [RD35].
- **[O]** Aynı yazarın 2026 yazısına göre fail Musab bin Umeyr Derneği'ne para gönderdi ve hükümlü bir El Kaide üyesine para aktardı; bu yazıda belge görüntüsü yok ve başka kaynakta teyit bulunamadı (C3) [RD36].
- **[O]** İHH'nin 17 Aralık 2016'daki sınır konvoyu "Rusya Suriye'den defol" protestosuna dönüştü [K15]; bir tanığa göre fail bu konvoyun davetini izin planı nedeniyle reddetti [RD34].
- **[D]** Küçük bağışlar ideolojik yakınlık göstergesidir, örgütsel yönlendirme kanıtı değildir. İHH yasal bir yardım kuruluşudur; bağışın varlığı tek başına suç ya da radikalleşme kanıtı sayılmamalıdır.

## Suriye'ye gitme isteği: iki tanık

- **[O]** Bir tanık (valizin bırakıldığı kişi), failin bunalımda olduğunu, görevden ayrılıp Suriye'ye gitmek ve "orada sıkıntı çeken Müslümanlara" yardım etmek istediğini ve kendisinin ona nasihat ettiğini anlattı (AA, iddianame aktarımı, B2) [RD33].
- **[O]** Başka bir tanık 26 Aralık 2016 tarihli ifadesinde failin iki yıldır tanıdığını, sohbet halkalarında görüştüklerini, cihat konuştuklarını ve failin işini bırakıp Suriye'ye gitmek istediğini söyledi (ifade tutanağı görüntüsüyle, C2) [RD34].
- **[O]** İsmailağa çevresinin Ankara uzantısından bir kişinin sonradan silinen tweet'ine göre fail Twitter'dan ulaştı, "FETÖ okullarında yetiştiğini" anlattı ve Çevik Kuvvet'ten ayrılıp "aktif görev" almak istediğini söyledi; tweet sahibi ona "Özel Harekât'a gir" dedi (C3) [RD26].
- **[D]** Suriye isteği iki ayrı tanıkla ve biri devlet ajansı, biri rejim kontrolünde olmayan kaynak olmak üzere iki farklı kaynak sınıfıyla destekleniyor; bu, failin süreciyle ilgili en güçlü olgulardan biridir. "Aktif görev" ifadesi iki yönlü okunabilir: cihat ya da Özel Harekât; WhatsApp mesajı ikincisini de gösteriyor [RD27].

## Dijital izler

- **[O]** İddianamedeki bilgisayar incelemesine göre fail 14 Şubat 2016'da YouTube'da "El Kaide – sen ancak kendinden sorumlusun" başlıklı videoyu aradı ve indirdi; video ortak kullanılan dizüstünde 18 Aralık 2016'da silindi (iddianame alıntısı, B2) [RD38].
- **[O]** Haziran 2017 tarihli teknik rapora göre (rejim kontrolünde olmayan kaynak aktarımı) fail 25 Ağustos 2016'da Halis Bayancuk, 12 Aralık'ta Ebu Basir el-Hindi, 15 Aralık'ta Awlaki, 18 Aralık'ta Kouachi kardeşler ve Bhutto suikastı aramaları yaptı; olay sabahı neşid dinledi; aynı raporda Che, Castro ve Saddam izlemeleri de var (C2) [RD39].
- **[O]** Savcılık kaynaklı habere göre fail cinayetten bir hafta önce "Sosyal doku" WhatsApp grubuna "El-Kaide tehlikeli bir örgüt" mesajı yazdı ve Kasım sonunda kız arkadaşına "Şahadet istiyorum" dedi (C3) [RD41].
- **[O]** Savcılık değerlendirmesine göre Arapça slogan, El-Nusra iltisaklı kişilerle iki ay boyunca "günlük görüşme" ve dağıtılan kitaplar "algı operasyonu" amaçlıydı (C4) [RD42]. **[D]** Bu cümle bir yorum içeriyor, ama aynı zamanda Nusra bağlantılı kişilerle günlük görüşme olgusunu savcılığın kendisinin kabul ettiğini gösteriyor.
- **[O]** Rus heyeti silinmiş dosyalarda 690 "Hizmet" ve 2 "Fetullah Gülen" adlı dosya buldu; silinmiş dosyalarda El Kaide, Nusra ve DEAŞ adlı dosya yoktu (C3) [RD40].
- **[D]** Arab News'ün aktarımı [K21] "dizüstünde cihatçı içerik bulunmadı" biçiminde okunabilir; ancak diğer kartlar bunun yalnızca silinmiş dosyalar için geçerli olduğunu gösteriyor: cihatçı içerik silinmemiş dosyalarda ve arama geçmişinde vardı, El Kaide videosu ise saldırıdan bir gün önce silinmişti [RD38], [RD39], [RD40]. 690 "Hizmet" dosyası, sözcüğün genel anlamı ve içeriğin bilinmemesi nedeniyle tek başına örgütsel bağ göstergesi olarak okunamaz. İki yönlü veri tarafsız biçimde birlikte sunulmalıdır: aynı cihazda hem Gülen hareketine ait sözcüklerle adlandırılmış silinmiş dosyalar hem cihatçı içerik vardı.

## "Garson" listesi, ByLock ve kod çelişkisi

- **[O]** Bir hükümete yakın köşe yazısına göre "Garson" kod adlı bir kişinin SD kartındaki 2014 kodlama listesinde fail "EA (Eşit Ağırlıklı)" koduyla "örgüte en sadık kişilerden biri" olarak kodlandı, 2015 listesinde "örgütle bağı zayıfladı" notu düşüldü; yazı belge sunmuyor (D4) [RD47].
- **[O]** Başka bir hükümete yakın kaynak "EA"yı "Ehil Dünya: örgüt içinde yer alan ancak tam teslimiyet göstermeyen" olarak tanımlıyor (arama özeti, C4) [RD48].
- **[D]** Aynı kodun iki hükümete yakın kaynakta zıt anlamlarla açıklanması bu kanıtın güvenilirliğini düşürüyor; her iki okumada da 2015'te bağın zayıfladığı notu var.
- **[O]** Telefon hattı incelemesinde failin ByLock kullanmadığı belirlendi (birden fazla yayın, B2) [RD46]. **[O]** Aynı incelemede sıklıkla görüştüğü 8 kişinin ByLock kullanıcısı olduğu bildirildi (C3) [RD50], [KR-086]. **[D]** Görüştüğü kişilerin bir kısmı polis okulu sınıf arkadaşlarıdır; bir iletişim ilişkisi örgüt üyeliğini tek başına göstermez. **[O]** Emniyet failin açığa alındığı iddiasını yalanladı ve fail OHAL kararnameleriyle ihraç edilen polisler arasında yer almadı [RD49].
- **[O]** Gerekçeli karar, Şahin Söğüt'ün 9 Aralık 2016'da failin saldırıyla ilgili talimatları verdiğini kabul etti [RD44]; Söğüt işkenceyle ifade alındığını iddia etti [RD44]. **[O]** Etkin pişmanlıktan yararlanan Salih Yılmaz, failin "kendi zümresi içinde gözüktüğünü" ve "Ahmet" kodlu Söğüt'e teslim edildiğini söyledi; cinayetle ilgisi olmadığını belirtti [RD23], [K23].

## Ailenin ve yakın çevrenin ifadeleri (rolleriyle)

| Kişi (rol) | Ne dedi | Kart | Derece |
|---|---|---|---|
| Anne | Olay günü 16:30'da arayıp helallik istedi; dershaneye gitmedi; içine kapanık, sessiz | [RD02] | B2 |
| Baba | Polis olduktan sonra ibadete düşkün, içine kapanık; terör örgütü, dini ağ ya da grup üyesi değil | [RD03], [RD10] | B2 / B3 |
| Abla | Beş vakit namaza polis okulunda başladı; dershaneye kendisi gitti; işadamı yardımı yok | [RD04], [RD05] | B2 |
| Akraba | Değişim mesleğe girdikten sonra, son 2–2,5 yılda | [RD09] | C2 |
| Dayı | "Aile olarak FETÖ'ye karşıyız"; cenazeyi kimsesizler mezarlığına gömün | [RD08], [KR-093] | C3 |
| Okul arkadaşı (sanık) | Fail "cep telefonu hastası", "bön" biriydi | [RD24] | C3 |
| Karlov'un eşi | "Zombileştirilmiş, etkilenebilir bir çocuk", "çok yalnız" | [R52], [RD32] | B1 / C3 |

**[D]** Aile beyanları birbiriyle tutarlı: dindarlaşma polis okulunda başlıyor, içe kapanma Ankara döneminde artıyor ve aile kendini Gülen hareketinden uzak tanımlıyor. Aile beyanları, gözaltı koşullarında ve kendini koruma motivasyonuyla verilmiş olabilir; bu nedenle tek başına belirleyici değildir.

## Modellerle eşleştirme

| Gösterge [RAD-A§7] | Bu vakada | Kart | Güç |
|---|---|---|---|
| 1. Ana akım dini otoriteden kopuş, alternatif kutsal otorite | Gülen çevresi (iddia) → Sosyal Doku/Yıldız → İsmailağa çevresi → Selefi yazar ve vaizler (iddia) | [RD13], [RD22], [RD37] | Orta |
| 2. Kapalı halkalara yoğunlaşma | Ortak evler, sohbet halkaları, WhatsApp grubu | [RD11], [RD16], [RD41] | Güçlü |
| 3. Çatışma bölgesine gitme isteği, bağış | İki tanık; İHH havaleleri | [RD33], [RD34], [RD35] | Güçlü / orta |
| 4. Şehitlik ve önem dili | "Şahadet istiyorum"; "aktif görev" | [RD41], [RD26] | Orta |
| 5. Cihatçı içerik ve kitap | Valiz, El Kaide videosu, arama geçmişi | [RD27], [RD38], [RD39] | Güçlü |
| 6. Niyet sızıntısı ve veda | Helallik telefonu; kitap valizi | [RD02], [RD27] | Güçlü |
| 7. Meslekten ayrılma isteği, operasyonel hazırlık | "Aktif görev"; keşif; otel; rapor | [RD26], [RD07], [RD45], [KR-073] | Güçlü |

- **[D] Wiktorowicz (bilişsel açılma) — güçlü uyum, muhtemel.** Dindarlaşma aileden kopuş ve yeni kurumsal kimlik döneminde (polis okulu) başlıyor [RD03], [RD04]; ardından ardışık dini grup arayışı geliyor [RD13], [RD22]. "Gülen sohbetlerine **de** gitmiştim" ifadesi çoklu arayışla uyumlu [RD22].
- **[D] McCauley ve Moskalenko — görüşte güçlü, eylemde sıçrama; olası.** Grup mağduriyeti (Halep) ve şehitlik dili belirgin [RD55], [RD41]; eylem piramidinde bağıştan doğrudan suikasta geçiş var ve ara basamaklar görünmüyor [RD35]. Bu sıçrama ya çok hızlı bir kişisel tırmanışa ya da bir dış tetikleyiciye işaret edebilir; eldeki kanıt ikisini ayırt etmiyor.
- **[D] Kruglanski (önem arayışı) — orta uyum, olası.** "Yalnız", "içine kapanık" betimlemeleri, "aktif göreve" geçme isteği ve şehitlik dili; anlatı (Kutub, Awlaki, neşid) ve ağ (sohbet halkaları) bileşenleri mevcut [RD24], [RD26], [RD27], [RD39].
- **[D] Sageman (akran ağı) — kısmi uyum, olası.** Okul arkadaşıyla birlikte grup değiştirme ve ortak evler [RD16], [RD19]; ancak saldırıyı birlikte planlayan bir arkadaş grubunun bağımsız kanıtı yok.
- **[D] Della Porta — sınırlı uyum.** 17–25 Aralık ve 15 Temmuz sonrası tasfiyeler bir bağlam sağlıyor; ideolojik kapsülleşmeye dair kanıt zayıf.
- **[D] Yalnız aktör eleştirisi — en tutarlı çerçeve, muhtemel.** Hangi anlatı doğru olursa olsun fail sosyal olarak yalnız değildi: radikal çevrelerle bağları, sızdırılmış niyetleri ve gözlemlenebilir hazırlıkları vardı [RAD-A§5].

**[D] Genel değerlendirme.** Selefi-cihatçı yönde bilişsel radikalleşme kanıtı güçlü ve çok kaynaklıdır. Gülen yapısına örgütsel bağlılık ve talimat zinciri ise kesinleşmiş mahkeme kararında yer alıyor, ancak kamuya açık doğrudan delili (talimat metni, iletişim içeriği) sınırlıdır ve büyük ölçüde geri alınmış ya da işkence iddiasıyla itiraz edilmiş ifadelere dayanıyor. Davranışsal sıçramanın kaynağı, yani kararın failin kendisine mi yoksa bir dış yönlendirmeye mi ait olduğu, açık kaynaklarla belirlenemiyor.

# Bağlam ve "neden şimdi?"

**[O]** Bu bölüm yalnızca kartlı bilgiyle sınırlıdır. Bazı yaygın bağlam iddiaları (ör. MİT'in 2015'te emniyete gönderdiği bir cihatçı tehdit uyarısı) bu çalışmanın girdi dosyalarında kartlı değildir ve bu yüzden olgu olarak kullanılmamıştır; bkz. Bölüm 10, soru 14.

## Dört sürecin kesişimi

1. **Türkiye–Rusya normalleşmesi.** **[O]** Normalleşme, Erdoğan'ın 27 Haziran 2016'da Putin'e gönderdiği mektupla başladı [K18]. **[O]** Erdoğan Ekim 2016'da Putin'le Fetih eş-Şam'ın Halep'ten çıkarılması konusunda anlaştıklarını söyledi [K16]. **[O]** Bir düşünce kuruluşu analizine göre Ankara "yakın zamana kadar" Nusra ve Ahrar eş-Şam gibi grupları Rusya'nın hedef listesinden çıkarmaya çalışıyordu (B3) [K17].
2. **Halep tahliyesi.** **[O]** Doğu Halep tahliyesi 15 Aralık'ta başladı, 22 Aralık'ta tamamlandı ve yaklaşık 35.000 kişiyi kapsadı; suikast tahliyenin ortasında gerçekleşti [K14].
3. **Türkiye'de Rusya karşıtı seferberlik.** **[O]** 13 Aralık'ta aralarında hükümete yakın gençlik örgütlerinin de bulunduğu STK'lar Ankara'da Rus Büyükelçiliği önünde protesto yaptı [K41]; 17 Aralık'ta İHH konvoyu sınırda "Rusya Suriye'den defol" protestosuna dönüştü [K15]. **[O]** Bir düşünce kuruluşu uzmanına göre Nusra ile doğrudan bağlantıya dair "az kanıt" var, ancak saldırı Ankara'nın Moskova'ya yanaşmasından rahatsız Sünni kamuoyu duyarlılığını yansıtıyor (B3) [K19]. **[D]** Ankara aynı hafta Moskova'yla tahliyeyi müzakere ederken kendi tabanına yakın sivil toplum Rusya'yı protesto ediyordu; bu çelişkili ortam, devlet aygıtındaki genç bir polisin devlet politikasına karşı radikalleşebileceği bir zemin sağlıyordu (olası).
4. **Moskova üçlü toplantısı.** **[O]** 20 Aralık'ta Türkiye, Rusya ve İran dışişleri bakanları Moskova'da toplandı; bildiri silahlı muhalefetin Doğu Halep'ten düzenli çıkışını memnuniyetle karşıladı ve DEAŞ ile Nusra'ya karşı ortak mücadeleyi teyit etti [K13], [R27], [KR-077]. **[O]** Türk Dışişleri Bakanı olay günü Rusya'daydı [KR-040].

## Güvenlik aygıtı: 15 Temmuz sonrası

- **[O]** 15 Temmuz 2016'dan sonra güvenlik önceliğinin FETÖ'ye de kaydığı akademik literatürde izlenebiliyor [RAD-A§6]. **[O]** Bir kaynağa göre OHAL kararnameleriyle 10.000'den fazla polis ihraç edildi ve fail bunlar arasında değildi [K32], [RD49].
- **[O]** Fail 16–17 Temmuz 2016'da izin kullandı; izni sonradan FETÖ'den tutuklanan bir şube müdürü verdi [RD51]; abla bu tarihlerde bir düğün için İzmir'de olduklarını söylüyor [RD51]. **[D]** İzin olgusu tutarlı; anlamı iki anlatıda zıt yönde yorumlanıyor.
- **[O]** Fail olay günü rapor alarak işe gitmemişti [KR-073]; SK Başkanı, rapor alma, otel rezervasyonu ve kimlikle aramasız giriş dahil hazırlık koşullarının belirlendiğini söyledi [R41].
- **[O]** Bir sanık ifadesine göre uçak krizinden sonra bir "cemaat abisi" bir eski MİT mensubuna Rus elçiliğinin güvenliğini sordu ve büyükelçinin koruma kullanmadığı bilgisi iletildi (iddianame, C3) [K25]. **[O]** Karlov'un eşi en az dört ay önce tehditler olduğunu ve kimsenin tepki vermediğini söyledi [R57]. **[O]** Kremlin, diplomatların güvenliğinden ev sahibi ülkenin sorumlu olduğunu ve olayın Ankara'nın prestijine darbe olduğunu vurguladı [R19].
- **[O]** Bir CHP milletvekili 27 Aralık 2016'da failin FETÖ mensubuysa neden 15 Temmuz sonrasında açığa alınmadığını ve Nusra sloganıyla neyin örtüldüğünü sordu [K37].

## Neden şimdi?

**[D]** Zamanlama hipotezler arasında ayrım yapmıyor: öfkeyle motive olmuş bir fail için tahliye haftası duygusal tepe noktası olabilir; normalleşmeyi hedefleyen örgütlü bir fail için Moskova toplantısının arifesi anlamlı olabilir [K13], [K14]. **[D]** Ayırt edici unsurlar zamanlamadan çok hazırlık takvimindedir: rezervasyon 14 Aralık'ta yapıldı [KR-004], sergi açılışı ertelenince rezervasyon değiştirildi [KR-006], fail 16 Aralık'ta sergide görüldü [KR-007]. Bu, tarihin büyük olasılıkla bir fırsata (sergi açılışı) göre seçildiğini gösteriyor. **[O]** İçişleri Bakanı'nın açıklamalarına göre fail olay günü izinliydi ve metal dedektörü öttüğü halde polis kimliğiyle içeri alındı [K02]. **[D]** İddianamedeki Haziran 2016 iftarı planı doğruysa [KR-002], Aralık tarihi motivasyonla değil fırsatla belirlenmiştir; ancak plan Ocak 2016'ya, yani normalleşme öncesine tarihleniyor ve bu, "ilişkileri bozma" amacıyla zaman uyumsuzluğu yaratıyor [K24], [K18]. Mahkeme amacı sonradan "örgütteki çözülmeyi engelleme ve darbe girişimine zemin hazırlama" olarak genişletti [K27], [K31].


# Hipotezler ve rakip hipotezler analizi (ACH)

## Ön kayıtlı hipotezler

**[O]** Ana hipotezler kanıt toplamaya başlamadan önce, 26 Ekim 2026 09:47 CET'te kaydedildi; H3a, H3b ve H5a rafinasyonları 09:58 CET'te "sonradan eklendi" işaretiyle eklendi [hipotezler.json].

| Kod | Tanım (özet) | Kayıt |
|---|---|---|
| H1 | Resmî tez: saldırı FETÖ yapılanmasınca planlandı/yönlendirildi; fail örgüt talimatıyla hareket etti; amaç Türkiye–Rusya ilişkilerini bozmak | Ön kayıt |
| H2 | Halep nedeniyle bireysel olarak radikalleşmiş, örgütsel talimat olmadan tek başına hareket eden fail | Ön kayıt |
| H3a | Cihatçı ortamdan esinlenme (örgütsel emir yok): Türkiye'deki İslamcı-cihatçı sosyal çevrede (sohbet halkaları, STK protestoları, Nusra söylemi) radikalleşme; Suriye'deki bir grup tarafından yönlendirilmedi | Rafinasyon (H3'ten) |
| H3b | Nusra/JFŞ/Ceyş el-Fetih ya da Türkiye'deki bir uzantısı eylemi planladı ya da emretti | Rafinasyon (H3'ten) |
| H4 | Türkiye–Rusya yakınlaşmasını raydan çıkarmak isteyen üçüncü bir devlet ya da istihbarat servisinin provokasyonu | Ön kayıt |
| H5a | Özgül kombinasyon: 2013 öncesi Gülen çevresiyle teması olan, 2014 sonrası Sosyal Doku/İslamcı çevrede dönüşen, Halep tahliyesiyle tetiklenen ve en az bir yardımcısı olan fail; yardımcının/yönlendiricinin kimliği belirlenemiyor | Rafinasyon (H5'ten) |

**[D]** Hipotezler birbirini dışlamaz: H5a, H3a'nın radikalleşme anlatısını içerir ve ona iki ek bileşen (erken Gülen teması, yardımcı) ekler. H1 ile H3a ise "örgütsel emir" konusunda doğrudan rakiptir. Resmî tez (H1) bu bölümde en az iki rakiple (H3a ve H5a; ayrıca H2) aynı ölçütle sınanır; hiçbir hipotez varsayılan kabul edilmez.

## Kanıt–hipotez matrisi

**[O]** Yöntem: her kanıt her hipotez için T (tutarlı), Ç (çelişir) ya da N (nötr) olarak işaretlendi; ağırlık = kaynak derecesi (A 1 · B 0,8 · C 0,6 · D 0,4) × bilgi derecesi (1 → 1 · 2 → 0,85 · 3 → 0,65 · 4 → 0,4 · 5 → 0,2); hipotezler ağırlıklı tutarsızlığa göre sıralanır (düşük = daha az çürütülmüş) [ACH]. Kanıt birden fazla karta dayanıyorsa birincil kartın derecesi kullanıldı.

<div class="tbl-ach">

| # | Kanıt | Kart(lar) | Derece (ağırlık) | H1 | H2 | H3a | H3b | H4 | H5a |
|---|---|---|---|---|---|---|---|---|---|
| E01 | Olay anında Arapça biat dizesi ve "Halep'i unutmayın" | RD55, K01, KR-024 | A1 (1) | Ç | T | T | T | N | T |
| E02 | Bir gün önce bırakılan valiz: Kutub, Benna, Yıldız, Şen kitapları; "özel harekat netleşmedi" | RD27 | B2 (0,68) | Ç | T | T | N | N | T |
| E03 | El Kaide videosu Şubat 2016'da indirildi, 18.12.2016'da silindi | RD38 | B2 (0,68) | Ç | T | T | T | N | T |
| E04 | Arama geçmişi: Bayancuk, Awlaki, Kouachi, Bhutto (Ağu–Ara 2016) | RD39 | C2 (0,51) | Ç | T | T | N | N | T |
| E05 | Suriye'ye gitme ve işi bırakma isteği (iki tanık) | RD33, RD34 | B2 (0,68) | Ç | T | T | N | N | T |
| E06 | Sosyal Doku / Nurettin Yıldız sohbetlerine 2014–2016 katılım | RD11, RD13, K27 | B2 (0,68) | N | Ç | T | N | N | T |
| E07 | İHH hesaplarına 11 havale (Oca 2015–Tem 2016) | RD35 | C2 (0,51) | N | N | T | N | N | T |
| E08 | "Şahadet istiyorum" (Kasım sonu) ve "El-Kaide tehlikeli" (1 hafta önce) | RD41 | C3 (0,39) | N | T | T | Ç | N | T |
| E09 | Gmail/Facebook yazışmaları fail öldükten sonra (≈2,5 saat) VPN üzerinden silindi | K20, KR-099, KR-100 | C3 (0,39) | T | Ç | N | T | T | T |
| E10 | Söğüt teması: hatsız telefon, Wi-Fi iletişimi, 9 Aralık 256 m baz yakınlığı | K22, RD44 | C3 (0,39) | T | Ç | Ç | N | N | T |
| E11 | Etkin pişmanlık beyanı: Altıntaş "kendi zümresi içinde" | RD23, K23 | C3 (0,39) | T | Ç | Ç | N | N | T |
| E12 | Polis okulunda (2012–2013) Gülen sohbetlerine katılım tanıklığı; bir ifade geri alındı | RD18–RD22, K30 | C3 (0,39) | T | N | N | N | N | T |
| E13 | Failin ByLock kullanmadığı belirlendi | RD46 | B2 (0,68) | Ç | T | T | N | N | N |
| E14 | Sık görüştüğü 8 kişi ByLock kullanıcısı | RD50 | C3 (0,39) | T | N | N | N | N | N |
| E15 | Rus heyeti silinmiş dosyalarda 690 "Hizmet", 2 "Fetullah Gülen"; silinenlerde El Kaide/Nusra/DEAŞ adlı dosya yok | RD40, K21 | C3 (0,39) | T | N | N | N | N | T |
| E16 | "Garson" listesi: 2014 "EA", 2015 "bağı zayıfladı"; EA'nın anlamı çelişkili | RD47, RD48 | D4 (0,16) | T | N | N | N | N | T |
| E17 | Üstlenme bildirisi sahte; Ceyş el-Fetih/JFŞ inkâr etti | K34, R49, KR-080, KR-081 | C2 (0,51) | N | T | N | Ç | T | N |
| E18 | JFŞ eylemi sahiplenmeden "doğal tepki" diye meşrulaştırdı | K35 | C3 (0,39) | N | T | T | Ç | N | N |
| E19 | Kremlin 21.12.2016'da FETÖ atfını onaylamadı ("acele etmeyin") | R18, K10, R46 | B1 (0,8) | Ç | N | N | N | N | N |
| E20 | İddianame: plan Ocak 2016, Haziran 2016 iftarında ilk girişim | K24 | C4 (0,24) | T | Ç | Ç | Ç | T | N |
| E21 | Plan tarihi (Oca 2016) normalleşmeden (Haz 2016) önce: "ilişkileri bozma" amacıyla zaman uyumsuzluğu | K18 × K24 | C4 (0,24) | Ç | N | N | N | N | N |
| E22 | Saldırıdan önceki hafta Rus temsilcilikleri önünde ve sınırda "Katil Rusya" protestoları | K41, K15 | C2 (0,51) | N | T | T | N | N | T |
| | **Ağırlıklı tutarsızlık (Σ Ç)** | | | **5,27** | **2,09** | **1,02** | **1,53** | **0,00** | **0,00** |
| | Ağırlıklı tutarlılık (Σ T) | | | 2,74 | 6,03 | 6,71 | 2,07 | 1,14 | 7,75 |
| | Çelişki sayısı | | | 8 | 5 | 3 | 4 | 0 | 0 |

</div>

**[D]** Matrisin okunması için üç uyarı:

1. **[D] Mekanik sıralama** H4 = H5a (0,00) < H3a (1,02) < H3b (1,53) < H2 (2,09) < H1 (5,27) biçimindedir. Heuer yönteminin bilinen kusuru nedeniyle hakkında neredeyse hiç kanıt bulunmayan H4 ve her veriyi emebilen bileşik H5a sıfır puan alıyor; bu iki puan açıklama gücünü değil, belirsizliği yansıtıyor.
2. **[D] Seçim yanlılığı riski:** Araştırma paketi radikalleşmeye odaklandığı için cihatçı yöndeki kanıtların sayısı arttı; H1 lehine kanıtların büyük kısmı ise iddianame aktarımıdır ve C3–C4 dereceli olduğu için düşük ağırlık alıyor. Bu, H1'in matriste olduğundan zayıf görünmesine yol açabilir.
3. **[D] Yorum bağımlılığı:** E01–E05'teki "Ç" işaretleri H1 için koşulludur. Resmî tezin "renklendirme" ve "hedef şaşırtma" varsayımı kabul edilirse bu kanıtlar H1 için nötre döner [K26], [RD43]. Ancak bu varsayım, Şubat 2016'daki video indirmesinin ve on aylık aramaların da planın parçası olduğunu kabul etmeyi gerektirir ve sınanamaz bir yapı üretir (çürütülemezlik riski).

## Güncel değerlendirme

**H3a — İslamcı-cihatçı ortamda radikalleşme, örgütsel emir yok: muhtemel (≈%55–70).**

- **[D] Lehine:** Olay anındaki sözler [RD55]; valiz kitapları [RD27]; El Kaide videosu ve arama geçmişi [RD38], [RD39]; iki tanıkla Suriye isteği [RD33], [RD34]; resmî ve bağımsız kaynakların birlikte teyit ettiği sohbet halkası katılımı [RD11], [RD43]; İHH bağışları [RD35]; failin kendisinin ByLock kullanmaması [RD46]; cihatçı grupların eylemi sahiplenmeden "doğal tepki" diye meşrulaştırması [K35]; tahliye haftasındaki Rusya karşıtı seferberlik [K15], [K41].
- **[D] Aleyhine:** Gmail/Facebook yazışmalarının fail öldükten sonra silinmesi [KR-099], [KR-100] bir yardımcıya işaret ediyor; yardımcı bir akran olabilir (H3a ile uyumlu), ama bir yönlendirici de olabilir (H1, H5a). İddianamedeki Söğüt teması (hatsız telefon, baz yakınlığı) doğruysa H3a ile çelişir [K22], [RD44]. Kesinleşmiş mahkeme kararı H3a'nın aksini hükme bağladı [KR-119].

**H5a — özgül kombinasyon: olası (≈%35–50).**

- **[D] Lehine:** Her bileşen için en az bir kart var: erken Gülen teması [RD18]–[RD22], dönüşüm [RD03], [RD04], [RD11], Halep tetikleyicisi [RD55], [K14], yardımcı izi [KR-099]. Mekanik tutarsızlığı sıfırdır.
- **[D] Aleyhine:** H5a bir bileşik hipotezdir; olasılığı en zayıf bileşeninden yüksek olamaz. "Erken Gülen teması" bileşeni geri alınmış ya da baskı altında verildiği iddia edilen ifadelere [RD18], [RD23], "yardımcı" bileşeni ise savcılık kaynaklı tek bir haber zincirine [KR-099], [KR-100] dayanıyor. Bileşik olasılık cezası nedeniyle ikinci sıraya indi.

**H1 — FETÖ organizasyonu (resmî tez): düşük olasılık–olası sınırında (≈%20–35).**

- **[D] Lehine:** Kesinleşmiş mahkeme kararı ve Yargıtay onaması [KR-114], [KR-119]; Söğüt'ün 9 Aralık talimatı ve baz yakınlığı iddiası [RD44], [K22]; etkin pişmanlık beyanı [RD23]; sık görüştüğü 8 kişinin ByLock kullanıcısı olması [RD50]; silinmiş dosyalardaki 690 "Hizmet" adlı dosya [RD40]; polis okulu dönemindeki temas tanıklıkları [RD19], [RD20]; ölüm sonrası profesyonel iz silme [KR-100].
- **[D] Aleyhine:** Siyasi atıf delilden önce geldi [K05], [K08], [GDELT-ek]; ilk resmî metin örgüt adı vermedi [K12]; failin kendisi ByLock kullanmadı [RD46]; iletişim içerikleri kamuya ve duruşmaya açıklanmadı [K30]; tanık ifadelerinin bir kısmı geri alındı ya da işkence iddiasıyla reddedildi [RD18], [RD44]; "Garson" kodu iki hükümete yakın kaynakta zıt anlamlıdır [RD47], [RD48]; Ocak 2016 plan tarihi normalleşmeden önceye düşüyor [K24], [K18]; amacın tanımı 2016–2021 arasında üç kez değişti [K24], [K27], [K31]; Rusya tezi on yıl boyunca açıkça benimsemedi [R18], [R42].
- **[D]** Aralığın bu düzeyde kalmasının nedeni negatif kanıtlardır (failin ByLock kullanmaması, "Garson" kod çelişkisi, tanık ifadelerinin geri alınması). Kararın varlığı bu hipotezi "çok düşük" seviyesine indirmeyi engelliyor.

**H3b — cihatçı ağ yönlendirmesi: olası değil (≈%5–15).**

- **[D]** Gerçek bir üstlenme yok; sahte bildiri hızla çöktü ve gruplar inkâr etti [K34], [R49], [KR-081]. **[D]** Buna karşılık savcılığın kendisi failin iki ay boyunca Nusra iltisaklı kişilerle "günlük görüşme" yaptığını kabul ediyor [RD42]; rejim kontrolünde olmayan bir kaynağa göre fail Ekim 2016'da bir Selefi yazarla görüştü [RD37]. Bu, Türkiye'deki bir uzantının yönlendirmesi ihtimalini biraz artırıyor; ancak temasın içeriği bilinmiyor ve kaynakların bir kısmında çıkar çatışması var.

**H2 — saf yalnız aktör: olası değil (≈%5–10).**

- **[D]** Fail sosyal olarak yalnız değildi [RD11], [RD16]; ölüm sonrası silme bir başkasının varlığını gösteriyor [KR-099]. Literatür de "yalnız kurt" tipolojisinin terk edilmesini öneriyor [RAD-A§5]. **[D]** "Eylemde yalnız" okuması H3a içinde yaşamaya devam ediyor.

**H4 — üçüncü devlet provokasyonu: çok düşük (<%5).**

- **[D]** Hiçbir devlet, Rusya dahil, somut bir üçüncü devlet adı vermedi; Klintseviç'in NATO iması kendi ifadesiyle "kanıtlaması zor" bir iddiadır [R09]; ABD iddiayı reddetti [K09]. Sahte üstlenme bildirisinin üç ülke medyası üzerinden yayılması bir dezenformasyon katmanına işaret ediyor, ama kaynağı bilinmiyor [KR-080], [K34]. Provokasyon amaçlandıysa başarısız oldu: toplantı ertesi gün yapıldı [R27].

## Sıralamayı ne değiştirir?

| Ortaya çıkacak belge ya da bulgu | Etkisi |
|---|---|
| Söğüt–Altıntaş yazışmalarının içeriği bağımsız denetime açılır ve açık talimat içerirse | H1 belirgin biçimde güçlenir; H3a zayıflar |
| Aynı içerik dini ya da Suriye odaklı bir dil taşırsa | H3a/H5a güçlenir |
| Gmail silme işleminin cihaz/IP kaydı bir akran çevresine işaret ederse | H3a güçlenir; bir örgüt hiyerarşisine işaret ederse H1 ya da H3b güçlenir |
| Rusya SK dosyasının bir bölümü açıklanırsa | İki yönde de belirleyici olabilir [R41] |
| Silinmiş 690 "Hizmet" dosyasının içeriği açıklanırsa | Örgütsel içerikse H1/H5a, genel içerikse etkisiz |
| Nusra iltisaklı kişilerle "günlük görüşmelerin" içeriği açıklanırsa | H3b yeniden değerlendirilir [RD42] |

## Şeytanın avukatı

- **[D] H3a'ya karşı en güçlü itiraz:** Cihatçı yöndeki ayrıntılı kanıtların önemli bir kısmı, vakada kişisel çıkar çatışması bulunan bir yazarın yayınından geliyor [RD34], [RD35], [RD39], [KR-124]. **[D] Yanıt:** Çekirdek olgular (Yıldız sohbetleri, Suriye isteği, valiz kitapları, El Kaide videosu) devlet ajansı ya da iddianame aktarımlarında da var [RD11], [RD27], [RD33], [RD38]; ayrıntılar ise ihtiyatla kullanılmalı.
- **[D] H1 lehine en güçlü dava:** Türk ve Rus soruşturmacılar birlikte çalıştı [R16], [R22]; Rus heyetinin silinmiş dosyalarda Gülen hareketine ait sözcüklerle adlandırılmış dosyalar bulması, baz kaydı, etkin pişmanlık beyanı ve Yargıtay onaması görünüşte bağımsız dört kanaldır [RD40], [K22], [RD23], [KR-119]. Sloganlar taklit edilmesi kolay bir yanıltma aracıdır.
- **[D] H1 aleyhine en güçlü dava:** Atıf olay gecesi delilsiz yapıldı ve iki gün içinde Cumhurbaşkanlığı düzeyinde sabitlendi [K05], [K08]; medyada çerçevenin temel unsurları ilk yedi saatte kuruldu [GDELT-ek]; Rusya "Rusya da biliyor" iddiasını ertesi gün desteklemedi [R18]; mahkemede bile iletişim içerikleri açıklanmadı [K30]; iddianame cihatçı izleri baştan "kurgu" sayan bir yorumlama kuralı içeriyor [K26] ve saldırı görüntülerinin TRT'de yayımlanmasını bile "habercilikle açıklanamaz" bularak saldırıyla ilişkilendiriyor [K42], [KR-016]; bir Türk düşünce kuruluşu uzmanının "önceden tasarlanmış senaryo gereği El Kaide bağlantılı gruplarla temasa sokuldu" iddiası da kanıt sunmuyor (C5) [K40].
- **[D] H5a'ya karşı:** "Biraz Gülen, biraz cihatçı, biraz yardımcı" formülü her veriyi emebilir; bu esneklik açıklama gücü değil belirsizlik olabilir [ACH].
- **[D] H4 lehine:** Toplantı arifesindeki zamanlama, sahte bildirinin uluslararası yayılması ve VPN ile iz silme bir istihbarat imzası olarak okunabilir [K13], [KR-080], [KR-100]. **[D] H4 aleyhine:** Pozitif tek bir kanıt yok.

# Kim kazandı? Anlatıların işlevi

**[D]** Bir aktörün bir olaydan ya da anlatıdan kazançlı çıkması, olayı onun planladığı ya da anlatının yanlış olduğu anlamına gelmez. Bu bölüm yalnızca sonuçları ve işlevleri değerlendirir ve her anlatıya aynı soruyu sorar: bu anlatı kime ne kazandırdı?

## Resmî anlatının (H1) işlevleri

| İşlev | Gösterge | Kart | Değerlendirme |
|---|---|---|---|
| Rusya ile ilişkiyi koruma | "İki ülke de tuzağa düşmeyecek"; ortak düşman olarak FETÖ'nün sunulması | [KR-053], [KR-078], [R32] | Muhtemel |
| Güvenlik zafiyetinin çerçevelenmesi | Bir polisin büyükelçiyi öldürmesi, "sızmış hücre" anlatısıyla düşmanın sinsiliğine dönüşüyor; Kremlin ise sorumluluğu ev sahibine hatırlattı | [R19], [R20], [RD56] | Olası |
| Gülen hareketine karşı iç ve dış mücadele | Yakalama kararı, kırmızı bülten, 2026 Kanada açıklaması, gazeteciye suç duyurusu | [KR-104], [KR-121], [KR-124] | Muhtemel |
| Hükümete yakın İslamcı çevrenin soruşturma dışında kalması | Sosyal Doku/İHH hattı "renklendirme" olarak kapatıldı; rejim kontrolünde olmayan bir kaynağa göre savcı İHH hattını soruşturmadı | [RD43], [K33] | Olası |
| Türkiye'nin Suriye politikasının sorgulanmasının önlenmesi | Hükümete yakın medyada cihatçı çerçeve 3, FETÖ 44 URL; cihatçı çerçeveyi kullanan yayınların hedef alınması | [GDELT-istatistik], [K36] | Olası |

## Karşı-anlatının (H3a/H5a ağırlıklı) işlevleri

| İşlev | Gösterge | Kart | Değerlendirme |
|---|---|---|---|
| Gülen hareketinin bir diplomat cinayetinin sorumluluğundan aklanması | Rejim kontrolünde olmayan kaynakların cihatçı radikalleşme ayrıntılarını öne çıkarması | [RD34], [RD35], [RD39], [KR-092] | Muhtemel |
| İade ve kırmızı bülten taleplerinin uluslararası düzeyde zayıflatılması | Yazarın kendisinin 2026'da MİT suç duyurusunun hedefi olması | [KR-124], [KR-125] | Olası |
| Türk hükümetinin Suriye politikasının ve hükümete yakın İslamcı çevrenin eleştirisi | "Erdoğan yanlısı vaiz" vurgusu; Rusya'nın kendi failini bulduğu iddiası | [KR-092], [KR-126] | Olası |

## Diğer aktörler

| Aktör | Kazanç / kayıp | Kart | Değerlendirme |
|---|---|---|---|
| Moskova | Ankara karşısında ahlaki kaldıraç; güvenlik güvencesi talebi; dosyayı "azmettirenler" sorusuyla açık tutma esnekliği | [R04], [R19], [R42] | Olası |
| Rus devlet medyası | Halep motivasyonunun geri planda tutulması, Rusya'nın Suriye politikasının saldırıya gerekçe olarak tartışılmasını önledi | [R45], [R43] | Olası |
| Cihatçı gruplar | Eylemi sahiplenmeden "doğal tepki" olarak meşrulaştırma ve propaganda değeri | [K35] | Olası |
| Türkiye–Rusya–İran ekseni | Moskova Bildirgesi ve Astana süreci kesintisiz sürdü | [R27], [R28] | Muhtemel |
| ABD | Belirgin bir kazanç yok; müdahale imalarını reddetti | [K09], [R61] | Olası |

**[D]** Simetrik sonuç: Bu dosyada tarafsız bir anlatıcı yok. Resmî anlatının devlet için işlevsel olduğu ve karşı-anlatının hükümetten bağımsız yayınlar ve onların çevresi için işlevsel olduğu muhtemeldir. İşlevsellik, ne resmî tezin ne de karşı-anlatının yanlış olduğunu gösterir; her iki tarafın iddiası da teyit durumuna göre ayrı ayrı derecelendirilmelidir. Bu dosyada hiçbir tarafın yorumuna muhtaç olmayan veriler failin kendi sözleri [RD55] ve gözlemlenebilir hazırlıklarıdır [KR-004], [KR-007], [RD27].

# Açık sorular

Her soru **[S]** türündedir. Son sütun, sorunun hangi belgeyle kapanabileceğini gösterir.

| # | Soru | Kapanabileceği belge | Kart |
|---|---|---|---|
| 1 | Gmail ve Facebook yazışmalarını fail öldükten sonra kim, hangi cihaz ve IP'den sildi? | Google'ın savcılığa verdiği döküm; bilirkişi raporu | [KR-099], [KR-100] |
| 2 | Söğüt–Altıntaş iletişiminin içeriği nedir; açık bir talimat içeriyor mu? | İddianame ekleri; HTS ve Wi-Fi iletişim raporları; gerekçeli karar | [K22], [RD44] |
| 3 | Sık görüşülen 8 ByLock kullanıcısıyla yazışmaların içeriği nedir? | ByLock içerik raporları (duruşmada açıklanmadı) | [RD50], [K30] |
| 4 | Silinmiş 690 "Hizmet" adlı dosyanın içeriği nedir? | Rus heyeti ve Türk bilirkişi raporları | [RD40] |
| 5 | Telefonun 16 haneli ikinci şifresi hiç çözüldü mü? | Bilirkişi raporu; Apple ve yabancı firma yazışmaları | [KR-105], [KR-102] |
| 6 | 19 Aralık gecesi Türk medyasının "Rus ajansı"/"Rusya devlet televizyonu" diye atıf yaptığı FETÖ iddiasının kaynağı kimdir? | İlgili Türk haberlerinin metinleri; Rus yayın akışı arşivleri | [GDELT-ek] |
| 7 | Fail 15 Temmuz sonrasında açığa alındı mı; göreve iadesinin gerekçesi nedir? | EGM yazısı; personel dosyası; CHP soru önergesinin yanıtı | [KR-003], [RD49], [K37] |
| 8 | Fail neden canlı yakalanamadı; çatışmanın kesin süresi ve öldürülme saati nedir? | Olay yeri ve operasyon tutanakları; Adli Tıp raporu | [KR-027], [KR-028], [KR-035], [K39] |
| 9 | Nusra iltisaklı kişilerle iki aylık "günlük görüşmeler" kimlerle ve ne içerikle yapıldı; bu kişiler neden kovuşturulmadı? | İddianame ekleri; ilgili tanık ifadeleri | [RD42], [RD37] |
| 10 | İHH havaleleri ve dernek bağışları neden soruşturma konusu yapılmadı? | MASAK raporları; savcılık takipsizlik kararları | [RD35], [RD36], [K33] |
| 11 | Rusya Soruşturma Komitesi'nin kendi dosyası neyi içeriyor; "başka sorular" nelerdir? | SK açıklamaları; Rus–Türk adli yardım yazışmaları | [R41], [R39], [KR-126] |
| 12 | İddianamedeki "FETÖ ve arkasındaki istihbarat örgütleri" ifadesi kimi kastediyor? | İddianame tam metni | [K24] |
| 13 | Büyükelçiye yönelik önceki tehditler kayıtlı mıydı; neden koruma artırılmadı? | Emniyet ve Dışişleri yazışmaları; Viyana Sözleşmesi kapsamındaki koruma kayıtları | [R57], [K25], [R19] |
| 14 | MİT'in 2015'te emniyete cihatçı tehdide ilişkin bir uyarı gönderdiği iddiası doğru mu ve failin çevresini kapsıyor muydu? | MİT/EGM yazışmaları (bu çalışmada kartı yok) | — |
| 15 | MİT'in 2026 suç duyurusunun dayandığı delil türü nedir; 2016'daki "ev" iddiası soruşturmada neden çürütüldü? | Suç duyurusu metni; 2016–2018 soruşturma kayıtları | [KR-124], [RD53], [RD54], [GDELT-ek] |
| 16 | Samanyolu dizisi haber dalgasının ilk kaynağı hangi ajanstır ve iddianamedeki delil statüsü nasıl değerlendirildi? | Ajans arşivleri; gerekçeli karar | [GDELT-istatistik], [KR-001], [KR-108] |
| 17 | Sahte üstlenme bildirisini ilk kim üretti ve yaydı? | Mısır ve Irak yayınlarının kaynak zinciri; SITE arşivi | [KR-080], [K34] |
| 18 | Firari sanıklar (Karaata dahil) yargılanacak mı; Kanada ile iade süreci var mı? | Ayrılan dosyanın durumu; Kanada yetkililerinin açıklamaları | [KR-114], [KR-121], [KR-123] |

# Kaynak eleştirisi ve veri boşlukları

1. **[O] Birincil belgelerin yokluğu.** İddianame, gerekçeli karar, Yargıtay kararı, MASAK raporları, EGM yazıları ve bilirkişi raporlarının hiçbiri bu çalışmada birincil metin olarak açılmadı; hepsine AA, Hürriyet, Odatv, TR724, Nordic Monitor ve benzeri yayınların aktarımları üzerinden ulaşıldı [RAD-B], [KR-106]. **[D]** Bu, hem H1 lehine hem H3a lehine kanıtların aynı katmanda, yani basın aktarımı katmanında kalmasına yol açıyor; aktaran yayının seçiciliği belirleyici hale geliyor.
2. **[O] Kaynak sınıfı dengesi.** H1 lehine iddianame ve karar içerikleri ağırlıkla devlet ajansı ve hükümete yakın yayınlardan geliyor [K22], [K27], [RD43]; H3a lehine ayrıntıların önemli bir kısmı rejim kontrolünde olmayan kaynaklardan geliyor [RD34], [RD35], [RD39]. **[D]** Bu asimetri simetriktir: iki yönde de kaynak kirliliği riski var ve bu raporda iki yöndeki kanıtlar aynı Admiralty ölçütüyle derecelendirildi.
3. **[O] Çıkar çatışması.** Nordic Monitor'un kurucusu Abdullah Bozkurt 2026'da MİT suç duyurusunun hedefidir; aynı yazar dosyanın cihatçı ayrıntılarının önemli bir kaynağıdır [KR-124], [RD36], [RD53], [RD54]. **[O]** Suç duyurusuna ilişkin bir aktarım, duyurunun esas olarak "iftira" ve "devlet kurumlarını aşağılama" suçlarına dayandığını, Bozkurt'un 2018 iddianamesinde ve 2021 kararında sanık olmadığını belirtiyor [KR-124], [KR-125]. **[D]** Bu durum yazarın verdiği belge görüntülerini geçersiz kılmaz; ancak belge görüntüsü olmayan iddialarına (ör. [RD36]) daha düşük ağırlık verilmesini gerektirir.
4. **[O] Rejim kontrolünde olmayan kaynakların sınırlı GDELT kapsamı.** Bu gruptan çekirdek kümede yalnızca 11 haber var; yayınların çoğu Temmuz 2016 KHK'larıyla kapatılmıştı [GDELT-istatistik]. **[D]** Bu grubun 2016'daki anlatısı nicel olarak ölçülemiyor; medya bölümündeki "denge" sonuçları bu eksik veriyle birlikte okunmalı.
5. **[O] Rus devlet medyası.** Olay gecesi saat saat kronolojinin önemli bir kısmı AiF, RIA ve TASS canlı akışlarından geliyor [KR-030]–[KR-065]. **[D]** Bu kaynaklar zaman damgası için güvenilir, yorum için devlet çizgisine bağlıdır; Rus devlet medyasının Halep motivasyonunu geri planda tuttuğu ayrıca belgelendi [R45].
6. **[O] Arama özeti bilgiler.** 7 kronoloji satırı, 13 Rusya/dünya kartı ve 17 radikalleşme kartı yalnızca arama özetinden alındı [KR-015], [R25], [RD06]. **[D]** Bu bilgiler metinde işaretlendi ve hiçbir kritik değerlendirme yalnızca bunlara dayandırılmadı.
7. **[O] Ankara Valiliği'nin olay gecesi açıklaması** bulunamadı [KR-062]; **Kremlin.ru** arşivinde 19 Aralık tarihli Erdoğan görüşme kaydı yok [KR-051].
8. **[O] Vikipedi kaynaklı değerler** (20:15 saati, 15–20 atış, 19:27 öldürülme) birincil kaynaklarla teyit edilemedi ve olgu olarak kullanılmadı [KR-017], [KR-025], [KR-027].
9. **[D] Sınıflandırma tutarsızlıkları.** Girdi dosyalarında Hürriyet bazı satırlarda "muhalif/bağımsız", bazı satırlarda "hükümete yakın" olarak kodlanmıştı; burada yayın tarihine göre düzeltildi (Ek A, † işareti). KEY_OUTLETS listesinin tarihsizliği GDELT gruplarında aynı sorunu yaratıyor.
10. **[D] Literatür erişimi.** Akademik kaynakların çoğu yalnızca yayıncı kaydı ve özetle doğrulandı, tam metni okunmadı [RAD-A§1]–[RAD-A§7]; model özetleri bu sınırla okunmalı.
11. **[D] Karşılaştırma notu.** Bu rapor, bir dış raporun bazı olgusal iddialarını (ör. kurşun sayıları, müdahale süreleri, Emniyet yazısının içeriği) kendi kartlarında teyit edemediği için kullanmadı; bu iddialar ancak kaynakları açıldığında değerlendirilebilir.

# Ek A: Kanıt kartı dizini {.unnumbered}

Tüm kartlar kısa satırla. Derece sütunu: K, R ve RD kartlarında Admiralty (kaynak + bilgi); KR satırlarında erişim durumu. Özel kişiler rolüyle anılır.

<div class="tbl-eka">

### A.1 Kanıt kartları (K01–K42, `kanitlar.json`) {.unnumbered}

| Kimlik | Kaynak | Yayın tarihi | Sınıf | Derece | Kısa içerik |
|---|---|---|---|---|---|
| K01 | BBC News | 2016-12-20 | Batı basını | B2 | Saldırgan ateş ettikten hemen sonra bozuk Arapçayla cihat biatı dizesini… |
| K02 | BBC News | 2016-12-20 | Batı basını | B2 | İçişleri Bakanı Soylu'ya göre saldırgan 22 yaşında, Söke doğumlu, 2,5… |
| K03 | BBC News | 2016-12-20 | Batı basını | B4 | Doğrulanmamış haberlere göre saldırgan, darbe girişimcileriyle bağlantı… |
| K04 | BBC News | 2016-12-20 | Batı basını | B2 | Ankara Belediye Başkanı Gökçek Twitter'da olası Gülen bağlantısını ima… |
| K05 | Al Jazeera English (Katar devleti finansmanlı) | 2016-12-19 | Arap/Körfez basını · devlet bağlantılı | B2 | Olay gecesi AKP milletvekili Kani Torun Al Jazeera'ya iki şey söyledi:… |
| K06 | Hürriyet Daily News – Abdulkadir Selvi | 2016-12-20 | hükümete yakın yayın | C4 | Selvi suikasti 'FETÖ suikast hücresi' olarak çerçeveledi ve Arapça sözleri… |
| K07 | BBC News Türkçe (AA'ya atfen) | 2016-12-20 | Batı basını · devlet bağlantılı | B3 | AA'nın diplomatik kaynaklara dayandırdığı habere göre Dışişleri Bakanı… |
| K08 | Milliyet / DHA | 2016-12-21 | TR ana akım basın | C4 | Erdoğan, Arnavutluk Cumhurbaşkanı ile ortak basın toplantısında… |
| K09 | TASS (Rusya devlet ajansı) | 2016-12-21 | Rus devlet basını · devlet bağlantılı | C3 | ABD Dışişleri Sözcüsü Kirby, saldırganın motivasyonunun henüz… |
| K10 | Euronews | 2016-12-21 | Batı basını | B2 | Kremlin Sözcüsü Peskov, Gülen iddiası sorulduğunda sonuç çıkarmak için… |
| K11 | Kremlin (resmi transkript) | 2016-12-19 | resmi-RU · devlet bağlantılı | A3 | Putin, olay gecesi Lavrov, Narışkin ve Bortnikov'la yaptığı toplantıda… |
| K12 | T.C. Dışişleri Bakanlığı, Basın Açıklaması No:327 | 2016-12-19 | resmi-TR · devlet bağlantılı | A1 | Dışişleri saldırıyı kınadı ve olayın 'tüm boyutlarıyla' soruşturulacağını… |
| K13 | T.C. Dışişleri Bakanlığı – İran/Rusya/Türkiye Moskova Ortak Bildirisi | 2016-12-20 | resmi-TR · devlet bağlantılı | A1 | Suikastın ertesi günü Moskova'da yayımlanan bildiriyle üç ülke Doğu… |
| K14 | ICRC (Uluslararası Kızılhaç Komitesi) | 2016-12-22 | uluslararası kuruluş | A1 | Doğu Halep tahliyesi 15 Aralık'ta (Perşembe) başladı ve 22 Aralık akşamı… |
| K15 | Middle East Eye | 2016-12-17 | Arap/Körfez basını | B2 | İHH'nin organize ettiği yaklaşık 5.000 araçlık yardım konvoyu… |
| K16 | Anadolu Ajansı (devlet) | 2016-10-19 | TR devlet basını · devlet bağlantılı | C2 | Erdoğan muhtarlara Putin'le telefonda Fetih el-Şam (eski Nusra) cephesinin… |
| K17 | Middle East Institute – Gönül Tol | 2016-10-26 | düşünce kuruluşu | B3 | MEI'ye göre Ankara 'yakın zamana kadar' Nusra ve Ahrar el-Şam gibi Türkiye… |
| K18 | Kremlin | 2016-06-27 | resmi-RU · devlet bağlantılı | A2 | Kremlin'in aktardığına göre Erdoğan, Kasım 2015'te düşürülen uçak için… |
| K19 | Brookings Doha Center – Beverley Milton-Edwards (Katar ortaklı;… | 2016-12-21 | düşünce kuruluşu | B3 | Milton-Edwards'a göre Nusra ile doğrudan bağlantıya dair 'az kanıt' var.… |
| K20 | Milliyet | 2017-01-29 | TR ana akım basın | C3 | Savcılık, saldırganın Gmail yazışmalarının ölümünden yaklaşık 2,5 saat… |
| K21 | Arab News (Suudi) – Menekşe Tokyay | 2017-12-19 | Arap/Körfez basını | C4 | Rus uzmanlar saldırganın dizüstü bilgisayarında silinmiş dosyaları… |
| K22 | Anadolu Ajansı (devlet) | 2018-11-24 | mahkeme/iddianame · devlet bağlantılı | C3 | Ankara Cumhuriyet Başsavcılığı iddiasına göre Altıntaş'ın 'mahrem imamı'… |
| K23 | Anadolu Ajansı (devlet) | 2018-11-24 | mahkeme/iddianame · devlet bağlantılı | C3 | Ankara Cumhuriyet Başsavcılığı iddiasına göre etkin pişmanlıktan… |
| K24 | Hürriyet | 2018-11-24 | mahkeme/iddianame | C4 | Savcı Adem Akıncı'nın 609 sayfalık iddianamesine göre plan Ocak 2016'da… |
| K25 | Hürriyet | 2018-11-24 | mahkeme/iddianame | C3 | İddianameye göre eski MİT mensubu Vehbi Kürşad Akalın, uçak düşürüldükten… |
| K26 | Hürriyet | 2018-11-24 | mahkeme/iddianame | C4 | İddianame, örgütün saldırının FETÖ eylemi olmadığı imajını yaratmak için… |
| K27 | Anadolu Ajansı (devlet) | 2021-04-19 | mahkeme/iddianame · devlet bağlantılı | C3 | Ankara 2. Ağır Ceza Mahkemesi'nin gerekçeli kararına göre talimat, MİT… |
| K28 | Anadolu Ajansı (devlet) | 2021-04-19 | mahkeme/iddianame · devlet bağlantılı | C2 | 9 Mart 2021 kararında 3 sanığa ikişer, 2 sanığa birer kez ağırlaştırılmış… |
| K29 | Daily Sabah | 2023-08-15 | hükümete yakın yayın | D2 | Yargıtay Haziran 2023'te Söğüt'ün iki ağırlaştırılmış müebbet cezasını… |
| K30 | Independent Türkçe (AA'ya atfen) | 2019-01-08 | TR ana akım basın · devlet bağlantılı | B3 | Polis okulundan sanıklardan biri Altıntaş'ı 2013 öncesinde FETÖ evlerinde… |
| K31 | Anadolu Ajansı (devlet) | 2021-04-19 | mahkeme/iddianame · devlet bağlantılı | C3 | Mahkeme, FETÖ'nün suikasttaki amacının 19 Ocak 2014 MİT tırlarının… |
| K32 | Turkish Minute | 2018-11-26 | rejim kontrolünde olmayan kaynaklar | D3 | Turkish Minute'e göre Emniyet 21 Aralık 2016'da açığa alınma iddiasını… |
| K33 | Nordic Monitor – Abdullah Bozkurt | 2019-03 (güncelleme 2021-04-02) | rejim kontrolünde olmayan kaynaklar | D3 | Nordic Monitor'un iddianameye eklendiğini söylediği MASAK raporlarına göre… |
| K34 | Lenta.ru (Rus özel medya; devlet çizgisine yakın sahiplik) | 2016-12-21 | Rus basını | C2 | SITE Intelligence Group'a göre JFŞ (eski Nusra) ve Ceyş el-Fetih,… |
| K35 | Protothema (Yunanistan) | 2016-12-21 | Avrupa basını | C3 | JFŞ sözcüsü sahiplenmeyi reddetti. Ancak aynı açıklamada suikastı,… |
| K36 | Sabah | 2016-12-20 | hükümete yakın yayın | D2 | Sabah, ertesi sabah FETÖ bağlantısından söz etmeyen Hürriyet, Cumhuriyet… |
| K37 | İstanbul Gerçeği / Vişne Haber Ajansı | 2016-12-27 | TR muhalefet | C2 | CHP Milletvekili Necati Yılmaz şunları sordu: Altıntaş FETÖ mensubuysa 15… |
| K38 | Daily Sabah | 2026-05-01 | hükümete yakın yayın | D4 | MİT, İsveç'te yaşayan Abdullah Bozkurt hakkında suç duyurusunda bulundu.… |
| K39 | BBC News Türkçe | 2016-12-20 | Batı basını | B2 | Kılıçdaroğlu saldırganın canlı yakalanmayıp öldürülmesinin ayrıca üzerinde… |
| K40 | Arab News – Eray Güçlüer (ASAM) ve Timur Akhmetov (RIAC) | 2017-12-19 | düşünce kuruluşu | C5 | ASAM'dan Güçlüer'e göre saldırgan 'önceden tasarlanmış bir senaryo gereği'… |
| K41 | Anadolu Ajansı (devlet) | 2016-12-14 | TR devlet basını · devlet bağlantılı | C2 | Aralarında BBP Gençlik Kolları ve TÜGVA'nın da bulunduğu STK'lar 13 Aralık… |
| K42 | Hürriyet | 2018-11-24 | mahkeme/iddianame | C4 | İddianame, saldırı görüntülerinin TRT'de yayımlanmasının da saldırıyla… |

### A.2 Kronoloji satırları (KR-001–KR-127, `kronoloji.json`) {.unnumbered}

KR satırlarının içeriği Bölüm 2 tablolarında tam olarak verilmiştir; burada yalnızca künye yer alır. KR satırları kronoloji kaydıdır; ayrı Admiralty derecesi taşımaz. "Derece" sütununda erişim durumu (açıldı / arama özeti / bulunamadı) ve kaynaklar arası çelişki notu (⚠) verilir. † = yayın grubu sahiplik dönemine göre düzeltilmiş sınıf.

| Kimlik | Kaynak | Yayın tarihi | Sınıf | Derece |
|---|---|---|---|---|
| KR-001 | Anadolu Ajansı | 2022-12-18 | devlet medyası (TR) | açıldı |
| KR-002 | Anadolu Ajansı | 2022-12-18 | devlet medyası (TR) | açıldı |
| KR-003 | Hürriyet Daily News | 2016-12-20 | yurt içi ana akım (Doğan dönemi)† | açıldı ⚠ |
| KR-004 | Anadolu Ajansı | 2022-12-18 | devlet medyası (TR) | açıldı ⚠ |
| KR-005 | Cumhuriyet | 2016-12-21 | yurt içi muhalif/bağımsız | açıldı ⚠ |
| KR-006 | Anadolu Ajansı | 2022-12-18 | devlet medyası (TR) | açıldı |
| KR-007 | Cumhuriyet | 2016-12-21 | yurt içi muhalif/bağımsız | açıldı ⚠ |
| KR-008 | Hürriyet | 2016-12-20 | yurt içi ana akım (Doğan dönemi)† | açıldı ⚠ |
| KR-009 | Anadolu Ajansı | 2022-12-18 | devlet medyası (TR) | açıldı ⚠ |
| KR-010 | Anadolu Ajansı | 2022-12-18 | devlet medyası (TR) | açıldı |
| KR-011 | Hürriyet | 2016-12-20 | yurt içi ana akım (Doğan dönemi)† | açıldı ⚠ |
| KR-012 | Cumhuriyet | 2016-12-21 | yurt içi muhalif/bağımsız | açıldı |
| KR-013 | Hürriyet | 2016-12-20 | yurt içi ana akım (Doğan dönemi)† | açıldı |
| KR-014 | Hürriyet | 2016-12-20 | yurt içi ana akım (Doğan dönemi)† | açıldı ⚠ |
| KR-015 | Livemint (AFP) | 2016-12-21 | yabancı bağımsız medya | arama özeti ⚠ |
| KR-016 | İstiklal | 2017-12-18 | hükümete yakın yayın | açıldı |
| KR-017 | Anadolu Ajansı | 2016-12-19 | devlet medyası (TR) | açıldı ⚠ |
| KR-018 | BBC News | 2016-12-20 | yabancı bağımsız medya | açıldı |
| KR-019 | DW Türkçe | 2016-12-19 | yabancı bağımsız medya | açıldı |
| KR-020 | Lenta.ru | 2016-12-20 | yabancı bağımsız medya | açıldı ⚠ |
| KR-021 | AP Images Blog | 2016-12-19 | yabancı bağımsız medya | açıldı ⚠ |
| KR-022 | The Guardian (AP, Burhan Özbilici) | 2016-12-20 | yabancı bağımsız medya | açıldı |
| KR-023 | AP Images Blog (Burhan Özbilici) | 2016-12-19 | yabancı bağımsız medya | açıldı |
| KR-024 | Lenta.ru | 2016-12-20 | yabancı bağımsız medya | açıldı |
| KR-025 | Hürriyet | 2016-12-20 | yurt içi ana akım (Doğan dönemi)† | açıldı ⚠ |
| KR-026 | Anadolu Ajansı | 2016-12-19 | devlet medyası (TR) | açıldı ⚠ |
| KR-027 | BBC News | 2016-12-20 | yabancı bağımsız medya | açıldı ⚠ |
| KR-028 | Lenta.ru | 2016-12-20 | yabancı bağımsız medya | açıldı |
| KR-029 | Milliyet (Sina Koloğlu) | 2016-12-20 | hükümete yakın yayın | açıldı |
| KR-030 | Argumenty i Fakty | 2016-12-19 | Rus devlet medyası | açıldı |
| KR-031 | Spektr.press | 2016-12-19 | rejim kontrolünde olmayan kaynaklar | açıldı ⚠ |
| KR-032 | Argumenty i Fakty | 2016-12-19 | Rus devlet medyası | açıldı ⚠ |
| KR-033 | Argumenty i Fakty | 2016-12-19 | Rus devlet medyası | açıldı |
| KR-034 | Anadolu Ajansı | 2016-12-19 | devlet medyası (TR) | açıldı ⚠ |
| KR-035 | Argumenty i Fakty | 2016-12-19 | Rus devlet medyası | açıldı |
| KR-036 | RIA Novosti | 2016-12-19 | Rus devlet medyası | açıldı ⚠ |
| KR-037 | TASS | 2016-12-19 | Rus devlet medyası | açıldı ⚠ |
| KR-038 | Anadolu Ajansı | 2016-12-19 | devlet medyası (TR) | açıldı |
| KR-039 | Anadolu Ajansı | 2016-12-19 | devlet medyası (TR) | açıldı ⚠ |
| KR-040 | Anadolu Ajansı | 2016-12-19 | devlet medyası (TR) | açıldı |
| KR-041 | Argumenty i Fakty | 2016-12-19 | Rus devlet medyası | açıldı |
| KR-042 | Timeturk | 2016-12-19 | hükümete yakın yayın | arama özeti ⚠ |
| KR-043 | Anadolu Ajansı | 2016-12-19 | devlet medyası (TR) | açıldı |
| KR-044 | Argumenty i Fakty | 2016-12-19 | Rus devlet medyası | açıldı ⚠ |
| KR-045 | Argumenty i Fakty | 2016-12-19 | Rus devlet medyası | açıldı |
| KR-046 | Argumenty i Fakty | 2016-12-19 | Rus devlet medyası | açıldı |
| KR-047 | T.C. Dışişleri Bakanlığı | 2016-12-19 | devlet kurumu/resmi | açıldı |
| KR-048 | Argumenty i Fakty | 2016-12-19 | Rus devlet medyası | açıldı |
| KR-049 | RBC | 2016-12-19 | yabancı bağımsız medya | açıldı |
| KR-050 | Kremlin (Rusya Devlet Başkanlığı) | 2016-12-19 | devlet kurumu/resmi | açıldı ⚠ |
| KR-051 | Argumenty i Fakty | 2016-12-19 | Rus devlet medyası | açıldı ⚠ |
| KR-052 | BBC Rusça | 2016-12-19 | yabancı bağımsız medya | açıldı |
| KR-053 | RFE/RL | 2016-12-19 | yabancı bağımsız medya | açıldı |
| KR-054 | RBC | 2016-12-19 | yabancı bağımsız medya | açıldı |
| KR-055 | RBC | 2016-12-19 | yabancı bağımsız medya | açıldı |
| KR-056 | RBC | 2016-12-19 | yabancı bağımsız medya | açıldı |
| KR-057 | RBC | 2016-12-19 | yabancı bağımsız medya | açıldı ⚠ |
| KR-058 | Argumenty i Fakty | 2016-12-19 | Rus devlet medyası | açıldı |
| KR-059 | Rusya Soruşturma Komitesi (sledcom.ru) | 2016-12-19 | devlet kurumu/resmi | açıldı |
| KR-060 | BBC News | 2016-12-20 | yabancı bağımsız medya | açıldı |
| KR-061 | BBC News | 2016-12-20 | yabancı bağımsız medya | açıldı |
| KR-062 | — | — | — | bulunamadı |
| KR-063 | Argumenty i Fakty | 2016-12-20 | Rus devlet medyası | açıldı ⚠ |
| KR-064 | RBC | 2016-12-20 | yabancı bağımsız medya | açıldı ⚠ |
| KR-065 | Argumenty i Fakty | 2016-12-20 | Rus devlet medyası | açıldı |
| KR-066 | TASS | 2016-12-20 | Rus devlet medyası | açıldı ⚠ |
| KR-067 | Argumenty i Fakty | 2016-12-20 | Rus devlet medyası | açıldı |
| KR-068 | TASS | 2016-12-20 | Rus devlet medyası | arama özeti |
| KR-069 | BBC Rusça | 2016-12-20 | yabancı bağımsız medya | açıldı |
| KR-070 | Odatv | 2016-12-20 | yurt içi muhalif/bağımsız | arama özeti |
| KR-071 | Hürriyet (AA) | 2016-12-20 | yurt içi ana akım (Doğan dönemi)† | açıldı ⚠ |
| KR-072 | Cumhuriyet | 2016-12-21 | yurt içi muhalif/bağımsız | açıldı |
| KR-073 | Hürriyet | 2016-12-20 | yurt içi ana akım (Doğan dönemi)† | açıldı ⚠ |
| KR-074 | Anadolu Ajansı | 2016-12-20 | devlet medyası (TR) | açıldı |
| KR-075 | Anadolu Ajansı (EN) | 2016-12-20 | devlet medyası (TR) | arama özeti |
| KR-076 | Anadolu Ajansı (EN) | 2016-12-20 | devlet medyası (TR) | açıldı |
| KR-077 | T.C. Dışişleri Bakanlığı | 2016-12-20 | devlet kurumu/resmi | açıldı |
| KR-078 | BBC Türkçe | 2016-12-20 | yabancı bağımsız medya | açıldı ⚠ |
| KR-079 | Anadolu Ajansı | 2017-01-12 | devlet medyası (TR) | açıldı |
| KR-080 | TASS (EN) | 2016-12-21 | Rus devlet medyası | açıldı ⚠ |
| KR-081 | Daily Sabah | 2016-12-21 | hükümete yakın yayın | açıldı |
| KR-082 | Milliyet (DHA) | 2016-12-21 | hükümete yakın yayın | açıldı |
| KR-083 | Nordic Monitor | 2020-10-30 | rejim kontrolünde olmayan kaynaklar | açıldı |
| KR-084 | Rusdialog.ru | 2016-12-22 | yabancı bağımsız medya | açıldı |
| KR-085 | Kremlin | 2016-12-22 | devlet kurumu/resmi | açıldı |
| KR-086 | Anadolu Ajansı (Rusça) | 2016-12-22 | devlet medyası (TR) | açıldı ⚠ |
| KR-087 | Hürriyet | 2016-12-22 | yurt içi ana akım (Doğan dönemi)† | açıldı |
| KR-088 | Ulusal Kanal (Star'a atfen) | 2016-12-22 | yurt içi muhalif/bağımsız | arama özeti |
| KR-089 | Habertürk | 2016-12-23 | hükümete yakın yayın | açıldı |
| KR-090 | Kremlin | 2016-12-23 | devlet kurumu/resmi | açıldı |
| KR-091 | Diken | 2016-12-24 | yurt içi muhalif/bağımsız | açıldı |
| KR-092 | Turkish Minute | 2016-12-24 | rejim kontrolünde olmayan kaynaklar | açıldı ⚠ |
| KR-093 | Sabah | 2016-12-24 | hükümete yakın yayın | açıldı ⚠ |
| KR-094 | Anadolu Ajansı | 2016-12-26 | devlet medyası (TR) | açıldı |
| KR-095 | Anadolu Ajansı | 2016-12-30 | devlet medyası (TR) | açıldı |
| KR-096 | Interfax | 2017-01-07 | yabancı bağımsız medya | açıldı |
| KR-097 | Anadolu Ajansı | 2017-01-12 | devlet medyası (TR) | açıldı |
| KR-098 | Anadolu Ajansı | 2017-01-16 | devlet medyası (TR) | açıldı |
| KR-099 | Milliyet | 2017-01-29 | hükümete yakın yayın | açıldı |
| KR-100 | Hürriyet Daily News | 2017-12-18 | yurt içi ana akım (Doğan dönemi)† | açıldı ⚠ |
| KR-101 | İstiklal | 2017-12-18 | hükümete yakın yayın | açıldı |
| KR-102 | Hürriyet Daily News | 2017-12-20 | yurt içi ana akım (Doğan dönemi)† | açıldı ⚠ |
| KR-103 | Hürriyet Daily News | 2018-03-09 | yurt içi ana akım/hükümete yakın (2018 geçiş yılı)† | açıldı |
| KR-104 | Anadolu Ajansı (EN) | 2018-04-02 | devlet medyası (TR) | açıldı |
| KR-105 | Habertürk | 2018-04-17 | hükümete yakın yayın | açıldı ⚠ |
| KR-106 | Anadolu Ajansı (EN) | 2018-11-23 | devlet medyası (TR) | açıldı ⚠ |
| KR-107 | TürkPress (AA Arapça aktarımı) | 2018-12-07 | devlet medyası (TR) | açıldı ⚠ |
| KR-108 | BirGün | 2018-11-25 | yurt içi muhalif/bağımsız | arama özeti |
| KR-109 | Anadolu Ajansı (EN) | 2018-12-07 | devlet medyası (TR) | açıldı |
| KR-110 | DW | 2019-01-08 | yabancı bağımsız medya | açıldı ⚠ |
| KR-111 | TR724 | 2019-01-15 | rejim kontrolünde olmayan kaynaklar | açıldı |
| KR-112 | Hürriyet Daily News | 2020-03-05 | hükümete yakın yayın (Demirören dönemi)† | açıldı |
| KR-113 | BBC Rusça | 2020-12-19 | yabancı bağımsız medya | açıldı |
| KR-114 | Anadolu Ajansı | 2021-03-09 | devlet medyası (TR) | açıldı ⚠ |
| KR-115 | BBC Rusça | 2021-03-09 | yabancı bağımsız medya | açıldı ⚠ |
| KR-116 | Kommersant | 2021-03-09 | yabancı bağımsız medya | açıldı |
| KR-117 | Anadolu Ajansı | 2022-12-18 | devlet medyası (TR) | açıldı ⚠ |
| KR-118 | Anadolu Ajansı | 2022-12-18 | devlet medyası (TR) | açıldı ⚠ |
| KR-119 | Anadolu Ajansı | 2023-06-23 | devlet medyası (TR) | açıldı |
| KR-120 | Daily Sabah | 2023-08-15 | hükümete yakın yayın | açıldı ⚠ |
| KR-121 | DHA | 2026-01-16 | hükümete yakın yayın | açıldı |
| KR-122 | Hürriyet Daily News | 2026-01-16 | hükümete yakın yayın (Demirören dönemi)† | açıldı |
| KR-123 | RIA Novosti | 2026-01-16 | Rus devlet medyası | açıldı ⚠ |
| KR-124 | Daily Sabah | 2026-05-01 | hükümete yakın yayın | açıldı ⚠ |
| KR-125 | T24 | 2026-05-01 | yurt içi muhalif/bağımsız | açıldı |
| KR-126 | Nordic Monitor | 2026-05-07 | rejim kontrolünde olmayan kaynaklar | açıldı |
| KR-127 | RIA Novosti | 2026-07-06 | Rus devlet medyası | açıldı |

### A.3 Rusya ve dünya kartları (R01–R69, `rusya_dunya.json`) {.unnumbered}

| Kimlik | Kaynak | Tarih | Sınıf | Derece | Kısa içerik |
|---|---|---|---|---|---|
| R01 | TASS | 2016-12-19 | Rus devlet medyası | B1 | Maria Zaharova (Rusya Dışişleri Sözcüsü): MİD olayı terör eylemi olarak… |
| R02 | Kremlin.ru (Rusya Devlet Başkanlığı) | 2016-12-19 | Rus devlet kurumu/resmi | A1 | Vladimir Putin: Lavrov, Narışkin (SVR) ve Bortnikov (FSB) ile acil… |
| R03 | Kremlin.ru | 2016-12-19 | Rus devlet kurumu/resmi | A1 | Vladimir Putin: Tek yanıtın terörle mücadelenin yoğunlaştırılması… |
| R04 | Kremlin.ru (İngilizce) | 2016-12-19 | Rus devlet kurumu/resmi | A1 | Vladimir Putin: Putin, katilin arkasındaki yönlendiriciyi bilmek… |
| R05 | NEWSru.com (mid.ru'daki yorumu aktarıyor) | 2016-12-19 | Rus bağımsız medya | B2 | Sergey Lavrov: Lavrov MİD sitesinde yayımlanan yorumunda amacın… |
| R06 | Interfax | 2016-12-19 | Rus bağımsız medya | B1 | Ramzan Kadırov (Çeçenistan lideri): Instagram'da suikastı 'alçakça' diye… |
| R07 | Sputnik | 2016-12-22 | Rus devlet medyası | C2 (arama özeti) | Ramzan Kadırov: Kadırov, NY Daily News'te suikastı 'adalet' diye niteleyen… |
| R08 | Lenta.ru | 2016-12-19 | Rusya'da hükümete yakın yayın | B1 | Frants Klintseviç (Federasyon Konseyi Savunma ve Güvenlik Komitesi 1. Bşk.… |
| R09 | NSN (Национальная служба новостей) | 2016-12-21 | Rusya'da hükümete yakın yayın | C5 (arama özeti) | Frants Klintseviç: ABD Dışişleri'nin yalanlamasından sonra NSN'ye ABD… |
| R10 | The Guardian | 2016-12-19 | yabancı bağımsız medya | B2 | Konstantin Kosaçev (Federasyon Konseyi Dış İlişkiler Komitesi Bşk.):… |
| R11 | AP (WTAP üzerinden) | 2016-12-19 | yabancı bağımsız medya | B2 | Leonid Slutskiy (Duma Dış İlişkiler Komitesi Bşk.): Rusya'nın… |
| R12 | BBC Rusça | 2016-12-19 | yabancı bağımsız medya | B1 | Aleksey Puşkov (Federasyon Konseyi Savunma ve Güvenlik Komitesi üyesi):… |
| R13 | BBC Rusça | 2016-12-19 | yabancı bağımsız medya | B1 | Vladimir Jirinovski (LDPR lideri): Suikastı provokasyon sayıp Batı'nın… |
| R14 | Interfax | 2016-12-19 | Rus bağımsız medya | B2 (arama özeti) | Rusya Soruşturma Komitesi (SK) – Sözcü Svetlana Petrenko: SK ilk olarak… |
| R15 | Lenta.ru (sledcom.ru açıklamasını aktarıyor) | 2016-12-19/20 | Rusya'da hükümete yakın yayın | B1 | Rusya Soruşturma Komitesi (SK – Özellikle Önemli Davalar Genel Müdürlüğü):… |
| R16 | Interfax | 2016-12-20 | Rus bağımsız medya | B1 | Dmitriy Peskov: Özel servisler, SK ve MİD temsilcilerinden oluşan 18… |
| R17 | BBC Rusça | 2016-12-20 | yabancı bağımsız medya | B1 | Dmitriy Peskov / SK: BBC: SK davayı iki maddeden birden ('korunan yabancı… |
| R18 | Komsomolskaya Pravda (RIA'yı aktarıyor) | 2016-12-21 | Rusya'da hükümete yakın yayın | B1 | Dmitriy Peskov: Çavuşoğlu'nun Kerry'ye 'Türkiye ve Rusya arkasında FETÖ… |
| R19 | Interfax | 2016-12-21 | Rus bağımsız medya | B1 | Dmitriy Peskov: Peskov 'Mir' kanalına suikastın Türk devletine de… |
| R20 | Kremlin.ru | 2016-12-23 | Rus devlet kurumu/resmi | A1 | Vladimir Putin: Yıllık basın toplantısında suikastı 'Rusya'ya ve Rus-Türk… |
| R21 | Moskva 24 | 2016-12-23 | Rus devlet medyası | B1 (arama özeti) | Vladimir Putin: Aynı basın toplantısında suikastın Rus-Türk ilişkilerinin… |
| R22 | Kremlin.ru (İngilizce) | 2016-12-23 | Rus devlet kurumu/resmi | A2 | Vladimir Putin / Recep Tayyip Erdoğan: Telefon görüşmesi: Erdoğan, Putin'e… |
| R23 | Interfax (İngilizce) | 2016-12-27 | Rus bağımsız medya | B1 | Maria Zaharova: Brifingde Batı'nın Suriye bağlamındaki 'amaçlı Rusya… |
| R24 | The Moscow Times | 2016-12-20 | Rus bağımsız medya | B2 | Maria Zaharova: Rossiya-1'de (Solovyov) Karlov'un Türkiye'deki Suriyeli… |
| R25 | Reuters | 2016-12-20 | yabancı bağımsız medya | B2 (arama özeti) | Sergey Lavrov: Moskova üçlü toplantısı öncesi yazılı açıklamada Lavrov,… |
| R26 | Rusya Dışişleri Bakanlığı (mid.ru) | 2016-12-20 | Rus devlet kurumu/resmi | A2 (arama özeti) | Lavrov – Zarif görüşmesi (Moskova): Lavrov, suikast organizatörlerinin… |
| R27 | T.C. Dışişleri Bakanlığı | 2016-12-20 | Türk devlet kurumu | A1 | Rusya, Türkiye, İran Dışişleri Bakanları: Suikastın ertesi günü toplantı… |
| R28 | ISPI | 2017-01 / 2019-03-28 | akademik | B1 | Analiz (ISPI): Suikastten kısa süre sonra, Ocak 2017'de Astana görüşmeleri… |
| R29 | INSS Insight No. 982 | 2017-09-10 / 2017-10-18 | akademik | B2 (arama özeti) | Analiz (INSS): Erdoğan'ın 10 Eylül 2017'de S-400 için Rusya'ya peşinat… |
| R30 | RT Rusça | 2017-03-09 | Rus devlet medyası | B1 | Dmitriy Peskov: Peskov, Putin–Erdoğan Moskova görüşmesinde dar formatta… |
| R31 | Vestnik Kavkaza (TASS'ı aktarıyor) | 2017-12-19 | Rusya'da hükümete yakın yayın | B2 | Aleksey Yerhov (Rusya'nın Ankara Büyükelçisi): Birinci yıl dönümü… |
| R32 | Life.ru (RIA Novosti röportajını aktarıyor) | 2021-12-19 | Rusya'da hükümete yakın yayın | B2 | Mevlüt Çavuşoğlu (Türkiye Dışişleri Bakanı): 5. yıl dönümünde RIA'ya:… |
| R33 | Kremlin.ru | 2016-12-20/21 | Rus devlet kurumu/resmi | A1 | Vladimir Putin (Kararname No. 694): Karlov'a ölümünden sonra 'Rusya… |
| R34 | Kremlin.ru (İngilizce) | 2016-12-22 | Rus devlet kurumu/resmi | A1 | Vladimir Putin, Medvedev, Matviyenko, Volodin, Lavrov: MİD binasında veda… |
| R35 | RIA Novosti | 2017-01-31 | Rus devlet medyası | B1 | Moskova Belediyesi: Kutuzovski Prospekt ile Bolşaya Dorogomilovskaya… |
| R36 | Interfax (Yeni Şafak'ı aktarıyor) | 2017-01-09 | Rus bağımsız medya | B1 | Ankara Büyükşehir Belediyesi / Çavuşoğlu girişimi: Rus Büyükelçiliğinin… |
| R37 | Rusya'nın Ankara Büyükelçiliği sitesi | 2017-08 / 2017-11-24 | Rus devlet kurumu/resmi | A2 (arama özeti) | Rusya'nın Ankara Büyükelçiliği: Büyükelçilik bahçesine MİD çalışanlarının… |
| R38 | Rusya Dışişleri Bakanlığı | 2017-12-19 | Rus devlet kurumu/resmi | A2 (arama özeti) | Sergey Lavrov: Birinci yıl dönümünde Moskova'da heykeltıraş… |
| R39 | Rusya Dışişleri Bakanlığı (Rus Diplomatlar… | 2021-12-19 | Rus devlet kurumu/resmi | A2 (arama özeti) | Rusya Dışişleri Bakanlığı / Lavrov: MİD'in 5. yıl anma metni: davanın Rus… |
| R40 | MK-Turkey (TASS'ı aktarıyor) | 2019-01-11 | Rusya'da hükümete yakın yayın | B1 | Maria Zaharova: Ankara'daki dava açılırken MİD, tüm sorumluların yasaya… |
| R41 | RIA Novosti (RG röportajını aktarıyor) | 2019-07-24 | Rus devlet medyası | B1 | Aleksandr Bastrıkin (SK Başkanı): Rossiyskaya Gazeta röportajı: Türkiye'de… |
| R42 | RIA Novosti (MİD açıklamasını aktarıyor) | 2021-03-09 | Rus devlet medyası | B1 | Rusya Dışişleri Bakanlığı: MİD, Ankara 2. Ağır Ceza'nın kararından… |
| R43 | BBC Monitoring | 2016-12-20 | yabancı bağımsız medya | B1 | Rus basını (Kommersant, Komsomolskaya Pravda, Izvestia, RBC): BBC… |
| R44 | BBC Rusça | 2016-12-20 | yabancı bağımsız medya | B2 | Rus sosyal medyası (BBC Rusça analizi): Rus sosyal medyasında muhalifler… |
| R45 | The Atlantic | 2016-12-25 | yabancı bağımsız medya | B3 (arama özeti) | The Atlantic (I. Lozovsky): Analiz: Batı haberlerinin ilk satırlarında yer… |
| R46 | MK-Turkey / Moskovski Komsomolets | 2018-04-04 | akademik | C3 | İlşat Saetov (RAN Şarkiyat Enstitüsü): MK'ye: Rus tarafının Gülen'in… |
| R47 | NTV | 2023-03-26 | Rus devlet medyası | C5 | NTV ('Novye russkie sensatsii') / Sergey Kudasov: Devlet kontrolündeki… |
| R48 | RIA Novosti | 2026-07-06 | Rus devlet medyası | B3 | RIA Novosti (Sabah'ı aktarıyor): RIA, Ankara 34. Ağır Ceza'nın eski MİT… |
| R49 | Delovoy Peterburg (SITE'ı aktarıyor) | 2016-12-21 | Rus bağımsız medya | C2 | Ceyş el-Fetih / Cebhet Fetih eş-Şam (eski Nusra): Irak'taki Al Sumaria ve… |
| R50 | Hürriyet | 2017-06-03 | yurt içi muhalif/bağımsız | B1 | Marina Karlova: Suikasttan altı ay sonra ilk kez Türk basınına (Nâzım… |
| R51 | RT Rusça | 2017-11-20 | Rus devlet medyası | B1 | Marina Karlova: RT'ye: trajediden iki hafta sonra Ankara'ya veda için… |
| R52 | RIA Novosti | 2018-12-19 | Rus devlet medyası | B1 | Marina Karlova: RIA'ya uzun röportaj: 'Türkiye'ye ve Türk halkına hiçbir… |
| R53 | RIA Novosti | 2018-12-19 | Rus devlet medyası | B1 | Marina Karlova: Aynı röportajda: davayı Rusya SK'nin yürüttüğünü ve onu… |
| R54 | Argumenty i Fakty (RIA'yı aktarıyor) | 2018-12-21 | Rusya'da hükümete yakın yayın | B1 | Marina Karlova (oğlu hakkında): Oğlu'un babasının ölümü sırasında KDHC'de… |
| R55 | RTİB (Sputnik Türkiye röportajını yeniden… | 2019-11-12 | Rus devlet medyası | B1 | Marina Karlova (Uluslararası Andrey Karlov Vakfı Başkanı): Malatya'da… |
| R56 | BBC Rusça | 2020-12-19 | yabancı bağımsız medya | B1 | Marina Karlova: BBC Rusça'ya: davanın asla aydınlatılmayacağından emin… |
| R57 | BBC Rusça | 2020-12-19 | yabancı bağımsız medya | B2 | Marina Karlova: Aynı röportaj: saldırıdan en az 4 ay önce tehditler… |
| R58 | RIA Novosti (Rossiya-24'ü aktarıyor) | 2021-03-09 | Rus devlet medyası | B1 | Marina Karlova: Rossiya-24'te karar sonrası: yargılamayı takip etmediğini,… |
| R59 | NTV | 2023-03-26 | Rus devlet medyası | B2 | Marina Karlova: NTV programında: eşinin uyarısının ardından sinyaller… |
| R60 | The Moscow Times / AFP | 2019-01-08 | Rus bağımsız medya | B3 (arama özeti) | Marina Karlova: AFP/Moscow Times: Karlova davanın açılış duruşmasında… |
| R61 | The American Presidency Project (UCSB) | 2016-12-19 | akademik | A1 | Donald Trump (seçilmiş ABD Başkanı): Geçiş ekibi açıklamasında Karlov'un… |
| R62 | ABD Dışişleri Bakanlığı (arşiv) | 2016-12-19 | yabancı devlet kurumu/resmi (listede karşılığı yok) | A1 | John Kerry (ABD Dışişleri Bakanı): ABD suikastı kınadı, soruşturmada Rusya… |
| R63 | Anadolu Ajansı | 2016-12-19/20 | devlet medyası (TR) | B1 | Beyaz Saray (Obama yönetimi), NATO Genel Sekreteri Stoltenberg, İran, Çin:… |
| R64 | Anadolu Ajansı | 2016-12-19 | devlet medyası (TR) | B1 | NATO Genel Sekreteri Jens Stoltenberg: Twitter'da suikastı kınadı. |
| R65 | UN News | 2016-12-19 | uluslararası kuruluş/resmi (listede karşılığı yok) | A1 | BM Genel Sekreteri Ban Ki-moon ve BM Güvenlik Konseyi: BMGK basın… |
| R66 | EEAS (AB Dış İlişkiler Servisi) | 2016-12-19 | uluslararası kuruluş/resmi (listede karşılığı yok) | A1 | Federica Mogherini (AB Yüksek Temsilcisi): Lavrov'a mesaj: AB saldırıyı en… |
| R67 | Press TV | 2016-12-19 | yabancı devlet medyası – İran (listede karşılığı yok) | B1 | Bahram Kasımi (İran Dışişleri Sözcüsü): İran, eylemi 'tekfirci' grupların… |
| R68 | AP (WTAP üzerinden) | 2016-12-19 | yabancı bağımsız medya | B2 | Suriye Dışişleri Bakanlığı (Esad yönetimi): Suriye rejimi suikastı… |
| R69 | AGİT | 2016-12-20 | uluslararası kuruluş/resmi (listede karşılığı yok) | A2 (arama özeti) | AGİT Daimi Konseyi: AGİT Daimi Konseyi suikastı 'ölümcül terör saldırısı'… |

### A.4 Radikalleşme kartları (RD01–RD56, `radikallesme_kartlar.json`) {.unnumbered}

| Kimlik | Kaynak | Yayın tarihi | Sınıf | Derece | Kısa içerik |
|---|---|---|---|---|---|
| RD01 | Diken (Soylu açıklamasını aktarıyor) | 2016-12-24 | yurt içi muhalif/bağımsız (resmi açıklamanın aktarımı) | A1 | İçişleri Bakanı'nın açıkladığı kimlik: 24 Haziran 1994 Söke doğumlu, Söke… |
| RD02 | Anadolu Ajansı | 2016-12-22 | devlet medyası (TR) (emniyet ifadesinden aktarım) | B2 | Anne ifadesi: oğlu olay günü 16.30'da aradı, helallik istedi; sınavlara… |
| RD03 | Anadolu Ajansı | 2016-12-22 | devlet medyası (TR) | B2 | Baba ifadesi: polis olduktan sonra ibadetlerine daha düşkün, içine kapanık… |
| RD04 | Hürriyet Daily News (Banu Şen) | 2016-12-27 | ana akım (Hürriyet, Doğan dönemi) | B2 | Abla: kardeşi çocukken cuma/teravihe gidiyordu; günde beş vakit namaza… |
| RD05 | Hürriyet Daily News | 2016-12-27 | ana akım (Hürriyet, Doğan dönemi) | B2 | Abla: Körfez dershanesine kardeşi değil kendisi kayıtlıydı; hiçbir işadamı… |
| RD06 | Anadolu Ajansı (haberintelifi) | 2016-12-20 | devlet medyası (TR) | C4 (arama özeti) | AA: Altıntaş'ın Söke'de 2014'te kapatılan FETÖ'ye ait Körfez… |
| RD07 | Sputnik Türkiye (Sözcü'ye atfen) | 2016-12-20 | devlet medyası (RU) / yurt içi muhalif aktarımı | D4 (arama özeti) | Sputnik TR, Sözcü'ye atfen: eğitim masraflarını firari bir işadamının… |
| RD08 | Habertürk | 2016-12-24 | hükümete yakın yayın | C3 (arama özeti) | Dayı: anne cenazeyi istemedi; 'aile olarak FETÖ'ye karşıyız'. |
| RD09 | Diken (Hürriyet'e atfen) | 2016-12-24 | yurt içi muhalif/bağımsız (Hürriyet aktarımı) | C2 | Hürriyet'e konuşan akraba: değişim son 2-2,5 yılda, yani meslekten sonra;… |
| RD10 | Reuters | 2016-12-26 | yabancı bağımsız medya | B3 (arama özeti) | Reuters: baba polise oğlunun herhangi bir terör örgütü, dini ağ ya da… |
| RD11 | Diken (Hürriyet 24.12.2016'ya atfen) | 2016-12-24 | yurt içi muhalif/bağımsız (Hürriyet aktarımı) | B2 | Hürriyet: Altıntaş, ev arkadaşları bir ev arkadaşı ve bir avukat ile… |
| RD12 | Düşünce Mektebi (Sosyal Doku Vakfı… | 2016-12-24 | ilgili taraf açıklaması (hükümete yakın çevre) | D3 (arama özeti) | Sosyal Doku Vakfı: Yıldız'ın Hacı Bayram vaazları halka açık ve iki yıl… |
| RD13 | Odatv (Akıncı iddianamesinden alıntı) | 2018-11-28 | yurt içi muhalif/bağımsız (iddianame alıntısı) | B2 | İddianame: Ankara'ya tayinden sonra 2014'te Sosyal Doku Ankara… |
| RD14 | Odatv (iddianameye dayanarak) | 2018-11-28 | yurt içi muhalif/bağımsız | B2 | İddianame: Altıntaş'ın ajandasında Nurettin Yıldız sohbetlerine dair… |
| RD15 | TR724 (BoldMedya/Cevheri Güven'e atfen,… | 2019-01-02 | rejim kontrolünde olmayan kaynaklar | C2 | Bilirkişi raporu (26.01.2018): USB bellekte Nurettin Yıldız sohbet… |
| RD16 | TR724 (Erman Yalaz) | 2019-01-15 | rejim kontrolünde olmayan kaynaklar | C3 (arama özeti) | Bir tanık: Ekim-Kasım 2014 temasından sonra Hacı Bayram'daki sohbete… |
| RD17 | Nordic Monitor (Abdullah Bozkurt) | 2021-04-05 | rejim kontrolünde olmayan kaynaklar (yazar vakada MİT suç duyurusunun hedefi: çıkar çatışması) | C2 | İHH çalışanı bir tanık: Altıntaş'ı Nurettin Yıldız sohbetlerinde gördü. |
| RD18 | Anadolu Ajansı (iddianame) | 2018-11-23 | devlet medyası (TR) (iddianamedeki şüpheli beyanı) | C3 | Polis okulundan bir şüpheli (iddianame): Altıntaş, 'Hamza' kod adlı bir… |
| RD19 | Anadolu Ajansı (iddianame) | 2018-11-23 | devlet medyası (TR) | C3 | Polis okulundan arkadaşı olan sanık (savcıya): 17-25 Aralık öncesi bir… |
| RD20 | Anadolu Ajansı (iddianame) | 2018-11-23 | devlet medyası (TR) | C3 | Sınıf komiseri: Altıntaş ve arkadaşı'ı uyardı; 17-25 Aralık sonrası… |
| RD21 | Anadolu Ajansı (iddianame) | 2018-11-23 | devlet medyası (TR) | C3 | Bir tanık: ikinci sınıftan itibaren okul arkadaşları ile takılmaya… |
| RD22 | Anadolu Ajansı (iddianame) | 2018-11-23 | devlet medyası (TR) | C3 | Bir tanık: Altıntaş 'Fetullah Gülen cemaati sohbetlerine de gitmiştim'… |
| RD23 | Anadolu Ajansı (iddianame) | 2018-11-23 | devlet medyası (TR) | C3 | Zümre başkanı olduğunu kabul eden Salih Yılmaz: bir kişi Altıntaş'ı… |
| RD24 | Cumhuriyet | 2019-01-11 | yurt içi muhalif/bağımsız | C3 (arama özeti) | Okul arkadaşı olan sanık duruşmada: Altıntaş 'cep telefonu hastası' ve… |
| RD25 | Yeni Şafak | 2016-12-27 | hükümete yakın yayın | D4 (arama özeti) | Altıntaş (82) ve bir ev arkadaşı (83) PMYO sınavını yakın puanla,… |
| RD26 | Diken (Hürriyet'e atfen) | 2016-12-24 | yurt içi muhalif/bağımsız (silinmiş tweet aktarımı) | C3 | İsmailağa çevresinin Ankara uzantısından bir kişinin tweet'i: Altıntaş… |
| RD27 | Odatv (iddianameden alıntı) | 2018-11-28 | yurt içi muhalif/bağımsız (iddianame alıntısı) | B2 | İddianame: saldırıdan bir gün önce 'taşınacağı gerekçesiyle' kitap… |
| RD28 | Odatv (iddianameden alıntı) | 2018-11-28 | yurt içi muhalif/bağımsız | B2 | İddianame: Keçiören'deki evde Yahya Konuk (Bülent Tokgöz) imzalı… |
| RD29 | Anadolu Ajansı | 2016-12-20 | devlet medyası (TR) | C3 | AA: evdeki aramada 'FETÖ ve El Kaide'ye ilişkin kitaplar bulundu'; polis… |
| RD30 | Nordic Monitor (Bozkurt) | 2020-08-24 | rejim kontrolünde olmayan kaynaklar | C3 | Teknik rapor/faturalar: Awlaki'nin '44 Ways to Support Jihad' kitabını… |
| RD31 | Karar | 2016-12-22 | hükümete yakın yayın | C3 | El yazısı not: 'ABD ve Rusya'nın sonu yakındır. Artık kıyam vaktidir';… |
| RD32 | Haberrus (İzvestia'ya atfen) | 2021-12-20 | yabancı medya (Rusya merkezli; bağımsızlığı belirsiz) | C3 (arama özeti) | Karlov'un eşi (İzvestia'ya): katil 'etkilenebilir bir zombi çocuk', 'çok… |
| RD33 | Anadolu Ajansı (iddianame) | 2018-11-23 | devlet medyası (TR) | B2 | Bir tanık: Altıntaş bunalımdaydı, görevden ayrılmak ve Suriye'ye gidip… |
| RD34 | Nordic Monitor (Bozkurt) | 2021-04-05 | rejim kontrolünde olmayan kaynaklar | C2 | Bir tanık (26.12.2016 ifade): 2 yıldır tanır, sohbet halkalarında görüşür,… |
| RD35 | Nordic Monitor (Bozkurt) | 2021-04-05 | rejim kontrolünde olmayan kaynaklar | C2 | MASAK raporları (23.12.2016, 16.02.2017; Kuveyt Türk/Albaraka hesapları):… |
| RD36 | Nordic Monitor (Bozkurt) | 2026-05-07 | rejim kontrolünde olmayan kaynaklar (çıkar çatışması) | C3 | Dosya ekleri iddiası: Altıntaş Musab Bin Umeyr Derneği'ne (bir dernek… |
| RD37 | Nordic Monitor (Bozkurt) | 2026-05-07 | rejim kontrolünde olmayan kaynaklar (çıkar çatışması) | C3 | Dosya ekleri iddiası: Altıntaş Abdulkadir Şen'in Suriye kitabını aldı, 8… |
| RD38 | TR724 (iddianame alıntısı, BoldMedya) | 2019-01-02 | rejim kontrolünde olmayan kaynaklar (iddianame alıntısı) | B2 | Bilgisayar incelemesi (iddianame): 14.02.2016'da YouTube'da 'El Kaide –… |
| RD39 | Nordic Monitor (Bozkurt) | 2020-08-24 | rejim kontrolünde olmayan kaynaklar | C2 | Haziran 2017 teknik rapor (Asus PC): Halis Bayancuk (25.08.2016), 11… |
| RD40 | Hürriyet (Mesut Hasan Benli) | 2017-12-18 | ana akım (Hürriyet, Doğan dönemi) | C3 | Rus heyeti silinmiş dosyaları kurtardı: 'Fetullah Gülen' 2, 'Hizmet' 690,… |
| RD41 | Hürriyet (Mesut Hasan Benli) | 2017-12-18 | ana akım (Hürriyet, Doğan dönemi) | C3 | iCloud/WhatsApp: cinayetten 1 hafta önce 'Sosyal doku' WhatsApp grubuna… |
| RD42 | Hürriyet | 2017-12-18 | ana akım (Hürriyet, Doğan dönemi) (savcılık değerlendirmesi) | C4 | Savcılık değerlendirmesi: Arapça slogan, El-Nusra iltisaklı kişilerle 2 ay… |
| RD43 | Anadolu Ajansı (Ankara 2. ACM gerekçeli… | 2021-04-19 | devlet medyası (TR) (resmi mahkeme kararının aktarımı) | B3 | Gerekçeli karar: 17-25 Aralık sonrası 'renklendirme' talimatıyla Altıntaş… |
| RD44 | Anadolu Ajansı (gerekçeli karar) | 2021-04-19 | devlet medyası (TR) | B3 | Gerekçeli karar: Şahin Söğüt 9 Aralık 2016'da Altıntaş'a saldırıyla ilgili… |
| RD45 | TRT Haber (AA kaynaklı) | 2016-12-20 | devlet medyası (TR) | B2 (arama özeti) | Otel: 14 Aralık'ta telefonla rezervasyon, 18 Aralık'ta 214 numaralı odaya… |
| RD46 | Gazete Duvar | 2016-12-22 | yurt içi muhalif/bağımsız | B2 (arama özeti) | Telefon hattı incelemesinde ByLock kullanmadığı belirlendi. |
| RD47 | Hürriyet – Nedim Şener köşe yazısı | 2023-07-10 | hükümete yakın yayın (Demirören dönemi köşe yazısı) | D4 | Garson SD kart: 2014 kodlama listesinde 'EA' koduyla 'en sadık' olarak… |
| RD48 | A Haber | 2026-06-15 | hükümete yakın yayın | C4 (arama özeti) | Garson kod sözlüğü: 'EA (Ehil Dünya)' = örgüt içinde ama tam teslimiyet… |
| RD49 | Turkish Minute | 2018-11-26 | rejim kontrolünde olmayan kaynaklar | C2 (temel kartlardan) | Emniyet 21 Aralık 2016'da açığa alınma iddiasını yalanladı; Altıntaş OHAL… |
| RD50 | Anadolu Ajansı | 2016-12-22 | devlet medyası (TR) | C3 (arama özeti) | AA: hat HTS incelemesinde sıklıkla görüştüğü 8 kişi ByLock kullanıcısı… |
| RD51 | Yeni Şafak | 2016-12-24 | hükümete yakın yayın | C3 (arama özeti) | Yeni Şafak: 16-17 Temmuz 2016'da senelik izin kullandı; izni FETÖ'den… |
| RD52 | Memurlar.net | 2018-12-04 | hükümete yakın yayın | C4 (arama özeti) | İddianame (KOM Daire Başkanlığı 'Emniyet Mahrem Yapılanması' raporuna… |
| RD53 | Odatv (Sabah'a atfen) | 2026-05-01 | yurt içi muhalif/bağımsız (MİT suç duyurusunun aktarımı) | D5 (arama özeti) | MİT suç duyurusu (Sabah'a atfen): Abdullah Bozkurt'un Altıntaş'ı… |
| RD54 | Nordic Monitor (Bozkurt) | 2026-05-07 | rejim kontrolünde olmayan kaynaklar (yazar iddianın hedefi: doğrudan çıkar çatışması) | C3 | Soruşturma iki ev belirledi: biri AKP'ye yakın bir avukata ait, diğeri… |
| RD55 | BBC News | 2016-12-20 | yabancı bağımsız medya | A1 (temel kartlardan) | Saldırı anında Arapça cihat biatı dizesi ve 'Halep'i unutmayın' sözleri. |
| RD56 | Turkish Minute | 2016-12-24 | rejim kontrolünde olmayan kaynaklar | C3 (arama özeti) | Turkish Minute: İçişleri Bakanı Soylu, radikal İslamcı izlerin Gülen… |

</div>

# Ek B: Yöntem {.unnumbered}

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
