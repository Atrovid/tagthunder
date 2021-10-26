from pydantic import BaseModel
import models.fields as fields


class HTMLP(BaseModel):
    content: str = fields.HTMLP


class HTMLPP(BaseModel):
    content: str = fields.HTMLPP


class Segmentation