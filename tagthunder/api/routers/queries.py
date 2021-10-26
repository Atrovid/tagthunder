from typing import Optional, Union

import api.configurations.algorithms as algos
import api.models.fields as fields

from pydantic.main import BaseModel
from pydantic.networks import HttpUrl



class BaseQuery(BaseModel):
    url: Optional[HttpUrl] = None
    html: Optional[str] = None


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
    htmlpp: str = fields.HTMLPP
    algorithm: Optional[Queries.CLEANING] = DefaultQueries.CLEANING


class SegmentationQuery(AlgorithmQuery):
    htmllpp: str = fields.HTMLPP
    algorithm: Optional[Queries.SEGMENTATION] = DefaultQueries.SEGMENTATION


class ExtractionQuery(AlgorithmQuery):
    htmlpp: str = fields.HTMLPP
    algorithm: Optional[Queries.EXTRACTION] = DefaultQueries.EXTRACTION


# class SpatializationQuery(AlgorithmQuery):
#     htmlpp: str = HTMLPP
#     algorithm: Union[SPATIALIZATION_QUERIES]


class PipelineQuery(BaseModel):
    url: HttpUrl
    htmlpp: str = fields.HTMLPP
    recompute: bool = False
    cleaning: Optional[Queries.CLEANING] = DefaultQueries.CLEANING
    segmentation: Optional[Queries.SEGMENTATION] = DefaultQueries.SEGMENTATION
    extraction: Optional[Queries.EXTRACTION] = DefaultQueries.EXTRACTION
