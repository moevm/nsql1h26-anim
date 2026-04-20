from fastapi import APIRouter, Depends, HTTPException
from schemas.response import PostResponse
from schemas.request import PostCreate, PostUpdate
from database.models import User
from services import post_service
from api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=PostResponse)
async def create_post(data: PostCreate, current_user: User = Depends(get_current_user)):
  try:
    return await post_service.create_post(data, author_id=current_user.id)
  except Exception as e:
    print(e)
    raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[PostResponse])
async def get_posts():
  return await post_service.get_all()

@router.post("/{post_id}/toggle-like")
async def toggle_post_like(
    post_id: str, 
    current_user: User = Depends(get_current_user)
):
  liked = await post_service.toggle_like(post_id=post_id, user_id=current_user.id)
  return {"is_liked": liked}