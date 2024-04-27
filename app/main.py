from fastapi import FastAPI

from app.users.user_api import user_router
from app.userevents.userevent_api import userevent_router
from app.usercontext.usercontext_api import usercontext_router
from app.usergoals.usergoal_api import usergoal_router
from config import PREFIX

app = FastAPI()

app.include_router(user_router, prefix=PREFIX)
app.include_router(userevent_router, prefix=PREFIX)
app.include_router(usercontext_router, prefix=PREFIX)
app.include_router(usergoal_router, prefix=PREFIX)
