from typing import List, Tuple

from algorithms.extraction._abstract import AbstractExtractionAlgorithm


class MotsBlancs(AbstractExtractionAlgorithm):

    def __call__(self, text: str, *, nb_keywords: int, **kwargs) -> List[str]:
        raise NotImplementedError