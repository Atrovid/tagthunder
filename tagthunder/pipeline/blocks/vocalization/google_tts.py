from gtts import gTTS
import io

from pipeline.blocks.vocalization._abstract import AbstractVocalizationBlock
from pipeline.blocks.vocalization._utils import play_song
from pipeline.models.responses import Zone, Keywords, Keyword


class GoogleTTS(AbstractVocalizationBlock):

    def __call__(self, keywords: Keywords, **kwargs) -> io.BytesIO:
        fp = io.BytesIO()
        for k in keywords:
            print(k.text, k.lang)
            tts = gTTS(k.text, k.lang)
            tts.write_to_fp(fp)
        fp.seek(0)

        return fp


if __name__ == '__main__':
    block = GoogleTTS()
    keywords: Keywords = [
        Keyword(text="Premier mot clef", lang="fr"),
        Keyword(text="Second key word", lang="en")
    ]
    fp = block(keywords)

    play_song(fp)
