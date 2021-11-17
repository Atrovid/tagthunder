import itertools
import json
from typing import List

import bs4
import numpy as np

from algorithms.models.responses import Segmentation, HTMLPP
from algorithms.segmentation._abstract import AbstractSegmentationAlgorithm
from algorithms.models.web_elements import BoundingBox, CoveringBoundingBox
import algorithms.segmentation.utils.distances as seg_distances
from algorithms.segmentation.utils.features_extractors import AbstractFeaturesExtractor, Features, LastBlockSemantic
from algorithms.segmentation.utils.visualisation import PlotClustering


class KMeans(AbstractSegmentationAlgorithm):

    def __init__(self, features_extractor: AbstractFeaturesExtractor):
        self.features_extractor: AbstractFeaturesExtractor = features_extractor

    def __call__(self, htmlpp: HTMLPP, *, nb_zones: int = 5, nb_iterations: int = 1e4) -> Segmentation:
        raise NotImplementedError

    def run(self, htmlpp: HTMLPP, nb_zones: int = 5, nb_iterations: int = 1e4):
        population: Features = self.features_extractor(htmlpp)
        bboxes = np.array(population.bboxes, dtype=object)
        centers = self._init_centers(nb_zones, bboxes)
        final_centers, labels = self.k_means(bboxes, centers.copy(), nb_zones, nb_iterations)

        return population, centers, final_centers, labels

    @classmethod
    def k_means(cls, bboxes, centers, nb_zones, nb_iterations):
        """initialization"""
        n = len(bboxes)

        labels = cls._association(bboxes, centers, n, nb_zones)

        """Iterations"""
        for _ in range(nb_iterations):
            centers = cls._update_centers(bboxes, labels, nb_zones)
            labels = cls._association(bboxes, centers, n, nb_zones)

        return centers, labels

    @classmethod
    def _init_centers(cls, k, bboxes):
        """
        Select k centroids elements
        :param k:
        :param bboxes:
        :return:
        """
        covering_bbox = cls._covering_bounding_box(bboxes)
        top_left = np.array(covering_bbox.top_left)
        dims_units = np.array([covering_bbox.width, covering_bbox.height]) // (k - 1)
        avg_dims = np.average(np.array([[bbox.width, bbox.height] for bbox in bboxes]), axis=0)

        return np.array(
            [
                BoundingBox(*(top_left + dims_units * i), *avg_dims)
                for i in range(k)
            ],
            dtype=object
        )

    @classmethod
    def _virtual_center(cls, bboxes: List[BoundingBox]):
        covering_bbox = cls._covering_bounding_box(bboxes)
        vbox_dims = np.average(np.array([[bbox.width, bbox.height] for bbox in bboxes]), axis=0)
        vbox_top_left = np.array(covering_bbox.center) - (vbox_dims / 2)
        return BoundingBox(*vbox_top_left, *vbox_dims)

    @classmethod
    def _covering_bounding_box(cls, bboxes: List[BoundingBox]):
        return CoveringBoundingBox(bboxes)

    @classmethod
    def _update_centers(cls, bboxes: np.ndarray, labels, k):
        new_centers = np.random.choice(bboxes, k)

        labels_with_bboxes = np.unique(labels)

        new_centers[labels_with_bboxes,] = np.vectorize(
            lambda center: cls._virtual_center(bboxes[labels == center]),
            otypes=[BoundingBox]
        )(labels_with_bboxes)

        return new_centers

    @classmethod
    def _distance(cls, bboxes, centers, n, k):
        """
        Compute distance between candidates and cluster centroides.
        :param bboxes:
        :param centers:
        :param n: number of candidates
        :param k: number au centroides
        :return:
        """
        distances = np.array(
            [
                seg_distances.bboxes(bbox, center)
                for bbox, center
                in itertools.product(bboxes, centers)
            ]
        )

        return distances.reshape((n, k))

    @classmethod
    def _association(cls, bboxes, centers, n, k):
        """
        Associates each candidate to a center.
        :param n: number of candidates
        :param k: number of centers
        :param centers:
        :param bboxes:
        :return:
        """
        distances = cls._distance(bboxes, centers, n, k)
        return np.argmin(distances, axis=1)


if __name__ == '__main__':
    json_file = "../data/html++/calvados.raw.json"
    with open(json_file, "r") as f:
        content = json.load(f)
        htmlpp = HTMLPP.parse_obj(content["html"])
    kmeans = KMeans(
        features_extractor=LastBlockSemantic()
    )
    res = kmeans.run(htmlpp, 5, 5)
    PlotClustering(ncols=2, nrows=1).clustering_plt(0, "K-Means", *res).show()
