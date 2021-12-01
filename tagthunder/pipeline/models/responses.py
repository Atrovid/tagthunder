from typing import Optional, List, Union, Tuple, NewType, Type

import bs4
from pydantic import BaseModel, Field

from pipeline.models.web_elements import HTMLPTag, HTMLPPTag


class HTML(bs4.BeautifulSoup):
    def __init__(self, markup=""):
        super(HTML, self).__init__(markup=markup, features="html5lib")


class HTMLP(bs4.BeautifulSoup):
    def __init__(self, markup=""):
        super(HTMLP, self).__init__(markup=markup, features="html5lib", element_classes={bs4.Tag: HTMLPTag})


class HTMLPP(bs4.BeautifulSoup):
    def __init__(self, markup="", parser="html5lib"):
        super(HTMLPP, self).__init__(markup=markup, features=parser, element_classes={bs4.Tag: HTMLPPTag})

    def find_all_visible(self, attrs={}, recursive=True, text=None, limit=None, **kwargs):
        return self.find_all(lambda tag: tag.is_visible, attrs=attrs, recursive=recursive, text=text, limit=limit,
                             **kwargs)

    @property
    def bbox(self):
        return self.body.bbox


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
    keywords: Optional[Keywords] = None

    class Config:
        arbitrary_types_allowed = True


class Segmentation(BaseModel):
    zones: List[Zone] = []

    @property
    def htmlpp(self):
        return [z.htmlpp for z in self.zones]
