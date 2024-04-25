from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    name: str
    tg_chat_id: int


class UserCreateDTO(UserBase): ...


class UserUpdateDTO(UserBase):
    name: Optional[str] = None


class UserResponseDTO(UserBase):
    id: int
