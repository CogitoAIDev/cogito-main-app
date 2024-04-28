from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

# Telegram bot token
TOKEN = "6918195838:AAGLMJv9BasfBFnh3Ji5b8XO46FkNEZ99hs"

# TelegramAPI, to which we send messages
telegram_api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = FastAPI()


class Message(BaseModel):
    """
     Message that is sent to user via telegram.
     Attributes:
        chat_id (int): User's tg chat id, same as the user_id in the DB.
        text (str): Text that is sent to user.

    """
    chat_id: int
    text: str
    def __init__(self, **data):
        super().__init__(**data)

    

@app.post("/send-message/")
async def send_message(request: Message):
    """
     Sending message to user via TelegramAPI.

     Parameters:
        request (Message): Message that is sent to user.

    """
    # Constructing dict to send
    message_data = {"chat_id": request.chat_id, "text": request.text}

    # Sending dict to TelegramAPI
    async with httpx.AsyncClient() as client:
        response = await client.post(telegram_api_url, json=message_data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to send message")

    return {"status": "Message sent successfully", "response": response.json()}
