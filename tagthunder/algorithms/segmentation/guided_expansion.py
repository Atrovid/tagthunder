from algorithms.segmentation._abstract import AbstractSegmentationAlgorithm

from algorithms.models.responses import Segmentation


class GuidedExpansion(AbstractSegmentationAlgorithm):
    def __call__(self, text: str, *, nb_zones: int, **kwargs) -> Segmentation:
        raise NotImplementedError
