from fastapi import APIRouter
from app.api.v1.endpoints import login, users, messages, test

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(test.router, prefix="/test", tags=["test"]) 