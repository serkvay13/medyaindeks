# Medya İndeksi paneli — Cloud Run kapsayıcısı.
#
# Neden Cloud Run: Streamlit Community Cloud tek süreç, 0,078–2 çekirdek ve 690 MB–2,7 GB aralığında
# kaynak veriyor ve 12 saatte bir uyuyor. 11 test kullanıcısında bu sınırlar bağlayıcı hâle geldi
# (ölçüm: YARDIM.md §13 "Eşzamanlı kullanım ve bellek").
#
# app.py'de HİÇBİR değişiklik gerekmedi. İki şey çevreden gelir:
#   - Port: Cloud Run $PORT verir (varsayılan 8080).
#   - Kimlik: .streamlit/secrets.toml imaja KONULMAZ; bq_credentials() secrets bulamayınca None döner
#     ve Google istemcisi ADC'ye düşer — Cloud Run'da bu, servise bağlı hesabın kimliğidir.
#
# Yerel arşiv imajda yoktur; panel otomatik olarak bulut arşivine (BigQuery, Storage Read) düşer.
#
# Kanıta bağlı analiz platformu (medya/) da imajdadır: vaka raporu sayfası (pages/), vaka paketleri (vakalar/),
# aktör tanımları (aktorler/) ve PDF üretimi (pandoc + WeasyPrint, DejaVu yazı tipleri). GDELT ham verisi
# imaja girmez; vaka paketlerindeki hesaplanmış istatistik (vakalar/<vaka>/gdelt/istatistik.json) yeterlidir.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# PDF raporu için sistem araçları: pandoc (Markdown → HTML), WeasyPrint'in Pango/HarfBuzz kütüphaneleri,
# Türkçe karakterli DejaVu yazı tipleri
RUN apt-get update \
    && apt-get install -y --no-install-recommends pandoc libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 \
       fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıklar önce: kod değişince katman yeniden kurulmaz
COPY requirements.txt requirements-platform.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-platform.txt

# Yalnızca panelin ihtiyacı olanlar
COPY app.py ./
COPY .streamlit/config.toml ./.streamlit/
COPY assets/ ./assets/
COPY yasal/ ./yasal/
# app.py bunları sys.path üzerinden içe alır (sapma: gündem sapmaları, adlar: Türkçe ad eşleştirmesi)
COPY pipeline/sapma.py pipeline/adlar.py ./pipeline/

# Analiz platformu: paket, Streamlit sayfası, vaka paketleri, aktör tanımları; LLM bütçe modülü (fiyat
# yapılandırması dahil; anahtarlar imaja girmez, ortam değişkeninden gelir)
COPY medya/ ./medya/
COPY pages/ ./pages/
COPY vakalar/ ./vakalar/
COPY aktorler/ ./aktorler/
COPY llm/__init__.py llm/butce.py llm/fiyatlar.toml ./llm/

# Cloud Run sağlık denetimi $PORT'a bağlanmayı bekler
EXPOSE 8080
# enableCORS kapatılmaz: Streamlit'in kendi uyarısı, kapalıyken her kaynaktan WebSocket bağlantısı
# kabul edildiğini ve XSRF korumasının bunu durdurmadığını söylüyor. Cloud Run arkasında varsayılan
# (açık) ayar sorunsuz çalışıyor.
CMD streamlit run app.py \
    --server.port=${PORT:-8080} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableXsrfProtection=true
