import httpx
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse

from gateway.config import APP_URL, PREFIX

userevent_router = APIRouter()


@userevent_router.get("/events/")
async def find_userevents():
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.get(f"{APP_URL}{PREFIX}/events/")
        return JSONResponse(content=response.json(), status_code=response.status_code)


@userevent_router.get("/events/{userevent_id}")
async def find_userevent_by_id(
    userevent_id: int,
    include_notifications: bool = Query(
        False, description="Find event with its notifications"
    ),
):
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.get(
            f"{APP_URL}{PREFIX}/events/{userevent_id}?include_notifications={include_notifications}"
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)


@userevent_router.post("/events/")
async def create_userevent(request: Request):
    body = await request.body()
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.post(f"{APP_URL}{PREFIX}/events", content=body)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@userevent_router.put("/events/{userevent_id}")
async def update_userevent(request: Request, userevent_id: int):
    body = await request.body()
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.put(
            f"{APP_URL}{PREFIX}/events/{userevent_id}", content=body
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)


@userevent_router.delete("/events/{userevent_id}")
async def delete_userevent(userevent_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.delete(f"{APP_URL}{PREFIX}/events/{userevent_id}")
        return JSONResponse(content=response.json(), status_code=response.status_code)
