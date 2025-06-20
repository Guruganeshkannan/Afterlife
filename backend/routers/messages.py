from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Any
from datetime import datetime
from ..core import security
from ..db.session import get_db
from ..models import models
from ..schemas import message as message_schemas
from ..routers.auth import get_current_user
from ..services import storage_service, ai_service

router = APIRouter()

@router.post("/create", response_model=message_schemas.Message)
def create_message(
    message: message_schemas.MessageCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Create a new message
    """
    # Verify recipient exists and belongs to user
    recipient = db.query(models.Recipient).filter(
        models.Recipient.id == message.recipient_id,
        models.Recipient.user_id == current_user.id
    ).first()
    
    if not recipient:
        raise HTTPException(
            status_code=404,
            detail="Recipient not found"
        )
    
    # Generate encryption key
    encryption_key = security.generate_encryption_key()
    
    # Create message
    db_message = models.Message(
        sender_id=current_user.id,
        recipient_id=message.recipient_id,
        title=message.title,
        content=message.content,
        message_type=message.message_type,
        delivery_trigger=message.delivery_trigger,
        trigger_date=message.trigger_date,
        encryption_key=encryption_key
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.post("/upload-media/{message_id}")
async def upload_media(
    message_id: int,
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Upload media for a message
    """
    message = db.query(models.Message).filter(
        models.Message.id == message_id,
        models.Message.sender_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )
    
    # Upload to S3
    media_url = await storage_service.upload_file(file, f"messages/{message_id}")
    
    # Update message with media URL
    message.media_url = media_url
    db.commit()
    
    return {"media_url": media_url}

@router.get("/list", response_model=List[message_schemas.Message])
def list_messages(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    List all messages for the current user
    """
    messages = db.query(models.Message).filter(
        models.Message.sender_id == current_user.id
    ).all()
    return messages

@router.get("/{message_id}", response_model=message_schemas.Message)
def get_message(
    message_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get a specific message
    """
    message = db.query(models.Message).filter(
        models.Message.id == message_id,
        models.Message.sender_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )
    
    return message

@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Delete a message
    """
    message = db.query(models.Message).filter(
        models.Message.id == message_id,
        models.Message.sender_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )
    
    db.delete(message)
    db.commit()
    return {"status": "success"}

@router.post("/{message_id}/deliver")
async def deliver_message(
    message_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Manually trigger message delivery
    """
    message = db.query(models.Message).filter(
        models.Message.id == message_id,
        models.Message.sender_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )
    
    if message.is_delivered:
        raise HTTPException(
            status_code=400,
            detail="Message already delivered"
        )
    
    # Decrypt message
    decrypted_content = security.decrypt_message(message.content, message.encryption_key)
    
    # Send message to recipient
    await ai_service.deliver_message(message, decrypted_content)
    
    # Update message status
    message.is_delivered = True
    message.delivery_date = datetime.utcnow()
    db.commit()
    
    return {"status": "success"} 