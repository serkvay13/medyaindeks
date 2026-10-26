# Medya İndeksi — kanıta bağlı analiz platformu (v1)

Bu belge `medya/` paketinin mimarisini, koda gömülü iki sert kuralı, uzman analiz akışını, ek soru
(derinleştirme) akışını ve nasıl çalıştırılacağını anlatır. Tasarımın dayanağı "Medya İndeksi: inceleme ve
analiz platformu önerisi" belgesidir (30.09.2026).

> Durum: ilk sürüm. Panel (`app.py`) değiştirilmedi; yeni paket onun yanında durur. Mevcut yardımcıların
> (`topic_patterns`, `preprocess`, `coverage_report` …) pakete taşınması Faz 0'ın ayrı işidir.

## 1. İki sert kural

### Kural 1 — Uydurma veri yok

- **Her olgu bir kanıt kartına bağlıdır.** Kart; URL, kurum/yayın, kısa özet, en çok 300 karakterlik birebir
  alıntı, yayın ve olay tarihi, erişim tarihi, arşiv adresi ve Admiralty derecesi taşır. Kimliği URL +
  alıntının SHA-256 özetidir (`k-…`): aynı kaynak, aynı kimlik.
- **Doğrulayıcı** (`medya/dogrulayici`) rapora girecek her cümleyi atıf yaptığı kartlarla karşılaştırır:
  sayılar, tarihler ("19 Aralık 2016", "19.12.2016", "2016-12-19", "Aralık 2016"), tırnak içi alıntılar ve büyük
  harfle başlayan adlar `fold_tr` ile normalize edilip kartlarda aranır. Bulunamayan cümle **rapordan çıkarılır**
  ve gerekçesiyle analist listesine yazılır.
- Rapor kurulmadan önce tutulan bütün cümleler yeniden doğrulanır (`kesin_dogrula`). Biri bile geçmezse rapor
  **kurulmaz**. Önceki sürümden taşınan cümleler de her yeni sürümde yeniden doğrulanır; kayıtlı rapora elle
  sokulmuş cümle doğrulama ve onay aşamasını geçemez.
- **LLM ölçmez, anlatır.** Model yalnızca o bölüm için seçilmiş kartları görür ve doğrulama da yalnızca o
  kartlara karşı yapılır: model görmediği bir karta dayanamaz.
- Yayımlamadan önce **insan onayı** zorunludur: `taslak → dogrulandi → onaylandi`; onaylayanın adı ve tarih
  rapora yazılır. Kapsam onayı (soru → rapor akışının ilk insan onayı) olmadan rapor doğrulanamaz.

### Kural 2 — Resmi anlatı olduğu gibi kabul edilmez; herkes aynı ölçekle tartılır

- Resmi açıklamalar `resmi_aciklama` türünde saklanır ve her yerde **"<kurum> iddiası"** olarak gösterilir.
  Yalnızca resmi açıklamaya dayanan bir olgu cümlesi atıf kalıbı taşımazsa ("açıkladı", "iddia etti", "-e göre")
  doğrulayıcı reddeder.
- Resmi, iktidara yakın, muhalif ve yabancı kaynaklar **aynı Admiralty ölçeğinden** geçer
  (kaynak A–F, bilgi 1–6). ACH'de kanıt ağırlığı yalnızca bu dereceden hesaplanır; kaynağın konumundan değil.
- **Simetri:** Resmi tez her zaman hipotezlerden biridir, asla varsayılan değildir. Resmi tez varsa yanında en
  az iki rakip hipotez (biri alternatif, yapısal, dış konjonktür ya da masum açıklama) bulunmak zorundadır.
  Eşitlikte sıralama hipotez türüne değil kimliğe bakar. Alternatif hipotez de baştan doğru kabul edilmez.
- **Dil disiplini:** olgu cümlesinde niyet fiilleri (kandırdı, amaçladı, planladı, yönlendirdi, gizledi, kasten,
  bilerek …) yasaktır. Niyet yalnızca değerlendirme cümlesinde, ACH sonucuna dayanarak ve Kent ölçeğinden bir
  olasılık terimiyle yazılabilir. Tek istisna, karttaki alıntıyla birebir eşleşen tırnak içi sözdür.

