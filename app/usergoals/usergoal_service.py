import json
import logging

from app.usergoals import usergoal_schema


async def find_goal_by_id(usercontext_id: int):
    return usergoal_schema.UserGoalResponseDTO(
        id=usercontext_id,
        goal_details=json.dumps({"goal": "Lol text"}),
        is_active=True,
        user_id=1,
    )


async def create_user_goal(usergoal: usergoal_schema.UserGoalCreateDTO):
    usergoal = usergoal
    usergoal.goal_details = json.dumps(usergoal.goal_details)
    usergoal = usergoal_schema.UserGoalResponseDTO(
        **usergoal.dict(),
        id=1,
    )
    return usergoal


async def update_user_goal(
    usergoal_id: int, updated_user_goal: usergoal_schema.UserGoalUpdateDTO
):
    updated_user_goal.goal_details = json.dumps(updated_user_goal.goal_details)
    usergoal = usergoal_schema.UserGoalResponseDTO(
        **updated_user_goal.dict(),
        id=usergoal_id,
    )
    return usergoal


async def delete_user_goal(usergoal_id: int):
    return usergoal_schema.UserGoalResponseDTO(id=usergoal_id)
