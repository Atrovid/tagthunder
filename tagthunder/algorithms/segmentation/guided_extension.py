from typing import List, Tuple

from algorithms.segmentation._abstract import AbstractSegmentationAlgorithm


class GuidedExtension(AbstractSegmentationAlgorithm):
    def __call__(self, text: str, *, nb_zones: int, **kwargs) -> List[Tuple[str, ...]]:
        raise NotImplementedError