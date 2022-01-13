import abc


class AbstractPipelineBlock(abc.ABC):

    @abc.abstractmethod
    def config(self, **kwargs):
        ...