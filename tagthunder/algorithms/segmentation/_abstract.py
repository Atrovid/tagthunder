from abc import ABC, abstractmethod

from algorithms.models.responses import Segmentation


class AbstractSegmentationAlgorithm(ABC):

    @abstractmethod
    def __call__(self, text: str, *, nb_zones: int, **kwargs) -> Segmentation:
        ...
