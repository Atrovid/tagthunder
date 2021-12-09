import pydantic as pydantic

from api.configurations.pipeline._abstract import BlocksEnum, BlockConfig, ParametersModelFactory
import pipeline.blocks.extraction


class ExtractionBlocks(BlocksEnum):
    yake = BlockConfig(
        name="yake",
        enable=True,
        algorithm=pipeline.blocks.extraction.Yake(),
        query=ParametersModelFactory.extraction(
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
