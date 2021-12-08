import io
from typing import Optional, overload
from pydantic import HttpUrl
import bs4

import api.models.schemas as schemas
import api.models.factories as factories
from api.services.dom_managment.text_content_extraction import TextContentExtractor
import api.configurations.pipeline as algorithms_conf


class AlgorithmServices:

    @classmethod
    def augmentation(cls, url: [HttpUrl], algorithm_name: str, parameters) -> Optional[schemas.HTMLP]:
        augmentation_block = algorithms_conf.AugmentationBlocks.get_algorithm(algorithm_name)

        htmlp = augmentation_block(url, **parameters)
        return factories.Responses.HTMLP(htmlp)

    @classmethod
    def cleaning(cls, htmlp: schemas.HTMLP, algorithm_name: str, parameters) -> schemas.HTMLPP:
        cleaning_algorithm = algorithms_conf.CleaningBlocks.get_algorithm(algorithm_name)
        html_cleaned = cleaning_algorithm(htmlp, **parameters)

        return factories.Responses.HTMLPP(html_cleaned)

    @classmethod
    def segmentation(cls, htmlpp: schemas.HTMLPP, algorithm_name: str, parameters) -> schemas.Segmentation:
        segmentation_algorithm = algorithms_conf.SegmentationBlocks.get_algorithm(algorithm_name)
        segmentation = segmentation_algorithm(
            factories.AlgorithmInput.HTMLPP(htmlpp),
            **parameters
        )

        return factories.Responses.Segmentation(segmentation)

    @classmethod
    def extraction(cls, htmlpp: schemas.HTMLPP, algorithm_name: str, parameters) -> schemas.Keywords:
        text = TextContentExtractor.extract_all_text(factories.AlgorithmInput.HTMLPP(htmlpp))
        text = "; ".join(text)

        extraction_algorithm = algorithms_conf.ExtractionBlocks.get_algorithm(algorithm_name)
        keywords = extraction_algorithm(text, **parameters)

        return factories.Responses.Keywords(keywords)

    @classmethod
    def vocalization(cls, keywords: schemas.Keywords, algorithm_name: str, parameters) -> io.BytesIO:
        vocalization_algorithm = algorithms_conf.VocalizationBlocks.get_algorithm(algorithm_name)
        return vocalization_algorithm(factories.AlgorithmInput.Keywords(keywords), **parameters)
