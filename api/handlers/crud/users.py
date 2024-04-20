from fastapi import APIRouter, status, HTTPException, Query

from fastapi.responses import JSONResponse

from models.user import User
from db.db import db

router = APIRouter()

@router.post('/api/v1/crud/users/create')
async def create_user(user: User):
    try:
        id = db.create_user(user)
        return JSONResponse(status_code=status.HTTP_200_OK, content={'row_id': id})
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'message': ex.__str__()})
    
@router.get('/api/v1/crud/users/get_user')
async def get_user(user_id: int = Query(..., description="Specified User ID as query param")):
    user = db.get_user(user_id)
    if user:
        return JSONResponse(status_code=status.HTTP_200_OK, content={'username': user.username, 'chatID': user.chatID})
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'message': 'user not found'})

@router.get('/api/v1/crud/users/get')
async def get_users():
    users = db.get_users()
    if users:
        return JSONResponse(status_code=status.HTTP_200_OK, content={'users': users})
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'no users found'})

