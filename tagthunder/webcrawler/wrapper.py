import requests
from pydantic import HttpUrl


class HTMLAugmentedRequester:
    STATUS_KEY = "status"
    STATUS_OK = 'Ok'
    STATUS_KO = 'Ko'
    
    def __init__(self, crawler_address: HttpUrl):
        self.crawler_address = crawler_address

    @classmethod
    def input_data_builder(cls, url: HttpUrl, recompute: bool):
        return {
            "url": url,
            "force": recompute
        }

    def request(self, url: HttpUrl, recompute: bool):
        r = requests.post(
            url=self.crawler_address,
            json=self.input_data_builder(url, recompute),
            allow_redirects=True, verify=False,
            proxies={'http': None, 'https': None})

        return r.json()

    @classmethod
    def is_ok(cls, response):
        return response[cls.STATUS_KEY] == cls.STATUS_OK

    def __call__(self, url: HttpUrl, recompute: bool):
        return self.request(url, recompute)
