from typing import Optional, Union

import api.configurations.pipeline as algos
import api.models.schemas as api_schemas

from pydantic.main import BaseModel
from pydantic.networks import HttpUrl


class HTMLAugmentationQuery(BaseModel):
    url: Union[HttpUrl]
    recompute: Optional[bool] = False


class Queries:
    EXTRACTION = Union[algos.ExtractionBlocks.query_types]
    CLEANING = Union[algos.CleaningBlocks.query_types]
    SEGMENTATION = Union[algos.SegmentationBlocks.query_types]
    VOCALIZATION = Union[algos.VocalizationBlocks.query_types]


class DefaultQueries:
    EXTRACTION = algos.ExtractionBlocks.default_query
    CLEANING = algos.CleaningBlocks.default_query
    SEGMENTATION = algos.SegmentationBlocks.default_query
    VOCALIZATION = algos.VocalizationBlocks.default_query


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


class VocalizationQuery(AlgorithmQuery):
    keywords: api_schemas.Keywords
    algorithm: Optional[Queries.VOCALIZATION] = DefaultQueries.VOCALIZATION


class PipelineQuery(AlgorithmQuery):
    url: HttpUrl
    htmlpp: Optional[api_schemas.HTMLPP]
    recompute: bool = False
    cleaning: Optional[Queries.CLEANING] = DefaultQueries.CLEANING
    segmentation: Optional[Queries.SEGMENTATION] = DefaultQueries.SEGMENTATION
    extraction: Optional[Queries.EXTRACTION] = DefaultQueries.EXTRACTION
    vocalization: Optional[Queries.VOCALIZATION] = DefaultQueries.VOCALIZATION
