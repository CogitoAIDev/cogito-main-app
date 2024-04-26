from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from filters import LLM_control_filters

router = Router()

#############################################################################################

@router.message(LLM_control_filters.GenerateLLMFilter_command())
async def LLM_generate(message: types.Message):

    result = 'Ответ:\n'

    '''
    TODO: Add LLM_generate logic
    '''

    await message.answer(result)


@router.message(Command(commands=['generate']))
async def LLM_generate_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/generate "текст"')