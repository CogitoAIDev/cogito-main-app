from aiogram.filters import Filter
from aiogram.types import Message

def is_may_be_int(text: str) -> bool:
    try:
        int(text)
        return True
    except ValueError:
        return False
    



class RegUserFilter_command(Filter):

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

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
            return dictOfArgs['command'] == '/reg_user' and is_may_be_int(dictOfArgs['userID'])
        except:
            return False
    
class GetUsersFilter_command(Filter):
    async def __call__(self, message: Message) -> bool:

        return message.text == '/get_users'
    
class GetUserFilter_command(Filter):

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

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
            return dictOfArgs['command'] == '/get_user' and is_may_be_int(dictOfArgs['userID'])
        except:
            return False
    
class DeleteUserFilter_command(Filter):

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

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
            return dictOfArgs['command'] == '/delete_user' and is_may_be_int(dictOfArgs['userID'])
        except:
            return False
    
class UpdateUserFilter_command(Filter):

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

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
            return dictOfArgs['command'] == '/update_user' and is_may_be_int(dictOfArgs['userID'])
        except:
            return False