from api.configurations.pipeline._abstract import AlgorithmsEnum, AlgorithmConfig, ParametersModelFactory
import pipeline.blocks.cleaning


class CleaningAlgorithms(AlgorithmsEnum):
    vision_based = AlgorithmConfig(
        name="vision_based",
        enable=True,
        algorithm=pipeline.blocks.cleaning.VisionBased(),
        query=ParametersModelFactory.cleaning(
            "vision_based"
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.vision_based.value.query()
