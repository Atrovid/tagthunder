import uvicorn
from fastapi import FastAPI

import api.routers as routers
from api.configurations.api import settings

app = FastAPI(
    title=settings.app_name,
    docs_url=settings.docs_url,
    openapi_tags=routers.tags,
)

for sub_router in routers.routes:
    app.include_router(sub_router)


def run():
    uvicorn.run("api.main:app", reload=True)
