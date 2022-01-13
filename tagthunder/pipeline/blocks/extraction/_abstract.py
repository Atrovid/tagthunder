from abc import ABC, abstractmethod
from typing import List

from pipeline.models.responses import Keywords, Segmentation
from pipeline.blocks._abstract import AbstractPipelineBlock


class AbstractExtractionBlock(AbstractPipelineBlock):

    @abstractmethod
    def __call__(self, segmentation: Segmentation) -> List[Keywords]:
        ...
