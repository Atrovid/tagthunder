import itertools
import json
from typing import List

import numpy as np

from pipeline.models.responses import Segmentation, HTMLPP
from pipeline.models.web_elements import BoundingBox, CoveringBoundingBox
import pipeline.blocks.segmentation.clustering.utils.distances as seg_distances
from pipeline.blocks.segmentation.clustering._abstract import AbstractClusteringBlock
from pipeline.blocks.segmentation.clustering.utils.features_extractors import (
    FeaturesDataFrame,
    LastBlockSemantic, AbstractFeaturesExtractor
)
import pipeline.blocks.segmentation.clustering.utils.seeds_initializer as seeds_initializer
from pipeline.experimentations.segmentation.visualisation import PlotClustering


class KMeans(AbstractClusteringBlock):

    def __init__(self, nb_zones: int = 5, nb_iterations: int = 1e4, features_extractor: str = None):
        self.nb_zones = nb_zones
        self.nb_iterations = nb_iterations
        self.features_extractor = features_extractor

    def __call__(self, htmlpp: HTMLPP) -> Segmentation:
        raise NotImplementedError

    def fit(self, features: FeaturesDataFrame, centers: FeaturesDataFrame):
        bboxes = np.array(features.bboxes, dtype=object)
        centers = centers.bboxes
        final_centers, labels = self.k_means(bboxes, centers.copy(), self.nb_zones, self.nb_iterations)

        return final_centers, labels

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
    json_file = "../../../data/html++/calvados.raw.json"

    with open(json_file, "r") as f:
        content = json.load(f)
        htmlpp = HTMLPP(content["html"])

    features_extractor = LastBlockSemantic()
    features = features_extractor(htmlpp)

    k = 5
    seeds_initializer = seeds_initializer.DiagonalFashion
    seeds = seeds_initializer.centroids(features, 5)

    kmeans = KMeans()
    res = kmeans.fit(features, seeds, 5, 5)
    PlotClustering(nrows=2) \
        .plot("K-Means", features.tags, seeds.tags, *res) \
        .show()
