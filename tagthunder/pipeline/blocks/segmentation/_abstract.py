from abc import abstractmethod

from pipeline.models.responses import Segmentation, HTMLPP
from pipeline.blocks._abstract import AbstractPipelineBlock


class AbstractSegmentationBlock(AbstractPipelineBlock):

    @abstractmethod
    def __call__(self, htmplpp: HTMLPP) -> Segmentation:
        ...

    @abstractmethod
    def fit(self, htmlpp: HTMLPP):
        """function used in experiments"""
        ...
