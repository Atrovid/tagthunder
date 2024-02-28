from typing import Optional, List, Any, Union

import fastapi
from pydantic import BaseModel, Field


class HTML(BaseModel):
    __root__: str = Field(title="HTML", description="HTML without computed styles.")


class HTMLP(BaseModel):
    __root__: str = Field(title="HTML+", description="HTML with computed styles in attributes.")


class HTMLPP(BaseModel):
    __root__: str = Field(title="HTML++", description="Cleaned HTML+.")


class Keyword(BaseModel):
    text: str
    score: Optional[float] = None

    class Config:
        arbitrary_types_allowed = True


Keywords = List[Keyword]


class Zone(BaseModel):
    id: int
    htmlpp: Union[List[HTMLPP], HTMLPP]
    keywords: Optional[Keywords] = []
    xpath : List[str] = []

    class Config:
        arbitrary_types_allowed = True


class Segmentation(BaseModel):
    __root__: List[Zone]


class Hyperlink(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    change_domain_name: Optional[bool]
