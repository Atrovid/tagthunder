import itertools
import json
from typing import List, Optional

import numpy as np

from algorithms.models.responses import Segmentation, HTMLPP
from algorithms.segmentation._abstract import AbstractSegmentationAlgorithm
from algorithms.models.web_elements import BoundingBox, CoveringBoundingBox
import algorithms.segmentation.clustering.utils.distances as seg_distances
from algorithms.segmentation.clustering.utils.features_extractors import (
    AbstractFeaturesExtractor,
    Features,
    LastBlockSemantic,
    LastBlocksWithComputedStyles
)
from algorithms.segmentation.clustering.utils.seeds_initialisations import VirtualSeeds
from algorithms.segmentation.clustering.utils.visualisation import PlotClustering


class KMeans(AbstractSegmentationAlgorithm):

    def __init__(self,
                 features_extractor: Optional[AbstractFeaturesExtractor] = None,
                 seeds_initializer=VirtualSeeds.reading):
        self.features_extractor: AbstractFeaturesExtractor = features_extractor
        self.seed_initializer = seeds_initializer

    def __call__(self, htmlpp: HTMLPP, *, nb_zones: int = 5, nb_iterations: int = 1e4) -> Segmentation:
        raise NotImplementedError

    def run(self, features: Features, nb_zones: int = 5, nb_iterations: int = 1e4):
        bboxes = np.array(features.bboxes, dtype=object)
        centers = self.seed_initializer(features, nb_zones).bboxes
        final_centers, labels = self.k_means(bboxes, centers.copy(), nb_zones, nb_iterations)

        return centers, final_centers, labels

    @classmethod
    def k_means(cls, bboxes, centers, nb_zones, nb_iterations):
        """initialization"""
        n = len(bboxes)

        labels = cls._association(bboxes, centers, n, nb_zones)

        for _ in range(nb_iterations):
            centers = cls._update_centers(bboxes, labels, nb_zones)
            labels = cls._association(bboxes, centers, n, nb_zones)

        return centers, labels

    @classmethod
    def _virtual_center(cls, bboxes: List[BoundingBox]):
        covering_bbox = CoveringBoundingBox(bboxes)
        vbox_dims = np.average(np.array([[bbox.width, bbox.height] for bbox in bboxes]), axis=0)
        vbox_top_left = covering_bbox.center.to_numpy() - (vbox_dims / 2)
        return BoundingBox(*vbox_top_left, *vbox_dims)

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
        htmlpp = HTMLPP(content["html"])
    features_extractor = LastBlockSemantic()
    features = features_extractor(htmlpp)
    kmeans = KMeans()
    res = kmeans.run(features, 5, 5)
    PlotClustering(nrows=2) \
        .plot("K-Means", features, *res) \
        .show()