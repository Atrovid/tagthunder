from abc import ABC, abstractmethod
from pipeline.blocks._abstract import AbstractPipelineBlock


class AbstractSpatializationBlock(AbstractPipelineBlock):

    @abstractmethod
    def __call__(self, **kwargs):
        ...
