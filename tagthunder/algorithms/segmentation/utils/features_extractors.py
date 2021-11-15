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
        nodes = root.find_all(
            self.keep_node,
            attrs={
                "data-style": re.compile("display:block"),
                "data-cleaned": "false"
            }
        )
        # return nodes
        return self.remove_redundancies(nodes)

    @classmethod
    def remove_redundancies(cls, nodes):
        """Remove element if it is contained by another one."""
        return list(filter(
            lambda node: all(parent not in nodes for parent in node.parents),
            nodes
        ))

    @classmethod
    def keep_node(cls, node):
        conditions = [
            # cls.is_div,
            cls.is_title,
            cls.is_paragraph,
            cls.is_list_item,
            cls.is_image,
            cls.is_form,
            cls.is_line_break,
        ]

        return any([cond(node) for cond in conditions])

    @classmethod
    def is_title(cls, node):
        return node.name in [f"h{i}" for i in range(1, 3)]

    @classmethod
    def is_paragraph(cls, node):
        return node.name == "p"

    @classmethod
    def is_div(cls, node):
        return node.name == "div" and bool(node.h1) and node.text != node.h1.text

    @classmethod
    def is_list_item(cls, node):
        return node.name == "li" and bool(
            [child for child in node.children if not isinstance(child, bs4.NavigableString)])

    @classmethod
    def is_line_break(cls, node):
        return node.name in ["br", "hr"]

    @classmethod
    def is_image(cls, node):
        return node.name == "a"

    @classmethod
    def is_form(cls, node):
        return node.name in ["label", "input"]


if __name__ == '__main__':
    json_file = "../../data/html++/calvados.html"
    with open(json_file, "r") as f:
        htmlpp = HTMLPP.parse_obj(" ".join(f.readlines()))

    extractor = AccordingRules()

    elements = extractor(htmlpp)
    print(len(elements))

    for e in elements:
        print(e.prettify())
