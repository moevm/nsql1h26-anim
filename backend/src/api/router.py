from fastapi import APIRouter
from api.v1.auth import router as auth_router
from api.v1.users import router as user_router
from api.v1.posts import router as post_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(post_router, prefix="/posts", tags=["Posts"])