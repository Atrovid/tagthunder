from dataclasses import Field

from pydantic import BaseModel

import api.models.domains as domains


class HTML(BaseModel):
    __root__: str = Field(title="HTML", description="HTML without computed styles.")


class HTMLP(BaseModel):
    __root__: str = Field(title="HTML+", description="HTML with computed styles in attributes.")


class HTMLPP(BaseModel):
    __root__: str = Field(title="HTML++", description="Cleaned HTML+.")


class Segmentation(domains.Segmentation):
    pass


Keywords = domains.Keywords
