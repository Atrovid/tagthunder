import itertools

import numpy as np

from models.web_elements import BoundingBox


def compute_min_bboxes_dist(b1: BoundingBox, b2: BoundingBox):
    def min_dist_point_segment(p: np.ndarray, start: np.ndarray, end: np.ndarray):
        try:
            u = np.sum((p - start) * (end - start)) / (np.linalg.norm(end - start) ** 2)
        except ZeroDivisionError:
            return np.nan
        if u <= 0 or u > 1:
            return np.min(np.linalg.norm(p - np.stack([start, end]), axis=1))
        return np.linalg.norm(p - (start + u * (end - start)))

    combinations = (
            list(itertools.product(b1.corners, b2.edges))
            + list(itertools.product(b2.corners, b1.edges))
    )

    return min([
        min_dist_point_segment(np.array(p), np.array(seg[0]), np.array(seg[1]))
        for p, seg
        in combinations
    ])