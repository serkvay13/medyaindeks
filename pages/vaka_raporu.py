"""Vaka raporu sayfası: kanıta bağlı olay raporu, ACH matrisi, kanıt kartları, reddedilen cümleler ve ek sorular.

app.py'den bağımsızdır (app.py'ye dokunulmadı). Aynı `medya/` paketini ve kanıt deposunu kullanır.
Parola kapısı app.py ile aynı kurala uyar: PANEL_PAROLA_OZETI tanımlıysa veri okunmadan önce sorulur
(çok sayfalı uygulamada bu sayfaya doğrudan adresle gelinebildiği için kapı burada da vardır).
LLM sağlayıcısı MEDYA_LLM_SAGLAYICI ile seçilir; anahtar yoksa offline sağlayıcı kullanılır.
"""
import hashlib
import hmac
import html
import os
import sys
import time
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import medya  # noqa: E402
from medya.gorsel import mk_renkleri  # noqa: E402
from medya.kanit import KanitDeposu  # noqa: E402
from medya.kanit.kart import BILGI_DERECELERI, KAYNAK_DERECELERI, TURLER  # noqa: E402
from medya.vaka import Vaka  # noqa: E402

st.set_page_config(page_title="Vaka raporu · Medya İndeksi", page_icon=":material/fact_check:", layout="wide")
MK = mk_renkleri()
st.markdown(
    f"""<style>
    .mk-note {{ font-size: .78rem; color: {MK["muted"]}; border-left: 3px solid {MK["amber"]};
        padding: .3rem .6rem; margin: .4rem 0 .8rem 0; background: {MK["surface"]}; }}
    .mk-kicker {{ font-family: "IBM Plex Mono", monospace; text-transform: uppercase; letter-spacing: .14em;
        font-size: .74rem; color: {MK["red"]}; }}
    .mk-iddia {{ color: {MK["amber_text"]}; font-weight: 600; }}
    </style>""",
    unsafe_allow_html=True,
)


def not_kutusu(metin: str, baslik: str = "Veri notu.") -> None:
    st.markdown(f'<div class="mk-note"><b>{html.escape(baslik)}</b> {html.escape(metin)}</div>', unsafe_allow_html=True)


# --------------------------------------------------------------------------------
# PAROLA KAPISI (app.py ile aynı kural)
# --------------------------------------------------------------------------------
PAROLA_OZETI = os.environ.get("PANEL_PAROLA_OZETI", "").strip().lower()


def parola_kapisi() -> bool:
    if not PAROLA_OZETI or st.session_state.get("girildi"):
        return True
    not_kutusu("Panel şu anda yalnızca davetli kullanıcılara açıktır. Erişim parolanızı girin.", "Erişim.")
    girdi = st.text_input("Erişim parolası", type="password", key="parola_girdi_vaka")
    if st.button("Giriş", type="primary", key="parola_git_vaka"):
        deneme = int(st.session_state.get("parola_deneme", 0))
        if deneme >= 3:
            time.sleep(min(2 ** (deneme - 2), 8))
        if hmac.compare_digest(hashlib.sha256((girdi or "").encode()).hexdigest(), PAROLA_OZETI):
            st.session_state["girildi"] = True
            st.session_state.pop("parola_deneme", None)
            st.rerun()
        else:
            st.session_state["parola_deneme"] = deneme + 1
            st.error("Parola yanlış.")
    st.caption(medya.GDELT_ATTRIBUTION)
    return False


st.markdown('<div class="mk-kicker">Medya İndeksi · Vaka raporu</div>', unsafe_allow_html=True)
st.title("Kanıta bağlı olay raporu")
st.caption(medya.GDELT_ATTRIBUTION)
if not parola_kapisi():
    st.stop()

# --------------------------------------------------------------------------------
# SAĞLAYICI VE DEPO
# --------------------------------------------------------------------------------
from medya.uzman import saglayici_al  # noqa: E402

try:
    SAGLAYICI = saglayici_al()
except Exception as e:  # bilinmeyen ad vb.
    st.warning(f"LLM sağlayıcısı kurulamadı ({e}); offline sağlayıcı kullanılıyor.")
    SAGLAYICI = saglayici_al("offline")


def depo() -> KanitDeposu:
    """Her kullanımda açılıp kapanır: DuckDB dosyasına aynı anda tek yazıcı bağlanabilir."""
    from medya.kanit import varsayilan_yol
    return KanitDeposu(varsayilan_yol())


vakalar = Vaka.liste()
with st.sidebar:
    st.subheader("Vaka")
    if not vakalar:
        st.info("Kayıtlı vaka yok.")
        if st.button("Sentetik örnek vakayı kur", icon=":material/science:"):
            from medya.ornek_veri import ornek_kur
            with depo() as d:
                ornek_kur(d)
            st.rerun()
        st.stop()
    secili = st.selectbox("Vaka seçin", vakalar, key="vr_vaka")
    st.caption(f"LLM: {SAGLAYICI.ad}/{SAGLAYICI.model}")

