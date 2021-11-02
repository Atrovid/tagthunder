from dataclasses import dataclass, field

import numpy as np


@dataclass
class Point:
    x: float
    y: float

    def __array__(self):
        return np.array([self.x, self.y])


@dataclass
class BoundingBox:
    x0: float
    y0: float
    x1: float = field(init=False)
    y1: float = field(init=False)

    width: float
    height: float

    top_left: Point = field(init=False)
    top_right: Point = field(init=False)
    bottom_left: Point = field(init=False)
    bottom_right: Point = field(init=False)

    def __post_init__(self):
        self.x1 = self.x0 + self.width
        self.y1 = self.y0 + self.height

        self.top_left = Point(self.x0, self.y0)
        self.top_right = Point(self.x1, self.y0)
        self.bottom_left = Point(self.x0, self.y1)
        self.bottom_right = Point(self.x1, self.y1)

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
