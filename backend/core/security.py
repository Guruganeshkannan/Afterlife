from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_encryption_key() -> str:
    """Generate a secure encryption key for message encryption"""
    return pwd_context.hash(str(datetime.utcnow().timestamp()))

def encrypt_message(message: str, key: str) -> str:
    """Encrypt a message using the provided key"""
    # Implementation of message encryption
    # This is a placeholder - implement proper encryption in production
    return message

def decrypt_message(encrypted_message: str, key: str) -> str:
    """Decrypt a message using the provided key"""
    # Implementation of message decryption
    # This is a placeholder - implement proper decryption in production
    return encrypted_message 