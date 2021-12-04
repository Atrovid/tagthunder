from abc import ABC, abstractmethod

from pipeline.models.responses import HTMLPP, HTMLP


class AbstractCleaningBlock(ABC):

    @abstractmethod
    def __call__(self, *, htmlp: HTMLP) -> HTMLPP:
        ...
