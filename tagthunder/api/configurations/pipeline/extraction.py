from typing import Type

import pydantic as pydantic

from api.configurations.pipeline._abstract import BlocksEnum, BlockConfig
import pipeline.blocks.extraction


class ExtractionBlockConfig(BlockConfig):
    @classmethod
    def build_request_body(cls, algorithm_name: str, nb_keywords: int = 4, **kwargs) -> Type[pydantic.BaseModel]:
        return BlockConfig.build_request_body(
            algorithm_name,
            nb_keywords=(int, pydantic.Field(nb_keywords, description="Number of keywords / keyphrases.")),
            **kwargs
        )


class ExtractionBlocks(BlocksEnum):
    yake = ExtractionBlockConfig(
        name="yake",
        enable=True,
        algorithm=pipeline.blocks.extraction.Yake(),
        query=ExtractionBlockConfig.build_request_body(
            "yake",
            nb_keywords=5,
            max_ngram_size=(int, pydantic.Field(4, description="Maximal keyphrases length.")),
            window_size=(int, pydantic.Field(3, description="Window size.")),
            language=(str, pydantic.Field("fr", description="Text content language."))
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.yake.value.query()
