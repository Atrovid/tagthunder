import io
from pydub import AudioSegment
from pydub.playback import play

from typing import List, Dict

import pycld2


def detect(text) -> List[Dict[str, str]]:
    languages = []
    _, _, _, detected_language = pycld2.detect(text, returnVectors=True)

    for start, end, _, lang in detected_language:
        languages.append({
            text[start:end]: lang
        })

    return languages


def play_song(fp: io.BytesIO):
    song = AudioSegment.from_file(fp, format="mp3")
    play(song)
