import dataclasses
import json
import pprint
from abc import ABC, abstractmethod
from typing import List

import bs4
import re

from algorithms.models.responses import HTMLPP
from algorithms.models.web_elements import BoundingBox, Tag


@dataclasses.dataclass
class Features:
    tags: List[Tag]
    bboxes: List[BoundingBox] = dataclasses.field(init=False)

    def __post_init__(self):
        self.bboxes = [tag.bbox for tag in self.tags]


class AbstractFeaturesExtractor(ABC):

    @abstractmethod
    def __call__(self, htmlpp: HTMLPP, **kwargs) -> Features:
        ...


class LastBlockSemantic(AbstractFeaturesExtractor):
    __basic_visual_elements__ = (
        "address",
        "article",
        "aside",
        "blockquote",
        "details",
        "dialog",
        "dd",
        "div",
        "dl",
        "dt",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        *[f"h{i}" for i in range(1, 7)],
        "header",
        "hgroup",
        "hr",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "ul"
    )

    def __call__(self, htmlpp: HTMLPP, **kwargs):
        tags = filter(
            (
                lambda e:
                not len(e.find_all(self.__basic_visual_elements__))
                and len(e.text)
                and e.attrs["data-cleaned"] == "false"
            ),
            htmlpp.find_all(self.__basic_visual_elements__)
        )
        tags = list(tags)
        return Features(tags=tags)


class LastBlocksWithComputedStyles(AbstractFeaturesExtractor):
    BLOCK_REGEX = re.compile(r"display:block")

    def __call__(self, htmlpp: HTMLPP, **kwargs):
        elements = self.find_basics_elements(htmlpp)
        elements = filter(
            (
                lambda e:
                not bool(len(self.find_basics_elements(e)))
                and len(e.contents)
            ),
            elements
        )
        elements = list(elements)
        return Features(tags=elements)

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

    def __call__(self, htmlpp: HTMLPP, **kwargs):
        nodes = htmlpp.find_all(
            self.keep_node,
            attrs={
                "data-style": re.compile("display:block"),
                "data-cleaned": "false"
            }
        )
        nodes = self.remove_redundancies(nodes)
        return Features(tags=nodes)

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
