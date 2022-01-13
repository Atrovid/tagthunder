from typing import Optional

import librosa
import soundfile

from pipeline.blocks.vocalization._abstract import AbstractVocalizationBlock, UnvocalizableError
from pipeline.models.responses import Segmentation, Zone


class ManuallyAdjustable(AbstractVocalizationBlock):

    def __init__(self):
        super().__init__()
        self.speed = None

    def config(self,
               tts_engine: Optional[str] = None,
               lang_detector: Optional[str] = None,
               speed: Optional[float] = 1.0
               ):
        super(ManuallyAdjustable, self).config(tts_engine, lang_detector)
        self.speed = speed

    def __call__(self, segmentation: Segmentation):
        return [
            self.vocalize_zone(zone)
            for zone in segmentation.zones
            if self.is_vocalizable(zone)
        ]

    def vocalize_zone(self, zone: Zone, **kwargs):
        try:
            vocalization = super().vocalize_zone(zone)
            data, sample_rate = librosa.load(vocalization)
            vocalization.seek(0)  # allow replacement of file-like content
            soundfile.write(
                vocalization,
                librosa.effects.time_stretch(data, self.speed),
                samplerate=sample_rate, format="wav"
            )
            return vocalization
        except UnvocalizableError:
            return None
