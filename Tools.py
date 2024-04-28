from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


from typing import Optional, Type

class AddGoalData(BaseModel):
    goal_name: str = Field(description="it is the name of the goal")
    goal_description: str = Field(description="Full description of a goal. Everything that you got from the user.")
    goal_end_state: str = Field(description="What should be done to consider a goal achieved.")
    user_id: int = Field(description="User's id passed by with the context")

class AddGoalTool(BaseTool):
    name = "Add user's new goal to DB"
    description = "If a user has provided all the required info to make a record about his new goal, then use this tool "
    args_schema: Type[BaseModel] = AddGoalData



    def _run(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:

     
        return "Just run"

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Add goal to a DB. """
        pass
        # If adding was succesfull return "Goal added sucessfully", else return "Mistake, try adding goal again!"
        return "Goal added sucessfully"