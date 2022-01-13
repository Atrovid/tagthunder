import enum
from typing import Type

import pydantic

from api.configurations.pipeline._abstract import BlocksEnum, BlockConfig
import pipeline.blocks.vocalization as vocalization

import pipeline.blocks.vocalization as pipeline

LanguageDetectors = enum.Enum(
    "LanguageDetectors",
    {k: k for k in pipeline.LanguageDetectors.__members__.keys()},
    type=str
)

TTSEngines = enum.Enum(
    "TTSEngines",
    {k: k for k in pipeline.TTSEngines.__members__.keys()},
    type=str
)


class VocalizationBlockConfig(BlockConfig):
    @classmethod
    def build_request_body(cls, algorithm_name: str, **kwargs) -> Type[pydantic.BaseModel]:
        return BlockConfig.build_request_body(
            algorithm_name,
            lang_detector=(
                LanguageDetectors,
                pydantic.Field(pipeline.LanguageDetectors.default.name, description="Language detector")),
            tts_engine=(
                TTSEngines,
                pydantic.Field(pipeline.TTSEngines.default.name, description="Text to speech engine")),
            **kwargs
        )


class VocalizationBlocks(BlocksEnum):
    playback_speed_area_size = VocalizationBlockConfig(
        name="playback_speed_area_size",
        enable=True,
        algorithm=vocalization.PlaybackSpeedAreaSize(),
        query=VocalizationBlockConfig.build_request_body(
            "playback_speed_area_size",
        )
    )

    manually_adjustable = VocalizationBlockConfig(
        name="manually_adjustable",
        enable=True,
        algorithm=vocalization.ManuallyAdjustable(),
        query=VocalizationBlockConfig.build_request_body(
            "manually_adjustable",
            speed=(float, pydantic.Field(1.0, description="Speed of the speech", le=0.5, ge=2.0))
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.playback_speed_area_size.value.query()
