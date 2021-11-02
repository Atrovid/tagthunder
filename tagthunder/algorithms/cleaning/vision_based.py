from algorithms.cleaning._abstract import AbstractCleaningAlgorithm
from algorithms.models.responses import HTMLPP


class VisionBased(AbstractCleaningAlgorithm):
    def __call__(self, html: str) -> HTMLPP:
        raise NotImplementedError
