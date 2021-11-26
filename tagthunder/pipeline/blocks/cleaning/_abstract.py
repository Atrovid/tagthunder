from abc import ABC, abstractmethod

from pipeline.models.responses import HTMLPP


class AbstractCleaningBlock(ABC):

    @abstractmethod
    def __call__(self, html: str) -> HTMLPP:
        ...
