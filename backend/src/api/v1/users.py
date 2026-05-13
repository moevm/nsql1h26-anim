from fastapi import APIRouter, Depends, status, Response
from typing import Annotated

from schemas.identity import UserResponse, UserUpdate
from schemas.pagination import UserPaginationParams, PaginatedResponse
from services.user_service import UserService
from models.user import User
from api.deps import get_user_service, get_current_user, get_current_user_id

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.patch("/me", response_model=UserResponse)
async def update_me(
    data: UserUpdate, 
    user_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[UserService, Depends(get_user_service)]
):
    return await service.update_profile(user_id, data)

@router.get("/", response_model=PaginatedResponse[UserResponse])
async def list_users(
    params: Annotated[UserPaginationParams, Depends()],
    service: Annotated[UserService, Depends(get_user_service)],
    user_id: Annotated[str, Depends(get_current_user_id)]
):
    return await service.list_users(params, user_id)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_profile(
    user_id: str, 
    service: Annotated[UserService, Depends(get_user_service)],
    current_id: Annotated[str | None, Depends(get_current_user_id)]
):
    return await service.get_user(user_id, current_id)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str, 
    current_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[UserService, Depends(get_user_service)]
):
    await service.remove_account(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/{user_id}/follow")
async def follow(
    user_id: str, 
    current_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[UserService, Depends(get_user_service)]
):
    success = await service.follow_user(current_id, user_id)
    return {"detail": "Follow relation toggled", "status": success}

@router.get("/{user_id}/followers", response_model=PaginatedResponse[UserResponse])
async def get_followers(
    user_id: str,
    service: Annotated[UserService, Depends(get_user_service)],
    current_id: Annotated[str | None, Depends(get_current_user_id)]
):
    return await service.get_followers(user_id, current_id)

@router.get("/{user_id}/following", response_model=PaginatedResponse[UserResponse])
async def get_following(
    user_id: str,
    service: Annotated[UserService, Depends(get_user_service)],
    current_id: Annotated[str | None, Depends(get_current_user_id)]
):
    return await service.get_following(user_id, current_id)