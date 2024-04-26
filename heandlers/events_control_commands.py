from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from filters import events_control_filters

router = Router()

#############################################################################################

@router.message(events_control_filters.RegEventFilter_command())
async def reg_new_event(message: types.Message):
    regSuccess = False

    '''
    TODO: Add registration logic
    '''

    if regSuccess:
        await message.answer('Регистрация события прошла успешно')
    else:
        await message.answer('Регистрация события не удалась')



@router.message(Command(commands=['reg_event']))
async def reg_event_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/reg_event "userName" "telegramChatId:int"')

#############################################################################################

@router.message(events_control_filters.GetEventsFilter_command())
async def get_events(message: types.Message):

    eventsList = []

    '''
    TODO: Add get_events logic
    '''

    resultMessage = 'Список событий:\n'

    for events in eventsList:
        resultMessage = resultMessage + events + '\n'

    await message.answer(resultMessage)


@router.message(Command(commands=['get_events']))
async def get_events_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/get_events #100 первых')

#############################################################################################

@router.message(events_control_filters.GetEventFilter_command())
async def get_event(message: types.Message):

    event = ''

    '''
    TODO: Add get_event logic
    '''

    await message.answer(event)


@router.message(Command(commands=['get_event']))
async def get_event_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/get_event "id:int"')

#############################################################################################


@router.message(events_control_filters.DeleteEventFilter_command())
async def delete_event(message: types.Message):

    '''
    TODO: Add delete_event logic
    '''

    await message.answer('Событие успешно удалено')


@router.message(Command(commands=['delete_event']))
async def delete_event_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/delete_event "id:int"')

#############################################################################################



@router.message(events_control_filters.UpdateEventFilter_command())
async def update_event(message: types.Message):

    '''
    TODO: Add update_event logic
    '''

    await message.answer('Событие успешно обновлено')


@router.message(Command(commands=['update_event']))
async def update_event_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/update_event "id" {}')

