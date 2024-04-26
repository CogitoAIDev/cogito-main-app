import asyncio
import logging
from dotenv import load_dotenv

load_dotenv()

from aiogram import Bot, Dispatcher

from heandlers import (
    unknown_commands,
    user_control_commands,
    events_control_commands,
    goal_control_commands,
    LLM_control_commands,
    context_control_commands
    )

import os

async def start_polling():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()

    dp.include_routers(
        user_control_commands.router,
        events_control_commands.router,
        goal_control_commands.router,
        LLM_control_commands.router,
        context_control_commands.router,

        unknown_commands.router
        )

    await bot.delete_webhook()
    await dp.start_polling(bot)

def main():
    asyncio.run(start_polling())

if __name__ == "__main__":
    main()