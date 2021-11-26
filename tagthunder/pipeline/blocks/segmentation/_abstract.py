from abc import ABC, abstractmethod

from pipeline.models.responses import Segmentation, HTMLPP


class AbstractSegmentationBlock(ABC):

    @abstractmethod
    def __call__(self, htmplpp: HTMLPP, *, nb_zones: int, **kwargs) -> Segmentation:
        ...

    @abstractmethod
    def fit(self, htmlpp: HTMLPP, nb_zones: int, **kwargs):
        """function used in experiments"""
        ...
