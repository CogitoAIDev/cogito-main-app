from aiogram.filters import Filter
from aiogram.types import Message

from lib import filter_functions

class GetGoalFilter_command(Filter):
    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if listOfArgs[0] != '/get_goal':
            return None

        if len(listOfArgs) != 2:
            return None

        dictOfArgs = {'command': listOfArgs[0],
                    'userID': listOfArgs[1]}
            
        return dictOfArgs

    async def __call__(self, message: Message) -> bool:
        dictOfArgs = self._get_args(message.text)

        if not dictOfArgs:
            return False

        try:
            return filter_functions.is_may_be_int(dictOfArgs['userID'])
        except:
            return False
        
class DeleteGoalFilter_command(Filter):
    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if listOfArgs[0] != '/delete_goal':
            return None

        if len(listOfArgs) != 2:
            return None

        dictOfArgs = {'command': listOfArgs[0],
                    'userID': listOfArgs[1]}
            
        return dictOfArgs

    async def __call__(self, message: Message) -> bool:
        dictOfArgs = self._get_args(message.text)

        if not dictOfArgs:
            return False

        try:
            return filter_functions.is_may_be_int(dictOfArgs['userID'])
        except:
            return False