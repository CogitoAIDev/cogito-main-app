from aiogram.filters import Filter
from aiogram.types import Message

from lib import filter_functions
    



class RegUserFilter_command(Filter):

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if listOfArgs[0] != '/reg_user':
            return None

        if len(listOfArgs) != 3:
            return None

        dictOfArgs = {'command': listOfArgs[0],
                    'name': listOfArgs[1],
                    'telegramChatID': listOfArgs[2]}
            
        return dictOfArgs


    async def __call__(self, message: Message) -> bool:
        dictOfArgs = self._get_args(message.text)


        if not dictOfArgs:
            return False

        try:
            return filter_functions.is_may_be_int(dictOfArgs['telegramChatID']) and len(dictOfArgs['name']) > 2
        except:
            return False
    
class GetUsersFilter_command(Filter):
    async def __call__(self, message: Message) -> bool:

        return message.text == '/get_users'
    
class GetUserFilter_command(Filter):

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if listOfArgs[0] != '/get_user':
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
    
class DeleteUserFilter_command(Filter):

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if listOfArgs[0] != '/delete_user':
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
    
class UpdateUserFilter_command(Filter):

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if listOfArgs[0] != '/update_user':
            return None

        if len(listOfArgs) != 3:
            return None

        dictOfArgs = {'command': listOfArgs[0],
                    'userID': listOfArgs[1],
                    'name': listOfArgs[2]}
            
        return dictOfArgs

    async def __call__(self, message: Message) -> bool:
        dictOfArgs = self._get_args(message.text)

        if not dictOfArgs:
            return False
        

        try:
            return filter_functions.is_may_be_int(dictOfArgs['userID'])
        except:
            return False