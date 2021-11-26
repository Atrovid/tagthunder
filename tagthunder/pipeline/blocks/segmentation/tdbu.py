from pipeline.blocks.segmentation._abstract import AbstractSegmentationBlock
from pipeline.models.responses import Segmentation, HTMLPP


class TopDownBottomUp(AbstractSegmentationBlock):
    def __call__(self, text: str, *, nb_zones: int, **kwargs) -> Segmentation:
        raise NotImplementedError

    def fit(self, htmlpp: HTMLPP, nb_zones: int, **kwargs):
        raise NotImplementedError
