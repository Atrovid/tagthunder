from typing import List, Tuple

import yake

from algorithms.extraction._abstract import AbstractExtractionAlgorithm
from algorithms.models import Keywords


class Yake(AbstractExtractionAlgorithm):

    def __call__(
            self,
            text: str,
            *,
            nb_keywords: int,
            language: str = "fr",
            max_ngram_size: int = 4,
            window_size: int = 3
    ) -> Keywords:
        custom_extractor = yake.KeywordExtractor(
            n=max_ngram_size,
            windowsSize=window_size,
            top=nb_keywords,
            lan=language
        )

        keywords = custom_extractor.extract_keywords(text)

        return keywords
