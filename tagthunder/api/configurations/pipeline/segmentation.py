from typing import Type

import pydantic as pydantic

from api.configurations.pipeline._abstract import BlocksEnum, BlockConfig
import pipeline.blocks.segmentation


class SegmentationBlockConfig(BlockConfig):
    @classmethod
    def build_request_body(cls, algorithm_name: str,
                           nb_zones: int = None, le: int = None, ge: int = None, **kwargs) -> Type[pydantic.BaseModel]:
        return BlockConfig.build_request_body(
            algorithm_name,
            nb_zones=(int, pydantic.Field(nb_zones, description="Number of zones", le=le, ge=ge)),
            **kwargs
        )


class SegmentationBlocks(BlocksEnum):
    TDBU = SegmentationBlockConfig(
        name="TDBU",
        enable=True,
        algorithm=pipeline.blocks.segmentation.TopDownBottomUp(),
        query=BlockConfig.build_request_body(
            "TDBU",
            nb_zones=5
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.TDBU.value.query()
