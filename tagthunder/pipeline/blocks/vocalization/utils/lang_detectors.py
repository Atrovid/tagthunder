import abc
import enum
import io
import zipfile
from typing import List, Dict, Callable
import langdetect
import googletrans
from pydub import AudioSegment
import inspect


class AbstractLanguageDetector(abc.ABC):

    @abc.abstractmethod
    def __call__(self, text) -> List[Dict[str, str]]:
        ...


class GoogleTranslate(AbstractLanguageDetector):
    __GOOGLE_TRANSLATOR = googletrans.Translator(service_urls=["translate.google.com"])

    def __call__(self, text) -> List[Dict[str, str]]:
        yield text, self.__GOOGLE_TRANSLATOR.detect(text).lang


class LangDetect(AbstractLanguageDetector):
    def __call__(self, text) -> List[Dict[str, str]]:
        langdetect.DetectorFactory.seed = 0
        yield text, langdetect.detect(text)


class LanguageDetectors(enum.Enum):
    google_translate = GoogleTranslate()
    langdetect = LangDetect()

    @classmethod
    @property
    def default(cls):
        return cls.google_translate
