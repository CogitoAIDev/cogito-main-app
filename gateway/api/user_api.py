from fastapi import APIRouter
from gateway.schemas import user_schema
from gateway.core.services import user_service


user_router = APIRouter()


@user_router.post("/users/", response_model=user_schema.UserResponseDTO)
def create_user(user: user_schema.UserResponseDTO):
    return user_service.create_user(user)


# @app.get("/users", response_model=List[User])
# def read_users():
#     return users_db


# @app.post("/users", response_model=User)
# def create_user(user: User):
#     user.id = uuid4()
#     users_db.append(user.dict())
#     return user


# @app.get("/users/{user_id}", response_model=User)
# def read_user(user_id: UUID):
#     for user in users_db:
#         if user["id"] == user_id:
#             return user
#     raise HTTPException(status_code=404, detail="User not found")


# @app.put("/users/{user_id}", response_model=User)
# def update_user(user_id: UUID, updated_user: User):
#     for index, user in enumerate(users_db):
#         if user["id"] == user_id:
#             updated_user_data = updated_user.dict(exclude_unset=True)
#             updated_user_data["id"] = user_id
#             users_db[index] = updated_user_data
#             return updated_user_data
#     raise HTTPException(status_code=404, detail="User not found")


# @app.delete("/users/{user_id}", response_model=User)
# def delete_user(user_id: UUID):
#     for index, user in enumerate(users_db):
#         if user["id"] == user_id:
#             return users_db.pop(index)
#     raise HTTPException(status_code=404, detail="User not found")
