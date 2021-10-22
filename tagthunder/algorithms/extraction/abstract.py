from abc import ABC, abstractmethod
from typing import List, Tuple


class AbstractExtractionAlgorithm(ABC):

    @abstractmethod
    def __call__(self, text: str, *, nb_keywords: int, **kwargs) -> List[Tuple[str, ...]]:
        ...
