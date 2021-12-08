from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import bs4
import numpy as np


@dataclass
class Point:
    x: float
    y: float

    def to_numpy(self):
        return np.array([self.x, self.y])


@dataclass
class BoundingBox:
    width: int
    height: int
    top_left: Point = field(init=False)
    top_right: Point = field(init=False)
    bottom_left: Point = field(init=False)
    bottom_right: Point = field(init=False)
    center: Point = field(init=False)

    def __init__(self, x0, y0, width, height):
        self.top_left = Point(x0, y0)
        self.width = width
        self.height = height

        x1 = x0 + self.width
        y1 = y0 + self.height

        self.top_right = Point(x1, y0)
        self.bottom_left = Point(x0, y1)
        self.bottom_right = Point(x1, y1)

        self.center = Point(x0 + self.width / 2, y0 + self.height / 2)

    @property
    def corners(self):
        return [self.top_left, self.top_right, self.bottom_right, self.bottom_left]

    @property
    def edges(self):
        return [
            (self.top_left, self.top_right),
            (self.top_right, self.bottom_left),
            (self.bottom_right, self.bottom_left),
            (self.bottom_left, self.top_left)
        ]

    @property
    def area(self):
        return self.height * self.width

    def to_numpy(self):
        return np.array(
            [c.to_numpy() for c in self.corners],
        )

    @property
    def is_visible(self):
        return self.width > 0 and self.height > 0


@dataclass
class CoveringBoundingBox(BoundingBox):
    def __init__(self, bboxes):
        corners = np.array([[bbox.top_left.to_numpy(), bbox.bottom_right.to_numpy()] for bbox in bboxes])
        top_left, bottom_right = np.min(corners[:, 0], axis=0), np.max(corners[:, 1], axis=0)
        dims = np.abs(top_left - bottom_right)
        super(CoveringBoundingBox, self).__init__(*top_left, *dims)


class Styles(dict):
    def __init__(self, styles=None):
        if styles is None:
            styles = {}
        super(Styles, self).__init__(styles)

    def __getitem__(self, item):
        return self.get(item)


class HTMLPTag(bs4.Tag):
    _BBOX_KEY = "data-bbox"
    _STYLES_KEY = "data-style"

    def __init__(self, parser=None, builder=None, name=None, namespace=None,
                 prefix=None, attrs=None, parent=None, previous=None,
                 is_xml=None, sourceline=None, sourcepos=None,
                 can_be_empty_element=None, cdata_list_attributes=None,
                 preserve_whitespace_tags=None, interesting_string_types=None,
                 bbox: BoundingBox = None, styles: Dict[str, Any] = None):
        super(HTMLPTag, self).__init__(parser=parser, builder=builder, name=name, namespace=namespace,
                                       prefix=prefix, attrs=attrs, parent=parent, previous=previous,
                                       is_xml=is_xml, sourceline=sourceline, sourcepos=sourcepos,
                                       can_be_empty_element=can_be_empty_element,
                                       cdata_list_attributes=cdata_list_attributes,
                                       preserve_whitespace_tags=preserve_whitespace_tags,
                                       interesting_string_types=interesting_string_types)

        self._bbox: Optional[BoundingBox] = bbox
        self._styles: Optional[Dict[str, Any]] = styles

    @property
    def bbox(self):
        if self._bbox is None:
            try:
                params = map(int, self.attrs[self._BBOX_KEY].split(" "))
            except KeyError:
                children = self.find_all(True, recursive=False)
                if children:
                    bbox = CoveringBoundingBox([c.bbox for c in children])
                    params = (bbox.top_left.x, bbox.top_left.y, bbox.width, bbox.height)
                else:
                    params = (0, 0, 0, 0)
            self._bbox = BoundingBox(*params)
        return self._bbox

    @property
    def styles(self):
        if self._styles is None:
            try:
                styles = self.attrs[self._STYLES_KEY].split(";")
                styles = filter(lambda couple: ":" in couple, styles)

                styles = {
                    style: value
                    for style, value
                    in map(lambda sv: sv.split(":", 1), styles)
                }
            except KeyError:
                styles = {}
            self._styles = Styles(styles)

        return self._styles

    @property
    def classes(self):
        return self.attrs.get("class", [])


class HTMLPPTag(HTMLPTag):
    _DATA_CLEANED_KEY = "data-cleaned"

    def __init__(self, parser=None, builder=None, name=None, namespace=None,
                 prefix=None, attrs=None, parent=None, previous=None,
                 is_xml=None, sourceline=None, sourcepos=None,
                 can_be_empty_element=None, cdata_list_attributes=None,
                 preserve_whitespace_tags=None, interesting_string_types=None,
                 bbox: BoundingBox = None, styles: Dict[str, Any] = None):

        super(HTMLPPTag, self).__init__(parser=parser, builder=builder, name=name, namespace=namespace,
                                        prefix=prefix, attrs=attrs, parent=parent, previous=previous,
                                        is_xml=is_xml, sourceline=sourceline, sourcepos=sourcepos,
                                        can_be_empty_element=can_be_empty_element,
                                        cdata_list_attributes=cdata_list_attributes,
                                        preserve_whitespace_tags=preserve_whitespace_tags,
                                        interesting_string_types=interesting_string_types,
                                        bbox=bbox, styles=styles)

        self._visible: Optional[bool] = None
        self._cleaned: Optional[bool] = None

    @property
    def is_visible(self):
        if self._visible is None:
            visible = not self.is_cleaned
            self._visible = visible
        return self._visible

    @property
    def is_cleaned(self) -> bool:
        if self._cleaned is None:
            res = (
                    not self.bbox.is_visible
                    or any([
                self.styles.get("display") == "none",
                self.styles.get("visiblity") == "hidden",
                self.styles.get("hidden") == "true",
                self.styles.get("x-visible") == "invisible"
            ])
            )
            self.set_data_cleaned_hmtl_attr(res)
            self._cleaned = res

        return self._cleaned

    def set_data_cleaned_hmtl_attr(self, value: bool):
        self.attrs[self._DATA_CLEANED_KEY] = str(value)

    def find_all_visible(self, attrs=None, recursive=True, text=None,
                         limit=None, **kwargs):
        if attrs is None:
            attrs = {}
        return self.find_all(lambda tag: tag.is_visible, attrs=attrs, recursive=recursive, text=text, limit=limit,
                             **kwargs)

    @property
    def has_visible_children(self):
        return bool(len(self.find_all_visible(recursive=False)))
