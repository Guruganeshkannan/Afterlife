from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
import uvicorn
import asyncio
import logging
from app.api.v1.endpoints import login, users, messages, test
from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import engine
from app.db.base import Base
from app.api.v1.api import api_router
from app.services.scheduler import start_scheduler, check_and_deliver_messages

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AfterLife Message Platform",
    description="A secure platform for creating and delivering messages to loved ones after passing away",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(login.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
app.include_router(test.router, prefix="/api/test", tags=["Test"])
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to AfterLife Message Platform API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.on_event("startup")
async def startup_event():
    """
    Start the message scheduler when the application starts if enabled
    """
    if settings.SCHEDULER_ENABLED:
        logger.info("Starting message scheduler...")
        # Create a task to run the scheduler
        asyncio.create_task(start_scheduler())
        # Also check for messages immediately on startup
        asyncio.create_task(check_and_deliver_messages())
        logger.info("Message scheduler started successfully")
    else:
        logger.info("Message scheduler is disabled")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 