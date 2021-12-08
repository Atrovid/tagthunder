from typing import Optional

import pydantic.networks as pn
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TagThunder API"
    admin_email: pn.EmailStr = "francois.ledoyen@unicaen.fr"
    # node.js app allows to build augmented HTML
    crawler_address: pn.HttpUrl = "http://0.0.0.0:8080/"
    host: str
    port: Optional[int]
    docs_url: str = "/"


class LocalSettings(Settings):
    host = "http://127.0.0.1"
    port = 8000


class AccessmanSettings(Settings):
    host = "https://accessman.greyc.fr/api"


settings = LocalSettings()
