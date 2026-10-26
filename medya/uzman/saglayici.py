"""LLM sağlayıcıları. Seçim `MEDYA_LLM_SAGLAYICI` ortam değişkeniyle: anthropic | openai | gemini | offline.
Varsayılan offline'dır: anahtar yoksa ya da test ortamında hiçbir ağ çağrısı yapılmaz.

Bütçe: anthropic çağrıları `llm/butce.py`'deki `cagir` üzerinden geçer (aylık ve çalışma tavanı, defter).
openai/gemini fiyatları koda yazılmaz, `llm/fiyatlar.toml`'dan (LLM_FIYAT_DOSYASI) okunur; model orada yoksa
maliyet önceden hesaplanamaz, uyarı verilir ve çağrı ancak `MEDYA_FIYATSIZ_IZIN=1` ile yapılır (deftere tutar 0,
"fiyatsiz" etiketiyle). Her çağrının token kullanımı isteğe bağlı bir `TokenSayaci`na da yazılır (rapor başına
tavan).

Anahtarlar yalnızca ortam değişkeninden okunur (OPENAI_API_KEY; GEMINI_API_KEY ya da GOOGLE_API_KEY); koda ve
repoya girmez. Anahtar yoksa çağrıdan önce açık bir hata verilir. Testler için `istemci` enjekte edilebilir
(ağ çağrısı yapılmaz).
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class SaglayiciHatasi(RuntimeError):
    pass


class Saglayici:
    ad = "temel"
    model = ""
    sayac = None        # llm.butce.TokenSayaci (isteğe bağlı)

    def tamamla(self, sistem: str, kullanici: str, gorev: str, max_tokens: int = 2000) -> str:
        raise NotImplementedError


def _butce():
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from llm import butce   # noqa: E402  (repo kökündeki bütçe defteri)
    return butce


class AnthropicSaglayici(Saglayici):
    ad = "anthropic"

    def __init__(self, model: str | None = None):
        self.model = model or os.environ.get("MEDYA_LLM_MODEL", "claude-haiku-5-5")

    def tamamla(self, sistem, kullanici, gorev, max_tokens=2000):
        butce = _butce()
        ek = {}
        if self.model.startswith("claude-haiku-5"):
            # llm/anlatici.py'deki ölçüm: Haiku 5.5'te düşünme varsayılan açık ve JSON çıktısını kesiyor
            ek["thinking"] = {"type": "disabled"}
        yanit = butce.cagir(model=self.model, etiket=f"medya-{gorev}", max_tokens=max_tokens, system=sistem,
                            messages=[{"role": "user", "content": kullanici}], **ek)
        return "".join(b.text for b in yanit.content if getattr(b, "type", "") == "text").strip()


def anahtar_al(*adlar: str) -> str:
    """Ortam değişkeninden API anahtarı; hiçbiri yoksa açık hata (kod anahtar içermez)."""
    for ad in adlar:
        if os.environ.get(ad, "").strip():
            return os.environ[ad].strip()
    raise SaglayiciHatasi(f"API anahtarı bulunamadı: {' ya da '.join(adlar)} ortam değişkenini tanımlayın. "
                          "Anahtar koda, repoya ya da vaka dosyalarına yazılmaz.")


class _FiyatsizSaglayici(Saglayici):
    """openai / gemini ortak bütçe kapısı."""
    anahtar_degiskenleri: tuple = ()

    def __init__(self, model: str | None = None, istemci=None, sayac=None):
        self.model = model or os.environ.get("MEDYA_LLM_MODEL", self.varsayilan_model)
        self._istemci = istemci
        self.sayac = sayac

    def _kapi(self, gorev, girdi_tahmini, max_tokens):
        butce = _butce()
        if self.sayac is not None:
            self.sayac.on_denetim(self.model, girdi_tahmini, max_tokens)
        if butce.fiyat_var_mi(self.model):
            butce.onayla(self.model, girdi=girdi_tahmini, cikti=max_tokens, etiket=gorev)
            return butce, True
        uyari = butce.fiyat_uyarisi(self.model)
        if os.environ.get("MEDYA_FIYATSIZ_IZIN") != "1":
            raise SaglayiciHatasi(f"{self.ad}/{self.model}: {uyari} Bilerek çağırmak için MEDYA_FIYATSIZ_IZIN=1.")
        print(f"[UYARI] {uyari}", file=sys.stderr)
        return butce, False

    def _defter(self, butce, fiyatli, gorev, girdi, cikti):
        tutar = butce.maliyet(self.model, girdi=girdi, cikti=cikti) if fiyatli else 0.0
        butce.yaz(self.model, f"medya-{gorev}" + ("" if fiyatli else "-fiyatsiz"), girdi, cikti, 0, 0, False, tutar)
        if self.sayac is not None:
            self.sayac.ekle(self.model, girdi, cikti)


class OpenAISaglayici(_FiyatsizSaglayici):
    ad = "openai"
    varsayilan_model = "gpt-5-mini"
    anahtar_degiskenleri = ("OPENAI_API_KEY",)

    def istemci(self):
        if self._istemci is None:
            anahtar = anahtar_al(*self.anahtar_degiskenleri)
            import openai  # isteğe bağlı paket
            self._istemci = openai.OpenAI(api_key=anahtar)
        return self._istemci

    def tamamla(self, sistem, kullanici, gorev, max_tokens=2000):
        istemci = self.istemci()
        butce, fiyatli = self._kapi(gorev, (len(sistem) + len(kullanici)) // 4 + 1, max_tokens)
        y = istemci.chat.completions.create(model=self.model, max_completion_tokens=max_tokens,
                                            messages=[{"role": "system", "content": sistem},
                                                      {"role": "user", "content": kullanici}])
        u = y.usage
        self._defter(butce, fiyatli, gorev, u.prompt_tokens, u.completion_tokens)
        return y.choices[0].message.content or ""


class GeminiSaglayici(_FiyatsizSaglayici):
    ad = "gemini"
    varsayilan_model = "gemini-2.5-flash"
    anahtar_degiskenleri = ("GEMINI_API_KEY", "GOOGLE_API_KEY")

    def istemci(self):
        if self._istemci is None:
            anahtar = anahtar_al(*self.anahtar_degiskenleri)
            from google import genai  # isteğe bağlı paket (google-genai)
            self._istemci = genai.Client(api_key=anahtar)
        return self._istemci

    def tamamla(self, sistem, kullanici, gorev, max_tokens=2000):
        istemci = self.istemci()
        butce, fiyatli = self._kapi(gorev, (len(sistem) + len(kullanici)) // 4 + 1, max_tokens)
        y = istemci.models.generate_content(model=self.model, contents=kullanici,
                                            config={"system_instruction": sistem, "max_output_tokens": max_tokens})
        u = getattr(y, "usage_metadata", None)
        self._defter(butce, fiyatli, gorev, getattr(u, "prompt_token_count", 0) or 0,
                     getattr(u, "candidates_token_count", 0) or 0)
        return y.text or ""


class OfflineSaglayici(Saglayici):
    """Ağsız, deterministik sağlayıcı: testler ve anahtarsız kullanım için.

    Gerçek bir analist değildir. Girdi paketindeki yapılandırılmış veriden (vaka tanımı, kanıt kartları,
    ACH) şablon cümleler kurar; dünya bilgisi kullanmaz. Çıktısı da doğrulayıcıdan geçer.
    `ek_yanitlar` ile görev başına sabit yanıt verilebilir (testlerde uydurma çıktı denemek için).
    """
    ad = "offline"
    model = "offline-sablon"

    def __init__(self, ek_yanitlar: dict | None = None):
        self.ek_yanitlar = ek_yanitlar or {}
        self.cagrilar: list[tuple[str, str]] = []

    def tamamla(self, sistem, kullanici, gorev, max_tokens=2000):
        self.cagrilar.append((gorev, kullanici))
        if gorev in self.ek_yanitlar:
            v = self.ek_yanitlar[gorev]
            return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
        from medya.uzman import offline
        paket = json.loads(kullanici.split("GİRDİ PAKETİ (JSON):", 1)[1])
        return json.dumps(getattr(offline, gorev)(paket), ensure_ascii=False)


def saglayici_al(ad: str | None = None, sayac=None) -> Saglayici:
    ad = (ad or os.environ.get("MEDYA_LLM_SAGLAYICI", "offline")).strip().lower()
    if ad == "offline":
        return OfflineSaglayici()
    if ad == "anthropic":
        return AnthropicSaglayici()
    if ad == "openai":
        return OpenAISaglayici(sayac=sayac)
    if ad == "gemini":
        return GeminiSaglayici(sayac=sayac)
    raise SaglayiciHatasi(f"Bilinmeyen sağlayıcı: {ad} (anthropic | openai | gemini | offline)")
