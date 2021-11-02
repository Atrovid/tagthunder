from typing import List, Tuple

from algorithms.extraction._abstract import AbstractExtractionAlgorithm
from algorithms.models.responses import Keywords


class MotsBlancs(AbstractExtractionAlgorithm):

    def __call__(self, text: str, *, nb_keywords: int, **kwargs) -> Keywords:
        raise NotImplementedError()
