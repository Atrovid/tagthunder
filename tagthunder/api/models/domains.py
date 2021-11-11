from typing import Optional, List

from pydantic import BaseModel, Field

import algorithms.models.responses as algo_responses


class HTMLP(algo_responses.HTMLP):
    pass


class HTMLPP(algo_responses.HTMLPP):
    pass


class Zone(algo_responses.Zone):
    pass


class Segmentation(algo_responses.Segmentation):
    pass


class Keywords(algo_responses.Keywords):
    pass


class Hyperlink(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    change_domain_name: Optional[bool]


class AccessmanZone(Zone):
    is_segmentable: bool = True
    html: str
    hyperlinks: Optional[List[Hyperlink]] = None
