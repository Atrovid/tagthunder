import base64
import io
import typing

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
    response_class=fastapi.responses.HTMLResponse,
    response_model=schemas.HTMLP
)
def post_html_augmentation(query: queries.AugmentationQuery):
    return services.AlgorithmServices.augmentation(
        query.url,
        query.algorithm.name,
        query.algorithm.parameters.dict()
    )


@router.post(
    Routes.CLEANING,
    description="Web page cleaning operation",
    response_class=fastapi.responses.HTMLResponse,
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
    response_class=fastapi.responses.JSONResponse,
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
    response_class=fastapi.responses.JSONResponse,
    response_model=schemas.Keywords
)
def extraction(
        query: queries.ExtractionQuery
):
    return services.AlgorithmServices.extraction(
        query.segmentation,
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
    return services.AlgorithmServices.vocalization(
        query.segmentation,
        query.algorithm.name,
        query.algorithm.parameters.dict()
    )


@router.post(
    Routes.PIPELINE,
    description="Pipeline of TagThunder operations",
    # response_class=typing.Union[
    #     fastapi.responses.StreamingResponse,
    #     fastapi.responses.JSONResponse
    # ],
    response_model=typing.Union[
        schemas.HTMLP,
        schemas.HTMLPP,
        schemas.Segmentation
    ]
)
def pipeline(
        query: queries.PipelineQuery
):
    res = None
    if query.augmentation is not None:
        res = services.AlgorithmServices.augmentation(
            query.url,
            query.augmentation.name,
            query.augmentation.parameters.dict()
        )
    if query.cleaning is not None:
        res = services.AlgorithmServices.cleaning(
            htmlp=res,
            algorithm_name=query.cleaning.name,
            parameters=query.cleaning.parameters.dict()
        )
    if query.segmentation is not None:
        res = services.AlgorithmServices.segmentation(
            htmlpp=res,
            algorithm_name=query.segmentation.name,
            parameters=query.segmentation.parameters.dict()
        )
    if query.extraction is not None:
        res = services.AlgorithmServices.extraction(
            segmentation=res,
            algorithm_name=query.extraction.name,
            parameters=query.extraction.parameters.dict()
        )

    if query.vocalization is not None:
        res = services.AlgorithmServices.vocalization(
            segmentation=res,
            algorithm_name=query.vocalization.name,
            parameters=query.vocalization.parameters.dict()
        )

    return res
