from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from filters import user_control_filters

router = Router()

#############################################################################################

@router.message(user_control_filters.RegUserFilter_command())
async def reg_new_user(message: types.Message):
    regSuccess = False

    '''
    TODO: Add registration logic
    '''

    if regSuccess:
        await message.answer('Регистрация прошла успешно')
    else:
        await message.answer('Регистрация не удалась')



@router.message(Command(commands=['reg_user']))
async def reg_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/reg_user "name" "telgramChatID"')

#############################################################################################

@router.message(user_control_filters.GetUsersFilter_command())
async def get_users(message: types.Message):

    usersList = []

    '''
    TODO: Add get_users logic
    '''

    resultMessage = 'Список пользователей:\n'

    for users in usersList:
        resultMessage = resultMessage + users + '\n'

    await message.answer(resultMessage)

#############################################################################################

@router.message(user_control_filters.GetUserFilter_command())
async def get_user(message: types.Message):

    user = 'Информация о пользователе:\n'

    '''
    TODO: Add get_user logic
    '''

    await message.answer(user)

@router.message(Command(commands=['get_user']))
async def get_user_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/get_user "id:int"')

#############################################################################################

@router.message(user_control_filters.DeleteUserFilter_command())
async def delete_user(message: types.Message):

    '''
    TODO: Add delete_user logic
    '''

    await message.answer('Пользователь успешно удален')

@router.message(Command(commands=['delete_user']))
async def delete_user_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/delete_user "id:int"')

#############################################################################################

@router.message(user_control_filters.UpdateUserFilter_command())
async def update_user(message: types.Message):

    '''
    TODO: Add update_user logic
    '''

    await message.answer('Пользователь успешно обновлен')

@router.message(Command(commands=['update_user']))
async def update_user_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/update_user "id:int" "name"')