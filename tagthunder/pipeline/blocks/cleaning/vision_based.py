from pipeline.blocks.cleaning._abstract import AbstractCleaningBlock
from pipeline.models.responses import HTMLPP, HTMLP


class VisionBased(AbstractCleaningBlock):
    def __call__(self, htmlp: HTMLP) -> HTMLPP:
        return HTMLPP(HTMLP.prettify())
