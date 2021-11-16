from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from algorithms.models.web_elements import BoundingBox


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
