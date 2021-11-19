import numpy as np

from algorithms.models.responses import HTMLPP, Segmentation
from algorithms.segmentation.clustering.k_means import KMeans


class ForceKMeans(KMeans):

    def __call__(self, htmlpp: HTMLPP, *, nb_zones: int = 5, nb_iterations: int = 1e4) -> Segmentation:
        raise NotImplementedError

    @classmethod
    def _distance(cls, bboxes, centers, n, k):
        euclidean_distances = super()._distance(bboxes, centers, n, k)
        # replace 0 by 1e-5 to avoid divsion by 0
        euclidean_distances = np.where(euclidean_distances == 0, 1e-5, euclidean_distances)

        areas_candidates = np.array([bbox.area for bbox in bboxes])
        areas_centers = np.array([center.area for center in centers])

        forces = np.multiply(*np.meshgrid(areas_centers, areas_candidates))
        return forces / np.square(euclidean_distances)

    @classmethod
    def _association(cls, bboxes, centers, n, k):
        distances = cls._distance(bboxes, centers, n, k)
        return np.argmax(distances, axis=1)
