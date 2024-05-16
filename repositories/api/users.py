from fastapi import APIRouter, HTTPException
from models.users import UserCreate, UserUpdate, User
from crud.crudUser import get_user, create_user, update_user, delete_user

router = APIRouter()

@router.post("/users/", response_model=User)
async def create_user_route(user: UserCreate):
    try:
        db_user = await create_user(user)
        if db_user:
            return db_user
        raise HTTPException(status_code=500, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.get("/users/{user_id}", response_model=User)
async def read_user_route(user_id: int):
    try:
        db_user = await get_user(user_id)
        if db_user:
            return db_user
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.put("/users/{user_id}", response_model=User)
async def update_user_route(user_id: int, user: UserUpdate):
    try:
        if not user.userName:  # Assuming userName is required to update
            raise HTTPException(status_code=400, detail="Invalid data: userName is required")
        updated_user = await update_user(user_id, user)
        if updated_user:
            return updated_user
        raise HTTPException(status_code=404, detail="User not found or not updated")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.delete("/users/{user_id}", response_model=User)
async def delete_user_route(user_id: int):
    try:
        deleted_user = await delete_user(user_id)
        if deleted_user:
            return deleted_user
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
