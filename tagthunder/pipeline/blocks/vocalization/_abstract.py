import io
from abc import ABC, abstractmethod
from typing import Optional, List, Type, Union

from pipeline.blocks.vocalization.utils.lang_detectors import LanguageDetectors
from pipeline.blocks.vocalization.utils.text_to_speech import TTSEngines
from pipeline.models.responses import Segmentation, Zone
from pipeline.blocks._abstract import AbstractPipelineBlock


class UnvocalizableError(Exception):
    pass


class AbstractVocalizationBlock(AbstractPipelineBlock):

    def __init__(self):
        self.tts_engine = None

    def config(self, tts_engine: Union[str, TTSEngines] = None,
               lang_detector: Union[str, LanguageDetectors] = None):
        self.tts_engine = self.get_tts_engine(tts_engine)(lang_detector)

    @abstractmethod
    def __call__(self, segmentation: Segmentation) -> List[io.BytesIO]:
        ...

    @classmethod
    def get_tts_engine(cls, name: Optional[str] = None):
        if name is None:
            return TTSEngines.default.value
        else:
            return TTSEngines[name].value

    def vocalize_zone(self, zone: Zone, **kwargs):
        if not self.is_vocalizable(zone):
            raise UnvocalizableError("This zone does not contains keywords.")
        res = self.tts_engine(zone.keywords)
        res.zone_id = zone.id
        return res

    @classmethod
    def is_vocalizable(cls, zone: Zone):
        return bool(zone.keywords)
