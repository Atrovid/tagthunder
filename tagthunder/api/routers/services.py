import io
from typing import Optional

from pydantic import HttpUrl

import api.models.schemas as schemas
import api.models.factories as factories
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
        html_cleaned = cleaning_algorithm(factories.AlgorithmInput.HTMLP(htmlp), **parameters)
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
    def extraction(cls, segmentation: schemas.Segmentation, algorithm_name: str, parameters) -> schemas.Segmentation:
        extraction_algorithm = algorithms_conf.ExtractionBlocks.get_algorithm(algorithm_name)
        segmentation = extraction_algorithm(factories.AlgorithmInput.Segmentation(segmentation), **parameters)

        return factories.Responses.Segmentation(segmentation)

    @classmethod
    def vocalization(cls, keywords: schemas.Keywords, algorithm_name: str, parameters) -> io.BytesIO:
        vocalization_algorithm = algorithms_conf.VocalizationBlocks.get_algorithm(algorithm_name)
        return vocalization_algorithm(factories.AlgorithmInput.Keywords(keywords), **parameters)
