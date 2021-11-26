from gtts import gTTS
import io

from pipeline.blocks.vocalization._abstract import AbstractVocalizationBlock
from pipeline.blocks.vocalization._utils import LanguageDetector
from pipeline.models.responses import Zone, Keywords, Keyword


class GoogleTTS(AbstractVocalizationBlock):

    def __call__(self, keywords: Keywords, **kwargs) -> io.BytesIO:
        fp = io.BytesIO()

        for k in keywords:
            for text, lang in LanguageDetector.langdetect(k.text):
                tts = gTTS(text=text, lang=lang, tld="com")
                tts.write_to_fp(fp)
        fp.seek(0)
        return fp