from unittest import TestCase

from pipeline.blocks.augmentation.puppeteer import Puppeteer
from pipeline.blocks import REQUIRED_STYLES
from pipeline.models.responses import HTMLP
from pipeline.models.web_elements import HTMLPTag


class TestPuppeteerCrawler(TestCase):
    crawler_address = "http://0.0.0.0:8080"
    block = Puppeteer(crawler_address)
    url = "https://www.example.com"
    htmlp: HTMLP = block(url=url, page_width=1200, page_height=1200, styles=REQUIRED_STYLES)

    def test_is_running(self):
        assert self.block.requester.is_running

    def test_get_htmlp(self):
        assert isinstance(self.htmlp, HTMLP)

    def test_htmlp_required_attrs(self):
        assert all([
            (HTMLPTag._BBOX_ATTR in tag.attrs, HTMLPTag.styles in tag.attrs, tag.attrs is not None)
            for tag in self.htmlp.find_all(True)
        ])
