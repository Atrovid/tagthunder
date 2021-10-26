from abc import ABC, abstractmethod

from algorithms.models import HTMLPP

class AbstractCleaningAlgorithm(ABC):

    @abstractmethod
    def __call__(self, html: str) -> HTMLPP:
        ...
