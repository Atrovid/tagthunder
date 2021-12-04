from api.configurations.pipeline._abstract import BlocksEnum, BlockConfig, ParametersModelFactory
import pipeline.blocks.cleaning


class CleaningBlocks(BlocksEnum):
    vision_based = BlockConfig(
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
