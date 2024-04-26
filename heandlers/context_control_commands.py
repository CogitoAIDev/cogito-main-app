from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from filters import context_control_filters

router = Router()

#############################################################################################

# Добавление новых команд для UserContext
@router.message(context_control_filters.GetContextFilter_command())
async def get_context(message: types.Message):

    context = 'Контекст:\n'
    '''
    TODO: Add get_context logic
    '''

    await message.answer(context)

@router.message(Command(commands=['get_context']))
async def get_context_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/get_context "id:int"')

#############################################################################################

@router.message(context_control_filters.DeleteContextFilter_command())
async def delete_context(message: types.Message):

    '''
    TODO: Add delete_context logic
    '''

    await message.answer('UserContext успешно удален')

@router.message(Command(commands=['delete_context']))
async def delete_context_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/delete_context "id:int"')