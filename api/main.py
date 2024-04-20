from fastapi import FastAPI, status

from fastapi.responses import JSONResponse

from handlers.crud import users

app = FastAPI()
"""
Запуск апи через uvicorn: uvicorn main:app --reload (из папки api)
"""


app.include_router(users.router)