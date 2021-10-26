from typing import Optional, List

from pydantic import BaseModel
import api.models.fields as fields


class HTMLP(BaseModel):
    content: str = fields.HTMLP


class HTMLPP(BaseModel):
    content: str = fields.HTMLPP


Keywords = List[str]


class Hyperlink(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    change_domain_name: Optional[bool]


class BaseZone(BaseModel):
    id: int
    htmlpp: str = HTMLPP  # HTML++
    keywords: Optional[Keywords] = None


class AccessmanZone(BaseZone):
    is_segmentable: bool = True
    html: str
    hyperlinks: Optional[List[Hyperlink]] = None


Zone = BaseZone


class Segmentation(BaseModel):
    zones: List[Zone] = []
