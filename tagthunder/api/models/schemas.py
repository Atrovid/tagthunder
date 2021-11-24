from typing import Optional, List, Any, Union

from pydantic import BaseModel, Field

import algorithms.models.responses as algo_responses


class HTML(BaseModel):
    __root__: str = Field(title="HTML", description="HTML without computed styles.")


class HTMLP(BaseModel):
    __root__: str = Field(title="HTML+", description="HTML with computed styles in attributes.")

    def __init__(self, htmlp: Union[algo_responses.HTMLP, str], **data: Any):
        if isinstance(htmlp, algo_responses.HTMLPP):
            htmlp = htmlp.prettify()

        super().__init__(__root__=htmlp, **data)


class HTMLPP(BaseModel):
    __root__: str = Field(title="HTML++", description="Cleaned HTML+.")

    def __init__(self, htmlpp: Union[algo_responses.HTMLPP, str], **data: Any):
        if isinstance(htmlpp, algo_responses.HTMLPP):
            htmlpp = htmlpp.prettify()

        super().__init__(__root__=htmlpp, **data)


class Segmentation(algo_responses.Segmentation):
    pass


class Keywords(algo_responses.Keywords):
    pass


class Hyperlink(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    change_domain_name: Optional[bool]


class Zone(algo_responses.Zone):
    pass
