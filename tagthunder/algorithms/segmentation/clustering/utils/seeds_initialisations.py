import numpy as np

from algorithms.models.web_elements import CoveringBoundingBox, BoundingBox, Tag
from algorithms.segmentation.clustering.utils.features_extractors import Features


class VirtualSeeds:
    @classmethod
    def reading(cls, features: Features, k):
        """
        k seeds located in top left to bottom right diagonal at equals distances.

        :param features:
        :param k:
        :return:
        """
        bboxes = features.bboxes

        covering_bbox = CoveringBoundingBox(bboxes)
        top_left = covering_bbox.top_left.to_numpy()
        dims_units = np.array([covering_bbox.width, covering_bbox.height]) // (k - 1)
        avg_dims = np.average(np.array([[bbox.width, bbox.height] for bbox in bboxes]), axis=0)

        return Features(
            [
                Tag(name="seed", bbox=BoundingBox(*(top_left + dims_units * i), *avg_dims))
                for i in range(k)
            ]
        )


class RealSeeds:
    @classmethod
    def reading(cls, features, k):
        bboxes = features.bboxes
        covering_bbox = CoveringBoundingBox(bboxes)
        top_left = covering_bbox.top_left.to_numpy()


if __name__ == '__main__':
    tag = Tag(name='seed', attrs={""})
    print(tag)
