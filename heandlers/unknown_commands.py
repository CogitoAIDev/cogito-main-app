from aiogram import types
from aiogram import Router

router = Router()


@router.message()
async def none_command(message: types.Message):

    await message.reply("К сожалению бот не поддерживает данную команду. Обратитесь к пункту меню")

