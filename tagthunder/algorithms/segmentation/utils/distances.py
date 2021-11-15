import numpy as np
import itertools

from algorithms.models.web_elements import BoundingBox


def bboxes(b1: BoundingBox, b2: BoundingBox):
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


def are_aligned(b1: BoundingBox, b2: BoundingBox):
    b1, b2 = np.array(b1), np.array(b2)

    return np.apply_along_axis(lambda c: (b1 == c).any(), axis=1, arr=b2).any()


if __name__ == '__main__':
    b1 = np.array(BoundingBox(0, 0, 10, 10))
    b2 = np.array(BoundingBox(11, 11, 10, 10))

    rep = are_aligned(b1, b2)
    print(rep)
