import httpx
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse

from gateway.config import APP_URL, PREFIX

usergoal_router = APIRouter()


@usergoal_router.get("/goals/{usergoal_id}")
async def find_usergoal_by_id(usergoal_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.get(f"{APP_URL}{PREFIX}/goals/{usergoal_id}")
        return JSONResponse(content=response.json(), status_code=response.status_code)


@usergoal_router.post("/goals/")
async def create_usergoal(request: Request):
    body = await request.body()
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.post(f"{APP_URL}{PREFIX}/goals", content=body)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@usergoal_router.put("/goals/{usergoal_id}")
async def update_usergoal(request: Request, usergoal_id: int):
    body = await request.body()
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.put(
            f"{APP_URL}{PREFIX}/goals/{usergoal_id}", content=body
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)


@usergoal_router.delete("/goals/{usergoal_id}")
async def delete_usergoal(usergoal_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.delete(f"{APP_URL}{PREFIX}/goals/{usergoal_id}")
        return JSONResponse(content=response.json(), status_code=response.status_code)
