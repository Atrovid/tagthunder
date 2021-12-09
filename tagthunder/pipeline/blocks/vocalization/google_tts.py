from typing import Callable, Dict

from gtts import gTTS
import io

from pipeline.blocks.vocalization._abstract import AbstractVocalizationBlock
from pipeline.blocks.vocalization._utils import LanguageDetector
from pipeline.models.responses import Zone, Keywords, Keyword, Segmentation


class GoogleTTS(AbstractVocalizationBlock):
    LANG_DETECTORS: Dict[str, Callable] = {
        "langdetect": LanguageDetector.langdetect,
        "google_translate": LanguageDetector.google_transalte
    }

    def __call__(self, segmentation: Segmentation, lang_getector: str = "google_translate") -> io.BytesIO:
        fp = io.BytesIO()

        # for k in keywords:
        #     for text, lang in self.LANG_DETECTORS['google_translate'](k.text):
        #         tts = gTTS(text=text, lang=lang, tld="com", slow=False)
        #         tts.write_to_fp(fp)
        # fp.seek(0)

        return fp
