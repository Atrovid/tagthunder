from typing import List

import fastapi

# import api.routers.logics as logics
import api.routers.queries as queries
import api.models.responses as responses

tag_name = "Algorithms"
tag = {
    "name": tag_name,
    "description": "Routes to call TagThunder algorithms"
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
    PIPELINE: str = "/pipeline/"


# @router.get(
#     Routes.AUGMENTATION,
#     description="HTML+ generation",
#     response_model=schemas.HTML,
# )
# def get_html_augmentation(
#         url: HttpUrl,
#         recompute: Optional[bool] = False
# ):
#     response = logics.make_html_augmented(url, recompute)
#     return response
#
#
# @router.post(
#     Routes.AUGMENTATION,
#     description="HTML+ generation",
#     response_model=schemas.HTML
# )
# def post_html_augmentation(query: queries.HTMLAugmentationQuery):
#     return get_html_augmentation(query.url, query.recompute)
#
#
@router.post(
    Routes.CLEANING,
    description="Web page cleaning operation",
    response_model=responses.HTMLPP
)
def cleaning(
        query: queries.CleaningQuery
):
    print(query)
    # pprint.pp(query)
    # parameters = dict(
    #     algorithm_name=query.algorithm.name,
    #     parameters=query.algorithm.parameters.dict()
    # )
#
#     return logics.make_cleaned_html.by_html(
#         html=query.html,
#         **parameters
#     )
#
#
@router.post(
    Routes.SEGMENTATION,
    description="Web page segmentation operation",
    response_model=responses.Segmentation,
)
def segmentation(
        query: queries.SegmentationQuery
):
    print(query)
#     return logics.make_segmented_html(
#         None,
#         query.html,
#         query.algorithm.name,
#         query.algorithm.parameters.dict(),
#         query.algorithm.parameters.is_segmentable_threshold
#     )
#

@router.post(
    Routes.EXTRACTION,
    description="Key terms extraction operation",
    response_model=responses.Keywords
)
def extraction(
        query: queries.ExtractionQuery
):
    print(query)
    # return logics.make_keywords(query.html, query.algorithm.name, query.algorithm.parameters.dict())


@router.post(
    Routes.PIPELINE,
    description="Pipeline of TagThunder operations",
    response_model=responses.Segmentation
)
def pipeline(
        query: queries.PipelineQuery
):
    print(query)
    # if not query.htmlpp:
    #     augmented_html = logics.make_html_augmented(query.url, query.recompute)
    #
    #     cleaned_html = logics.make_cleaned_html.by_html(
    #         augmented_html.html,
    #         query.cleaning.name,
    #         query.cleaning.parameters.dict()
    #     )
    #
    #     query.htmlpp = cleaned_html.html
    # print("HTMLPP", query.htmlpp)
    # segmentation = logics.make_segmented_html(
    #     query.url,
    #     query.htmlpp,
    #     query.segmentation.name,
    #     query.segmentation.parameters.dict(),
    #     query.segmentation.parameters.is_segmentable_threshold
    # )
    #
    # for zone in segmentation.zones:
    #     keywords = logics.make_keywords(
    #         zone.htmlpp,
    #         query.extraction.name,
    #         query.extraction.parameters.dict()
    #     )
    #     zone.keywords = keywords
    #
    # return segmentation
