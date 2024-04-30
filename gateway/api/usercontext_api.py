import httpx
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse

from gateway.config import APP_URL, PREFIX

usercontext_router = APIRouter()


@usercontext_router.get("/contexts/{usercontext_id}")
async def find_usercontext_by_id(
    usercontext_id: int,
    include_notifications: bool = Query(
        False, description="Find context with its notifications"
    ),
):
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.get(
            f"{APP_URL}{PREFIX}/contexts/{usercontext_id}?include_notifications={include_notifications}"
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)


@usercontext_router.put("/contexts/{usercontext_id}")
async def update_usercontext(request: Request, usercontext_id: int):
    body = await request.body()
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.put(
            f"{APP_URL}{PREFIX}/contexts/{usercontext_id}", content=body
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)


@usercontext_router.delete("/contexts/{usercontext_id}")
async def delete_usercontext(usercontext_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.delete(
            f"{APP_URL}{PREFIX}/contexts/{usercontext_id}"
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)
