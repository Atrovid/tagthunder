from typing import Optional, List

from pydantic import BaseModel, Field

import algorithms.models


class Hyperlink(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    change_domain_name: Optional[bool]


class AccessmanZone(algorithms.models.Zone):
    is_segmentable: bool = True
    html: str
    hyperlinks: Optional[List[Hyperlink]] = None


Zone = algorithms.models.Zone

Segmentation = algorithms.models.Segmentation

Keywords = algorithms.models.Keywords
