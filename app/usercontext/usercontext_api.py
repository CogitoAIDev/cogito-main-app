import logging
from typing import List
import json

from fastapi import APIRouter, HTTPException

from app.usercontext import usercontext_schema, usercontext_service

usercontext_router = APIRouter()


@usercontext_router.get(
    "/contexts/{usercontext_id}",
    response_model=usercontext_schema.UserContextResponseDTO,
)
async def find_context_by_id(usercontext_id: int):
    try:
        user_context = await usercontext_service.find_context_by_id(usercontext_id)
        user_context.context = json.dumps(user_context.context)
        return user_context
    except ValueError as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="UserContext not found")


@usercontext_router.put(
    "/contexts/{usercontext_id}",
    response_model=usercontext_schema.UserContextResponseDTO,
)
async def update_context(
    usercontext_id: int, updated_context: usercontext_schema.UserContextUpdateDTO
):
    try:
        user_context = await usercontext_service.update_context(
            usercontext_id, updated_context
        )
        user_context.context = json.dumps(user_context.context)
        return user_context
    except ValueError:
        raise HTTPException(status_code=404, detail="UserContext not found")
