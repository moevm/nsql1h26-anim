from fastapi import APIRouter, Response, Request
from services import auth_service
from schemas.response import UserResponse
from schemas.request import RegisterRequest, LoginRequest

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_route(data: RegisterRequest, response: Response):
  return await auth_service.register(data, response)

@router.post("/login", response_model=UserResponse)
async def login_route(data: LoginRequest, response: Response):
  return await auth_service.login(data, response)

@router.post("/logout")
async def logout_route(response: Response):
  return await auth_service.logout(response)

@router.post("/refresh", response_model=UserResponse)
async def refresh_route(request: Request, response: Response):
  refresh_token = request.cookies.get("refresh_token")
  return await auth_service.refresh(refresh_token, response)