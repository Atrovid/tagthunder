import io

from pydub import AudioSegment
from pydub.playback import play

from pipeline.blocks.vocalization.utils.text_to_speech import GoogleTTS
from pipeline.models.responses import Keyword, Keywords


def play_song(fp: io.BytesIO):
    song = AudioSegment.from_file(fp, format="mp3")
    play(song)


if __name__ == '__main__':
    block = GoogleTTS()
    keywords: Keywords = [
        Keyword(text="Premier mot clef"),
        Keyword(text="Second key word")
    ]
    fp = block(keywords)

    play_song(fp)
