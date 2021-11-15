from __future__ import annotations

from copy import copy
from dataclasses import dataclass, field
from typing import Any, Dict

import numpy as np

from algorithms.models.responses import HTMLPP


@dataclass
class Point:
    x: float
    y: float

    def __array__(self):
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

    def __array__(self):
        return np.array(
            [np.array(c) for c in self.corners]
        )


class DataStyles(dict):
    def __init__(self, data_styles: DataStyles = {}):
        super().__init__(data_styles)
