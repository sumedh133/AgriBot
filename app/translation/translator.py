from deep_translator import GoogleTranslator

LANG_CODE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Telugu": "te",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Kannada": "kn",
}

class Translator:
    def translate(self, text: str, target_lang: str) -> str:
        """Translates text to the target language using Google Translate (free, no quota)."""
        if not text or target_lang.lower() == "english":
            return text
        
        lang_code = LANG_CODE_MAP.get(target_lang, "en")
        try:
            translated = GoogleTranslator(source="auto", target=lang_code).translate(text)
            return translated or text
        except Exception:
            return text  # Fallback: return original text if translation fails

    def detect_and_translate_to_english(self, text: str) -> str:
        """Detects if text is in an Indian language and translates it to English for processing."""
        if not text:
            return text
        try:
            translated = GoogleTranslator(source="auto", target="en").translate(text)
            return translated or text
        except Exception:
            return text  # Fallback: return original text if translation fails
