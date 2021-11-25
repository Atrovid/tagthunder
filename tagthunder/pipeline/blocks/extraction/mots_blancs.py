from pipeline.blocks.extraction._abstract import AbstractExtractionAlgorithm
from pipeline.models.responses import Keywords


class MotsBlancs(AbstractExtractionAlgorithm):

    def __call__(self, text: str, *, nb_keywords: int, **kwargs) -> Keywords:
        raise NotImplementedError()
