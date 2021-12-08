from abc import ABC, abstractmethod

from pipeline.models.responses import Keywords


class AbstractExtractionBlock(ABC):

    @abstractmethod
    def __call__(self, text: str, *, nb_keywords: int, **kwargs) -> Keywords:
        ...