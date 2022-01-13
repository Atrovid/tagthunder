from typing import List

import yake

from pipeline.blocks.extraction._abstract import AbstractExtractionBlock
from pipeline.blocks.extraction.utils.text_content_extraction import TextExtractor
from pipeline.models.responses import Keyword, Segmentation


class Yake(AbstractExtractionBlock):

    def __init__(self):
        self.window_size = None
        self.max_ngram_size = None
        self.language = None
        self.nb_keywords = None

    def config(
            self,
            nb_keywords: int = 5,
            language: str = "fr",
            max_ngram_size: int = 5,
            window_size: int = 4
    ):
        self.nb_keywords = nb_keywords
        self.language = language
        self.max_ngram_size = max_ngram_size
        self.window_size = window_size

    def __call__(self, segmentation: Segmentation) -> Segmentation:
        custom_extractor = yake.KeywordExtractor(
            n=self.max_ngram_size,
            windowsSize=self.window_size,
            top=self.nb_keywords,
            lan=self.language
        )

        for zone in segmentation.zones:
            zone.keywords = [
                Keyword(text=k, score=s)
                for k, s in custom_extractor.extract_keywords(";".join(TextExtractor.extract(zone.htmlpp)))
            ]

        return segmentation
