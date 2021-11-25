from algorithms.segmentation._abstract import AbstractSegmentationAlgorithm

from algorithms.models.responses import Segmentation, HTMLPP


class GuidedExpansion(AbstractSegmentationAlgorithm):

    def __call__(self, htmlpp: HTMLPP, *, nb_zones: int, **kwargs) -> Segmentation:
        raise NotImplementedError

    def fit(self, htmlpp: HTMLPP, nb_zones: int, **kwargs):
        pass

