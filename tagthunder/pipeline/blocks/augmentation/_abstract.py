from abc import ABC, abstractmethod
from typing import Optional, List

from pydantic import HttpUrl

from pipeline.models.responses import HTML, HTMLP
from pipeline.blocks._abstract import AbstractPipelineBlock


class AbstractAugmentationBlock(AbstractPipelineBlock):

    def __init__(self):
        self.styles = None

    def config(self, styles: Optional[List[str]] = None):
        if styles is None:
            styles = []
        self.styles = styles

    @abstractmethod
    def __call__(self, html: HTML, url: HttpUrl, **kwargs) -> HTMLP:
        ...
