from api.configurations.pipeline._abstract import BlocksEnum, BlockConfig
import pipeline.blocks.cleaning


class CleaningBlockConfig(BlockConfig):
    pass


class CleaningBlocks(BlocksEnum):
    vision_based = CleaningBlockConfig(
        name="vision_based",
        enable=True,
        algorithm=pipeline.blocks.cleaning.VisionBased(),
        query=CleaningBlockConfig.build_request_body(
            "vision_based"
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.vision_based.value.query()
