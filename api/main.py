from fastapi import FastAPI, status

from fastapi.responses import JSONResponse

app = FastAPI()
"""
Запуск апи через uvicorn: uvicorn main:app --reload (из папки api)
"""


@app.get('/api/v1/ping')
async def ping():
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'OK'})