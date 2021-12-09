from typing import List

import yake

from pipeline.blocks.extraction._abstract import AbstractExtractionBlock
from pipeline.blocks.extraction.utils.text_content_extraction import TextExtractor
from pipeline.models.responses import Keywords, Segmentation


class Yake(AbstractExtractionBlock):

    def __call__(
            self,
            segmentation: Segmentation,
            *,
            nb_keywords: int,
            language: str = "fr",
            max_ngram_size: int = 4,
            window_size: int = 3
    ) -> Segmentation:
        custom_extractor = yake.KeywordExtractor(
            n=max_ngram_size,
            windowsSize=window_size,
            top=nb_keywords,
            lan=language
        )

        for zone in segmentation.zones:
            zone.keywords = Keywords(custom_extractor.extract_keywords(TextExtractor.extract(zone.htmlpp)))

        return segmentation