from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    name: str


class UserCreateDTO(UserBase):
    tg_chat_id: int


class UserUpdateDTO(UserBase):
    name: Optional[str] = None


class UserResponseDTO(UserBase):
    id: int
