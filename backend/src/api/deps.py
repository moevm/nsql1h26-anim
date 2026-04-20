from fastapi import status, HTTPException, Request
from services import user_service
from database.models import User
from core.utils import decode_token


async def get_current_user(request: Request) -> User:
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
  )

  token = request.cookies.get("access_token")
  if not token:
    raise credentials_exception
  
  payload = decode_token(token)
  if payload is None or payload.type != 'access':
    raise credentials_exception
  
  user = await user_service.get_user_by_id(payload.sub)
  if user is None:
    raise credentials_exception
  
  return user
