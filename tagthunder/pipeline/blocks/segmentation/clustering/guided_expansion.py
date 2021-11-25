from pipeline.blocks.segmentation._abstract import AbstractSegmentationAlgorithm

from pipeline.models.responses import Segmentation, HTMLPP


class GuidedExpansion(AbstractSegmentationAlgorithm):

    def __call__(self, htmlpp: HTMLPP, *, nb_zones: int, **kwargs) -> Segmentation:
        raise NotImplementedError

    def fit(self, htmlpp: HTMLPP, nb_zones: int, **kwargs):
        pass
