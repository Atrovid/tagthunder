from typing import Optional, List, Union, Tuple, NewType, Type

import bs4
from pydantic import BaseModel, Field

from pipeline.models.web_elements import HTMLPTag, HTMLPPTag


class HTML(bs4.BeautifulSoup):
    def __init__(self, markup="", parser="lxml", **kwargs):
        super(HTML, self).__init__(markup=markup, features=parser, **kwargs)


class HTMLP(HTML):
    def __init__(self, markup="", tag_class=HTMLPTag, **kwargs):
        super(HTMLP, self).__init__(markup=markup, element_classes={bs4.Tag: tag_class}, **kwargs)

    def get_comments(self, recursive=False):
        return self(text=lambda text: isinstance(text, bs4.Comment), recursive=recursive)

    def contains_comments(self, recursive=False):
        return bool(self.get_comments(recursive))

    @property
    def bbox(self):
        return self.body.bbox

    def get_leafs(self):
        return [node for node in self.find_all() if node.find() is None]


class HTMLPP(HTMLP):
    def __init__(self, markup="", **kwargs):
        super(HTMLPP, self).__init__(markup=markup, tag_class=HTMLPPTag, **kwargs)

    def find_all_usable(self, attrs=None, recursive=True, text=None, limit=None, **kwargs):
        if attrs is None:
            attrs = {}
        return self.body.find_all(lambda tag: tag.is_usable, attrs=attrs, recursive=recursive, text=text, limit=limit,
                                  **kwargs)

    def remove_unusable_tags(self):
        for t in self.body.find_all(lambda tag: not tag.is_usable, recursive=True):
            t.extract()

    def __copy__(self):
        return type(self)(self.prettify())

    def get_leafs(self, usable_tags: bool = True):
        return [node for node in self.find_all() if node.find() is None and node.is_usable]

    @classmethod
    def from_tags(cls, tags: List[HTMLPPTag]):
        return cls("".join(map(str, tags)))


class Keyword(BaseModel):
    text: str
    score: Optional[float] = None
    lang: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


Keywords = List[Keyword]


class Zone(BaseModel):
    id: int
    htmlpp: Union[List[HTMLPP], HTMLPP]
    keywords: Optional[Keywords] = []

    class Config:
        arbitrary_types_allowed = True


class Segmentation(BaseModel):
    zones: List[Zone] = []

    @property
    def htmlpp(self):
        return [z.htmlpp for z in self.zones]
