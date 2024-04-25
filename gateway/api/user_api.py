from fastapi import APIRouter, HTTPException
from typing import List

from gateway.schemas import user_schema
from gateway.services import user_service


user_router = APIRouter()


@user_router.post("/users/", response_model=user_schema.UserResponseDTO)
async def register_user(user: user_schema.UserCreateDTO):
    return await user_service.register_user(user)


@user_router.get("/users/", response_model=List[user_schema.UserResponseDTO])
async def find_users():
    return await user_service.find_users()


@user_router.get("/users/{user_id}", response_model=user_schema.UserResponseDTO)
async def find_user_by_id(user_id: int):
    try:
        return await user_service.find_user_by_id(user_id)
    except ValueError:
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
