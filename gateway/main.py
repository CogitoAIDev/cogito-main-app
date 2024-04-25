from fastapi import FastAPI

from api import user_router

app = FastAPI()

app.include_router(user_router, prefix="/api/v1")
