from abc import ABC, abstractmethod


class AbstractVocalizationBlock(ABC):

    @abstractmethod
    def __call__(self, **kwargs):
        ...
