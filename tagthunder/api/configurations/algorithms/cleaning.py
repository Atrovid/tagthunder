import pydantic as pydantic

from api.configurations.algorithms.abstract import AlgorithmsEnum, AlgorithmConfig, ParametersModelFactory
import algorithms as algorithms


class CleaningAlgorithms(AlgorithmsEnum):

    vision_based = AlgorithmConfig(
        name="vision_based",
        enable=True,
        algorithm=algorithms.cleaning.VisionBased(),
        query=ParametersModelFactory.cleaning(
            "vision_based"
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.vision_based.value.query()

