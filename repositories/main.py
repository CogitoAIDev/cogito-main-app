from fastapi import FastAPI
from api import users, events, notifications, messagesMetadata
from models.dataAccess import DatabaseConnectionPool

app = FastAPI()

@app.on_event("startup")
async def startup():
    DatabaseConnectionPool.initialize_pool(1, 10)

@app.on_event("shutdown")
async def shutdown():
    DatabaseConnectionPool.close_all_connections()

app.include_router(users.router)
app.include_router(events.router)
app.include_router(notifications.router)
app.include_router(messagesMetadata.router)
