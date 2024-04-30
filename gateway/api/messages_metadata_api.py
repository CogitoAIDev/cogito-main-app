import httpx
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse

from gateway.config import APP_URL, PREFIX

messages_metadata_router = APIRouter()


@messages_metadata_router.get("/messages_metadata/{message_metadata_id}")
async def find_messages_metadata_by_id(message_metadata_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as http_client:
        response = await http_client.get(
            f"{APP_URL}{PREFIX}/messages_metadata/{message_metadata_id}"
        )
        return JSONResponse(content=response.json(), status_code=response.status_code)
