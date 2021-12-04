import pydantic as pydantic

from api.configurations.pipeline._abstract import BlocksEnum, BlockConfig, ParametersModelFactory
import pipeline.blocks.segmentation


class SegmentationBlocks(BlocksEnum):
    tdbu = BlockConfig(
        name="TDBU",
        enable=True,
        algorithm=pipeline.blocks.segmentation.TopDownBottomUp(),
        query=ParametersModelFactory.segmentation(
            "TDBU",
            nb_zones=5
        )
    )

    ge = BlockConfig(
        name="GE",
        enable=False,
        algorithm=pipeline.blocks.segmentation.GuidedExpansion(),
        query=ParametersModelFactory.segmentation(
            "GE",
            nb_zones=5
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.tdbu.value.query()
