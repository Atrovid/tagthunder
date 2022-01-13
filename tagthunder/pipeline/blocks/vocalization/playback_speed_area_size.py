from typing import Optional

import numpy as np
import librosa
import soundfile

from pipeline.blocks.vocalization._abstract import AbstractVocalizationBlock, UnvocalizableError
from pipeline.models.responses import Segmentation, Zone
from pipeline.models.web_elements import CoveringBoundingBox


class PlaybackSpeedAreaSize(AbstractVocalizationBlock):

    def __init__(self):
        super().__init__()
        self.max_rate = None
        self.min_rate = None

    def config(self,
               tts_engine: Optional[str] = None,
               lang_detector: Optional[str] = None,
               min_rate: float = 0.5, max_rate: float = 1.8
               ):
        super(PlaybackSpeedAreaSize, self).config(tts_engine, lang_detector)
        self.min_rate = min_rate
        self.max_rate = max_rate

    def __call__(self, segmentation: Segmentation):
        rates = self.compute_rate(segmentation)
        return [
            self.vocalize_zone(zone, rate)
            for zone, rate in zip(segmentation.zones, rates)
            if self.is_vocalizable(zone)
        ]

    def vocalize_zone(self, zone: Zone, rate: float = 1.0):
        try:
            vocalization = super().vocalize_zone(zone)
            data, sample_rate = librosa.load(vocalization)
            vocalization.seek(0)  # allow replacement of file-like content
            soundfile.write(
                vocalization,
                librosa.effects.time_stretch(data, rate),
                samplerate=sample_rate, format="wav"
            )
            return vocalization
        except UnvocalizableError:
            return None

    def compute_rate(self, segmentation: Segmentation):
        return self.rate_function(self.compute_zone_area_props(segmentation))

    @classmethod
    def compute_zone_area_props(cls, segmentation: Segmentation):
        zone_bboxes = [zone.htmlpp.bbox for zone in segmentation.zones]
        zones_areas = [bbox.area for bbox in zone_bboxes]
        page_area = CoveringBoundingBox(zone_bboxes).area
        return [zone_area / page_area for zone_area in zones_areas]

    @property
    def rate_function(self):
        return np.poly1d(
            np.polyfit(
                x=[0, 1],
                y=[self.min_rate, self.max_rate],
                deg=1
            )
        )
