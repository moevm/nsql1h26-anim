from fastapi import APIRouter

from api.v1.auth import router as auth_router
from api.v1.posts import router as post_router
from api.v1.users import router as user_router
from api.v1.comments import router as comment_router
from api.v1.system import router as system_router
from api.v1.stats import router as stats_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(post_router)
api_router.include_router(comment_router)
api_router.include_router(system_router)
api_router.include_router(stats_router)