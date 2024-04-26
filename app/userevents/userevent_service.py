from app.userevents import userevent_schema


async def create_userevent(userevent: userevent_schema.UserEventCreateDTO):
    userevent = userevent_schema.UserEventResponseDTO(**userevent.dict(), id=1)
    return userevent


async def find_userevents():
    return [
        userevent_schema.UserEventResponseDTO(
            name="event1",
            id=1,
            description="Just text about event1",
            isComplete=False,
            goal_id=1,
            user_id=1,
        ),
        userevent_schema.UserEventResponseDTO(
            name="event1",
            id=1,
            description="Just text about event1",
            isComplete=False,
            goal_id=1,
            user_id=1,
        ),
    ]


async def find_userevent_by_id(userevent_id: int):
    if userevent_id == 1:
        raise ValueError
    return userevent_schema.UserEventResponseDTO(
        name="event1",
        id=userevent_id,
        description="Just text about event1",
        isComplete=False,
        goal_id=1,
        user_id=1,
    )


async def update_userevent(
    userevent_id: int, updated_userevent: userevent_schema.UserEventUpdateDTO
):
    return userevent_schema.UserEventResponseDTO(
        name="event1",
        id=userevent_id,
        description="Just text about event1",
        isComplete=False,
        goal_id=1,
        user_id=1,
    )


async def delete_userevent(userevent_id: int):
    return userevent_schema.UserEventResponseDTO(
        name="event1",
        id=userevent_id,
        description="Just text about event1",
        isComplete=False,
        goal_id=1,
        user_id=1,
    )
