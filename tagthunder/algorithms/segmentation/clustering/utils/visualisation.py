from typing import List, Iterable

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from algorithms.models.web_elements import BoundingBox, Tag


class PlotClustering:
    def __init__(self, **kwargs):

        self.fig, self.axes = plt.subplots(kwargs.pop("nrows", 1), 1)

        if not isinstance(self.axes, np.ndarray):
            self.axes = np.array([self.axes])

        gridspec = self.axes[0].get_subplotspec().get_gridspec()
        self.subfigs = [self.fig.add_subfigure(gs) for gs in gridspec]
        self.current_row = 0

    @classmethod
    def bboxes(cls, ax, tags: Iterable[Tag], labels=None, **kwargs):
        bboxes = [tag.bbox for tag in tags]

        if labels is None:
            labels = np.ones(len(bboxes))

        for bbox, l in zip(bboxes, labels):
            coords = bbox.to_numpy()
            color = plt.cm.tab10(l)
            patch = Polygon(coords, fc="none", ec=color, **kwargs)
            ax.add_patch(patch)
            ax.scatter(coords[:, 0], coords[:, 1], c="none")

    @classmethod
    def _axes(cls, fig, nrows, ncols, **kwargs):
        axes = fig.subplots(nrows=nrows, ncols=ncols, **kwargs)

        if (nrows, ncols) == (1, 1):
            axes = np.array([axes])

        for ax in axes.reshape(-1):
            ax.invert_yaxis()
            ax.xaxis.tick_top()

        return axes

    @classmethod
    def population(cls, ax, tags, labels=None):
        cls.bboxes(ax, tags, labels)
        return ax

    @classmethod
    def centers(cls, ax, tags, labels=None):
        cls.bboxes(ax, tags, labels, hatch="//", ls="--")
        return cls

    def plot_centers(self, title, population: Iterable[Tag], centers: Iterable[Tag]):
        fig = self.subfigs[self.current_row]
        fig.suptitle(title)
        ax = self._axes(fig, nrows=1, ncols=1)[0]

        self.population(ax, population)

        k = len(centers)
        centers_labels = np.arange(k)
        self.centers(ax, centers, centers_labels)

        return self

    def plot(self, title, population: Iterable[Tag], init_centers: Iterable[Tag], centers: Iterable[Tag], labels):

        fig = self.subfigs[self.current_row]
        fig.suptitle(title, fontweight='semibold')

        k = len(centers)
        centers_labels = np.arange(k)

        axes = self._axes(fig, nrows=1, ncols=2)

        ax = axes[0]
        ax.set_title("Initialisation")
        self.population(ax, population)
        self.centers(ax, init_centers, centers_labels)

        ax = axes[1]
        ax.set_title("Results")
        self.population(ax, population, labels)
        self.centers(ax, centers, centers_labels)

        self.current_row += 1
        return self

    def show(self):
        plt.show()
