from abc import ABC, abstractmethod
from typing import List, Tuple

from algorithms.models import Segmentation


class AbstractSegmentationAlgorithm(ABC):

    @abstractmethod
    def __call__(self, text: str, *, nb_zones: int, **kwargs) -> Segmentation:
        ...
