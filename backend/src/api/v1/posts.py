from fastapi import APIRouter, Depends, HTTPException, status
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

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str):
  was_deleted = await post_service.delete_post(post_id)
    
  if not was_deleted:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Пост с ID {post_id} не найден"
    )
    
  return None