from pydantic import BaseModel, Json
from typing import Optional, List

from app.usercontext import usercontext_schema


class UserBase(BaseModel):
    name: str


class UserCreateDTO(UserBase):
    tg_chat_id: int


class UserUpdateDTO(UserBase):
    name: Optional[str] = None


class UserResponseDTO(UserBase):
    usercontext: Optional[Json] = None
    usergoal_ids: Optional[List[int]] = None
    id: int