vaka = Vaka(secili)
tanim = vaka.tanim
st.subheader(tanim["ad"])
st.markdown(f"**Soru:** {tanim['soru']}")

with depo() as d:
    kartlar = d.vaka_sozluk(vaka.id)

surumler = vaka.rapor_surumleri()
c1, c2 = st.columns([3, 1])
with c2:
    if st.button("Yeni rapor sürümü üret", icon=":material/description:", width="stretch"):
        from medya.aktor import profilleri_yukle
        from medya.rapor import markdown_uret, rapor_uret
        try:
            profiller = profilleri_yukle(yalniz_raporlanabilir=True)
        except Exception:
            profiller = []
        with depo() as d:
            sorular = [s for s in vaka.sorular() if s["durum"] == "islendi"]
            r = rapor_uret(vaka, d, SAGLAYICI, ek_sorular=sorular, profiller=profiller)
            vaka.rapor_yaz(r, markdown_uret(r, d.vaka_sozluk(vaka.id)))
        st.rerun()
with c1:
    if not surumler:
        st.info("Bu vaka için henüz rapor yok. Sağdaki düğmeyle ilk sürümü üretin.")
        rapor = None
    else:
        surum = st.selectbox("Rapor sürümü", list(reversed(surumler)), format_func=lambda s: f"v{s}", key="vr_surum")
        rapor = vaka.rapor_oku(surum)

if rapor:
    durum = {"taslak": "Taslak", "dogrulandi": "Doğrulandı", "onaylandi": "Onaylandı"}[rapor["durum"]]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Durum", durum)
    m2.metric("Cümle", sum(len(b["cumleler"]) for b in rapor["bolumler"]))
    m3.metric("Reddedilen", len(rapor["reddedilenler"]))
    m4.metric("Kanıt", len(rapor["kanit_ids"]))
    if rapor.get("onay"):
        st.success(f"Onaylayan: {rapor['onay']['onaylayan']} · {rapor['onay']['tarih']}", icon=":material/verified:")
    else:
        not_kutusu("Bu sürüm insan onayından geçmedi; yayımlanamaz. Onay: python -m medya onayla …", "Durum.")

sekmeler = st.tabs(["Rapor", "ACH matrisi", "Kanıt kartları", "Reddedilen cümleler", "Ek soru"])

# ---------------------------------------------------------------- Rapor
with sekmeler[0]:
    if rapor:
        md_yol = vaka.dizin / "raporlar" / f"v{rapor['surum']}.md"
        metin = md_yol.read_text(encoding="utf-8") if md_yol.exists() else ""
        st.download_button("Markdown indir", metin, file_name=f"{vaka.id}_v{rapor['surum']}.md",
                           icon=":material/download:")
        st.markdown(metin)
    else:
        st.write("Rapor yok.")

# ---------------------------------------------------------------- ACH
with sekmeler[1]:
    ach = vaka.ach()
    if not ach.hipotezler:
        st.write("Hipotez ön kaydı yok.")
    else:
        on = ach.on_kayit
        not_kutusu(f"Hipotezler {on.get('zaman', '—')} tarihinde, kanıt bağlanmadan önce kaydedildi "
                   f"(SHA-256 {on.get('ozet', '')[:16]}…). Sıralama en az çürütülen sırasıdır; hiçbir hipotez "
                   "doğru kabul edilmez. Ağırlık = Admiralty kaynak × bilgi derecesi.", "Yöntem notu.")
        sira = pd.DataFrame(ach.sirala(kartlar))
        if len(sira):
            st.dataframe(sira[["sira", "hipotez_id", "tur", "metin", "agirlikli_celiski", "celisen_kanit",
                               "tanisal_tutarlilik", "az_kanit", "sonradan_eklendi"]], width="stretch", hide_index=True)
        satirlar = []
        for kid in ach.kanit_idleri():
            k = kartlar.get(kid)
            satir = {"kanıt": kid, "kaynak": k.baslik() if k else "kart yok", "derece": k.derece if k else "—",
                     "tanısallık": ach.tanisallik(kid)}
            satir.update({h: ach.deger(kid, h) for h in ach.hipotezler})
            satirlar.append(satir)
        if satirlar:
            st.dataframe(pd.DataFrame(satirlar), width="stretch", hide_index=True)
        with st.expander("Hipotez metinleri"):
            for h in ach.hipotezler.values():
                st.markdown(f"**{h.id}** ({h.tur}{', sonradan eklendi' if h.sonradan_eklendi else ''}): {h.metin}")

