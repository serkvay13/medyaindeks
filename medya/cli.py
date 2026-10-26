"""Komut satırı: python -m medya <komut> …

    python -m medya vaka yeni <id> --ad "…" --soru "…" --olay-tarihi YYYY-AA-GG
    python -m medya vaka liste | goster <id> | kapsam-onayla <id> --onaylayan "…" [--tarih …]
    python -m medya kanit ekle <vaka> --tur haber --url … --kurum … --ozet … --kaynak B --bilgi 2 [--alinti …] …
    python -m medya kanit ice-aktar <vaka> kartlar.json | disa-aktar <vaka> cikti.json | liste <vaka>
    python -m medya hipotez kaydet <vaka> hipotezler.json     # ön kayıt (kanıttan önce)
    python -m medya hipotez ekle <vaka> --id H6 --tur alternatif --metin "…"
    python -m medya hipotez oner <vaka>                       # uzman katmanı: öneri — kanıt aranacak
    python -m medya ach degerlendir <vaka> --kanit k-… --hipotez H1 --deger T|Ç|N [--gerekce …]
    python -m medya ach goster <vaka> | kirmizi-takim <vaka> [--dosya kt.json]
    python -m medya baglam <vaka> [--girdi baglam.json]
    python -m medya rapor uret <vaka> | dogrula <vaka> [--surum N] | goster <vaka> [--surum N]
    python -m medya soru ekle <vaka> "…" | isle <vaka> S1 [--kanit yeni_kartlar.json]
    python -m medya onayla <vaka> --surum N --onaylayan "…" --tarih YYYY-AA-GG
    python -m medya aktor dogrula [--dizin aktorler] | tepki --csv olaylar.csv --a TUR --b RUS --y 4 --x 3 [--gun 7]
    python -m medya ornek kur                                  # sentetik örnek vaka (deneme için)
    python -m medya vaka-ice-aktar <klasör> <vaka_id>          # K/KR/R/RD kart dosyalarını vakaya aktar
    python -m medya gdelt indir <vaka> [--paralel 8] | tara <vaka> [--en-fazla N] | istatistik <vaka>
    python -m medya vaka-rapor <vaka> --cevrimdisi [--cikti DİZİN] [--pdf-yok] [--kati]
    python -m medya vaka-rapor <vaka> --saglayici openai|gemini|anthropic [--tavan-usd 2] [--tavan-token N]
    python -m medya vaka-anlati-cikar <referans.md> <vaka>        # elle derlenmiş rapordan çevrimdışı anlatı
    python -m medya arastirma baslat <vaka> --hipotezler h.json --dizin <d> [--web] | al <vaka> <d> | kapsam <vaka>

Sağlayıcı: MEDYA_LLM_SAGLAYICI (offline varsayılan) · Depo: MEDYA_KANIT_DB · Çalışma alanı: MEDYA_CALISMA
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

import medya
from medya.aktor import profilleri_yukle, tepki_olasiligi
from medya.baglam import protokol_calistir
from medya.hipotez import Hipotez, KirmiziTakim
from medya.kanit import KanitDeposu, KanitKarti
from medya.rapor import markdown_uret, onayla, rapor_dogrula, rapor_uret
from medya.rapor.motor import _ek_adlar
from medya.uzman import hipotez_uret, kirmizi_takim_oner, saglayici_al
from medya.vaka import Vaka, kutuphane_yukle


def _profiller():
    try:
        return profilleri_yukle(yalniz_raporlanabilir=True)
    except Exception as e:  # bozuk profil raporu durdurmaz ama söylenir
        print(f"[UYARI] aktör profilleri yüklenemedi: {e}", file=sys.stderr)
        return []


def _yaz(x):
    print(json.dumps(x, ensure_ascii=False, indent=2, default=str))


def cmd_vaka(a):
    if a.alt == "yeni":
        v = Vaka.yeni(a.id, a.ad, a.soru, a.olay_tarihi, etiketler=a.etiket or [], yer=a.yer or "",
                      veri_anlik_goruntu=a.anlik or "")
        print(f"[OK] vaka oluşturuldu: {v.dizin}")
    elif a.alt == "liste":
        for v in Vaka.liste():
            print(v)
    elif a.alt == "goster":
        _yaz(Vaka(a.id).tanim)
    elif a.alt == "kapsam-onayla":
        v = Vaka(a.id)
        v.tanim_guncelle(kapsam_onayi={"onaylayan": a.onaylayan, "tarih": a.tarih or date.today().isoformat()})
        print("[OK] kapsam onaylandı")


def cmd_kanit(a):
    with KanitDeposu() as d:
        if a.alt == "ekle":
            Vaka(a.vaka).tanim  # vaka var mı
            k = KanitKarti(tur=a.tur, kaynak_url=a.url, kurum=a.kurum, ozet=a.ozet, alinti=a.alinti or "",
                           kaynak_derecesi=a.kaynak, bilgi_derecesi=a.bilgi, yayin_tarihi=a.yayin_tarihi or "",
                           olay_tarihi=a.olay_tarihi or "", yayin_grubu=a.grup or "",
                           yayin_grubu_tarihi=a.grup_tarihi or "", yayin_grubu_dayanak=a.grup_dayanak or "",
                           arsiv_url=a.arsiv_url or "", etiketler=a.etiket or [])
            yeni = d.ekle(k, vaka_id=a.vaka)
            print(f"[OK] {k.kanit_id} {'eklendi' if yeni else 'zaten vardı (vakaya bağlandı)'} — {k.baslik()}")
        elif a.alt == "ice-aktar":
            n, hatalar = d.ice_aktar(a.dosya, vaka_id=a.vaka)
            print(f"[OK] {n} kart eklendi")
            for h in hatalar:
                print(f"[RED] {h}")
        elif a.alt == "disa-aktar":
            print(f"[OK] {d.disa_aktar(a.vaka, a.dosya)} kart yazıldı: {a.dosya}")
        elif a.alt == "liste":
            for k in d.vaka_kartlari(a.vaka):
                print(f"{k.gorunen_id:<14}  {k.derece}  {k.tur:<18} {k.baslik()[:50]:<50} {k.ozet[:70]}")


def cmd_hipotez(a):
    v = Vaka(a.vaka)
    m = v.ach()
    if a.alt == "kaydet":
        liste = json.loads(Path(a.dosya).read_text(encoding="utf-8"))
        liste = liste.get("hipotezler", liste) if isinstance(liste, dict) else liste
        hs = [Hipotez(id=h["id"], metin=h["metin"], tur=h.get("tur", "diger"), oneren=h.get("oneren", "analist"),
                      destekleyici_gostergeler=h.get("destekleyici_gostergeler", []),
                      curutucu_gostergeler=h.get("curutucu_gostergeler", [])) for h in liste]
        ozet = m.on_kaydet(hs)
        v.ach_kaydet(m)
        print(f"[OK] {len(hs)} hipotez ön kaydedildi · {m.on_kayit['zaman']} · SHA-256 {ozet}")
    elif a.alt == "ekle":
        h = m.ekle(Hipotez(id=a.id, metin=a.metin, tur=a.tur))
        v.ach_kaydet(m)
        print(f"[OK] {h.id} eklendi" + (" — SONRADAN EKLENDİ (kanıt bağlandıktan sonra)" if h.sonradan_eklendi else ""))
    elif a.alt == "oner":
        sag = saglayici_al(a.saglayici)
        _yaz(hipotez_uret(sag, v.tanim, None))


def cmd_ach(a):
    v = Vaka(a.vaka)
    m = v.ach()
    with KanitDeposu() as d:
        kartlar = d.vaka_sozluk(a.vaka)
        if a.alt == "degerlendir":
            if a.kanit not in kartlar:
                raise SystemExit(f"Kanıt bu vakada yok: {a.kanit}")
            m.degerlendir(a.kanit, a.hipotez, a.deger, a.gerekce or "")
            v.ach_kaydet(m)
            print("[OK] kaydedildi")
        elif a.alt == "goster":
            print(m.matris_markdown(kartlar))
            print()
            for r in m.sirala(kartlar):
                print(f"{r['sira']}. {r['hipotez_id']} ({r['tur']}) çelişki={r['agirlikli_celiski']:.2f} "
                      f"tanısal tutarlılık={r['tanisal_tutarlilik']:.2f}{' [sonradan eklendi]' if r['sonradan_eklendi'] else ''}")
            print("\nSıralama en az çürütülen sırasıdır; hiçbir hipotez doğru kabul edilmez.")
        elif a.alt == "kirmizi-takim":
            if a.dosya:
                kt = json.loads(Path(a.dosya).read_text(encoding="utf-8"))
            else:
                lider = m.sirala(kartlar)[0]
                kt = kirmizi_takim_oner(saglayici_al(a.saglayici), lider, list(kartlar.values()),
                                        [{"kanit_id": k, "hipotez_id": h, **x} for (k, h), x in m.hucreler.items()])
                print("[BİLGİ] LLM önerisi kaydedildi; karşı argümanlara yanıtları analist yazmalı.")
            m.kirmizi_takim_ekle(KirmiziTakim(hipotez_id=kt["hipotez_id"], karsi_argumanlar=kt["karsi_argumanlar"],
                                              yapan=kt.get("yapan", "insan")))
            v.ach_kaydet(m)
            print("[OK] kırmızı takım kaydı eklendi")


def cmd_baglam(a):
    v = Vaka(a.vaka)
    if a.girdi:
        v.baglam_girdisi_kaydet(json.loads(Path(a.girdi).read_text(encoding="utf-8")))
    with KanitDeposu() as d:
        kartlar = d.vaka_sozluk(a.vaka)
    sonuc = protokol_calistir(v.baglam_girdisi(), v.tanim["olay_tarihi"], ach=v.ach(), kartlar=kartlar,
                              kutuphane=kutuphane_yukle())
    for ad in sonuc["adimlar"]:
        print(f"{ad['adim']:>2}. {ad['ad']:<28} {ad['durum']:<14} kanıt={len(ad['kanit_ids'])} "
              f"red={len(ad['reddedilen'])}  {' '.join(ad['notlar'])[:100]}")
    print(f"\nProtokol tamamlandı: {'evet' if sonuc['tamamlandi'] else 'hayır'}")


def cmd_rapor(a):
    v = Vaka(a.vaka)
    with KanitDeposu() as d:
        kartlar = d.vaka_sozluk(a.vaka)
        if a.alt == "uret":
            sorular = [s for s in v.sorular() if s["durum"] == "islendi"]
            r = rapor_uret(v, d, saglayici_al(a.saglayici), ek_sorular=sorular, profiller=_profiller())
            v.rapor_yaz(r, markdown_uret(r, kartlar))
            print(f"[OK] v{r['surum']} (taslak) · {sum(len(b['cumleler']) for b in r['bolumler'])} cümle, "
                  f"{len(r['reddedilenler'])} red · {v.dizin / 'raporlar' / ('v%d.md' % r['surum'])}")
        elif a.alt == "dogrula":
            r = v.rapor_oku(a.surum)
            rapor_dogrula(r, kartlar, _ek_adlar(v.ach(), _profiller()))
            v.rapor_yaz(r, markdown_uret(r, kartlar), uzerine=True)
            print(f"[OK] v{r['surum']} doğrulandı")
        elif a.alt == "goster":
            r = v.rapor_oku(a.surum)
            print(markdown_uret(r, kartlar) if r else "Rapor yok.")


def cmd_soru(a):
    from medya.derinlestir import soru_ekle, soru_isle
    v = Vaka(a.vaka)
    with KanitDeposu() as d:
        sag = saglayici_al(a.saglayici)
        if a.alt == "ekle":
            s = soru_ekle(v, a.metin, sag, d)
            print(f"[OK] {s['id']} kaydedildi ({s['zaman']}). Araştırma planı ({s['plan']['etiket']}):")
            _yaz(s["plan"])
        elif a.alt == "isle":
            kartlar = []
            if a.kanit:
                veri = json.loads(Path(a.kanit).read_text(encoding="utf-8"))
                kartlar = [KanitKarti.from_dict(x) for x in (veri.get("kartlar", veri) if isinstance(veri, dict) else veri)]
            r = soru_isle(v, a.soru_id, d, sag, kartlar, profiller=_profiller())
            print(f"[OK] v{r['surum']} üretildi")
            for x in r["degisiklikler"]:
                print("  - " + x)


def cmd_onayla(a):
    v = Vaka(a.vaka)
    with KanitDeposu() as d:
        kartlar = d.vaka_sozluk(a.vaka)
    r = v.rapor_oku(a.surum)
    if not r:
        raise SystemExit("Rapor yok")
    onayla(r, a.onaylayan, a.tarih)
    v.rapor_yaz(r, markdown_uret(r, kartlar), uzerine=True)
    print(f"[OK] v{r['surum']} onaylandı: {a.onaylayan}, {a.tarih}")


def cmd_aktor(a):
    if a.alt == "dogrula":
        for p in profilleri_yukle(a.dizin):
            durum = "raporlanabilir" if p.raporlanabilir else f"rapora girmez ({p.durum}, kaynaksız: {len(p.kaynaksiz)})"
            print(f"{Path(p.dosya).name:<40} {p.aktor[:40]:<40} {durum}")
    elif a.alt == "tepki":
        import pandas as pd
        df = pd.read_csv(a.csv)
        r = tepki_olasiligi(df, a.a, a.b, a.y, a.x, a.gun, sinif_kolonu=a.sinif)
        print(r)
        print(r.not_)
        print(medya.GDELT_ATTRIBUTION_DUZ)


def cmd_ornek(a):
    from medya.ornek_veri import ornek_kur
    with KanitDeposu() as d:
        v = ornek_kur(d)
    print(f"[OK] sentetik örnek vaka kuruldu: {v.id} ({v.dizin}). Sonra: python -m medya rapor uret {v.id}")


def cmd_vaka_ice_aktar(a):
    from medya.vaka_paketi import vakaya_aktar
    with KanitDeposu() as d:
        r = vakaya_aktar(a.klasor, a.vaka_id, d)
    print(f"[OK] {r['vaka']}: {r['kart']} kart ({r['yeni_kart']} yeni) · "
          + ", ".join(f"{ad} ({s})" for ad, s in r["dosyalar"].items()))
    if r["on_kayit"]:
        print(f"[OK] hipotezler ön kaydedildi · SHA-256 {r['on_kayit']['ozet']}")
    for u in r["uyarilar"]:
        print(f"[UYARI] {u}")
    for h in r["hatalar"]:
        print(f"[RED] {h}")


def cmd_gdelt(a):
    from medya import gdelt
    from medya.gdelt import grafik
    from medya.gdelt.indirici import indir
    from medya.gdelt.sorgu import VakaSorgusu
    from medya.vaka_paketi import VakaPaketi
    paket = VakaPaketi(a.vaka)
    ayar = paket.alt_ayar("gdelt")
    ham = Path(a.ham) if a.ham else gdelt.ham_dizin(ayar, a.vaka)
    if a.alt == "indir":
        r = indir(a.baslangic or ayar["baslangic"], a.bitis or ayar["bitis"], ham, akis=ayar.get("akis", "translation"),
                  dil=ayar.get("dil", "tur"), alan_soneki=ayar.get("alan_soneki", ".tr"), paralel=a.paralel)
        print(f"[OK] {ham}: {r.say()}")
    elif a.alt == "tara":
        r = VakaSorgusu.ayardan(ayar, ham).tara(en_fazla=a.en_fazla)
        print(f"[OK] {r['islenen']} dosya işlendi, {r['kalan']} kaldı (toplam {r['toplam']})")
    elif a.alt == "istatistik":
        ist, s = gdelt.vaka_istatistigi(ayar, a.vaka, ham)
        hedef = paket.yol("gdelt")
        gdelt.kaydet(ist, hedef / "istatistik.json")
        grafik.gunluk_grafik(ist, hedef / "gunluk.png", ayar.get("grafik"))
        grafik.saatlik_grafik(ist, hedef / "saatlik.png", ayar.get("grafik"))
        print(f"[OK] çekirdek {ist['tekil_url']} haber, {ist['tekil_site']} site; {hedef / 'istatistik.json'}")
        if ist["gurultu"]["uyari"]:
            print(f"[UYARI] {ist['gurultu']['uyari']}")
    print(medya.GDELT_ATTRIBUTION_DUZ)


def cmd_arastirma(a):
    from medya import arastirma as ar
    from medya.vaka_paketi import VakaPaketi, vakaya_aktar
    paket = VakaPaketi(a.vaka)
    if a.alt == "baslat":
        d = Path(a.dizin)
        on_kayit_yolu = d / "on_kayit.json"
        if a.hipotezler:
            k = ar.on_kayit_kilitle(json.loads(Path(a.hipotezler).read_text(encoding="utf-8")), on_kayit_yolu,
                                    paket.ayar.get("hipotez_turleri"))
            print(f"[OK] hipotezler kilitlendi · {k['zaman']} · SHA-256 {k['ozet']}")
        if not on_kayit_yolu.exists():
            raise SystemExit("Hipotez ön kaydı yok: --hipotezler ile kilitleyin (kanıttan önce).")
        gorevler = ar.gorev_listesi(paket.ayar, on_kayit=on_kayit_yolu)
        sag = ar.ManuelSaglayici(d)
        yol = sag.gorevleri_yaz(gorevler, a.vaka)
        print(f"[OK] {len(gorevler)} görev yazıldı: {yol}")
        if a.web:
            sonuc = ar.WebAramaSaglayici().gorevleri_calistir(gorevler)
            (d / "aday_sonuclar.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[OK] web araması: {sum(len(v) for v in sonuc.values())} aday (kart değildir; açılıp kartlaştırılmalı)")
    elif a.alt == "al":
        with KanitDeposu() as dp:
            r = vakaya_aktar(Path(a.dizin) / "kartlar", a.vaka, dp, ayar=paket.ayar)
        print(f"[OK] {r['kart']} kart alındı ({r['yeni_kart']} yeni)")
        for h in r["hatalar"]:
            print(f"[RED] {h}")
    elif a.alt == "kapsam":
        from medya.rapor.vaka_raporu import kapsam_raporu
        r = kapsam_raporu(paket)
        print(r.markdown())
        print("\nKapsam tamam." if r.tamam else "\nEksikler:\n" + "\n".join(f"- {e}" for e in r.eksikler))


def cmd_vaka_rapor(a):
    from medya.rapor.vaka_raporu import vaka_raporu_uret
    sag = sayac = None
    if not a.cevrimdisi:
        from llm.butce import TokenSayaci
        from medya.uzman import saglayici_al
        sayac = TokenSayaci(tavan_usd=a.tavan_usd, tavan_token=a.tavan_token)
        sag = saglayici_al(a.saglayici, sayac=sayac)
    s = vaka_raporu_uret(a.vaka, cevrimdisi=a.cevrimdisi, saglayici=sag, cikti=a.cikti, pdf=not a.pdf_yok,
                         kati=a.kati, sayac=sayac)
    print(s.kapsam.markdown())
    for e in s.kapsam.eksikler:
        print(f"[KAPSAM] {e}")
    for u in s.uyarilar:
        print(f"[UYARI] {u}")
    if s.reddedilenler:
        print(f"[RED] doğrulayıcı {len(s.reddedilenler)} cümleyi düşürdü (rapor_ozeti.json)")
    print(f"[OK] {s.md}" + (f" · {s.pdf} ({s.sayfa} sayfa)" if s.pdf else "") + f" · {s.kullanilan_kart} kart atıflı")
    print("Taslak — insan onayı bekliyor. " + medya.GDELT_ATTRIBUTION_DUZ)


def cmd_vaka_anlati_cikar(a):
    from medya.rapor.sablon import anlati_cikar, anlati_yaz
    from medya.vaka_paketi import VakaPaketi
    paket = VakaPaketi(a.vaka)
    g = anlati_cikar(Path(a.referans).read_text(encoding="utf-8"),
                     {"gunluk": "gdelt_gunluk.png", "saatlik": "gdelt_saatlik.png"})
    g.pop("_basliklar")
    for p in anlati_yaz(g, paket.yol("anlati")):
        print(f"[OK] {p}")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m medya", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--saglayici", default=None, help="anthropic | openai | gemini | offline")
    s = p.add_subparsers(dest="komut", required=True)

    v = s.add_parser("vaka").add_subparsers(dest="alt", required=True)
    x = v.add_parser("yeni")
    x.add_argument("id")
    x.add_argument("--ad", required=True)
    x.add_argument("--soru", required=True)
    x.add_argument("--olay-tarihi", required=True)
    x.add_argument("--etiket", action="append")
    x.add_argument("--yer")
    x.add_argument("--anlik", help="veri anlık görüntüsü tarihi")
    v.add_parser("liste")
    x = v.add_parser("goster")
    x.add_argument("id")
    x = v.add_parser("kapsam-onayla")
    x.add_argument("id")
    x.add_argument("--onaylayan", required=True)
    x.add_argument("--tarih")

    k = s.add_parser("kanit").add_subparsers(dest="alt", required=True)
    x = k.add_parser("ekle")
    x.add_argument("vaka")
    for ad in ("--tur", "--url", "--kurum", "--ozet", "--kaynak", "--bilgi"):
        x.add_argument(ad, required=True)
    for ad in ("--alinti", "--yayin-tarihi", "--olay-tarihi", "--grup", "--grup-tarihi", "--grup-dayanak",
               "--arsiv-url"):
        x.add_argument(ad)
    x.add_argument("--etiket", action="append")
    for ad in ("ice-aktar", "disa-aktar"):
        x = k.add_parser(ad)
        x.add_argument("vaka")
        x.add_argument("dosya")
    x = k.add_parser("liste")
    x.add_argument("vaka")

    h = s.add_parser("hipotez").add_subparsers(dest="alt", required=True)
    x = h.add_parser("kaydet")
    x.add_argument("vaka")
    x.add_argument("dosya")
    x = h.add_parser("ekle")
    x.add_argument("vaka")
    x.add_argument("--id", required=True)
    x.add_argument("--tur", required=True)
    x.add_argument("--metin", required=True)
    x = h.add_parser("oner")
    x.add_argument("vaka")

    c = s.add_parser("ach").add_subparsers(dest="alt", required=True)
    x = c.add_parser("degerlendir")
    x.add_argument("vaka")
    x.add_argument("--kanit", required=True)
    x.add_argument("--hipotez", required=True)
    x.add_argument("--deger", required=True)
    x.add_argument("--gerekce")
    x = c.add_parser("goster")
    x.add_argument("vaka")
    x = c.add_parser("kirmizi-takim")
    x.add_argument("vaka")
    x.add_argument("--dosya")

    x = s.add_parser("baglam")
    x.add_argument("vaka")
    x.add_argument("--girdi")

    r = s.add_parser("rapor").add_subparsers(dest="alt", required=True)
    x = r.add_parser("uret")
    x.add_argument("vaka")
    for ad in ("dogrula", "goster"):
        x = r.add_parser(ad)
        x.add_argument("vaka")
        x.add_argument("--surum", type=int)

    q = s.add_parser("soru").add_subparsers(dest="alt", required=True)
    x = q.add_parser("ekle")
    x.add_argument("vaka")
    x.add_argument("metin")
    x = q.add_parser("isle")
    x.add_argument("vaka")
    x.add_argument("soru_id")
    x.add_argument("--kanit")

    x = s.add_parser("onayla")
    x.add_argument("vaka")
    x.add_argument("--surum", type=int)
    x.add_argument("--onaylayan", required=True)
    x.add_argument("--tarih", required=True)

    ak = s.add_parser("aktor").add_subparsers(dest="alt", required=True)
    x = ak.add_parser("dogrula")
    x.add_argument("--dizin")
    x = ak.add_parser("tepki")
    x.add_argument("--csv", required=True)
    x.add_argument("--a", required=True)
    x.add_argument("--b", required=True)
    x.add_argument("--y", required=True, help="A'nın B'ye karşı tetik sınıfı")
    x.add_argument("--x", required=True, help="B'nin A'ya karşı tepki sınıfı")
    x.add_argument("--gun", type=int, default=7)
    x.add_argument("--sinif", default="QuadClass")

    o = s.add_parser("ornek").add_subparsers(dest="alt", required=True)
    o.add_parser("kur")

    gd = s.add_parser("gdelt", help="GDELT ham veri: indir, tara, istatistik").add_subparsers(dest="alt", required=True)
    for ad in ("indir", "tara", "istatistik"):
        x = gd.add_parser(ad)
        x.add_argument("vaka")
        x.add_argument("--ham", help="ham veri dizini (varsayılan: MEDYA_GDELT_HAM ya da vaka ayarı)")
        if ad == "indir":
            x.add_argument("--baslangic")
            x.add_argument("--bitis")
            x.add_argument("--paralel", type=int, default=8)
        if ad == "tara":
            x.add_argument("--en-fazla", type=int, default=None)

    x = s.add_parser("vaka-rapor", help="vaka paketinden rapor (MD + HTML + PDF)")
    x.add_argument("vaka")
    x.add_argument("--cevrimdisi", action="store_true", help="anlatıyı LLM yerine vakalar/<vaka>/anlati/'dan al")
    x.add_argument("--saglayici", default=None, help="openai | gemini | anthropic (varsayılan MEDYA_LLM_SAGLAYICI)")
    x.add_argument("--cikti", default=None)
    x.add_argument("--pdf-yok", action="store_true")
    x.add_argument("--kati", action="store_true", help="kapsam eksikse rapor üretme")
    x.add_argument("--tavan-usd", type=float, default=None)
    x.add_argument("--tavan-token", type=int, default=None)
    x = s.add_parser("vaka-anlati-cikar", help="elle derlenmiş rapordan çevrimdışı anlatı dosyaları")
    x.add_argument("referans")
    x.add_argument("vaka")

    ar = s.add_parser("arastirma", help="araştırma protokolü: ön kayıt, görevler, kapsam").add_subparsers(
        dest="alt", required=True)
    x = ar.add_parser("baslat")
    x.add_argument("vaka")
    x.add_argument("--dizin", required=True)
    x.add_argument("--hipotezler", help="hipotezler.json (kart toplamadan önce kilitlenir)")
    x.add_argument("--web", action="store_true", help="MEDYA_ARAMA_URL ile web araması da yap")
    x = ar.add_parser("al")
    x.add_argument("vaka")
    x.add_argument("dizin")
    x = ar.add_parser("kapsam")
    x.add_argument("vaka")

    x = s.add_parser("vaka-ice-aktar", help="kart klasörünü (K/KR/R/RD şemaları) vakaya aktar")
    x.add_argument("klasor")
    x.add_argument("vaka_id")
    return p


KOMUTLAR = {"vaka": cmd_vaka, "kanit": cmd_kanit, "hipotez": cmd_hipotez, "ach": cmd_ach, "baglam": cmd_baglam,
            "rapor": cmd_rapor, "soru": cmd_soru, "onayla": cmd_onayla, "aktor": cmd_aktor, "ornek": cmd_ornek,
            "vaka-ice-aktar": cmd_vaka_ice_aktar, "gdelt": cmd_gdelt, "arastirma": cmd_arastirma,
            "vaka-rapor": cmd_vaka_rapor, "vaka-anlati-cikar": cmd_vaka_anlati_cikar}


def main(argv=None):
    a = parser().parse_args(argv)
    KOMUTLAR[a.komut](a)


if __name__ == "__main__":
    main()
