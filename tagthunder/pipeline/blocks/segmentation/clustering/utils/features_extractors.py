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

from pipeline.models.responses import HTMLPP
from pipeline.models.web_elements import BoundingBox, HTMLPPTag


class FeaturesDataFrame(DataFrame):

    def __init__(self, tags=None, index=None, columns=None, dtype=None, copy=None):
        if tags is not None:
            tags = [self._tag_to_entry(tag) for tag in tags]

        super(FeaturesDataFrame, self).__init__(
            data=tags,
            index=index, columns=columns, dtype=dtype, copy=copy
        )

    @classmethod
    def _tag_to_entry(cls, tag: HTMLPPTag):
        res = Series({
            "name": tag.name,
            "bbox": tag.bbox,
            "visible": tag.is_usable,
            "styles": tag.styles,
            "tag": tag
        })
        return res

    def append(
            self,
            other,
            ignore_index: bool = False,
            verify_integrity: bool = False,
            sort: bool = False,
    ) -> DataFrame:
        if isinstance(other, HTMLPPTag):
            other = self._tag_to_entry(other)
            ignore_index = True
        return super(FeaturesDataFrame, self).append(other, ignore_index, verify_integrity, sort)


class AbstractFeaturesExtractor(ABC):

    @abstractmethod
    def __call__(self, htmlpp: HTMLPP, **kwargs) -> FeaturesDataFrame:
        ...

    @classmethod
    def is_visible(cls, node: HTMLPPTag):
        return node.is_usable

    @classmethod
    def is_block(cls, node: HTMLPPTag, block_attrs=None):
        if block_attrs is None:
            block_attrs = ["block", "inline-block"]
        style = node.styles.get("display")
        return style in block_attrs

    @classmethod
    def has_content(cls, node: HTMLPPTag):
        return bool(node.contents)


class LastBlockSemantic(AbstractFeaturesExtractor):
    TVE = (
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
        return FeaturesDataFrame(tags=htmlpp.find_all(self.keep_node))

    @classmethod
    def keep_node(cls, node):
        return all([
            cls.is_visible(node),
            cls.in_tve(node),
            cls.no_child_in_tve(node),
            cls.contents_text(node),
        ])

    @classmethod
    def contents_text(cls, node: HTMLPPTag):
        return len(node.text)

    @classmethod
    def in_tve(cls, node):
        return node.name in cls.TVE

    @classmethod
    def no_child_in_tve(cls, node: HTMLPPTag):
        return not len(node.find_all(cls.in_tve))


class LastBlocksWithComputedStyles(AbstractFeaturesExtractor):

    def __call__(self, htmlpp: HTMLPP, **kwargs):
        elements = htmlpp.find_all(self.keep_node)
        df = FeaturesDataFrame(tags=elements)
        return df

    @classmethod
    def keep_node(cls, node: HTMLPPTag):
        return all([
            cls.is_basic_block(node),
            cls.has_content(node),
            not cls.has_basic_block_children(node)
        ])

    @classmethod
    def is_basic_block(cls, node):
        return cls.is_visible(node) and cls.is_block(node, ["block"])

    @classmethod
    def has_basic_block_children(cls, node: HTMLPPTag):
        return bool(node.find_all(lambda child: cls.is_basic_block(child)))


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
        return FeaturesDataFrame(tags=self.get_features(htmlpp))

    @classmethod
    def get_features(self, htmlpp: HTMLPP):
        return htmlpp.find_all(self.keep_node)

    @classmethod
    def keep_node(cls, node) -> bool:
        if cls.is_visible(node) and not cls.in_not_tve(node):
            if cls.in_tve(node) or cls.is_block(node):
                return any(
                    [
                        cls.all_children(node, lambda child: any([cls.in_not_tve(child), cls.is_inline(child)])),
                        cls.has_exactly_one_child(node)
                    ]
                )
            else:
                return not cls.has_children(node)
        return False

    @classmethod
    def is_visible(cls, node: HTMLPPTag):
        return node.is_usable

    @classmethod
    def all_children(cls, node: HTMLPPTag, condition):
        return all(
            cls.is_visible(child) and condition(child)
            for child in node.find_all(True)
        )

    @classmethod
    def in_not_tve(cls, node: HTMLPPTag):
        return node.name in cls.NOT_TVE

    @classmethod
    def in_tve(cls, node: HTMLPPTag):
        return node.name in cls.TVE

    @classmethod
    def is_inline(cls, node: HTMLPPTag):
        return node.styles["display"] == "inline"

    @classmethod
    def has_children(cls, node: HTMLPPTag):
        return bool(node.contents)

    @classmethod
    def has_exactly_one_child(cls, node: HTMLPPTag):
        return len(node.contents) == 1
