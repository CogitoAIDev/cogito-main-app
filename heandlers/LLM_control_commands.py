from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from filters import user_control_filters

router = Router()

#############################################################################################

@router.message(user_control_filters.LLMGenerateFilter_command())
async def LLM_generate(message: types.Message):

    result = ''

    '''
    TODO: Add LLM_generate logic
    '''

    await message.answer(result)


@router.message(Command(commands=['LLM_generate']))
async def LLM_generate_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\nLLM_generate "текст"')