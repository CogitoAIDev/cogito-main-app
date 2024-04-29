from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from LangMain import start

app = FastAPI()

@app.post("/receive_message")
async def receive_message(request: Request):
    """
    Receiving messages from Telegram and starting LLM processing.
    """
    # Getting data as JSON
    data = await request.json()

    # Starting LLM processing
    await start(data['chat_id'], data['text'])

    return JSONResponse(content={"status": "Success", "message": "Data received"}, status_code=status.HTTP_200_OK)

