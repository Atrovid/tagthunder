import copy
from typing import List

import numpy as np

from pipeline.blocks.segmentation._abstract import AbstractSegmentationBlock
import pipeline.blocks.segmentation.clustering.utils.distances as distances
from pipeline.models.responses import Segmentation, HTMLPP, Zone
from pipeline.models.web_elements import HTMLPPTag, BoundingBox, CoveringBoundingBox


class TopDownBottomUp(AbstractSegmentationBlock):
    _MERGED_ZONE_TAG = "div"
    _MERGED_ZONE_CLASS = "tt_merged_zone"

    def __call__(self, htmlpp: HTMLPP, *, nb_zones: int, **kwargs) -> Segmentation:
        zones = sorted(self.fit(htmlpp=htmlpp, nb_zones=nb_zones), key=lambda tag: tag.bbox.top_left.y)

        return Segmentation(zones=[
            Zone(id=i, htmlpp=self.prepare_zone(z))
            for i, z in enumerate(zones)
        ]
        )

    @classmethod
    def prepare_zone(cls, zone) -> HTMLPP:
        if cls._is_merged_zone(zone):
            children = zone.find_all(True, recursive=False)
            res = HTMLPP.from_tags(children)
        else:
            pass
            res = HTMLPP(str(zone))
        return res

    def fit(self, htmlpp: HTMLPP, nb_zones: int, **kwargs):
        htmlpp = copy.copy(htmlpp)
        zones = htmlpp.body.find_all_visible(recursive=False)
        nb_visible_children = len(htmlpp.find_all_visible())
        if nb_visible_children < nb_zones:
            nb_zones = nb_visible_children

        while len(zones) != nb_zones:
            if len(zones) > nb_zones:
                self.merge(zones)
            else:
                self.split(zones)

        return zones

    @classmethod
    def merge(cls, zones: List[HTMLPPTag]):
        ids = cls.sort_by_area(zones, reverse=True)
        i, smallest_tag = ids[0], zones[ids[0]]
        j, closest_tag = cls.get_closest_node(smallest_tag, [zones[i] for i in ids[1:]])
        zones.remove(smallest_tag)
        zones.remove(closest_tag)
        zones.append(cls.merge_nodes(smallest_tag, closest_tag))
        return zones

    @classmethod
    def get_closest_node(cls, node: HTMLPPTag, candidates: List[HTMLPPTag]):
        i = np.argsort(np.array([distances.bboxes(node.bbox, cand.bbox) for cand in candidates]))[0]
        return i, candidates[i]

    @classmethod
    def merge_nodes(cls, *nodes):
        bbox = CoveringBoundingBox([node.bbox for node in nodes])
        new_tag = HTMLPPTag(name=cls._MERGED_ZONE_TAG, bbox=bbox, attrs={"class": [cls._MERGED_ZONE_TAG]})

        sub_nodes = []
        for node in nodes:
            if cls._is_merged_zone(node):
                sub_nodes.extend(node.find_all(recursive=False))
            else:
                sub_nodes.append(node)

        for node in sub_nodes:
            new_tag.append(node)

        return new_tag

    @classmethod
    def _is_merged_zone(cls, node: HTMLPPTag):
        try:
            return cls._MERGED_ZONE_CLASS in node.classes
        except KeyError:
            return False

    @classmethod
    def split(cls, zones: List[HTMLPPTag]):
        ids = list(filter(
            lambda i: zones[i].has_visible_children,
            cls.sort_by_area(zones, reverse=True)
        ))
        zone = zones.pop(ids[0])
        zones.extend(cls.split_node(zone))

    @classmethod
    def split_node(cls, tag: HTMLPPTag):
        return tag.find_all_visible(recursive=False)

    @classmethod
    def sort_by_area(cls, tags: List[HTMLPPTag], reverse=False):
        _reverse = 1
        if reverse:
            _reverse = -1

        return np.argsort(np.array([_reverse * tag.bbox.area for tag in tags]))
