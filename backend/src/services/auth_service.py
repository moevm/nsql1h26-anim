from fastapi import HTTPException, status, Response
from datetime import timedelta
from services import user_service
from database.models import User
from schemas.request import RegisterRequest, LoginRequest
from core.utils import create_token, decode_token, verify_password
from core.config import settings

async def _generate_auth_response(user: User, response: Response):
  access_token = create_token(
    id=user.id,
    expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    token_type="access"
  )  
  
  refresh_token = create_token(
    id=user.id,
    expires_delta= timedelta(days=settings.refresh_token_expire_days),
    token_type="refresh"
  )

  response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    httponly=True,
    path="/api/v1/auth",
    secure=True,
    samesite="lax",
    max_age=settings.refresh_token_expire_days * 24 * 3600
  )

  response.set_cookie(
    key="access_token",
    value=access_token,
    httponly=True,
    path="/",
    secure=True,
    samesite="lax",
    max_age=settings.access_token_expire_minutes * 60
  )

  return user

async def register(data: RegisterRequest, response: Response):
  if (await user_service.get_user_by_identifier(data.email)):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="User with the email is already existed"
    )
  
  if await user_service.get_user_by_identifier(data.username):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="This username is already taken"
    )

  user = await user_service.create_user(data)

  return await _generate_auth_response(user, response)

async def login(data: LoginRequest, response: Response):
  identifier = data.identifier
  password = data.password

  user = await user_service.get_user_by_identifier(identifier)

  if not user or not verify_password(password, user.password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid login or password"
    )

  return await _generate_auth_response(user, response)

async def logout(response: Response):
  response.delete_cookie(
    key="refresh_token",
    httponly=True,
    path="/api/v1/auth",
    samesite="lax",
    secure=True
  )
  
  response.delete_cookie(
    key="access_token",
    httponly=True,
    path="/",
    samesite="lax",
    secure=True
  )

  return {"detail": "Successfully logged out"}

async def refresh(refresh_token: str | None, response: Response):
  if not refresh_token:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Refresh token missing"
    )
  
  payload = decode_token(refresh_token)

  if not payload or payload.type != 'refresh':
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Invalid credentials"
    )
  
  user = await user_service.get_user_by_id(payload.sub)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail="User not found"
    )

  return await _generate_auth_response(user, response)