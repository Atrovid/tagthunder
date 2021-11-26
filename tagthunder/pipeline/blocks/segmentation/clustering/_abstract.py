from abc import ABC

from pipeline.blocks.segmentation._abstract import AbstractSegmentationBlock


class AbstractClusteringBlock(AbstractSegmentationBlock, ABC):
    ...
