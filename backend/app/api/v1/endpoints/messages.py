from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.schemas.message import Message, MessageCreate, MessageUpdate
from app.models.message import Message as MessageModel
from app.models.user import User as UserModel
from app.core.tasks import send_message_scheduled_notification_background
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=List[Message])
def read_messages(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve messages.
    """
    messages = (
        db.query(MessageModel)
        .filter(MessageModel.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return messages

@router.post("/", response_model=Message)
async def create_message(
    *,
    db: Session = Depends(deps.get_db),
    message_in: MessageCreate,
    background_tasks: BackgroundTasks,
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new message.
    """
    message = MessageModel(
        **message_in.dict(),
        user_id=current_user.id
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # Send a notification that the message has been scheduled
    if settings.SEND_NOTIFICATION_EMAILS and message.recipient_email:
        await send_message_scheduled_notification_background(
            background_tasks=background_tasks,
            recipient_email=message.recipient_email,
            message_title=message.title,
            delivery_date=message.delivery_date.strftime('%Y-%m-%d %H:%M:%S')
        )
    
    return message

@router.put("/{message_id}", response_model=Message)
async def update_message(
    *,
    db: Session = Depends(deps.get_db),
    message_id: int,
    message_in: MessageUpdate,
    background_tasks: BackgroundTasks,
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a message.
    """
    message = (
        db.query(MessageModel)
        .filter(
            MessageModel.id == message_id,
            MessageModel.user_id == current_user.id
        )
        .first()
    )
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Store the old delivery date to check if it changed
    old_delivery_date = message.delivery_date
    
    # Update the message
    for field, value in message_in.dict(exclude_unset=True).items():
        setattr(message, field, value)
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # If the delivery date changed and there's a recipient email, send a notification
    if (settings.SEND_NOTIFICATION_EMAILS and 
        message.recipient_email and 
        (old_delivery_date != message.delivery_date or 
         not hasattr(message, 'delivery_date_changed_notification_sent') or 
         not message.delivery_date_changed_notification_sent)):
        
        await send_message_scheduled_notification_background(
            background_tasks=background_tasks,
            recipient_email=message.recipient_email,
            message_title=message.title,
            delivery_date=message.delivery_date.strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # Mark that we've sent the notification
        message.delivery_date_changed_notification_sent = True
        db.add(message)
        db.commit()
    
    return message

@router.get("/{message_id}", response_model=Message)
def read_message(
    *,
    db: Session = Depends(deps.get_db),
    message_id: int,
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get message by ID.
    """
    message = (
        db.query(MessageModel)
        .filter(
            MessageModel.id == message_id,
            MessageModel.user_id == current_user.id
        )
        .first()
    )
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.delete("/{message_id}")
def delete_message(
    *,
    db: Session = Depends(deps.get_db),
    message_id: int,
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a message.
    """
    message = (
        db.query(MessageModel)
        .filter(
            MessageModel.id == message_id,
            MessageModel.user_id == current_user.id
        )
        .first()
    )
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    db.delete(message)
    db.commit()
    return {"status": "success"} 