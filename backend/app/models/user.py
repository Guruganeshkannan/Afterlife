from typing import Optional, List
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "user"
    
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Personality profile fields
    personality_data: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    writing_samples: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    voice_samples: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Relationships
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="user") 