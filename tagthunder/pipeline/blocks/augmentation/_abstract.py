from abc import ABC, abstractmethod

from pipeline.models.responses import HTML, HTMLP


class AbstractAugmentationBlock(ABC):

    @abstractmethod
    def __call__(self, html: str) -> HTMLP:
        ...
