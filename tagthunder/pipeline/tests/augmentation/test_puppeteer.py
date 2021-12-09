from pipeline.blocks.augmentation.puppeteer import Puppeteer
from pipeline.blocks import REQUIRED_STYLES
from pipeline.models.responses import HTMLP
from pipeline.models.web_elements import HTMLPTag

crawler_address = "http://0.0.0.0:8080"
block = Puppeteer(crawler_address)
url = "https://www.example.com"


def test_is_running():
    assert block.requester.is_running


htmlp: HTMLP = block(url=url, page_width=1200, page_height=1200, styles=REQUIRED_STYLES)


def test_get_htmlp():
    assert isinstance(htmlp, HTMLP)


def test_htmlp_styles():
    assert all([
        (HTMLPTag._BBOX_ATTR in tag.attrs, HTMLPTag.styles in tag.attrs)
        for tag in htmlp.find_all(True)
    ])
