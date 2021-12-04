from abc import ABC, abstractmethod
from typing import Optional

from pydantic import HttpUrl

from pipeline.models.responses import HTML, HTMLP


class AbstractAugmentationBlock(ABC):

    @abstractmethod
    def __call__(self, *, html: HTML, url: HttpUrl) -> HTMLP:
        ...
