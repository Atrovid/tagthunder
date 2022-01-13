import io
import zipfile
from pydub import AudioSegment


def convert_mp3_to_wav(file):
    # file.seek(0)
    sound = AudioSegment.from_mp3(file)
    res = io.BytesIO()
    sound.export(res, format="wav")
    res.seek(0)
    return res


def zip_files(*files):
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_tmp:
        for file in files:
            zip_tmp.write(file)
    return zip_io
