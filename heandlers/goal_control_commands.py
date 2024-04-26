from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from filters import goal_control_filters

router = Router()

#############################################################################################

@router.message(goal_control_filters.GetGoalFilter_command())
async def get_goal(message: types.Message):

    goal = ''
    '''
    TODO: Add get_goal logic
    '''

    await message.answer(goal)

@router.message(Command(commands=['get_goal']))
async def get_goal_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/get_goal "id:int"')

#############################################################################################

@router.message(goal_control_filters.DeleteGoalFilter_command())
async def delete_goal(message: types.Message):

    '''
    TODO: Add delete_goal logic
    '''

    await message.answer('UserGoal успешно удален')

@router.message(Command(commands=['delete_goal']))
async def delete_goal_command(message: types.Message):
    await message.answer('Выполните запрос по шаблону (без кавычек):\n/delete_goal "id:int"')