## 2. Mimari

```
medya/
  metin.py         fold_tr / tr_lower (app.py ile birebir), Türkçe tarih ve sayı ayrıştırma
  kanit/           kanıt kartı + DuckDB deposu (MEDYA_KANIT_DB, varsayılan data/store/kanit.duckdb)
  dogrulayici/     cümle modeli {tur: olgu|degerlendirme|acik_soru, metin, kanit_ids, guven} + doğrulayıcı
  hipotez/         ACH (Heuer): ön kayıt + SHA-256 kilidi, T/Ç/N matrisi, tanısallık, ağırlık, kırmızı takım
  baglam/          on adımlık bağlam protokolü
  aktor/           aktör profilleri (aktorler/*.toml) + tepki fonksiyonları (Wilson %95 GA)
  uzman/           sağlayıcıdan bağımsız LLM katmanı; istemler/*.md (Türkçe sistem istemleri);
                   yazim.py: bölüm bazlı rapor yazımı + kural denetimi + doğrulama
  rapor/           14 bölümlük rapor motoru, Markdown çıktı, durum geçişleri;
                   vaka_raporu.py + yapi.py + tablolar.py + pdf.py: vaka paketinden MD/HTML/PDF (referans yapı)
  gdelt/           GDELT GKG 2.1 ham veri: indirici, vaka sorgusu, istatistik, göstergeler, grafikler
  arastirma/       araştırma protokolü (beş hat), görev listesi, arama sağlayıcıları, kapsam denetçisi
  vaka_paketi.py   vakalar/<vaka>/ paketleri (vaka.yaml, kartlar/, anlati/, gdelt/ …)
  derinlestir/     ek sorular → araştırma planı → yeni kanıt → yeni sürüm + değişiklik günlüğü
  vaka.py          vaka çalışma alanı (MEDYA_CALISMA, varsayılan data/vakalar_calisma/) + vaka kütüphanesi
  cli.py           python -m medya …
  ornek_veri.py    SENTETİK örnek vaka (kurgusal "Kuzey Limanı"; testler ve arayüz denemesi için)
aktorler/          aktör profilleri (örnekler taslak, raporlara girmez)
vakalar/           vaka kütüphanesi (ilk atıf ve nihai sonuç alanlarıyla)
pages/vaka_raporu.py  Streamlit sayfası
tests/             pytest, ağsız, küçük sentetik veri
```

`data/` git dışıdır: kanıt deposu, vaka çalışma alanları ve rapor sürümleri repoya girmez.

### Kanıt kartı türleri

