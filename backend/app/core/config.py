from typing import Any, Dict, Optional
from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AfterLife Message Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./afterlife.db"

    # Scheduler Configuration
    SCHEDULER_ENABLED: bool = True  # Enabled by default
    
    # Notification Configuration
    SEND_NOTIFICATION_EMAILS: bool = False  # Disabled by default

    # Email Configuration
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int = 465
    MAIL_SERVER: str
    MAIL_FROM_NAME: str = "AfterLife Message Platform"
    MAIL_TLS: bool = False
    MAIL_SSL: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = False  # Changed to False to avoid SSL verification issues

    # AWS Settings
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "afterlife-messages"
    
    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"  # This allows extra fields in the settings

settings = Settings() 