import asyncio
import logging
import sys

from datetime import datetime

from dotenv import load_dotenv
import os

from pydantic import BaseModel
import httpx

from fastapi import FastAPI, HTTPException

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message


load_dotenv()

# Telegram bot token
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

# Dispatcher
dp = Dispatcher()

# URL of our LangChain app. Will change later when langchain app is on server.
url = "http://localhost:8000/receive_message"



# Initializing bot
async def main() -> None:
    bot = Bot(token=TG_BOT_TOKEN)
    await dp.start_polling(bot)




# Message handlers below
    
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Привет! Я бот Cogito, моя цель - помочь тебе эффективно ставить и достигать цели!")


@dp.message()
async def message_handler(message: Message) -> None:
    """
    This handler forwards messages to LangChain server
    """

    # Data that we send to LangCHain app
    data_to_send = {
        "chat_id": message.chat.id,
        "text": message.text
    }
    
    # Sending data
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data_to_send)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to forward message")
    
    return {"status": "Message forwarded", "response": response.json()}


# Starting the bot programme
if __name__ == "__main__":
    # Logging 
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())