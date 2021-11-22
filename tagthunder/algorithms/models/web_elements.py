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


@dataclass
class CoveringBoundingBox(BoundingBox):
    def __init__(self, bboxes):
        corners = np.array([[bbox.top_left.to_numpy(), bbox.bottom_right.to_numpy()] for bbox in bboxes])
        top_left, bottom_right = np.min(corners[:, 0], axis=0), np.max(corners[:, 1], axis=0)
        dims = np.abs(top_left - bottom_right)
        super(CoveringBoundingBox, self).__init__(*top_left, *dims)


class Tag(bs4.Tag):
    _BBOX_KEY = "data-bbox"
    _STYLES_KEY = "data-style"
    _CLEAN_KEY = "data-cleaned"

    def __init__(self, parser=None, builder=None, name=None, namespace=None,
                 prefix=None, attrs=None, parent=None, previous=None,
                 is_xml=None, sourceline=None, sourcepos=None,
                 can_be_empty_element=None, cdata_list_attributes=None,
                 preserve_whitespace_tags=None, interesting_string_types=None,
                 bbox: BoundingBox = None, styles: Dict[str, Any] = None):
        super(Tag, self).__init__(parser=parser, builder=builder, name=name, namespace=namespace,
                                  prefix=prefix, attrs=attrs, parent=parent, previous=previous,
                                  is_xml=is_xml, sourceline=sourceline, sourcepos=sourcepos,
                                  can_be_empty_element=can_be_empty_element,
                                  cdata_list_attributes=cdata_list_attributes,
                                  preserve_whitespace_tags=preserve_whitespace_tags,
                                  interesting_string_types=interesting_string_types)

        self._bbox: Optional[BoundingBox] = bbox
        self._styles: Optional[Dict[str, Any]] = styles
        self._visible: Optional[bool] = None

    @property
    def bbox(self):
        if not self._bbox:
            try:
                params = map(int, self.attrs[self._BBOX_KEY].split(" "))
            except KeyError:
                params = (0, 0, 0, 0)
            self._bbox = BoundingBox(*params)
        return self._bbox

    @property
    def styles(self):
        if not self._styles:
            try:
                styles = self.attrs[self._STYLES_KEY].split(";", 1)
                if "" in styles:
                    styles.remove("")

                self._styles = {
                    style: value
                    for style, value
                    in map(lambda sv: sv.split(":", 1), styles)
                }
            except KeyError:
                self._styles = {}

        return self._styles

    @property
    def visible(self):
        if not self._visible:
            try:
                visible = self.attrs[self._CLEAN_KEY] == "false"
            except KeyError:
                visible = False
            self._visible = visible
        return self._visible
