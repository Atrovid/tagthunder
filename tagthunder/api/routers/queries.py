from typing import Optional, Union

import api.configurations.pipeline as algos
import api.models.schemas as api_schemas

from pydantic.main import BaseModel
from pydantic.networks import HttpUrl


class HTMLAugmentationQuery(BaseModel):
    url: Union[HttpUrl]
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
    htmlp: api_schemas.HTMLP
    algorithm: Optional[Queries.CLEANING] = DefaultQueries.CLEANING


class SegmentationQuery(AlgorithmQuery):
    htmllpp: api_schemas.HTMLPP
    algorithm: Optional[Queries.SEGMENTATION] = DefaultQueries.SEGMENTATION


class ExtractionQuery(AlgorithmQuery):
    htmlpp: api_schemas.HTMLPP
    algorithm: Optional[Queries.EXTRACTION] = DefaultQueries.EXTRACTION


class PipelineQuery(AlgorithmQuery):
    url: HttpUrl
    htmlpp: Optional[api_schemas.HTMLPP]
    recompute: bool = False
    cleaning: Optional[Queries.CLEANING] = DefaultQueries.CLEANING
    segmentation: Optional[Queries.SEGMENTATION] = DefaultQueries.SEGMENTATION
    extraction: Optional[Queries.EXTRACTION] = DefaultQueries.EXTRACTION
