from typing import Optional, Union
from pydantic import HttpUrl
import bs4

import api.models.schemas as schemas
from api.services.dom_managment.augmentation import get_augmented_html
from api.services.dom_managment.text_content_extraction import TextContentExtractor
import api.configurations.algorithms as algorithms


def make_html_augmented(url: HttpUrl, recompute: bool = False) -> Optional[schemas.HTMLP]:
    response = get_augmented_html(url, recompute)

    if get_augmented_html.is_ok(response):
        return schemas.HTMLP(response)
    return


def make_cleaned_html(input: Union[HttpUrl, schemas.HTMLP], algorithm_name: str, parameters) -> schemas.HTMLPP:
    cleaning_algorithm = algorithms.CleaningAlgorithms.get_algorithm(algorithm_name)
    if isinstance(input, HttpUrl):
        html = make_html_augmented(input)
    else:
        html = input

    html_cleaned = cleaning_algorithm(html, **parameters)
    return schemas.HTMLPP(__root__=html_cleaned)


def make_segmented_html(url: Optional[str], html: str, algorithm_name: str, parameters,
                        segmentation_threshold) -> schemas.Segmentation:
    segmentation_algorithm = algorithms.SegmentationAlgorithms.get_algorithm(algorithm_name)
    segmentation = segmentation_algorithm(html, **parameters)
    return schemas.Segmentation()
    # response = SegmentationResponseBuilder.build_response(url, segmentation["zones"], segmentation_threshold)
    # return response


def make_keywords(html: str, algorithm_name: str, parameters) -> schemas.Keywords:
    soup = bs4.BeautifulSoup(html, "html.parser")
    text = TextContentExtractor.extract_all_text(soup)
    text = "; ".join(text)

    extraction_algorithm = algorithms.ExtractionAlgorithms.get_algorithm(algorithm_name)
    keywords = extraction_algorithm(text, **parameters)

    return keywords
