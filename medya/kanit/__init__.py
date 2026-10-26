"""Kanıt deposu: rapordaki her cümlenin dayandığı kanıt kartları (DuckDB)."""
from medya.kanit.kart import (BILGI_DERECELERI, KAYNAK_DERECELERI, TURLER, KanitHatasi, KanitKarti,
                              kanit_id_uret)
from medya.kanit.depo import KanitDeposu, varsayilan_yol

__all__ = ["KanitKarti", "KanitDeposu", "KanitHatasi", "kanit_id_uret", "TURLER", "KAYNAK_DERECELERI",
           "BILGI_DERECELERI", "varsayilan_yol"]
