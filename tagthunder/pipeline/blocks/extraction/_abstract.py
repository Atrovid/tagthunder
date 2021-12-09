from abc import ABC, abstractmethod
from typing import List

from pipeline.models.responses import Keywords, Segmentation


class AbstractExtractionBlock(ABC):

    @abstractmethod
    def __call__(self, segmentation: Segmentation, *, nb_keywords: int, **kwargs) -> List[Keywords]:
        ...
