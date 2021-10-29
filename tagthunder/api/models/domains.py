from typing import Optional, List

from pydantic import BaseModel, Field

import algorithms.models


class HTMLP(algorithms.models.HTMLP):
    pass


class HTMLPP(algorithms.models.HTMLPP):
    pass

class Zone(algorithms.models.responses.Zone):
    pass


class Segmentation(algorithms.models.responses.Segmentation):
    pass


class Keywords(algorithms.models.responses.Keywords):
    pass


class Hyperlink(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    change_domain_name: Optional[bool]


class AccessmanZone(Zone):
    is_segmentable: bool = True
    html: str
    hyperlinks: Optional[List[Hyperlink]] = None
