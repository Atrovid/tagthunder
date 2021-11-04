import itertools
from typing import List, Tuple

import matplotlib

matplotlib.use('tkagg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

from models.web_elements import BoundingBox


def compute_min_bboxes_dist(b1: BoundingBox, b2: BoundingBox):
    def min_dist_point_segment(p: np.ndarray, start: np.ndarray, end: np.ndarray):
        try:
            u = np.sum((p - start) * (end - start)) / (np.linalg.norm(end - start) ** 2)
        except ZeroDivisionError:
            return np.nan
        if u <= 0 or u > 1:
            return np.min(np.linalg.norm(p - np.stack([start, end]), axis=1))
        return np.linalg.norm(p - (start + u * (end - start)))

    combinations = (
            list(itertools.product(b1.corners, b2.edges))
            + list(itertools.product(b2.corners, b1.edges))
    )

    return min([
        min_dist_point_segment(np.array(p), np.array(seg[0]), np.array(seg[1]))
        for p, seg
        in combinations
    ])


class PlotClustering:
    def __init__(self, title=""):
        self.fig, self.ax = plt.subplots(1)
        self.ax.set_title = title
        self.ax.xaxis.tick_top()
        self.ax.invert_yaxis()

    def bboxes(self, bboxes: List[BoundingBox], labels=None, **kwargs):

        if labels is None:
            labels = np.ones(len(bboxes))

        for bbox, l in zip(bboxes, labels):
            coords = np.array(bbox)
            color = plt.cm.tab10(l)
            patch = Polygon(coords, fc="none", ec=color, **kwargs)
            self.ax.add_patch(patch)
            self.ax.scatter(coords[:, 0], coords[:, 1], c="none")

        return self

    def population(self, bboxes, labels):
        return self.bboxes(bboxes, labels)

    def centers(self, bboxes, labels):
        return self.bboxes(bboxes, labels, hatch="//", ls="--")

    def show(self):
        plt.show()
