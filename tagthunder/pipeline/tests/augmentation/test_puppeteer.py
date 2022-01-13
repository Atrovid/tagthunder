from unittest import TestCase

from pipeline.blocks.augmentation.puppeteer import Puppeteer
from pipeline.blocks import REQUIRED_STYLES
from pipeline.models.responses import HTMLP
from pipeline.models.web_elements import HTMLPTag


class TestPuppeteerCrawler(TestCase):
    crawler_address = "http://0.0.0.0:8080"
    block = Puppeteer(crawler_address)
    block.config(1200, 1200, REQUIRED_STYLES)
    url = "https://www.example.com"
    htmlp: HTMLP = block(url=url)

    def test_is_running(self):
        assert self.block.requester.is_running

    def test_get_htmlp(self):
        assert isinstance(self.htmlp, HTMLP)

    def test_htmlp_required_attrs(self):
        assert all([
            (HTMLPTag._BBOX_ATTR in tag.attrs, HTMLPTag.styles in tag.attrs, tag.attrs is not None)
            for tag in self.htmlp.find_all(True)
        ])
