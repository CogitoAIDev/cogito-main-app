from aiogram.filters import Filter
from aiogram.types import Message

from lib import filter_functions

class GenerateLLMFilter_command(Filter):
    def _get_args(self, text: str) -> dict:
        listOfArgs = text.split()

        if listOfArgs[0] != '/generate':
            return None
        
        if len(listOfArgs) <= 1:
            return None

        dictOfArgs = {'command': listOfArgs[0],
                    'text': ''}
        
        for arg in listOfArgs[1:]:
            dictOfArgs['text'] = dictOfArgs['text'] + ' ' + arg
            
        return dictOfArgs
    
    async def __call__(self, message: Message) -> bool:
        dictOfArgs = self._get_args(message.text)

        if not dictOfArgs:
            return False

        try:
            return len(dictOfArgs['text']) > 1
        except:
            return False