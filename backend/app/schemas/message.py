from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr
from app.schemas.base import BaseSchema

class MessageBase(BaseModel):
    title: str
    content: str
    media_urls: Optional[List[str]] = None
    delivery_date: datetime
    delivery_method: str
    recipient_email: Optional[EmailStr] = None
    recipient_phone: Optional[str] = None
    personality_profile: Optional[Dict] = None
    generation_settings: Optional[Dict] = None

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    media_urls: Optional[List[str]] = None
    delivery_date: Optional[datetime] = None
    delivery_method: Optional[str] = None
    recipient_email: Optional[EmailStr] = None
    recipient_phone: Optional[str] = None
    personality_profile: Optional[Dict] = None
    generation_settings: Optional[Dict] = None
    is_delivered: Optional[bool] = None

class MessageInDBBase(MessageBase, BaseSchema):
    id: Optional[int] = None
    user_id: int
    is_delivered: bool = False

    class Config:
        orm_mode = True

class Message(MessageInDBBase):
    pass

class MessageInDB(MessageInDBBase):
    pass 