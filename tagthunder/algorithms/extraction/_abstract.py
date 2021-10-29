from abc import ABC, abstractmethod

from algorithms.models.responses import Keywords


class AbstractExtractionAlgorithm(ABC):

    @abstractmethod
    def __call__(self, text: str, *, nb_keywords: int, **kwargs) -> Keywords:
        ...
