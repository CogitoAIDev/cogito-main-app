from pydantic import BaseModel, Field
from datetime import datetime

# Base model for common attributes
class NotificationBase(BaseModel):
    eventId: int = Field(..., description="The ID of the related event")
    time: datetime = Field(..., description="Timestamp of the notification")

# Schema for request on creation
class NotificationCreate(NotificationBase):
    # Inherits eventId and time, no additional fields needed for creation
    pass

# Schema for request on update (allowing partial updates)
class NotificationUpdate(BaseModel):
    time: datetime | None = Field(None, description="New timestamp for the notification")
    isComplete: bool | None = Field(None, description="Status indicating if the notification is completed")

# Schema for response
class Notification(BaseModel):
    notificationId: int
    eventId: int
    time: datetime
    isComplete: bool
