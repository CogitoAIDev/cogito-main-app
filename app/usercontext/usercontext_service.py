import json

from app.usercontext import usercontext_schema
from app.users import user_schema


async def find_context_by_id(
    usercontext_id: int,
) -> usercontext_schema.UserContextResponseDTO:
    return usercontext_schema.UserContextResponseDTO(
        context=json.dumps({"mood": "good"}), id=usercontext_id
    )

async def update_context(
    usercontext_id: int,
    updated_context: usercontext_schema.UserContextUpdateDTO,
) -> usercontext_schema.UserContextResponseDTO:
    return usercontext_schema.UserContextResponseDTO(
        context=json.dumps({"mood": "good"}), id=usercontext_id
    )

async def find_context_by_user_id(
    user_id: int,
) -> usercontext_schema.UserContextResponseDTO:
    return usercontext_schema.UserContextResponseDTO(
        context=json.dumps({"mood": "good"}), id=5
    )


async def create_context_for_user(
    user_id: int,
) -> usercontext_schema.UserContextResponseDTO:
    return usercontext_schema.UserContextResponseDTO(
        context=json.dumps({"mood": "good"}), id=5
    )
