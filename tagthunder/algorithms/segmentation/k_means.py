from algorithms.models import Segmentation
from algorithms.segmentation._abstract import AbstractSegmentationAlgorithm


class KMeans(AbstractSegmentationAlgorithm):
    def __call__(self, text: str, *, nb_zones: int, **kwargs) -> Segmentation:
        raise NotImplementedError

    @classmethod
    def compute_edges(cls, ):
