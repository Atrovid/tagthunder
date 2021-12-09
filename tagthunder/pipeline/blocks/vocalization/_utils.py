import io
from typing import List, Dict
import langdetect
import googletrans


class LanguageDetector:
    GOOGLE_TRANSLATOR = googletrans.Translator(service_urls=["translate.google.com"])

    @classmethod
    def langdetect(cls, text) -> List[Dict[str, str]]:
        langdetect.DetectorFactory.seed = 0
        yield text, langdetect.detect(text)

    @classmethod
    def google_transalte(cls, text) -> List[Dict[str, str]]:
        yield text, cls.GOOGLE_TRANSLATOR.detect(text).lang
