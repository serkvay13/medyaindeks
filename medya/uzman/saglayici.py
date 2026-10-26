"""LLM sağlayıcıları. Seçim `MEDYA_LLM_SAGLAYICI` ortam değişkeniyle: anthropic | openai | gemini | offline.
Varsayılan offline'dır: anahtar yoksa ya da test ortamında hiçbir ağ çağrısı yapılmaz.

Bütçe: anthropic çağrıları `llm/butce.py`'deki `cagir` üzerinden geçer (aylık ve çalışma tavanı, defter).
openai/gemini için `llm/butce.py`'nin fiyat tablosunda model yoksa maliyet önceden hesaplanamaz; bu durumda
çağrı ancak `MEDYA_FIYATSIZ_IZIN=1` verilirse yapılır ve deftere tutarı 0 olarak, "fiyatsiz" etiketiyle yazılır.
Anahtarlar yalnızca ortam değişkeninden okunur; koda ve repoya girmez.
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


class _FiyatsizSaglayici(Saglayici):
    """openai / gemini ortak bütçe kapısı."""

    def _kapi(self, gorev, girdi_tahmini, max_tokens):
        butce = _butce()
        if self.model in butce.FIYAT:
            butce.onayla(self.model, girdi=girdi_tahmini, cikti=max_tokens, etiket=gorev)
            return butce, True
        if os.environ.get("MEDYA_FIYATSIZ_IZIN") != "1":
            raise SaglayiciHatasi(f"{self.ad}/{self.model} için fiyat tanımlı değil (llm/butce.py FIYAT); "
                                  "bütçe tavanı uygulanamaz. Bilerek çağırmak için MEDYA_FIYATSIZ_IZIN=1.")
        return butce, False

    def _defter(self, butce, fiyatli, gorev, girdi, cikti):
        tutar = butce.maliyet(self.model, girdi=girdi, cikti=cikti) if fiyatli else 0.0
        butce.yaz(self.model, f"medya-{gorev}" + ("" if fiyatli else "-fiyatsiz"), girdi, cikti, 0, 0, False, tutar)


class OpenAISaglayici(_FiyatsizSaglayici):
    ad = "openai"

    def __init__(self, model: str | None = None):
        self.model = model or os.environ.get("MEDYA_LLM_MODEL", "gpt-5-mini")

    def tamamla(self, sistem, kullanici, gorev, max_tokens=2000):
        butce, fiyatli = self._kapi(gorev, (len(sistem) + len(kullanici)) // 4 + 1, max_tokens)
        import openai  # isteğe bağlı paket
        istemci = openai.OpenAI()   # OPENAI_API_KEY ortamdan
        y = istemci.chat.completions.create(model=self.model, max_completion_tokens=max_tokens,
                                            messages=[{"role": "system", "content": sistem},
                                                      {"role": "user", "content": kullanici}])
        u = y.usage
        self._defter(butce, fiyatli, gorev, u.prompt_tokens, u.completion_tokens)
        return y.choices[0].message.content or ""


class GeminiSaglayici(_FiyatsizSaglayici):
    ad = "gemini"

    def __init__(self, model: str | None = None):
        self.model = model or os.environ.get("MEDYA_LLM_MODEL", "gemini-2.5-flash")

    def tamamla(self, sistem, kullanici, gorev, max_tokens=2000):
        butce, fiyatli = self._kapi(gorev, (len(sistem) + len(kullanici)) // 4 + 1, max_tokens)
        from google import genai  # isteğe bağlı paket (google-genai)
        istemci = genai.Client()   # GEMINI_API_KEY ortamdan
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


def saglayici_al(ad: str | None = None) -> Saglayici:
    ad = (ad or os.environ.get("MEDYA_LLM_SAGLAYICI", "offline")).strip().lower()
    if ad == "offline":
        return OfflineSaglayici()
    if ad == "anthropic":
        return AnthropicSaglayici()
    if ad == "openai":
        return OpenAISaglayici()
    if ad == "gemini":
        return GeminiSaglayici()
    raise SaglayiciHatasi(f"Bilinmeyen sağlayıcı: {ad} (anthropic | openai | gemini | offline)")