# ---------------------------------------------------------------- Kanıt kartları
with sekmeler[2]:
    if not kartlar:
        st.write("Kanıt kartı yok.")
    else:
        df = pd.DataFrame([{"kimlik": k.kanit_id, "başlık": k.baslik(), "tür": TURLER[k.tur], "derece": k.derece,
                            "kaynak güvenilirliği": KAYNAK_DERECELERI[k.kaynak_derecesi],
                            "bilgi doğruluğu": BILGI_DERECELERI[k.bilgi_derecesi], "yayın": k.yayin_tarihi,
                            "olay": k.olay_tarihi, "grup": k.grup_metni(), "özet": k.ozet, "url": k.kaynak_url}
                           for k in kartlar.values()])
        st.dataframe(df, width="stretch", hide_index=True,
                     column_config={"url": st.column_config.LinkColumn("kaynak")})
        not_kutusu("Resmi açıklamalar \"<kurum> iddiası\" olarak gösterilir. Tüm kaynaklar aynı Admiralty "
                   "ölçeğiyle derecelendirilir: kaynak A–F, bilgi 1–6.")
        with st.expander("Kanıtı göster (alıntılar)"):
            for k in kartlar.values():
                st.markdown(k.markdown())

# ---------------------------------------------------------------- Reddedilenler
with sekmeler[3]:
    if not rapor or not rapor["reddedilenler"]:
        st.write("Bu sürümde reddedilen cümle yok.")
    else:
        st.dataframe(pd.DataFrame([{"bölüm": r["bolum"], "tür": r["cumle"]["tur"], "cümle": r["cumle"]["metin"],
                                    "kanıt": ", ".join(r["cumle"]["kanit_ids"]), "neden": "; ".join(r["nedenler"])}
                                   for r in rapor["reddedilenler"]]), width="stretch", hide_index=True)
        not_kutusu("Doğrulayıcıdan geçmeyen cümleler rapora girmez; bu liste analist içindir.")

# ---------------------------------------------------------------- Ek soru
with sekmeler[4]:
    st.markdown("Rapora bir soru ekleyin. Soru kimlik ve zamanla kaydedilir; uzman katmanı bir **araştırma planı** "
                "önerir (öneri — kanıt aranacak). Kanıt eklendikten sonra soru işlenir ve yeni bir rapor sürümü üretilir.")
    soru = st.text_area("Ek soru", key="vr_soru", placeholder="Örn. Olaydan önceki haftalarda bölgede ne değişti?")
    if st.button("Soruyu kaydet ve plan üret", icon=":material/add_comment:", disabled=not (soru or "").strip()):
        from medya.derinlestir import soru_ekle
        with depo() as d:
            try:
                s = soru_ekle(vaka, soru, SAGLAYICI, d)
                st.session_state["vr_son_soru"] = s["id"]
            except Exception as e:
                st.error(str(e))
    sorular = vaka.sorular()
    for s in reversed(sorular):
        with st.expander(f"{s['id']} · {s['durum']} · {s['zaman']}", expanded=s["id"] == st.session_state.get("vr_son_soru")):
            st.markdown(f"**Soru:** {s['metin']}")
            plan = s.get("plan") or {}
            st.caption(plan.get("etiket", ""))
            if plan.get("alt_hipotezler"):
                st.markdown("**Alt hipotezler**")
                for a in plan["alt_hipotezler"]:
                    st.markdown(f"- {a.get('id', '')}: {a.get('metin', '')} — destekler: {a.get('destekler', '')}; "
                                f"çürütür: {a.get('curutur', '')}")
            if plan.get("kanit_ihtiyaclari"):
                st.markdown("**Kanıt ihtiyacı**")
                for a in plan["kanit_ihtiyaclari"]:
                    st.markdown(f"- {a.get('aciklama', '')} ({a.get('kaynak_turu', '')})")
            if plan.get("kaynaklar_sorgular"):
                st.markdown("**Kaynak ve sorgular**")
                for a in plan["kaynaklar_sorgular"]:
                    st.markdown(f"- {a.get('kaynak_turu', '')}: `{a.get('sorgu', '')}`")
            if s["durum"] != "islendi" and surumler:
                if st.button("Soruyu işle (yeni sürüm)", key=f"isle_{s['id']}", icon=":material/update:"):
                    from medya.derinlestir import soru_isle
                    with depo() as d:
                        r = soru_isle(vaka, s["id"], d, SAGLAYICI)
                    st.success(f"v{r['surum']} üretildi: " + " · ".join(r["degisiklikler"]))
                    st.rerun()
            elif s["durum"] == "islendi":
                st.caption(f"İşlendi → v{s['rapor_surumu']}")
    not_kutusu("Soruya bağlı kanıt kartları komut satırından eklenir: python -m medya soru isle <vaka> <S…> "
               "--kanit kartlar.json. Kanıtsız işlenen soru, 'Eksik veri' bölümünde belirtilir.")

st.divider()
st.caption(medya.GDELT_ATTRIBUTION)
