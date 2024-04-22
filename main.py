import asyncio
import logging

from aiogram import Bot, Dispatcher

from heandlers import unknown_commands

import os

async def start_polling():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()

    dp.include_routers(
        unknown_commands.router,
        )

    await bot.delete_webhook()
    await dp.start_polling(bot)

def main():
    asyncio.run(start_polling())

if __name__ == "__main__":
    main()