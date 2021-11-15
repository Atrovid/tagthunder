import json
import pprint
from abc import ABC, abstractmethod
from typing import List

import bs4
import re

from algorithms.models.responses import HTMLPP


class AbstractFeaturesExtractor(ABC):

    @abstractmethod
    def __call__(self, htmlpp: HTMLPP):
        ...

    @classmethod
    def root(cls, htmlpp: HTMLPP):
        return bs4.BeautifulSoup(htmlpp.__root__, 'html.parser')


class LastBlocks(AbstractFeaturesExtractor):
    BLOCK_REGEX = re.compile(r"display:block")

    def __call__(self, htmlpp: HTMLPP):
        root = self.root(htmlpp)
        elements = self.find_basics_elements(root)
        elements = filter(
            (
                lambda e:
                not bool(len(self.find_basics_elements(e)))
                and len(e.contents)
            ),
            elements
        )
        return set(elements)

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
        root = self.root(htmlpp)

        return set()

    @classmethod
    def _titles(cls, node):
        return node.find_all([f"h{i}" for i in range(1, 2)])

    @classmethod
    def _paragraphs(cls, node):
        return node.find_all("p")

    @classmethod
    def _div(cls, node):
        divs = node.div
        divs = filter(
            lambda div: bool(div.h1),
            divs
        )



if __name__ == '__main__':
    json_file = "../../data/html++/calvados.html"
    with open(json_file, "r") as f:
        htmlpp = HTMLPP.parse_obj(" ".join(f.readlines()))

    extractor = AccordingRules()

    elements = extractor(htmlpp)
    print(len(elements))
    for e in elements:
        print(e, "\n")
