from typing import Optional

from pydantic import HttpUrl

from pipeline.blocks.augmentation._abstract import AbstractAugmentationBlock
from pipeline.models.responses import HTMLP

from webcrawler.wrapper import HTMLAugmentedRequester


class Puppeteer(AbstractAugmentationBlock):
    def __init__(self, crawler_address):
        self.crawler_address: HttpUrl = crawler_address
        self.requester = HTMLAugmentedRequester(crawler_address=self.crawler_address)

    def __call__(self, url: HttpUrl, recompute: bool = False) -> HTMLP:
        response = self.requester(url, recompute=recompute)
        if not self.requester.is_ok(response):
            raise RuntimeError()
        return HTMLP(markup=self.requester.get_content(response))
