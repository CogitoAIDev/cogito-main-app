import httpx
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse

from gateway.config import APP_URL, PREFIX

user_router = APIRouter()


@user_router.get("/users/")
async def find_users():
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.get(f"{APP_URL}{PREFIX}/users")
        return JSONResponse(content=response.json(), status_code=response.status_code)


@user_router.get("/users/{user_id}")
async def find_user_by_id(
    user_id: int,
    include_context: bool = Query(
        False, description="Find user with his context details"
    ),
    include_goals: bool = Query(False, description="Find user with his goals ids"),
):
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.get(
            f"{APP_URL}{PREFIX}/users/{user_id}?include_context={include_context}&include_goals={include_goals}"
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)


@user_router.post("/users/")
async def register_user(request: Request):
    body = await request.body()
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.post(f"{APP_URL}{PREFIX}/users", content=body)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@user_router.put("/users/{user_id}")
async def update_user(request: Request, user_id: int):
    body = await request.body()
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.put(
            f"{APP_URL}{PREFIX}/users/{user_id}", content=body
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)


@user_router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.delete(f"{APP_URL}{PREFIX}/users/{user_id}")
        return JSONResponse(content=response.json(), status_code=response.status_code)
