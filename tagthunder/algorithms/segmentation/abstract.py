from abc import ABC, abstractmethod
from typing import List, Tuple


class AbstractSegmentationAlgorithm(ABC):

    @abstractmethod
    def __call__(self, text: str, *, nb_zones: int, **kwargs) -> List[Tuple[str, ...]]:
        ...
