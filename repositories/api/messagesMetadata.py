from fastapi import APIRouter, HTTPException
from models.messagesMetadata import MessageMetadataCreate, MessageMetadataUpdate, MessageMetadata
from crud.crudMessagesMetadata import get_message_metadata, create_message_metadata, update_message_metadata, delete_message_metadata

router = APIRouter()

@router.post("/messages_metadata/", response_model=MessageMetadata)
async def create_message_metadata_route(message: MessageMetadataCreate):
    db_message = await create_message_metadata(message)
    if db_message:
        return db_message
    raise HTTPException(status_code=500, detail="Failed to create message metadata")

@router.get("/messages_metadata/{message_id}", response_model=MessageMetadata)
async def read_message_metadata_route(message_id: int):
    db_message = await get_message_metadata(message_id)
    if db_message:
        return db_message
    raise HTTPException(status_code=404, detail="Message metadata not found")

@router.put("/messages_metadata/{message_id}", response_model=MessageMetadata)
async def update_message_metadata_route(message_id: int, message: MessageMetadataUpdate):
    updated_message = await update_message_metadata(message_id, message)
    if updated_message:
        return updated_message
    raise HTTPException(status_code=404, detail="Failed to update message metadata")

@router.delete("/messages_metadata/{message_id}", response_model=MessageMetadata)
async def delete_message_metadata_route(message_id: int):
    deleted_message = await delete_message_metadata(message_id)
    if deleted_message:
        return deleted_message
    raise HTTPException(status_code=404, detail="Message metadata not found")
