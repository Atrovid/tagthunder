from abc import ABC, abstractmethod

from algorithms.models.responses import Segmentation, HTMLPP


class AbstractSegmentationAlgorithm(ABC):

    @abstractmethod
    def __call__(self, htmplpp: HTMLPP, *, nb_zones: int, **kwargs) -> Segmentation:
        ...

    @abstractmethod
    def fit(self, htmlpp: HTMLPP, nb_zones: int, **kwargs):
        ...
