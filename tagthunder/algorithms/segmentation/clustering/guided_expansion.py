from algorithms.segmentation._abstract import AbstractSegmentationAlgorithm

from algorithms.models.responses import Segmentation, HTMLPP


class GuidedExpansion(AbstractSegmentationAlgorithm):

    def __call__(self, htmlpp: HTMLPP, *, nb_zones: int, **kwargs) -> Segmentation:
        raise NotImplementedError

    def __init__(self):
        pass

    def _init_centers(self):
        pass
