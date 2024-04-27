import logging
import json

from fastapi import APIRouter, HTTPException

from app.usergoals import usergoal_schema, usergoal_service


usergoal_router = APIRouter()

logging.basicConfig(level=logging.DEBUG)


@usergoal_router.get(
    "/goals/{usergoal_id}",
    response_model=usergoal_schema.UserGoalResponseDTO,
)
async def find_goal_by_id(usergoal_id: int):
    try:
        user_goal = await usergoal_service.find_goal_by_id(usergoal_id)
        user_goal.goal_details = json.dumps(user_goal.goal_details)
        return user_goal
    except ValueError as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="UserGoal not found")


@usergoal_router.post("/goals/", response_model=usergoal_schema.UserGoalResponseDTO)
async def create_user_goal(usergoal: usergoal_schema.UserGoalCreateDTO):
    try:
        usergoal = await usergoal_service.create_user_goal(usergoal)
        usergoal.goal_details = json.dumps(usergoal.goal_details)
        return usergoal
    except ValueError as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail="UserGoal not created")


@usergoal_router.put(
    "/goals/{usergoal_id}", response_model=usergoal_schema.UserGoalResponseDTO
)
async def update_user_goal(
    usergoal_id: int, updated_user_goal: usergoal_schema.UserGoalUpdateDTO
):
    try:
        user_goal = await usergoal_service.update_user_goal(
            usergoal_id, updated_user_goal
        )
        user_goal.goal_details = json.dumps(user_goal.goal_details)
        return user_goal
    except ValueError as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="UserGoal not found")


@usergoal_router.delete(
    "/goals/{usergoal_id}", response_model=usergoal_schema.UserGoalResponseDTO
)
async def delete_user_goal(usergoal_id: int):
    try:
        user_goal = await usergoal_service.delete_user_goal(usergoal_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="UserGoal not found")
    return user_goal
