from typing import List, Tuple

from algorithms.segmentation._abstract import AbstractSegmentationAlgorithm

from algorithms.models import Segmentation


class GuidedExtension(AbstractSegmentationAlgorithm):
    def __call__(self, text: str, *, nb_zones: int, **kwargs) -> Segmentation:
        raise NotImplementedError
