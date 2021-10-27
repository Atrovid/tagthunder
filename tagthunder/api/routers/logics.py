from typing import Optional

import bs4
from models import CLEANING_ALGORITHMS, SEGMENTATION_ALGORITHMS, EXTRACTION_ALGORITHMS
from models.dom_managment.augmentation import HTMLAugmentedRequester
from models.dom_managment.extraction import TextContentExtractor
from models.responses.response_builder import SegmentationResponseBuilder
from models.responses.schemas import HTML, Segmentation, Keywords
from pydantic.networks import HttpUrl


def make_html_augmented(url: HttpUrl, recompute: bool = False) -> Optional[HTML]:
    response = HTMLAugmentedRequester.call(url, recompute)

    if response[HTMLAugmentedRequester.STATUS_KEY] == HTMLAugmentedRequester.STATUS_OK:
        return HTML(**response)
    return


class HTMLCleaner:

    @classmethod
    def by_html(cls, html: str, algorithm_name: str, parameters) -> HTML:
        cleaning_algorithm = CLEANING_ALGORITHMS[algorithm_name]
        html_cleaned = cleaning_algorithm(html, **parameters)
        return HTML(html=html_cleaned)

    @classmethod
    def by_url(cls, url: HttpUrl, algorithm_name: str, parameters) -> HTML:
        html_augmented = make_html_augmented(url)
        if not html_augmented:
            raise ValueError

        html_cleaned = cls.by_html(html_augmented.html, algorithm_name, parameters)
        html_cleaned.url = url

        return html_cleaned


make_cleaned_html = HTMLCleaner


def make_segmented_html(url: Optional[str], html: str, algorithm_name: str, parameters,
                        segmentation_threshold) -> Segmentation:
    segmentation_algorithm = SEGMENTATION_ALGORITHMS[algorithm_name]
    segmentation = segmentation_algorithm(html, **parameters)
    response = SegmentationResponseBuilder.build_response(url, segmentation["zones"], segmentation_threshold)
    return response


def make_keywords(html: str, algorithm_name: str, parameters) -> Keywords:
    soup = bs4.BeautifulSoup(html, "html.parser")
    text = TextContentExtractor.extract_all_text(soup)
    text = "; ".join(text)

    extraction_algorithm = EXTRACTION_ALGORITHMS[algorithm_name]
    keywords = extraction_algorithm(text, **parameters)

    return keywords
