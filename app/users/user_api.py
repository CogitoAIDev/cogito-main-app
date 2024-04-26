from typing import List
import logging

from fastapi import APIRouter, HTTPException, Query

from app.users import user_service, user_schema
from app.usercontext import usercontext_service, usercontext_schema


user_router = APIRouter()


@user_router.post("/users/", response_model=user_schema.UserResponseDTO)
async def register_user(
    user: user_schema.UserCreateDTO,
    include_context: bool = Query(
        False, description="Create user and return his context details"
    ),
):
    user_data = await user_service.register_user(user)
    user_context = await usercontext_service.create_context_for_user(user_data.id)
    if include_context:
        user_data.usercontext = user_context.json()
    return user_data


@user_router.get("/users/", response_model=List[user_schema.UserResponseDTO])
async def find_users():
    return await user_service.find_users()


@user_router.get("/users/{user_id}", response_model=user_schema.UserResponseDTO)
async def find_user_by_id(
    user_id: int,
    include_context: bool = Query(
        False, description="Find user with his context details"
    ),
):
    try:
        user_data = await user_service.find_user_by_id(user_id)
        if include_context:
            user_context = await usercontext_service.find_context_by_user_id(user_id)
            print(user_context)
            user_data.usercontext = user_context.json()
        return user_data
    except ValueError as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="User not found")


@user_router.put("/users/{user_id}", response_model=user_schema.UserResponseDTO)
async def update_user(user_id: int, updated_user: user_schema.UserUpdateDTO):
    try:
        return await user_service.update_user(user_id, updated_user)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.delete("/users/{user_id}", response_model=user_schema.UserResponseDTO)
async def delete_user(user_id: int):
    try:
        return await user_service.delete_user(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
