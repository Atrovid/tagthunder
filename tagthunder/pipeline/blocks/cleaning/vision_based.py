from pipeline.blocks.cleaning._abstract import AbstractCleaningBlock
from pipeline.models.responses import HTMLPP


class VisionBased(AbstractCleaningBlock):
    def __call__(self, html: str) -> HTMLPP:
        raise NotImplementedError
