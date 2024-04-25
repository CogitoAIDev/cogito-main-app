from fastapi import FastAPI

from users.user_api import user_router
from userevents.userevent_api import userevent_router

PREFIX = "/api/v1"

app = FastAPI()

app.include_router(user_router, prefix=PREFIX)
app.include_router(userevent_router, prefix=PREFIX)
