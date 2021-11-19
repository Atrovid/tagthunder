from typing import List

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from algorithms.models.web_elements import BoundingBox
from algorithms.segmentation.clustering.utils.features_extractors import Features


class PlotClustering:
    def __init__(self, **kwargs):

        self.fig, self.axes = plt.subplots(kwargs.pop("nrows", 1), 1)

        if not isinstance(self.axes, np.ndarray):
            self.axes = np.array([self.axes])

        gridspec = self.axes[0].get_subplotspec().get_gridspec()
        self.subfigs = [self.fig.add_subfigure(gs) for gs in gridspec]
        self.current_row = 0

    @classmethod
    def bboxes(cls, ax, bboxes: List[BoundingBox], labels=None, **kwargs):

        if labels is None:
            labels = np.ones(len(bboxes))

        for bbox, l in zip(bboxes, labels):
            coords = bbox.to_numpy()
            color = plt.cm.tab10(l)
            patch = Polygon(coords, fc="none", ec=color, **kwargs)
            ax.add_patch(patch)
            ax.scatter(coords[:, 0], coords[:, 1], c="none")

    def population(self, ax, bboxes, labels=None):
        self.bboxes(ax, bboxes, labels)
        return ax

    def centers(self, ax, bboxes, labels=None):
        self.bboxes(ax, bboxes, labels, hatch="//", ls="--")
        return self

    def plot(self, title, population: Features, init_centers, centers, labels):

        fig = self.subfigs[self.current_row]
        fig.suptitle(title, fontweight='semibold')

        k = len(centers)
        bboxes = population.bboxes
        centers_labels = np.arange(k)

        axes = fig.subplots(nrows=1, ncols=2)
        for ax in axes.reshape(-1):
            ax.invert_yaxis()
            ax.xaxis.tick_top()

        ax = axes[0]
        ax.set_title("Init")
        self.population(ax, bboxes)
        self.centers(ax, init_centers, centers_labels)

        ax = axes[1]
        ax.set_title("Results")
        self.population(ax, bboxes, labels)
        self.centers(ax, centers, centers_labels)

        self.current_row += 1
        return self

    def show(self):
        plt.show()
