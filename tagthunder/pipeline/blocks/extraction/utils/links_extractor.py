import urllib
from urllib.parse import urlparse

import bs4

from api.models.schemas import Hyperlink
from pipeline.blocks.extraction.utils.text_content_extraction import TextExtractor


class LinksExtractor:
    @classmethod
    def get_hyperlinks(cls, url: urllib.parse.ParseResult, soup: bs4.BeautifulSoup) -> list[Hyperlink]:
        links = soup.find_all(True, attrs={"href": True})
        res = []
        for link in links:
            if url:
                href = urlparse(link["href"] if "href" in link.attrs else "")
                if not cls.is_same_link(url, href):
                    hl = Hyperlink(
                        url=cls.get_url(url, href),
                        text=cls.get_link_text(link),
                        change_domain_name=cls.is_other_site(url, href)
                    )
                    res.append(hl)
        return res

    @classmethod
    def is_local_anchor(cls, url: urllib.parse.ParseResult, href: urllib.parse.ParseResult):
        return cls.is_same_link(url, href) and cls.is_anchor(href)

    @classmethod
    def is_same_link(cls, url: urllib.parse.ParseResult, href: urllib.parse.ParseResult):
        return all((not bool(x) for x in list(href)[:3])) or (cls.is_local_link(url, href) and href.path == url.path)

    @classmethod
    def is_local_link(cls, url: urllib.parse.ParseResult, href: urllib.parse.ParseResult):
        return not bool(href.netloc) or href.netloc == url.netloc

    @classmethod
    def is_anchor(cls, href: urllib.parse.ParseResult):
        return bool(href.fragment)

    @classmethod
    def is_other_site(cls, url: urllib.parse.ParseResult, href: urllib.parse.ParseResult):
        return bool(href.netloc) and url.netloc != href.netloc

    @classmethod
    def get_link_text(cls, link):
        if "title" in link.attrs:
            return link["title"]

        text = TextExtractor.extract_text(link)
        if text: return text[0]

        alt = TextExtractor.extract_alt(link)
        if alt: return alt[0]

        return [None]

    @classmethod
    def get_url(cls, url: urllib.parse.ParseResult, href: urllib.parse.ParseResult):
        if href.netloc:
            return href.geturl()
        else:
            new_path = urllib.parse.ParseResult(
                url.scheme, url.netloc, href.path, href.params, href.query, href.query
            )
            return urllib.parse.urlunparse(new_path)
