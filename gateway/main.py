from fastapi import FastAPI

from gateway.api import (
    user_router,
    usergoal_router,
    userevent_router,
    usercontext_router,
    messages_metadata_router,
    notification_router,
)
from gateway.config import PREFIX


app = FastAPI()

app.include_router(user_router, prefix=PREFIX)
app.include_router(usergoal_router, prefix=PREFIX)
app.include_router(userevent_router, prefix=PREFIX)
app.include_router(usercontext_router, prefix=PREFIX)
app.include_router(messages_metadata_router, prefix=PREFIX)
app.include_router(notification_router, prefix=PREFIX)
