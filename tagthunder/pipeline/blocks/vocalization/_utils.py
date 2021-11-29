import io
from typing import List, Dict
import pycld2
import langdetect
import googletrans


class LanguageDetector:
    GOOGLE_TRANSLATOR = googletrans.Translator(service_urls=["translate.google.com"])

    @classmethod
    def cld2(cls, text) -> List[Dict[str, str]]:
        """Not working for short sequence"""
        _, _, _, detected_language = pycld2.detect(text, returnVectors=True)

        for start, end, LANG, lang in detected_language:
            yield text[start:end], LANG

    @classmethod
    def langdetect(cls, text) -> List[Dict[str, str]]:
        langdetect.DetectorFactory.seed = 0
        yield text, langdetect.detect(text)

    @classmethod
    def google_transalte(cls, text) -> List[Dict[str, str]]:
        yield text, cls.GOOGLE_TRANSLATOR.detect(text).lang
