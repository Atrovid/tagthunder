from dataclasses import dataclass, field

import numpy as np


@dataclass
class Point:
    x: float
    y: float

    def __array__(self):
        return np.array([self.x, self.y])


class BoundingBox:
    def __init__(self, x0, y0, w, h):
        self.top_left = Point(x0, y0)

        self.width = w
        self.height = h

        x1 = x0 + w
        y1 = y0 + h

        self.top_right = Point(x1, y0)
        self.bottom_left = Point(x0, y1)
        self.bottom_right = Point(x1, y1)

        self.center = Point(x0 + w / 2, y0 + h / 2)

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

    def __repr__(self):
        return f'BoundindBox({" ".join(map(str, self.corners))})'
