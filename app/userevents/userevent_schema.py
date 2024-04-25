from pydantic import BaseModel
from typing import Optional


class UserEventBase(BaseModel):
    name: str
    event_description: str
    isComplete: bool
    goal_id: int
    user_id: int


class UserEventCreateDTO(UserEventBase): ...


class UserEventUpdateDTO(UserEventBase):
    name: Optional[str] = None
    event_description: Optional[str] = None
    isComplete: Optional[bool] = None


class UserEventResponseDTO(UserEventBase):
    id: int
