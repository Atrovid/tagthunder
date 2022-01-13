from unittest import TestCase
import json

from pipeline.blocks.extraction import Yake
from pipeline.models.responses import Segmentation, Zone, HTMLPP

with open("../data/segmentation_calvados.json", 'r') as f:
    data = json.load(f)
    segmentation = Segmentation(zones=[Zone(id=z["id"], htmlpp=HTMLPP(z["htmlpp"])) for z in data])


class TestYake(TestCase):
    block = Yake()
    block.config()

    def test_call(self):
        res = self.block(segmentation)
        for z in res.zones:
            print(z.keywords)
