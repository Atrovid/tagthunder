from typing import Optional, List

from pydantic import BaseModel, Field

import algorithms.models


class HTMLP(algorithms.models.HTMLP):
    pass


class HTMLPP(algorithms.models.HTMLPP):
    pass


class Hyperlink(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    change_domain_name: Optional[bool]


class Zone(algorithms.models.Zone):
    is_segmentable: bool = True
    html: str
    hyperlinks: Optional[List[Hyperlink]] = None


Segmentation = algorithms.models.Segmentation

Keywords = algorithms.models.Keywords
