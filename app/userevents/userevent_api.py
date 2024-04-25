from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas import userevent_schema
from app.services import userevent_service

userevent_router = APIRouter()


@userevent_router.post("/events/", response_model=userevent_schema.UserEventResponseDTO)
async def create_userevent(user: userevent_schema.UserEventCreateDTO):
    return await userevent_service.register_user(user)


@userevent_router.get(
    "/events/", response_model=List[userevent_schema.UserEventResponseDTO]
)
async def find_users():
    return await userevent_service.find_users()


@userevent_router.get(
    "/events/{user_id}", response_model=userevent_schema.UserEventResponseDTO
)
async def find_user_by_id(user_id: int):
    try:
        return await userevent_service.find_user_by_id(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@userevent_router.put(
    "/events/{user_id}", response_model=userevent_schema.UserEventResponseDTO
)
async def update_user(user_id: int, updated_user: userevent_schema.UserUpdateDTO):
    try:
        return await userevent_service.update_user(user_id, updated_user)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@userevent_router.delete(
    "/events/{user_id}", response_model=userevent_schema.UserEventResponseDTO
)
async def delete_user(user_id: int):
    try:
        return await userevent_service.delete_user(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
