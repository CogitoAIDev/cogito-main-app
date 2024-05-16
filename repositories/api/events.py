from fastapi import APIRouter, HTTPException
from models.events import EventCreate, EventUpdate, Event
from crud.crudEvents import get_event, create_event, update_event, delete_event

router = APIRouter()
# TODO: Implement robust error handling
# TODO: Implement logging
# TODO

@router.post("/events/", response_model=Event)
async def create_event_route(event: EventCreate):
    db_event = await create_event(event)
    if db_event:
        return db_event
    raise HTTPException(status_code=500, detail="Failed to create event")

@router.get("/events/{event_id}", response_model=Event)
async def read_event_route(event_id: int):
    db_event = await get_event(event_id)
    if db_event:
        return db_event
    raise HTTPException(status_code=404, detail="Event not found")

@router.put("/events/{event_id}", response_model=Event)
async def update_event_route(event_id: int, event: EventUpdate):
    updated_event = await update_event(event_id, event)
    if updated_event:
        return updated_event
    raise HTTPException(status_code=404, detail="Failed to update event")

@router.delete("/events/{event_id}", response_model=Event)
async def delete_event_route(event_id: int):
    deleted_event = await delete_event(event_id)
    if deleted_event:
        return deleted_event
    raise HTTPException(status_code=404, detail="Event not found")
