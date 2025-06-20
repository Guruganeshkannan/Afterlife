from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.core.security import get_password_hash

def init_db(db: Session) -> None:
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create first superuser if it doesn't exist
    user = db.query(User).filter(User.email == "admin@afterlife.com").first()
    if not user:
        user = User(
            email="admin@afterlife.com",
            hashed_password=get_password_hash("admin"),
            full_name="Admin User",
            is_superuser=True,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user) 