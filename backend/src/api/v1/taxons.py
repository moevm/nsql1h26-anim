from fastapi import APIRouter
from schemas.response import PostResponse
from schemas.request import PostCreate
from database.models import User
from services import post_service
from api.deps import get_current_user

router = APIRouter(prefix="/taxons", tags=["Taxons"])

@router.post("/", response_model=PostResponse)
async def create_post(data: PostCreate, current_user: User = (get_current_user)):
  return post_service.create_post(data, author_id=current_user.id)