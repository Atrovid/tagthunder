import pydantic

from api.configurations.pipeline._abstract import BlocksEnum, BlockConfig, ParametersModelFactory
from api.configurations.api import settings
import pipeline.blocks.augmentation


class AugmentationBlocks(BlocksEnum):
    puppeteer = BlockConfig(
        name="puppeteer",
        enable=True,
        algorithm=pipeline.blocks.augmentation.Puppeteer(settings.crawler_address),
        query=ParametersModelFactory.augmentation(
            "puppeteer",
            recompute=(bool,
                       pydantic.Field(True, description="Force to recompute cached HTML+")
                       )
        )
    )

    @classmethod
    @property
    def default_query(cls):
        return cls.puppeteer.value.query()
