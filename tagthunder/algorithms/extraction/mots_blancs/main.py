from typing import List, Tuple

from tagthunder.algorithms.extraction.abstract import AbstractExtractionAlgorithm


class MotsBlancs(AbstractExtractionAlgorithm):

    def __call__(self, text: str, *, nb_keywords: int, **kwargs) -> List[str]:
        raise NotImplementedError