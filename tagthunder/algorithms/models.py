from typing import Optional, List, Union, Tuple, NewType, Type

from pydantic import BaseModel, Field


class HTML(BaseModel):
    __root__: str = Field(title="HTML", description="HTML without computed styles.")


class HTMLP(BaseModel):
    __root__: str = Field(title="HTML+", description="HTML with computed styles in attributes.")


class HTMLPP(BaseModel):
    __root__: str = Field(title="HTML++", description="Cleaned HTML+.")


class Keyword(BaseModel):
    keyword: str
    score: Optional[float] = None


Keywords = List[Keyword]


class Zone(BaseModel):
    id: int
    htmlpp: HTMLPP
    keywords: Optional[Keywords] = None


class Segmentation(BaseModel):
    zones: List[Zone] = []

