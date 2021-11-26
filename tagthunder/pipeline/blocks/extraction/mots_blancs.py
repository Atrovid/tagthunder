from pipeline.blocks.extraction._abstract import AbstractExtractionBlock
from pipeline.models.responses import Keywords


class MotsBlancs(AbstractExtractionBlock):

    def __call__(self, text: str, *, nb_keywords: int, **kwargs) -> Keywords:
        raise NotImplementedError()
