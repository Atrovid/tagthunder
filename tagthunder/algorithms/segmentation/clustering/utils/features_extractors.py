import dataclasses
import json
import pprint
from abc import ABC, abstractmethod
from typing import List, Iterable

import bs4
import re

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

from algorithms.models.responses import HTMLPP
from algorithms.models.web_elements import BoundingBox, Tag


class FeaturesDataFrame(DataFrame):

    def __init__(self, tags=None, index=None, columns=None, dtype=None, copy=None):
        if tags is not None:
            tags = [self._tag_to_entry(tag) for tag in tags]

        super(FeaturesDataFrame, self).__init__(
            data=tags,
            index=index, columns=columns, dtype=dtype, copy=copy
        )

    @classmethod
    def _tag_to_entry(cls, tag: Tag):
        res = Series({
            "name": tag.name,
            "bbox": tag.bbox,
            "visible": tag.visible,
            "styles": tag.styles
        })
        return res

    def append(
            self,
            other,
            ignore_index: bool = False,
            verify_integrity: bool = False,
            sort: bool = False,
    ) -> DataFrame:
        if isinstance(other, Tag):
            other = self._tag_to_entry(other)
            ignore_index = True
        return super(FeaturesDataFrame, self).append(other, ignore_index, verify_integrity, sort)


class AbstractFeaturesExtractor(ABC):

    @abstractmethod
    def __call__(self, htmlpp: HTMLPP, **kwargs) -> FeaturesDataFrame:
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
        return FeaturesDataFrame(tags=tags)


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
        return FeaturesDataFrame(tags=elements)

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
        return FeaturesDataFrame(tags=nodes)

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


class TOIS(AbstractFeaturesExtractor):
    NOT_TVE = (
        "html", "head", "iframe", "title", "meta",
        "link", "script", "style", "strong", "b",
        "big", "i", "small", "tt", "abbr", "acronym",
        "cite", "code", "dfn", "em", "kbd", "samp",
        "var", "a", "bdo", "br", "map", "object",
        "q", "span", "sub", "sup", "button", "input",
        "label", "select", "option", "textarea"
    )
    TVE = (
        "div", "section", "article", "main", "aside", "header", "footer"
    )

    def __call__(self, htmlpp: HTMLPP, **kwargs) -> FeaturesDataFrame:
        return FeaturesDataFrame(self.get_features(htmlpp))

    @classmethod
    def get_features(self, htmlpp: HTMLPP):
        return htmlpp.find_all(lambda node: self.keep_node(node))

    @classmethod
    def keep_node(cls, node):
        return (
                cls.is_visible(node)
                and
                not cls.in_not_tve(node)
                and (
                        ((cls.in_tve(node) or cls.is_block(node))
                         and (
                                 cls.all_children(node, lambda child: cls.in_not_tve(child) or cls.is_inline(child))
                                 or cls.has_exactly_one_child(node)
                         ))
                        or not cls.has_children(node)
                )
        )

    @classmethod
    def is_visible(cls, node: Tag):
        return node.visible

    @classmethod
    def all_children(cls, node, condition):
        return all(
            condition(child)
            for child in node.find_all(True, 1)
        )

    @classmethod
    def in_not_tve(cls, node: Tag):
        return node.name in cls.NOT_TVE

    @classmethod
    def in_tve(cls, node: Tag):
        return node.name in cls.TVE

    @classmethod
    def is_block(cls, node: Tag):
        return node.styles.get("display") in ("block", "inline-block")

    @classmethod
    def is_inline(cls, node: Tag):
        return node.styles.get("display") == "inline"

    @classmethod
    def has_children(cls, node: Tag):
        return bool(node.contents)

    @classmethod
    def has_exactly_one_child(cls, node: Tag):
        return len(node.contents) == 1


if __name__ == '__main__':
    json_file = "../../../data/html++/calvados.raw.json"

    with open(json_file, "r") as f:
        content = json.load(f)
        htmlpp = HTMLPP(content["html"])

    features_extractor = TOIS()
    features = features_extractor.get_features(htmlpp)
    print(len(features))
    print(f"keep_node : {all([TOIS.keep_node(tag) for tag in features])}")
