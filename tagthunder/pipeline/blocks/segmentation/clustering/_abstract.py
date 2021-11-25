from abc import ABC

from pipeline.blocks.segmentation._abstract import AbstractSegmentationAlgorithm


class AbstractClusteringAlgorithm(AbstractSegmentationAlgorithm, ABC):
    ...
