from abc import ABC, abstractmethod

from algorithms.models.responses import HTMLPP


class AbstractCleaningAlgorithm(ABC):

    @abstractmethod
    def __call__(self, html: str) -> HTMLPP:
        ...
