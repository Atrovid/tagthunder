from abc import ABC, abstractmethod

from tagthunder.algorithms.models import HTMLPP


class AbstractCleaningAlgorithm(ABC):

    @abstractmethod
    def __call__(self, html) -> HTMLPP:
        ...
