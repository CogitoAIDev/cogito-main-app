import httpx
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse

from gateway.config import APP_URL, PREFIX

notification_router = APIRouter()


@notification_router.get("/notifications/{notification_id}")
async def find_notification_by_id(notification_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.get(
            f"{APP_URL}{PREFIX}/notifications/{notification_id}"
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)


@notification_router.post("/notifications/")
async def create_notification(request: Request):
    body = await request.body()
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.post(
            f"{APP_URL}{PREFIX}/notifications/", content=body
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)


@notification_router.put("/notifications/{notification_id}")
async def update_notification(request: Request, notification_id: int):
    body = await request.body()
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.put(
            f"{APP_URL}{PREFIX}/notifications/{notification_id}", content=body
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)


@notification_router.delete("/notifications/{notification_id}")
async def delete_notification(notification_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.delete(
            f"{APP_URL}{PREFIX}/notifications/{notification_id}"
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)
