from flask import Flask, request, jsonify

import aiofiles
import asyncio

from LangMain import start
app = Flask(__name__)


@app.route('/receive_message', methods=['POST'])
async def receive_message():
    """
     Receiving messages from Telegram and starting LLM processing,

    """

    # Getting data json
    data = request.json

    # Starting LLM processing
    await start(data['chat_id'], data['text'])

    return jsonify({"status": "Success", "message": "Data received"}), 200

# Starting the programme
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
