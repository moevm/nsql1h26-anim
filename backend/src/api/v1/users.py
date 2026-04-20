from fastapi import APIRouter, Depends
from api.deps import get_current_user
from services import user_service
from schemas.response import UserResponse
from database.models import User

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_users_me(current_user: User = Depends (get_current_user)):
  return current_user