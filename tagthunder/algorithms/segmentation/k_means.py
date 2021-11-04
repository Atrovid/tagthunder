import itertools
import json
from typing import List

import bs4
import numpy as np

from algorithms.models.responses import Segmentation, HTMLPP
from algorithms.segmentation._abstract import AbstractSegmentationAlgorithm
from models.web_elements import BoundingBox
from segmentation.utils import PlotClustering, compute_min_bboxes_dist


class KMeans(AbstractSegmentationAlgorithm):
    __needed_styles__ = ()

    # https://developer.mozilla.org/en-US/docs/Web/HTML/Block-level_elements
    __basic_visual_elements__ = (
        "address",
        "article",
        "aside",
        "blockquote",
        "details",
        "dialog",
        "dd",
        "div",
        "dl",
        "dt",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        *[f"h{i}" for i in range(1, 7)],
        "header",
        "hgroup",
        "hr",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "ul"
    )

    def __init__(self, plot=False):
        self.plot = plot

    def __call__(self, htmlpp: HTMLPP, *, nb_zones: int = 5, nb_iterations: int = 1e4) -> Segmentation:
        raise NotImplementedError

    def kmeans(self, htmlpp, nb_zones, nb_iterations):
        """initialization"""
        bboxes = self.get_basic_visual_elements(htmlpp)
        n, k = len(bboxes), nb_zones
        centers = self._init_centers(nb_zones, bboxes)
        association = self._association(bboxes, centers, n, k)

        if self.plot:
            PlotClustering("Initialization") \
                .population(bboxes, association) \
                .centers(centers, np.arange(k)) \
                .show()

        """Iterations"""
        for _ in range(nb_iterations):
            centers = self._update_centers(
                bboxes,
                association,
                k
            )
            association = self._association(bboxes, centers, n, k)

        if self.plot:
            PlotClustering(f"End ({nb_iterations} iterations)") \
                .population(bboxes, association) \
                .centers(centers, np.arange(k)) \
                .show()

        return centers, association

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
            ]
        )

    @classmethod
    def _virtual_center(cls, bboxes: List[BoundingBox]):
        covering_bbox = cls._covering_bounding_box(bboxes)
        vbox_dims = np.average(np.array([[bbox.width, bbox.height] for bbox in bboxes]), axis=0)
        vbox_top_left = np.array(covering_bbox.center) - (vbox_dims / 2)
        return BoundingBox(*vbox_top_left, *vbox_dims)

    @classmethod
    def _covering_bounding_box(cls, bboxes: List[BoundingBox]):
        top_left_points = np.array([np.array(bbox.top_left) for bbox in bboxes])
        top_rigth_points = np.array([np.array(bbox.top_right) for bbox in bboxes])
        top_left = np.min(top_left_points, axis=0)
        bottom_right = np.max(top_rigth_points, axis=0)
        w, h = np.abs(top_left - bottom_right)
        return BoundingBox(*top_left, w, h)

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
        return np.array(
            [
                compute_min_bboxes_dist(bbox, center)
                for bbox, center
                in itertools.product(bboxes, centers)
            ]
        ).reshape((n, k))

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

    @classmethod
    def get_basic_visual_elements(cls, htmlpp: HTMLPP):
        """Extract last block elements in each branch of the DOM"""
        soup = bs4.BeautifulSoup(htmlpp.__root__, 'html.parser')
        elements = soup.find_all(cls.__basic_visual_elements__)
        elements = filter(
            (
                lambda e:
                len(e.find_all(cls.__basic_visual_elements__)) == 0
                and len(e.contents)
                and e.attrs['data-bbox'] != '0 0 0 0'
            ),
            elements
        )

        return np.array([
            BoundingBox(*map(float, e.attrs["data-bbox"].split(" "))) for e in
            elements
        ])


if __name__ == '__main__':
    json_file = "../data/cleaned_html/response_1633951666404.json"
    with open(json_file, "r") as f:
        content = json.load(f)
        htmlpp = HTMLPP.parse_obj(content["html"])

    kmeans = KMeans(True)
    kmeans.kmeans(htmlpp, 5, 5)
