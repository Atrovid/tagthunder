from unittest import TestCase
from pydub import AudioSegment
from pydub.playback import play

import numpy as np

from pipeline.blocks.vocalization.playback_speed_area_size import PlaybackSpeedAreaSize
from pipeline.models.responses import Zone, Segmentation, HTMLPP, Keyword, Keywords

kws = [Keyword(text="Mot clef")]
data = [
    ('0 0 210 30', kws),
    ('0 30 210 60', kws),
    ('0 90 60 150', kws),
    ('60 90 150 150', kws),
    ('0 240 210 30', kws)
]

segmentation = Segmentation(zones=[
    Zone(id=id + 1, htmlpp=HTMLPP(f"<div bbox='{dims}'></div>"), keywords=kws)
    for id, (dims, kws) in enumerate(data)
])


class TestPlaybackSpeedAreaSize(TestCase):
    vocalizer = PlaybackSpeedAreaSize()

    def test_rate_function(self):
        vocalizer = self.vocalizer
        vocalizer.config(min_rate=1.5, max_rate=0.25)
        cpt = vocalizer.rate_function([0, .5, 1])
        assert np.allclose(cpt, np.array([1.5, 0.875, 0.25]))

        vocalizer.config(min_rate=0.25, max_rate=1.5)
        cpt = vocalizer.rate_function([0, .5, 1])
        assert np.allclose(cpt, [0.25, 0.875, 1.5])

    def test_compute_zone_area_props(self):
        expected = [
            z.htmlpp.bbox.area / (270 * 210)
            for z in segmentation.zones
        ]
        props = self.vocalizer.compute_zone_area_props(segmentation)
        assert props == expected

    def test_vocalization(self):
        self.vocalizer.config()
        speechs = self.vocalizer(segmentation)
        for s in speechs:
            s.seek(0)
            play(AudioSegment.from_wav(s))
            s.seek(0)

        assert True
