import io
from typing import List

import fastapi
import pydantic

import api.routers.queries as queries
import api.models.schemas as schemas
import api.routers.services as services

pydantic.BaseConfig.arbitrary_types_allowed = True

tag_name = "Algorithms"
tag = {
    "name": tag_name,
    "description": "Routes to call TagThunder pipeline"
}

router = fastapi.APIRouter(
    prefix="/ask",
    tags=[tag_name]
)


class Routes:
    AUGMENTATION: str = "/augmentation/"
    CLEANING: str = "/cleaning/"
    SEGMENTATION: str = "/segmentation/"
    EXTRACTION: str = "/extraction/"
    VOCALIZATION: str = "/vocalization/"
    PIPELINE: str = "/pipeline/"


@router.post(
    Routes.AUGMENTATION,
    description="HTML+ generation",
    response_model=schemas.HTMLP
)
def post_html_augmentation(query: queries.HTMLAugmentationQuery):
    return services.AlgorithmServices.html_augmentation(query.url, query.recompute)


@router.post(
    Routes.CLEANING,
    description="Web page cleaning operation",
    response_model=schemas.HTMLPP
)
def cleaning(
        query: queries.CleaningQuery
):
    return services.AlgorithmServices.cleaning(
        query.htmlp,
        query.algorithm.name,
        query.algorithm.parameters.dict()
    )


@router.post(
    Routes.SEGMENTATION,
    description="Web page segmentation operation",
    response_model=schemas.Segmentation
)
def segmentation(
        query: queries.SegmentationQuery
):
    return services.AlgorithmServices.segmentation(
        query.htmllpp,
        query.algorithm.name,
        query.algorithm.parameters.dict()
    )


@router.post(
    Routes.EXTRACTION,
    description="Key terms extraction operation",
    response_model=schemas.Keywords
)
def extraction(
        query: queries.ExtractionQuery
):
    return services.AlgorithmServices.extraction(
        query.htmlpp,
        query.algorithm.name,
        query.algorithm.parameters.dict()
    )


@router.post(
    Routes.VOCALIZATION,
    description="Vocalization of key-terms",
    response_class=fastapi.responses.StreamingResponse
)
async def vocalization(
        query: queries.VocalizationQuery
):
    audio = services.AlgorithmServices.vocalization(
        query.keywords,
        query.algorithm.name,
        query.algorithm.parameters.dict()
    )
     
    return fastapi.responses.StreamingResponse(audio, media_type="audio/mpeg3")


@router.post(
    Routes.PIPELINE,
    description="Pipeline of TagThunder operations",
    response_model=schemas.Segmentation
)
def pipeline(
        query: queries.PipelineQuery
):
    raise NotImplementedError()
