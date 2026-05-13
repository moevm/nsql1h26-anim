from fastapi import APIRouter, Depends, Response, Cookie, status
from typing import Annotated

from schemas.identity import RegisterRequest, LoginRequest, UserResponse
from services.auth_service import AuthService
from api.deps import get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest, 
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    return await service.register(data, response)

@router.post("/login", response_model=UserResponse)
async def login(
    data: LoginRequest, 
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    return await service.login(data, response)

@router.post("/logout")
async def logout(
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    return await service.logout(response)

@router.post("/refresh", response_model=UserResponse)
async def refresh(
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)],
    refresh_token: str | None = Cookie()
):
    return await service.refresh(refresh_token, response)