from fastapi import FastAPI

from api import user_router, userevent_router

PREFIX = "/api/v1"

app = FastAPI()

app.include_router(user_router, prefix=PREFIX)
app.include_router(userevent_router, prefix=PREFIX)