`haber`, `resmi_aciklama`, `mahkeme_kaydi`, `arastirma_kurumu`, `uluslararasi_basin`, `uluslararasi_kurum`,
`veri_serisi`, `olay_kaydi`, `arsiv`. Yayın grubu ancak tarihi ve dayanağıyla yazılabilir ("şu tarihteki şu
kaynağa göre"). Radikal örgütlerin kendi yayınları kaynak olarak taranmaz; bu söylem araştırma kurumları ve
mahkeme kayıtlarının aktardığı biçimiyle kullanılır.

### ACH (modül 10)

- Hipotezler kanıta bakılmadan **önce** kaydedilir (`hipotez kaydet`). Kayıt anı ve kümenin SHA-256 özeti
  saklanır; ilk kanıt bağlandığında küme kilitlenir. Kilitten sonra eklenen hipotez **"sonradan eklendi"**
  diye işaretlenir. Ön kayıtlı bir hipotezin metni sonradan değiştirilirse yükleme hata verir.
- Matris: T (tutarlı) / Ç (çelişkili) / N (nötr). Ağırlık = kaynak derecesi × bilgi derecesi
  (A=1,0 … E=0,2; F=0,3 · 1=1,0 … 5=0,2; 6=0,3). Tanısallık: kanıt bütün hipotezlerde aynı değeri alıyorsa 0.
- Sıralama **ağırlıklı çelişkiye** göredir (en az çürütülen önce). Az kanıtla sınanmış hipotez işaretlenir
  (`az_kanit`): öne çıkması kanıt kapsamının darlığını yansıtabilir.
- Öne çıkan hipotez için kırmızı takım (şeytanın avukatı) kaydı tutulur; yoksa "Eksik veri"ye yazılır.
- Her hipotezin destekleyici ve çürütücü göstergeleri izleme listesine girer.

### Bağlam protokolü (her vakada aynı on adım)

| # | Adım | Kod |
|---|---|---|
| 1 | Çok şeritli zaman çizgisi (iç siyaset, dış politika, bölgesel çatışma, ekonomi, yargı, güvenlik, uluslararası aktörler; varsayılan −12/+6 ay) | `zaman_cizgisi` |
| 2 | "Neden şimdi?" kırılma noktaları (taban yüzdeliği + z; n ve taban raporlanır; neden dili yok) | `neden_simdi` |
| 3 | Çıkar haritası — "Kazanmak kasıt kanıtı değildir." | `cui_bono` |
| 4 | Tez soykütüğü (ilk görünüş, gecikme, bulgulardan önce/sonra, yayılma sırası) | `tez_soykutugu` |
| 5 | Tarihsel benzerler (vaka kütüphanesi, etiket benzerliği; ilk atıf ve nihai sonuç yan yana) | `tarihsel_benzerler` |
| 6 | Önceden işaret (yalnızca olaydan önce tarihli ve kaynaklı) | `erken_isaretler` |
| 7 | Temel varsayımlar | `temel_varsayimlar` |
| 8 | Rakip hipotezler (ACH) | `rakip_hipotezler_adimi` |
| 9 | Şeytanın avukatı | `kirmizi_takim_adimi` |
| 10 | İzlenecek göstergeler | `izlenecek_gostergeler` |

Kanıt kimliği taşımayan girdi satırı adımın çıktısına girmez. Girdisi verilmemiş adım "eksik" sayılır; analist
boşluğun nedenini yazarsa "bos_gerekceli" olur. Protokol tamamlanmadan raporun 3, 5, 11 ve 12. bölümleri
üretilmez. Zaman çizgisi ve çıkar haritası satırları da doğrulayıcıdan geçer.

### Aktör kütüphanesi

- **Katman 2 — profiller** (`aktorler/*.toml`): çıkarlar, kırmızı çizgiler, tipik hamleler, anlatı kalıpları.
  Her kayıt en az bir kaynak (url + tarih) ve profil bir gözden geçirme tarihi taşır. Aktif profilde kaynaksız
  kayıt varsa yükleyici reddeder; taslak profiller raporlara girmez. Özel kişi profili tutulmaz.
- **Katman 1 — tepki fonksiyonları**: GDELT olay verisi benzeri tablodan
  P(B, N gün içinde A'ya X yapar | A, B'ye Y yaptı) ile taban oranı; her sonuç n ve Wilson %95 güven aralığı
  taşır, n < 20 "yetersiz" işaretlenir. İlişki ölçüsüdür, nedensellik değildir.

### Rapor (14 bölüm)

Soru ve kapsam · Özet bulgular · Olayın gelişimi · Aktörler · Bağlantılar · Resmi anlatı · Ana akım medyanın
senaryosu · Senaryonun zayıf noktaları · Manipülasyon göstergeleri · Suç isnatları · İsnadın olası amaçları ·
Olayın kök nedenleri · İstatistiksel bağlam · Yöntem, kapsam, kaynaklar.

Başlıkta veri anlık görüntüsü, git commit, kod kitabı sürümü ve yayın grubu başına kapsam yer alır. "Eksik veri"
bölümü zorunludur ve otomatik doldurulur (ölçülmemiş kapsam, eksik protokol adımları, henüz olmayan modüller,
kanıtı olmayan bölümler, reddedilen cümle sayısı, GDELT sınırları). GDELT atfı başta ve sonda bulunur.
Bu sürümde 5. bölüm (ilişki grafiği) ve 9. bölüm (manipülasyon göstergesi modülleri) henüz ölçülmez; rapor
bunu açıkça yazar ve gösterge uydurmaz.

## 3. Uzman analiz akışı

Sağlayıcı `MEDYA_LLM_SAGLAYICI` ile seçilir: `anthropic` | `openai` | `gemini` | `offline` (varsayılan).
Anthropic çağrıları `llm/butce.py` üzerinden geçer (aylık ve çalışma tavanı, harcama defteri). OpenAI/Gemini için
fiyat `llm/butce.py`'de tanımlı değilse çağrı yalnızca `MEDYA_FIYATSIZ_IZIN=1` ile yapılır. Anahtarlar yalnızca
ortam değişkeninden okunur. `offline` sağlayıcı ağsız ve deterministiktir; testler ve anahtarsız deneme içindir.

1. **hipotez_uret** — vaka tanımı ve bağlam çıktısından rakip hipotez **önerileri**: resmi tez, alternatif,
   yapısal/jeopolitik (bölgesel savaş dinamikleri, silahlı gruplar üzerindeki baskı), dış konjonktür (büyük güç
   pazarlığı, diplomatik takvim) ve masum açıklamalar. Her biri için destekleyecek/çürütecek kanıt, kaynak türleri
   ve arama sorguları. Çıktı **"öneri — kanıt aranacak"** etiketlidir; eksik tür varsa bildirilir. Ön kayda
   alınması analistin kararıdır.
2. Analist kanıt toplar, kartları derecelendirir, hipotezleri ön kaydeder, matrisi doldurur.
3. **bolum_yaz** — model yalnızca bölüm için seçilmiş kartları + ACH + bağlam çıktısını görür; cümleleri JSON
   olarak yazar (olasılık dili, bilinmeyeni açıkça söyleme, resmi açıklamayı iddia olarak aktarma, dış aktörler ve
   teşvikler). Bütün çıktı doğrulayıcıdan geçer.
4. **kirmizi_takim** — ayrı bir oturumda öne çıkan hipotezi çürütmeye çalışır; yanıtları analist yazar.

İstemler: `medya/uzman/istemler/` (`ortak_kurallar.md`, `hipotez_uret.md`, `bolum_yaz.md`, `arastirma_plani.md`,
`kirmizi_takim.md`).

## 4. Ek sorular (derinleştirme)

1. `soru ekle` — soru `S1, S2 …` kimliği ve zaman damgasıyla saklanır.
2. Uzman katmanı araştırma planı önerir: alt hipotezler, kanıt ihtiyacı, kaynak ve sorgular, etkilenen bölümler.
3. Yeni kartlar soruya bağlanarak eklenir (`soru isle … --kanit kartlar.json`).
4. Etkilenen bölümler yeniden yazılır, "Ek soru N" bölümü eklenir; diğer bölümler önceki sürümden alınır ama
   **her cümle yeniden doğrulanır**.
5. Yeni sürüm değişiklik günlüğüyle kaydedilir (`raporlar/vN.json` + `vN.md`); eski sürümler değiştirilmez.
   Yeni sürüm taslak olarak başlar ve yeniden onay ister.

## 5. Çalıştırma

```bash
python3 -m venv venv
venv/bin/pip install -r requirements-platform.txt
venv/bin/python -m pytest -q                       # ağsız testler

# Sentetik örnekle uçtan uca
venv/bin/python -m medya ornek kur
venv/bin/python -m medya baglam ornek-liman
venv/bin/python -m medya ach goster ornek-liman
venv/bin/python -m medya rapor uret ornek-liman
venv/bin/python -m medya rapor dogrula ornek-liman
venv/bin/python -m medya onayla ornek-liman --onaylayan "Ad Soyad" --tarih 2026-10-26
venv/bin/python -m medya soru ekle ornek-liman "Olaydan önce limanda denetim yapıldı mı?"
venv/bin/python -m medya soru isle ornek-liman S1 --kanit yeni_kartlar.json

# Yeni vaka
venv/bin/python -m medya vaka yeni ankara-2016 --ad "…" --soru "…" --olay-tarihi 2016-12-19
venv/bin/python -m medya hipotez oner ankara-2016            # öneri — kanıt aranacak
venv/bin/python -m medya hipotez kaydet ankara-2016 hipotezler.json   # KANITTAN ÖNCE
venv/bin/python -m medya kanit ice-aktar ankara-2016 kartlar.json
venv/bin/python -m medya ach degerlendir ankara-2016 --kanit k-… --hipotez H1 --deger Ç
venv/bin/python -m medya vaka kapsam-onayla ankara-2016 --onaylayan "…"

# Arayüz (panelle birlikte; sayfa kenar çubuğunda "vaka raporu" olarak görünür)
venv/bin/streamlit run app.py
```

Ortam değişkenleri: `MEDYA_KANIT_DB`, `MEDYA_CALISMA`, `MEDYA_LLM_SAGLAYICI`, `MEDYA_LLM_MODEL`,
`MEDYA_FIYATSIZ_IZIN`, `LLM_AYLIK_TAVAN`, `LLM_CALISMA_TAVANI`, `LLM_FIYAT_DOSYASI`, `OPENAI_API_KEY`,
`GEMINI_API_KEY`/`GOOGLE_API_KEY`, `ANTHROPIC_API_KEY`, `MEDYA_GDELT_HAM`, `MEDYA_ARAMA_URL`,
`MEDYA_ARAMA_ANAHTAR`, `PANEL_PAROLA_OZETI`.

## 6. Vaka paketi → rapor (Karlov örneği)

Bir vaka paketi `vakalar/<vaka>/` altında durur:

```
vakalar/karlov/
  vaka.yaml          olay tarihi, anonimleştirme kuralları, şema ayarları, araştırma değişkenleri,
                     rapor künyesi (kapak, başlıklar, kaynak tabanı sınıf kuralları, kart dizini etiketleri)
  kartlar/           kanitlar.json (K) · kronoloji.json (KR) · rusya_dunya.json (R) ·
                     radikallesme_kartlar.json (RD) · hipotezler.json (ön kayıt)
  gdelt.yaml         GDELT sorgusu: tarih aralığı, ad/URL kalıpları, çerçeve sözlüğü, gösterge eşikleri
  gdelt/             hesaplanmış istatistik.json + gunluk.png + saatlik.png (ham veri depoda değil)
  ach_matris.yaml    tanısal kanıt satırları (E01…), hipotez sırası, kaynak × bilgi ağırlıkları
  celiskiler.yaml    kaynaklar arası çelişki kayıtları (kartlara bağlı)
  anlati/            çevrimdışı anlatı: <sıra>_<bölüm>.md (yer tutucularla)
  kaynaklar/         kavram notu (literatür künyeli)
  referans/          elle derlenmiş rapor ve GDELT çıktıları (yalnızca eşleşme testleri)
```

```bash
# Kart klasörünü çalışma alanındaki bir vakaya aktar (K/KR/R/RD şemaları; KR-001, K24 … kimlikleri korunur)
python -m medya vaka-ice-aktar vakalar/karlov/kartlar karlov

# GDELT: indir (yalnızca ilk kez; devam ettirilebilir), tara (önbellekli), istatistik + grafik
python -m medya gdelt indir karlov --paralel 8          # ham veri: MEDYA_GDELT_HAM ya da gdelt.yaml > ham_veri
python -m medya gdelt tara karlov --en-fazla 600        # büyük veride parça parça
python -m medya gdelt istatistik karlov                 # vakalar/karlov/gdelt/istatistik.json + PNG

# Araştırma protokolü
python -m medya arastirma baslat yeni-vaka --hipotezler hipotezler.json --dizin is/   # ön kayıt + görevler
python -m medya arastirma al yeni-vaka is/                                           # doldurulan kartlar
python -m medya arastirma kapsam karlov                                              # beş hat denetimi

# Rapor
python -m medya vaka-rapor karlov --cevrimdisi                  # anlatı anlati/'dan; MD + HTML + PDF
python -m medya vaka-rapor karlov --saglayici openai --tavan-usd 2   # anlatı LLM'den, cümle cümle doğrulanır
# Çıktı: data/raporlar/<vaka>/<dosya_adi>.{md,html,pdf} + rapor_ozeti.json (kapsam, uyarılar, düşürülen cümleler)
```

### GDELT modülü (`medya/gdelt`)

- **İndirici:** masterfile listesi (ya da zaman damgası üretimi) → 15 dakikalık `translation`/`english` GKG
  dosyaları; satırlar `srclc:tur` ve/veya `.tr` alan adıyla süzülür, GCAM alanı boşaltılır. Durum
  `_durum.json`'da tutulur; ikinci çalıştırma yalnızca eksik/hatalı dosyaları ister; boş dosya da kaydedilir.
- **Vaka sorgusu:** geniş küme = ad alanlarında (kişi, kurum, başlık) ad kalıbı; çekirdek küme = geniş ∩ URL
  kalıbı, URL'ye göre tekil. URL kalıbının tek başına yakaladığı site-geneli gürültü ayrıca sayılır ve uyarılır.
- **İstatistik:** günlük hacim ve Türkçe arşivdeki pay, saatlik eğri (UTC ve yerel saat), izlenen yayınların ilk
  haber zamanı, yayın grupları (`KEY_OUTLETS` kopyası; "rejim kontrolünde olmayan kaynaklar"), ton, kopya-slug
  kümeleri, çerçeve sayımları.
- **Çerçeve sözlüğü** vaka ayarındadır (`gdelt.yaml > cerceveler`). URL yüzde kodlaması çözülür, Türkçe katlanır,
  harf/rakam dışı her şey `-` olur; kalıplar `-` ile başlamak zorundadır (sözcük başı sınırı). Böylece
  "dışişleri" içindeki "isis" ya da "saldırısıdır" içindeki "isid" çerçeve sayılmaz (test:
  `test_cerceve_sozcuk_siniri_alt_dize_hatasini_engeller`). Joker (`.{1,8}`) kullanılamaz.
- **Göstergeler** (aday, hüküm değil; her biri masum açıklamasıyla): sessizlik (çerçevenin bir grupta
  beklenenden az görünmesi), eşzamanlı söylem (aynı slug ya da aynı çerçeve aynı 15 dk dosyasında ≥3 sitede),
  atıf aklama adayı (çerçevenin ilk dosyasında yabancı kaynağa atıf kalıbı, ör. `-rus-ajansi-`).
- Karlov eşleşmesi: FETÖ/Gülen 217, çekirdek 4.185 haber, 211 site, hükümete yakın 322 haberde FETÖ 44 /
  cihatçı 3, muhalif/bağımsız 276 haberde 14 / 14; günlük, saatlik, ilk haber, ton, kopya-slug ve grafikler
  referansla birebir (ham veri yoksa ham veriden yeniden hesap testi atlanır, kayıtlı istatistik testi çalışır).

### LLM yazım katmanı (`medya/uzman/yazim.py`)

- Sabit sistem istemi: `medya/uzman/istemler/rapor_yazim.md`. Kurallar: yalnızca verilen kartlar; cümle türü
  `[O]`/`[D]`/`[S]`; her olgu kart kimliğine bağlı; resmî açıklama kurum iddiası; hipotezler nötr H1…Hn ve
  kişiye atfedilmez; "rejim kontrolünde olmayan kaynaklar" (Gülen cemaati iddiası yasak); özel kişiler rolüyle;
  rapor sürümü anlatılmaz; "Bu rapor ne değildir" bölümü yazılmaz.
- Bölüm başına yalnızca o bölüme seçilen kartlar (ve GDELT / kavram notu / ACH satırları için sözde kartlar)
  modele gider. Dönen her cümle kural denetiminden ve doğrulayıcıdan geçer; geçmeyen düşürülür ve
  `rapor_ozeti.json`'da nedeniyle listelenir.
- Sağlayıcılar: `anthropic`, `openai`, `gemini` (anahtar yalnızca ortamdan: `ANTHROPIC_API_KEY`,
  `OPENAI_API_KEY`, `GEMINI_API_KEY`/`GOOGLE_API_KEY`; yoksa çağrıdan önce net hata).
- Bütçe: Claude fiyatları `llm/butce.py`'de; diğer modellerin fiyatları koda yazılmaz, `llm/fiyatlar.toml`'dan
  (`LLM_FIYAT_DOSYASI`) okunur. Dosya boş gelir: fiyatsız modelde uyarı verilir ve çağrı yalnızca
  `MEDYA_FIYATSIZ_IZIN=1` ile yapılır. `TokenSayaci` rapor başına token/USD tavanı uygular
  (`--tavan-usd`, `--tavan-token`).

### Araştırma protokolü (`medya/arastirma`)

Her vakada zorunlu beş hat (`protokol.yaml`): (a) dakika dakika kronoloji — TR/EN/RU + ilgili diller, çelişki
işaretiyle; (b) diğer aktörlerin tepkileri, kendi soruşturmaları ve mağdur yakınları; (c) her yeni kavram için
akademik açıklama + vakaya özgü süreç; (d) GDELT; (e) kanıt + ACH. Görev listesi şablonlardan ve vaka
değişkenlerinden (`vaka.yaml > arastirma`) üretilir, **hipotez ön kaydı olmadan üretilmez** (SHA-256 kilidi,
`on_kayit.json`). Arama: web adaptörü (`MEDYA_ARAMA_URL`, sonuçlar aday) ya da manuel/harici ajan modu
(görev JSON'u + kart şeması → doldurulan kart dosyaları içe aktarıcıdan). Kapsam denetçisi rapordan önce
çalışır: hat başına asgari kart, olay günü kronoloji eşiği, zorunlu tema (mağdur yakınları), kavram notu,
GDELT çekirdek kümesi, ön kayıt ve ACH satırı.

### Rapor motoru (`medya/rapor/vaka_raporu.py`)

Yapı: kapak + kaynak tabanı/okuma kılavuzu, yönetici özeti, kronoloji (4 alt dönem + çelişki tablosu), GDELT,
diğer aktörler, kavram, fail süreci, bağlam, hipotezler + ACH, kim kazandı, açık sorular, kaynak eleştirisi,
Ek A (kart dizini), Ek B (yöntem). Deterministik parçalar koddan üretilir (kapak, kaynak tabanı, KR tabloları,
çelişki tablosu, GDELT tabloları ve grafikleri, ACH matrisi ve ağırlıklı toplamlar, kart dizini); anlatı LLM'den
ya da `anlati/` dosyalarından gelir. Kapakta her zaman "Taslak — insan onayı bekliyor" ve GDELT atfı yazılır.
Gövdedeki her `[kimlik]` atfı kart olarak var olmalıdır. PDF: pandoc (`markdown-smart+raw_html`, numaralı,
içindekiler kapaktan sonra) + WeasyPrint, stil `medya/rapor/stil/style.css`.

Karlov çevrimdışı çıktısı referans raporla birebir test edilir (`tests/test_vaka_raporu.py`). Tek bilinen fark:
R50 (Hürriyet, 2017-06-03) — girdi dosyasında "yurt içi muhalif/bağımsız"; platform Hürriyet için 2018 öncesine
sahiplik düzeltmesini ("yurt içi ana akım (Doğan dönemi)†") tutarlı uygular, referans bu satırda uygulamamıştı.

## 7. Bilinen sınırlar

- Ad denetimi büyük harf ve kök eşleşmesine dayanır (çekim eki için sözcük sonundan en çok 4 harf kırpılır);
  küçük harfle yazılmış uydurma bir ad ya da yazıyla yazılmış büyük sayılar ("bin iki yüz") yakalanmayabilir.
  Doğrulayıcı uydurmayı zorlaştırır, insan onayının yerini tutmaz.
- Sessizlik, eşzamanlı söylem ve atıf aklama göstergeleri GDELT modülünde var (aday üretir); ilişki grafiği,
  değişiklik/silme ve gündem kaydırma modülleri yok.
- GDELT çerçeve sayımı URL'ye dayanır (2019 öncesinde başlık yok): başlığa/URL'ye taşınmayan çerçeveyi kaçırır.
- Çevrimdışı anlatı dosyaları elle derlenmiş metindir; motor yalnızca atıfları denetler, cümleleri yeniden
  doğrulamaz. LLM modunda her cümle doğrulanır.
- Doğrulayıcının kalıpları Python `re` ile çalışır; BigQuery/DuckDB'ye giden arama kalıpları gibi RE2 kısıtına
  tabi değildir (joker kullanılmaz, kelime başı sınırı korunur).
- `pages/` klasörü Streamlit'in çok sayfalı düzenini açar; Cloud Run imajı (`Dockerfile`) artık `medya/`,
  `pages/`, `vakalar/` ve `aktorler/`'i kopyalar, pandoc ve WeasyPrint'i kurar.

---
Veri kaynağı: [The GDELT Project](https://www.gdeltproject.org/). GDELT verisi açık ve ücretsizdir; bu platform
GDELT tarafından geliştirilmemiştir.
