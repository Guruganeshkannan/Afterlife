from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..db.base import BaseModel

class MessageType(str, enum.Enum):
    TEXT = "text"
    VOICE = "voice"
    VIDEO = "video"

class DeliveryTrigger(str, enum.Enum):
    DATE = "date"
    BIRTHDAY = "birthday"
    ANNIVERSARY = "anniversary"
    LIFE_EVENT = "life_event"

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Relationships
    messages = relationship("Message", back_populates="sender")
    recipients = relationship("Recipient", back_populates="user")
    personality_profile = relationship("PersonalityProfile", back_populates="user", uselist=False)

class Recipient(BaseModel):
    __tablename__ = "recipients"

    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    email = Column(String)
    relationship = Column(String)
    birth_date = Column(DateTime)
    death_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="recipients")
    messages = relationship("Message", back_populates="recipient")

class Message(BaseModel):
    __tablename__ = "messages"

    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("recipients.id"))
    title = Column(String)
    content = Column(Text)
    message_type = Column(Enum(MessageType))
    media_url = Column(String, nullable=True)
    delivery_trigger = Column(Enum(DeliveryTrigger))
    trigger_date = Column(DateTime)
    is_delivered = Column(Boolean, default=False)
    delivery_date = Column(DateTime, nullable=True)
    encryption_key = Column(String)
    
    # Relationships
    sender = relationship("User", back_populates="messages")
    recipient = relationship("Recipient", back_populates="messages")

class PersonalityProfile(BaseModel):
    __tablename__ = "personality_profiles"

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    writing_style = Column(Text)
    speech_patterns = Column(Text)
    personality_traits = Column(JSON)
    training_data = Column(JSON)
    is_trained = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="personality_profile")

class LifeEvent(BaseModel):
    __tablename__ = "life_events"

    recipient_id = Column(Integer, ForeignKey("recipients.id"))
    event_type = Column(String)
    event_date = Column(DateTime)
    description = Column(Text)
    is_triggered = Column(Boolean, default=False)
    
    # Relationships
    recipient = relationship("Recipient") 