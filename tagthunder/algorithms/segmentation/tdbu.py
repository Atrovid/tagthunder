from typing import List, Tuple

from algorithms.segmentation._abstract import AbstractSegmentationAlgorithm
from algorithms.models.responses import Segmentation, HTMLPP


class TopDownBottomUp(AbstractSegmentationAlgorithm):
    def __call__(self, text: str, *, nb_zones: int, **kwargs) -> Segmentation:
        raise NotImplementedError

    def fit(self, htmlpp: HTMLPP, nb_zones: int, **kwargs):
        raise NotImplementedError
