from typing import List, Type

import pydantic

from api.configurations.pipeline._abstract import BlocksEnum, BlockConfig
from api.configurations.api import settings
import pipeline.blocks
import pipeline.blocks.augmentation


class AugmentationBlockConfig(BlockConfig):
    pass


class AugmentationBlocks(BlocksEnum):
    puppeteer = AugmentationBlockConfig(
        name="puppeteer",
        enable=True,
        algorithm=pipeline.blocks.augmentation.Puppeteer(settings.crawler_address),
        query=AugmentationBlockConfig.build_request_body(
            "puppeteer",
            page_width=(int, pydantic.Field(1200, description="Width of the emulate web page.")),
            page_height=(int, pydantic.Field(1200, description="Height of the emulate web page.")),
            styles=(List[str], pydantic.Field(pipeline.blocks.REQUIRED_STYLES, description="Styles to be retrieved.")),
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.puppeteer.value.query()

    @classmethod
    def build_request_body_factory(cls):
        pass
