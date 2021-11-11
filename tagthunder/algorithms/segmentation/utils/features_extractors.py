import json
from abc import ABC, abstractmethod
from typing import List

import bs4
import re

from algorithms.models.responses import HTMLPP
from models.factories import DataStylesFactory


class AbstractFeaturesExtractor(ABC):

    @abstractmethod
    def __call__(self, htmlpp: HTMLPP):
        ...


class LastBlocks(AbstractFeaturesExtractor):
    BLOCK_REGEX = re.compile(r"display:block")

    def __call__(self, htmlpp: HTMLPP):
        soup = bs4.BeautifulSoup(htmlpp.__root__, 'html.parser')
        elements = self.find_basics_elements(soup)
        elements = filter(
            (
                lambda e:
                bool(len(self.find_basics_elements(e)))
                and len(e.contents)
            ),
            elements
        )
        return list(elements)

    @classmethod
    def find_basics_elements(cls, node):
        return node.find_all(
            True,
            attrs={
                "data-cleaned": "false",
                "data-style": cls.BLOCK_REGEX
            }
        )


class AccordingRules(AbstractFeaturesExtractor):

    def __call__(self, htmlpp: HTMLPP):
        pass

    # @classmethod


if __name__ == '__main__':
    json_file = "../../data/cleaned_html/response_1633951666404.json"
    with open(json_file, "r") as f:
        content = json.load(f)
        htmlpp = HTMLPP.parse_obj(content["html"])

    extractor = LastBlocks()

    elements = extractor(htmlpp)
    print(len(elements))
