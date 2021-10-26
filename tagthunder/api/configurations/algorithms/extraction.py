import pydantic as pydantic

from api.configurations.algorithms.abstract import AlgorithmsEnum, AlgorithmConfig, ParametersModelFactory
import algorithms as algorithms


class ExtractionAlgorithms(AlgorithmsEnum):
    mots_blancs = AlgorithmConfig(
        name="mots_blancs",
        enable=False,
        algorithm=algorithms.extraction.MotsBlancs(),
        query=ParametersModelFactory.extraction(
            "mots_blancs",
            nb_keywords=5
        )
    )

    yake = AlgorithmConfig(
        name="yake",
        enable=True,
        algorithm=algorithms.extraction.Yake(),
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
