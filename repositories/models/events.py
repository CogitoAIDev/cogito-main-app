from pydantic import BaseModel, Field

# Base model for common attributes
class EventBase(BaseModel):
    eventName: str = Field(..., description="The name of the event")
    eventDescription: str = Field(..., description="A detailed description of the event")

# Schema for request on creation
class EventCreate(EventBase):
    userId: int = Field(..., description="The ID of the user associated with the event")
    goalId: int = Field(..., description="The ID of the goal associated with the event")

# Schema for request on update (allowing partial updates)
class EventUpdate(BaseModel):
    eventName: str | None = Field(None, description="The name of the event")
    eventDescription: str | None = Field(None, description="A detailed description of the event")
    isComplete: bool | None = Field(None, description="Status indicating if the event is completed")

# Schema for response
class Event(BaseModel):
    eventId: int
    eventName: str
    eventDescription: str
    userId: int
    goalId: int
    isComplete: bool
