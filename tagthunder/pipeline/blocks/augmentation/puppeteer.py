from typing import Optional, List, Tuple

import pydantic
import requests
from pydantic import HttpUrl

from pipeline.blocks.augmentation._abstract import AbstractAugmentationBlock
from pipeline.models.responses import HTMLP


class Puppeteer(AbstractAugmentationBlock):
    def __init__(self, crawler_address):
        super(Puppeteer, self).__init__()
        self.page_height = None
        self.page_width = None
        self.requester = PuppeteerCrawlerWrapper(crawler_address=crawler_address)

    def config(self, page_width: int = 1200, page_height: int = 1200, styles: Optional[List[str]] = None):
        super(Puppeteer, self).config(styles)
        self.page_width, self.page_height = page_width, page_height

    def __call__(self, url: HttpUrl, **kwargs) -> HTMLP:
        response = self.requester(url=url, width=self.page_width, height=self.page_height, styles=self.styles)
        return HTMLP(markup=response.content)


class PuppeteerCrawlerWrapper:

    def __init__(self, crawler_address: HttpUrl):
        self.crawler_address = crawler_address

    class Body(pydantic.BaseModel):
        url: HttpUrl
        width: int
        height: int
        styles: List[str]

    def request(self, request) -> requests.Response:
        return requests.post(
            url=self.crawler_address,
            json=request,
            allow_redirects=True, verify=False,
            proxies={'http': None, 'https': None})

    @property
    def is_running(self):
        try:
            return requests.get(url=self.crawler_address).status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    @classmethod
    def is_OK(cls, response: requests.Response):
        return response.status_code == 200

    def __call__(self, **kwargs):
        return self.request(self.Body(**kwargs).dict())
