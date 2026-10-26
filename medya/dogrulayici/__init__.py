"""Rapor cümle modeli ve doğrulayıcı (uydurmaya karşı kilit)."""
from medya.dogrulayici.model import CUMLE_TURLERI, KENT_OLCEGI, Cumle, cumleler_from_json
from medya.dogrulayici.dogrula import (DogrulamaHatasi, DogrulamaSonucu, Red, cumle_dogrula, dogrula,
                                       kesin_dogrula, NIYET_KOKLERI)

__all__ = ["Cumle", "CUMLE_TURLERI", "KENT_OLCEGI", "cumleler_from_json", "dogrula", "cumle_dogrula",
           "kesin_dogrula", "DogrulamaSonucu", "DogrulamaHatasi", "Red", "NIYET_KOKLERI"]
