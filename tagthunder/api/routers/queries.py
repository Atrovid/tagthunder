from typing import Optional, Union

import fastapi
import pydantic

import api.configurations.pipeline as algos
import api.models.schemas as api_schemas

from pydantic.main import BaseModel
from pydantic.networks import HttpUrl


class Queries:
    AUGMENTATION = Union[algos.AugmentationBlocks.query_types]
    EXTRACTION = Union[algos.ExtractionBlocks.query_types]
    CLEANING = Union[algos.CleaningBlocks.query_types]
    SEGMENTATION = Union[algos.SegmentationBlocks.query_types]
    VOCALIZATION = Union[algos.VocalizationBlocks.query_types]


class DefaultQuery:
    AUGMENTATION = algos.AugmentationBlocks.default_query
    EXTRACTION = algos.ExtractionBlocks.default_query
    CLEANING = algos.CleaningBlocks.default_query
    SEGMENTATION = algos.SegmentationBlocks.default_query
    VOCALIZATION = algos.VocalizationBlocks.default_query


class AlgorithmQuery(BaseModel):
    pass


class AugmentationQuery(AlgorithmQuery):
    url: HttpUrl = pydantic.Field(..., description="url", example="https://www.example.com")
    algorithm: Optional[Queries.AUGMENTATION] = DefaultQuery.AUGMENTATION


class CleaningQuery(AlgorithmQuery):
    htmlp: api_schemas.HTMLP
    algorithm: Optional[Queries.CLEANING] = DefaultQuery.CLEANING


class SegmentationQuery(AlgorithmQuery):
    htmllpp: api_schemas.HTMLPP
    algorithm: Optional[Queries.SEGMENTATION] = DefaultQuery.SEGMENTATION


class ExtractionQuery(AlgorithmQuery):
    segmentation: api_schemas.Segmentation
    algorithm: Optional[Queries.EXTRACTION] = DefaultQuery.EXTRACTION


class VocalizationQuery(AlgorithmQuery):
    segmentation: api_schemas.Segmentation
    algorithm: Optional[Queries.VOCALIZATION] = DefaultQuery.VOCALIZATION


class PipelineQuery(AlgorithmQuery):
    url: HttpUrl = pydantic.Field(..., description="url", example="https://www.example.com")
    htmlpp: Optional[api_schemas.HTMLPP] = pydantic.Field(..., description="HTML++", example="")
    augmentation: Optional[Queries.AUGMENTATION] = None
    cleaning: Optional[Queries.CLEANING] = None
    segmentation: Optional[Queries.SEGMENTATION] = None
    extraction: Optional[Queries.EXTRACTION] = None
    vocalization: Optional[Queries.VOCALIZATION] = None
