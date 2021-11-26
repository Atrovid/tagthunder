from abc import ABC, abstractmethod


class AbstractSpatializationBlock(ABC):

    @abstractmethod
    def __call__(self, **kwargs):
        ...
