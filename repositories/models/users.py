from pydantic import BaseModel, Field

class UserBase(BaseModel):
    userName: str

class UserCreate(UserBase):
    telegramChatId: int | None = Field(default=None, description="Unique Telegram chat ID")

class UserUpdate(BaseModel):
    userName: str  # Only username is updatable (?)

class User(UserBase):
    userId: int
    telegramChatId: int | None
