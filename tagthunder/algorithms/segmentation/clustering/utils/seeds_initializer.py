import json
import numpy as np
from sklearn.metrics import pairwise_distances

from algorithms.models.responses import HTMLPP
from algorithms.models.web_elements import CoveringBoundingBox, BoundingBox, Tag
from algorithms.segmentation.clustering.utils.features_extractors import FeaturesDataFrame, LastBlockSemantic


class DiagonalFashion:
    @classmethod
    def centroids(cls, features: FeaturesDataFrame, k: int):
        """
        k seeds located in top left to bottom right diagonal at equals distances.

        :param features:
        :param k:
        :return:
        """
        bboxes = features.bboxes
        covering_bbox = CoveringBoundingBox(bboxes)
        top_left = covering_bbox.top_left.to_numpy()
        covering_bbox_dims = np.array([covering_bbox.width, covering_bbox.height])
        dims_units = covering_bbox_dims // (k - 1)

        avg_dims = np.average(np.array([[bbox.width, bbox.height] for bbox in bboxes]), axis=0)

        seeds = [
            cls._create_seed(bbox=BoundingBox(*(top_left + dims_units * i - avg_dims / 2), *avg_dims))
            for i in range(k)
        ]

        return FeaturesDataFrame(seeds)

    @classmethod
    def medoids(cls, features: FeaturesDataFrame, k: int):
        tags = features.tags
        bboxes = features.bboxes
        covering_bbox = CoveringBoundingBox(bboxes)
        cb_top_left = covering_bbox.top_left.to_numpy()
        covering_bbox_dims = np.array([covering_bbox.width, covering_bbox.height])
        dims_units = covering_bbox_dims // (k - 1)

        points = np.array(
            [
                [bbox.top_left.to_numpy(), bbox.center.to_numpy(), bbox.bottom_right.to_numpy()]
                for bbox in bboxes
            ]
        )

        seeds_ids = [pairwise_distances(
            points[:, 0],
            covering_bbox.top_left.to_numpy()[None, :]
        ).argmin()]

        if k > 1:
            seeds_ids.append(
                pairwise_distances(
                    points[:, 2],
                    np.expand_dims(covering_bbox.bottom_right.to_numpy(), axis=0)
                ).argmin()
            )

        if k > 2:
            diag_points = np.array([cb_top_left + dims_units * i for i in range(1, k - 1)])
            distances = pairwise_distances(
                points[~np.isin(np.arange(len(tags)), seeds_ids), 1],
                diag_points
            )
            for id in np.argmin(distances, axis=0):
                seeds_ids.insert(-1, id)

        return FeaturesDataFrame(
            [tags[i] for i in seeds_ids]
        )

    @classmethod
    def _create_seed(cls, **kwargs):
        return Tag(name="seed", **kwargs)


if __name__ == '__main__':
    json_file = "../../../data/html++/calvados.raw.json"

    with open(json_file, "r") as f:
        content = json.load(f)
        htmlpp = HTMLPP(content["html"])
    features_extractor = LastBlockSemantic()
    features = features_extractor(htmlpp)
    print(features)
    # centers = DiagonalFashion.medoids(features, 5)
    # PlotClustering(nrows=1) \
    #     .plot_centers("Diagonal Fashion", features.tags, centers.tags) \
    #     .show()
