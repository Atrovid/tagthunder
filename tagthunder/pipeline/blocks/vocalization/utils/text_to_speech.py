import enum
import pprint
from typing import List, Optional, Type, Union, Callable
import abc

import pydub.exceptions
from gtts import gTTS
import io
import pipeline.blocks.vocalization.utils.output_management as utils
from pipeline.blocks.vocalization.utils.lang_detectors import LanguageDetectors, AbstractLanguageDetector
from pipeline.models.responses import Keywords


class AbstractTextToSpeechEngine(abc.ABC):

    def __init__(self, lang_detector: Optional[str] = None):
        self.lang_detector = self.get_lang_detector(lang_detector)

    @abc.abstractmethod
    def __call__(self, keywords: Keywords, lang_detector: Optional[str] = None, **kwargs) -> io.BytesIO:
        ...

    @classmethod
    def get_lang_detector(cls, name: Optional[str]) -> Union[property, AbstractLanguageDetector]:
        if name is None:
            return LanguageDetectors.default.value
        else:
            return LanguageDetectors[name].value


class GoogleTTS(AbstractTextToSpeechEngine):

    def __init__(self, lang_detector: Optional[str] = None):
        super(GoogleTTS, self).__init__(lang_detector)

    def __call__(self, keywords: Keywords, **kwargs):
        if keywords:
            mp3_file = io.BytesIO()

            for k in keywords:
                for text, lang in self.lang_detector(k.text):
                    tts = self.call_gtts(text, lang)
                    tts.write_to_fp(mp3_file)

            return utils.convert_mp3_to_wav(mp3_file)
        return None

    @classmethod
    def call_gtts(cls, text, lang):
        return gTTS(text=text, lang=lang, tld="com", slow=False)


class TTSEngines(enum.Enum):
    google_tts = GoogleTTS

    @classmethod
    @property
    def default(cls):
        return cls.google_tts
