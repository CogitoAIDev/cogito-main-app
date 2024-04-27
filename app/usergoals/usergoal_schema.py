from typing import Optional
from pydantic import BaseModel, Json


class UserGoalBase(BaseModel):
    goal_details: Json
    is_active: bool
    user_id: int


class UserGoalCreateDTO(UserGoalBase):
    is_active: Optional[bool] = True
    goal_details: Optional[Json] = "{}"


class UserGoalUpdateDTO(UserGoalBase):
    is_active: Optional[bool] = None
    goal_details: Optional[Json] = None
    user_id: Optional[int] = None


class UserGoalResponseDTO(UserGoalBase):
    goal_details: Optional[Json] = None
    is_active: Optional[bool] = None
    user_id: Optional[int] = None
    id: int
