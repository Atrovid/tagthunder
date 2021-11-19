from typing import Optional, List, Union, Tuple, NewType, Type

import bs4
from pydantic import BaseModel, Field

from algorithms.models.web_elements import Tag


class HTML(BaseModel):
    __root__: str = Field(title="HTML", description="HTML without computed styles.")


class HTMLP(BaseModel):
    __root__: str = Field(title="HTML+", description="HTML with computed styles in attributes.")


class HTMLPP(bs4.BeautifulSoup):
    def __init__(self, markup=""):
        super(HTMLPP, self).__init__(markup=markup, features="html.parser", element_classes={bs4.Tag: Tag})


class Keyword(BaseModel):
    keyword: str
    score: Optional[float] = None

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
