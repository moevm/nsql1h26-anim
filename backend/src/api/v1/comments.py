from fastapi import APIRouter, Depends, status
from typing import Annotated

from schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from schemas.pagination import CommentPaginationParams, PaginatedResponse
from services.comment_service import CommentService
from api.deps import get_comment_service, get_current_user_id

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    schema: CommentCreate,
    service: Annotated[CommentService, Depends(get_comment_service)],
    user_id: Annotated[str, Depends(get_current_user_id)]
):
    return await service.create_comment(schema, user_id)

@router.get("/post/{post_id}", response_model=PaginatedResponse[CommentResponse])
async def get_post_comments(
    post_id: str,
    params: Annotated[CommentPaginationParams, Depends()],
    service: Annotated[CommentService, Depends(get_comment_service)],
    user_id: Annotated[str | None, Depends(get_current_user_id)]
):
    return await service.get_comment_tree(post_id, params, user_id)

@router.patch("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: str,
    schema: CommentUpdate,
    service: Annotated[CommentService, Depends(get_comment_service)],
    user_id: Annotated[str, Depends(get_current_user_id)]
):
    return await service.update_comment(comment_id, schema, user_id)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: str,
    service: Annotated[CommentService, Depends(get_comment_service)],
    user_id: Annotated[str, Depends(get_current_user_id)]
):
    await service.delete_comment(comment_id, user_id)

@router.post("/{comment_id}/like")
async def toggle_comment_like(
    comment_id: str,
    service: Annotated[CommentService, Depends(get_comment_service)],
    user_id: Annotated[str, Depends(get_current_user_id)]
):
    liked = await service.toggle_like(comment_id, user_id)
    return {"liked": liked}