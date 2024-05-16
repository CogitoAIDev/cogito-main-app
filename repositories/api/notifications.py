from fastapi import APIRouter, HTTPException
from models.notifications import NotificationCreate, NotificationUpdate, Notification
from crud.crudNotifications import get_notification, create_notification, update_notification, delete_notification

router = APIRouter()

@router.post("/notifications/", response_model=Notification)
async def create_notification_route(notification: NotificationCreate):
    db_notification = await create_notification(notification)
    if db_notification:
        return db_notification
    raise HTTPException(status_code=500, detail="Failed to create notification")

@router.get("/notifications/{notification_id}", response_model=Notification)
async def read_notification_route(notification_id: int):
    db_notification = await get_notification(notification_id)
    if db_notification:
        return db_notification
    raise HTTPException(status_code=404, detail="Notification not found")

@router.put("/notifications/{notification_id}", response_model=Notification)
async def update_notification_route(notification_id: int, notification: NotificationUpdate):
    updated_notification = await update_notification(notification_id, notification)
    if updated_notification:
        return updated_notification
    raise HTTPException(status_code=404, detail="Failed to update notification")

@router.delete("/notifications/{notification_id}", response_model=Notification)
async def delete_notification_route(notification_id: int):
    deleted_notification = await delete_notification(notification_id)
    if deleted_notification:
        return deleted_notification
    raise HTTPException(status_code=404, detail="Notification not found")
