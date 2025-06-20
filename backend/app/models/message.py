from typing import Optional
from datetime import datetime
from sqlalchemy import Boolean, String, ForeignKey, DateTime, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Message(Base):
    __tablename__ = "message"
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    media_urls: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Delivery settings
    delivery_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_delivered: Mapped[bool] = mapped_column(Boolean, default=False)
    delivery_method: Mapped[str] = mapped_column(String)
    recipient_email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    recipient_phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # AI generation settings
    personality_profile: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    generation_settings: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Relationships
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="messages") 