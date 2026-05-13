# routers/posts.py
from fastapi import APIRouter, Depends, status
from typing import Annotated

from schemas.post import PostCreate, PostUpdate, PostResponse, PostDetailResponse
from schemas.pagination import PostPaginationParams, PaginatedResponse
from services.post_service import PostService
from api.deps import get_post_service, get_current_user_id

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    schema: PostCreate,
    service: Annotated[PostService, Depends(get_post_service)],
    user_id: Annotated[str, Depends(get_current_user_id)]
):
    return await service.create_post(schema, user_id)

@router.get("", response_model=PaginatedResponse[PostResponse])
async def get_feed(
    params: Annotated[PostPaginationParams, Depends()],
    service: Annotated[PostService, Depends(get_post_service)],
    user_id: Annotated[str | None, Depends(get_current_user_id)]
):
    return await service.get_feed(params, user_id)

@router.get("/{post_id}", response_model=PostDetailResponse)
async def get_post_detail(
    post_id: str,
    service: Annotated[PostService, Depends(get_post_service)],
    user_id: Annotated[str | None, Depends(get_current_user_id)]
):
    return await service.get_post(post_id, user_id)

@router.patch("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    schema: PostUpdate,
    service: Annotated[PostService, Depends(get_post_service)],
    user_id: Annotated[str, Depends(get_current_user_id)]
):
    return await service.update_post(post_id, schema, user_id)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    service: Annotated[PostService, Depends(get_post_service)],
    user_id: Annotated[str, Depends(get_current_user_id)]
):
    await service.delete_post(post_id, user_id)

@router.post("/{post_id}/like")
async def toggle_post_like(
    post_id: str,
    service: Annotated[PostService, Depends(get_post_service)],
    user_id: Annotated[str, Depends(get_current_user_id)]
):
    liked = await service.toggle_like(post_id, user_id)
    return {"liked": liked}