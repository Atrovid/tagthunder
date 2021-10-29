from typing import Optional, Union

import algorithms.models
import api.configurations.algorithms as algos

from pydantic.main import BaseModel
from pydantic.networks import HttpUrl


class HTMLAugmentationQuery(BaseModel):
    input: Union[HttpUrl, str]
    recompute: Optional[bool] = False


class Queries:
    EXTRACTION = Union[algos.ExtractionAlgorithms.query_types]
    CLEANING = Union[algos.CleaningAlgorithms.query_types]
    SEGMENTATION = Union[algos.SegmentationAlgorithms.query_types]


class DefaultQueries:
    EXTRACTION = algos.ExtractionAlgorithms.default_query
    CLEANING = algos.CleaningAlgorithms.default_query
    SEGMENTATION = algos.SegmentationAlgorithms.default_query


class AlgorithmQuery(BaseModel):
    pass


class CleaningQuery(AlgorithmQuery):
    htmlp: algorithms.responses.HTMLP
    algorithm: Optional[Queries.CLEANING] = DefaultQueries.CLEANING


class SegmentationQuery(AlgorithmQuery):
    htmllpp: algorithms.responses.HTMLPP
    algorithm: Optional[Queries.SEGMENTATION] = DefaultQueries.SEGMENTATION


class ExtractionQuery(AlgorithmQuery):
    htmlpp: algorithms.responses.HTMLPP
    algorithm: Optional[Queries.EXTRACTION] = DefaultQueries.EXTRACTION


# class SpatializationQuery(AlgorithmQuery):
#     htmlpp: str = HTMLPP
#     algorithm: Union[SPATIALIZATION_QUERIES]


class PipelineQuery(BaseModel):
    url: HttpUrl
    htmlpp: algorithms.responses.HTMLPP
    recompute: bool = False
    cleaning: Optional[Queries.CLEANING] = DefaultQueries.CLEANING
    segmentation: Optional[Queries.SEGMENTATION] = DefaultQueries.SEGMENTATION
    extraction: Optional[Queries.EXTRACTION] = DefaultQueries.EXTRACTION
