from pipeline.blocks.cleaning._abstract import AbstractCleaningAlgorithm
from pipeline.models.responses import HTMLPP


class VisionBased(AbstractCleaningAlgorithm):
    def __call__(self, html: str) -> HTMLPP:
        raise NotImplementedError
