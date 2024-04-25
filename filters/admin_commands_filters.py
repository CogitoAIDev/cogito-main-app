from aiogram.filters import Filter
from aiogram.types import Message

def is_may_be_int(text: str) -> bool:
    try:
        int(text)
        return True
    except ValueError:
        return False

class RegFilter_command(Filter):

    def _is_invalid_syntax(self, listOfArgs: list) -> bool:
        return len(listOfArgs) != 3

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if self._is_invalid_syntax(listOfArgs):
            return None

        dictOfArgs = {'command': listOfArgs[0],
                      'name': listOfArgs[1],
                      'userID': listOfArgs[2]}
        
        return dictOfArgs

    async def __call__(self, message: Message) -> bool:
        dictOfArgs = self._get_args(message.text)

        if not dictOfArgs:
            return False

        return dictOfArgs['command'] == '/reg' and is_may_be_int(dictOfArgs['userID'])
    
class emptyRegFilter_command(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.text == '/reg'

class ErrorRegFilter_command(Filter):

    def _is_invalid_syntax(self, listOfArgs: list) -> bool:
        return len(listOfArgs) != 3

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()
        if self._is_invalid_syntax(listOfArgs):
            return None
        
        dictOfArgs = {'command': listOfArgs[0],
                      'name': listOfArgs[1],
                      'userID': listOfArgs[2]}
        
        return dictOfArgs

    async def __call__(self, message: Message) -> bool:
        dictOfArgs = self._get_args(message.text)
        if not dictOfArgs:
            return False
        return dictOfArgs['command'] == '/reg' and is_may_be_int(dictOfArgs['userID'])