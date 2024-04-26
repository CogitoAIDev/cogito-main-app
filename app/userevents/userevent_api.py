from fastapi import APIRouter, HTTPException
from typing import List

from app.userevents import userevent_schema, userevent_service

userevent_router = APIRouter()


@userevent_router.post("/events/", response_model=userevent_schema.UserEventResponseDTO)
async def create_userevent(userevent: userevent_schema.UserEventCreateDTO):
    return await userevent_service.create_userevent(userevent)


@userevent_router.get(
    "/events/", response_model=List[userevent_schema.UserEventResponseDTO]
)
async def find_userevents():
    return await userevent_service.find_userevents()


@userevent_router.get(
    "/events/{userevent_id}", response_model=userevent_schema.UserEventResponseDTO
)
async def find_userevent_by_id(userevent_id: int):
    try:
        return await userevent_service.find_userevent_by_id(userevent_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@userevent_router.put(
    "/events/{user_id}", response_model=userevent_schema.UserEventResponseDTO
)
async def update_userevent(
    user_id: int, updated_user: userevent_schema.UserEventUpdateDTO
):
    try:
        return await userevent_service.update_userevent(user_id, updated_user)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@userevent_router.delete(
    "/events/{user_id}", response_model=userevent_schema.UserEventResponseDTO
)
async def delete_userevent(user_id: int):
    try:
        return await userevent_service.delete_userevent(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
