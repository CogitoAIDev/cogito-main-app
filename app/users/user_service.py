from app.users import user_schema


async def register_user(user: user_schema.UserCreateDTO):
    user = user_schema.UserResponseDTO(**user.dict(), id=1)
    return user


async def find_users():
    return [
        user_schema.UserResponseDTO(name="user1", tg_chat_id=1, id=1),
        user_schema.UserResponseDTO(name="user2", tg_chat_id=2, id=2),
    ]


async def find_user_by_id(user_id: int):
    if id == 1:
        raise ValueError
    return user_schema.UserResponseDTO(name="user1", tg_chat_id=1, id=user_id)


async def update_user(user_id: int, updated_user: user_schema.UserUpdateDTO):
    return user_schema.UserResponseDTO(name=updated_user.name, id=user_id)


async def delete_user(user_id: int):
    return user_schema.UserResponseDTO(name="user1", tg_chat_id=1, id=user_id)
