"""Araştırma protokolü: her vaka için zorunlu beş hat, görev listesi, arama sağlayıcıları ve kapsam denetçisi.

    (a) dakika dakika kronoloji (TR/EN/RU + ilgili diller, çelişki işaretiyle)      → KR kartları
    (b) diğer aktörlerin tepkileri, kendi soruşturmaları, mağdur yakınları           → R kartları
    (c) her yeni kavram için akademik açıklama + vakaya özgü süreç                   → RD kartları + kavram notu
    (d) GDELT medya istatistikleri                                                   → medya.gdelt
    (e) kanıt + ACH (hipotezler kart toplamadan ÖNCE SHA-256 ile kilitlenir)         → K kartları + matris

Akış:
    on_kayit_kilitle (hipotez ön kaydı) → gorev_listesi (sorgu şablonları + kart şeması) →
    sağlayıcı (web araması ya da manuel/harici ajan: görev JSON'u yazılır, doldurulan kart JSON'u içe aktarıcıdan
    geri alınır) → kapsam_denetle (rapordan önce: hat başına asgari kart, olay günü satır eşiği …)
"""
from medya.arastirma.gorevler import (HATLAR, ArastirmaHatasi, gorev_listesi, on_kayit_dogrula, on_kayit_kilitle,
                                      protokol_yukle)
from medya.arastirma.kapsam import KapsamRaporu, kapsam_denetle
from medya.arastirma.saglayici import AramaSaglayici, ManuelSaglayici, WebAramaSaglayici

__all__ = ["HATLAR", "ArastirmaHatasi", "protokol_yukle", "gorev_listesi", "on_kayit_kilitle", "on_kayit_dogrula",
           "kapsam_denetle", "KapsamRaporu", "AramaSaglayici", "ManuelSaglayici", "WebAramaSaglayici"]
