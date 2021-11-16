import numpy as np

from algorithms.models.responses import HTMLPP, Segmentation
from algorithms.models.web_elements import BoundingBox
from algorithms.segmentation.k_means import KMeans


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

if __name__ == '__main__':
    def build_bboxes(*params):
        return [
            BoundingBox(*p)
            for p in params
        ]

    bboxes = build_bboxes(
        (0, 0, 10, 10),
        (0, 0, 5, 5),
        (0, 0, 2, 2),
        (0, 0, 15, 15)
    )

    centers = build_bboxes(
        (15, 15, 3, 2),
        (15, 15, 7, 9),
        (15, 15, 10, 10)
    )


    n, k = len(bboxes), len(centers)

    forces = ForceKMeans._distance(bboxes, centers, n, k)
    print(forces.shape)
    print(forces)