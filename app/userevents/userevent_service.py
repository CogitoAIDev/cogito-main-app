from gateway.schemas import userevent_schema


async def create_userevent(userevent: userevent_schema.UserEventCreateDTO):
    user = user_schema.UserResponseDTO(**user.dict(), id=1)
    return user


async def find_userevents():
    return [
        userevent_schema.UserEventResponseDTO(
            name="event1",
            id=1,
            event_description="Just text about event1",
            isComplete=False,
            goal_id=1,
            user_id=1,
        ),
    ]


async def find_userevent_by_id(id: int):
    if id == 1:
        raise ValueError
    return (
        userevent_schema.UserEventResponseDTO(
            name="event1",
            id=1,
            event_description="Just text about event1",
            isComplete=False,
            goal_id=1,
            user_id=1,
        ),
    )


async def update_userevent(
    id: int, updated_userevent: userevent_schema.UserEventUpdateDTO
):
    return (
        userevent_schema.UserEventResponseDTO(
            name="event1",
            id=1,
            event_description="Just text about event1",
            isComplete=False,
            goal_id=1,
            user_id=1,
        ),
    )


async def delete_userevent(id: int):
    return (
        userevent_schema.UserEventResponseDTO(
            name="event1",
            id=1,
            event_description="Just text about event1",
            isComplete=False,
            goal_id=1,
            user_id=1,
        ),
    )
