"""GDELT grafikleri (PNG): günlük hacim + Türkçe arşivdeki pay; yerel saate çevrilmiş saatlik eğri.

Rapor (PDF) için üretilir; panelin Plotly/MK görsel dili burada geçerli değildir. Her grafiğin başlığında
veri kaynağı yazılır; rapordaki resim altyazısı GDELT atfını taşır.
"""
from pathlib import Path

RENK_CUBUK = "#4a6fa5"
RENK_VURGU = "#c0392b"


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams["font.family"] = "DejaVu Sans"
    return plt


def gunluk_grafik(ist: dict, yol: str | Path, ayar: dict | None = None) -> Path:
    ayar = ayar or {}
    plt = _plt()
    g = ist["gunluk"]
    gunler = list(g)
    deger = [g[d]["haber"] for d in gunler]
    pay = [g[d]["pay_yuzde"] for d in gunler]
    etiket = [f"{d[6:]}.{d[4:6]}" for d in gunler]
    fig, ax = plt.subplots(figsize=(8, 3.3))
    ax.bar(etiket, deger, color=RENK_CUBUK)
    ax.set_ylabel("Haber (çekirdek küme)", fontsize=8)
    ax2 = ax.twinx()
    ax2.plot(etiket, pay, color=RENK_VURGU, marker="o", ms=3)
    ax2.set_ylabel("Türkçe arşivdeki pay (%)", color=RENK_VURGU, fontsize=8)
    for n in ayar.get("gunluk_notlar", []):
        if n["gun"] in etiket:
            i = etiket.index(n["gun"])
            ax.annotate(n["metin"], (i, deger[i]), xytext=(i + 0.8, deger[i] + n.get("dy", 300)), fontsize=7,
                        arrowprops=dict(arrowstyle="->", lw=.6))
    plt.setp(ax.get_xticklabels(), rotation=70, fontsize=7)
    ax.set_title(ayar.get("gunluk_baslik", "Günlük hacim (GDELT GKG 2.1)"), fontsize=9)
    fig.tight_layout()
    Path(yol).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(yol, dpi=200)
    plt.close(fig)
    return Path(yol)


def saatlik_grafik(ist: dict, yol: str | Path, ayar: dict | None = None) -> Path:
    """Yerel saatle saatlik eğri. Başlangıç: kümenin ilk saati; uzunluk `saatlik_saat_sayisi` (varsayılan 30)."""
    ayar = ayar or {}
    plt = _plt()
    h = ist["saatlik_yerel"]
    anahtarlar = list(h)[:int(ayar.get("saatlik_saat_sayisi", 30))]
    fig, ax = plt.subplots(figsize=(8, 3.1))
    ax.plot(range(len(anahtarlar)), [h[k] for k in anahtarlar], marker="o", ms=3, color=RENK_CUBUK)
    ax.set_xticks(range(len(anahtarlar)))
    ax.set_xticklabels([f"{k[6:8]}.{k[4:6]} {k[9:]}:00" for k in anahtarlar], rotation=70, fontsize=6.5)
    ax.set_ylabel("Haber / saat", fontsize=8)
    ax.set_title(ayar.get("saatlik_baslik", "Saatlik hacim (yerel saat)"), fontsize=9)
    for n in ayar.get("saatlik_notlar", []):
        if n["saat"] in anahtarlar:
            k = anahtarlar.index(n["saat"])
            ax.axvline(k, color=RENK_VURGU, lw=.6, ls="--")
            ax.text(k + .2, n.get("y", 0), n["metin"], fontsize=7, color=RENK_VURGU)
    fig.tight_layout()
    Path(yol).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(yol, dpi=200)
    plt.close(fig)
    return Path(yol)
