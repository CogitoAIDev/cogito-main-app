from aiogram.filters import Filter
from aiogram.types import Message

from lib import filter_functions

class RegEventFilter_command(Filter):

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if listOfArgs[0] != '/reg_event':
            return None

        if len(listOfArgs) != 2:
            return None

        dictOfArgs = {'command': listOfArgs[0],
                    'userName': listOfArgs[1],
                    'ID': listOfArgs[2]}
            
        return dictOfArgs


    async def __call__(self, message: Message) -> bool:
        dictOfArgs = self._get_args(message.text)


        if not dictOfArgs:
            return False

        try:
            return filter_functions.is_may_be_int(dictOfArgs['ID'])
        except:
            return False
        
class GetEventFilter_command(Filter):
    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if listOfArgs[0] != '/get_events':
            return None


        if len(listOfArgs) != 2:
            return None

        dictOfArgs = {'command': listOfArgs[0],
                    'userName': listOfArgs[1]}
            
        return dictOfArgs

    async def __call__(self, message: Message) -> bool:
        dictOfArgs = self._get_args(message.text)

        if not dictOfArgs:
            return False

        try:
            return filter_functions.is_may_be_int(dictOfArgs['ID'])
        except:
            return False
        
class GetEventsFilter_command(Filter):
    async def __call__(self, message: Message) -> bool:

        return message.text == '/get_events'
    
class UpdateEventFilter_command(Filter):

    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if listOfArgs[0] != '/update_event':
            return None


        if len(listOfArgs) <= 2:
            return None

        dictOfArgs = {'command': listOfArgs[0],
                    'ID': listOfArgs[1],
                    'event': ''}
        
        for arg in listOfArgs[2:]:
            dictOfArgs['event'] = dictOfArgs['event'] + ' ' + arg    
            
        return dictOfArgs
    

    async def __call__(self, message: Message) -> bool:
        dictOfArgs = self._get_args(message.text)

        if not dictOfArgs:
            return False
        

        try:
            return filter_functions.is_may_be_int(dictOfArgs['ID']) and filter_functions.is_may_be_dict(dictOfArgs['event'])
        except:
            return False
        

class DeleteEventFilter_command(Filter):
    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if listOfArgs[0] != '/delete_event':
            return None

        if len(listOfArgs) != 2:
            return None

        dictOfArgs = {'command': listOfArgs[0],
                    'ID': listOfArgs[1]}
            
        return dictOfArgs
    
    async def __call__(self, message: Message) -> bool:
        dictOfArgs = self._get_args(message.text)

        if not dictOfArgs:
            return False

        try:
            return filter_functions.is_may_be_int(dictOfArgs['ID'])
        except:
            return False