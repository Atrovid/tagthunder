from typing import List, Tuple

from algorithms.segmentation.abstract import AbstractSegmentationAlgorithm


class TopDownBottomUp(AbstractSegmentationAlgorithm):
    def __call__(self, text: str, *, nb_zones: int, **kwargs) -> List[Tuple[str, ...]]:
        raise NotImplementedError
