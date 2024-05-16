from pydantic import BaseModel, Field
from datetime import datetime

# Base model for common attributes
class MessageMetadataBase(BaseModel):
    sentTime: datetime = Field(..., description="Timestamp when the message was sent")
    userId: int = Field(..., description="The ID of the user associated with the message")
    modelId: int | None = Field(None, description="The ID of the model used for the message, if any")

# Schema for request on creation
class MessageMetadataCreate(MessageMetadataBase):
    # Inherits all fields from MessageMetadataBase
    pass

# Schema for request on update (allowing partial updates)
class MessageMetadataUpdate(BaseModel):
    sentTime: datetime | None = Field(None, description="New timestamp for when the message was sent")
    modelId: int | None = Field(None, description="New model ID associated with the message")

# Schema for response
class MessageMetadata(BaseModel):
    messageId: int
    sentTime: datetime
    userId: int
    modelId: int | None
