from asgiref.wsgi import WsgiToAsgi
from LangApp import app


# Асинхронный враппер для тестов
asgi_app = WsgiToAsgi(app)
