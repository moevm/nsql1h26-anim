import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from core.config import settings
from schemas.token import TokenPayload

ph = PasswordHasher()

def get_now_iso() -> str:
  return datetime.now(timezone.utc).isoformat()

def generate_uid() -> str:
  return str(uuid4())

def hash_password(value: str) -> str:
  return ph.hash(value)

def verify_password(plain_value: str, hashed_value: str) -> bool:
  try:
    return ph.verify(hashed_value, plain_value)
  except VerifyMismatchError:
    return False
  
def create_token(id: str, expires_delta: timedelta, token_type: str = "access") -> str:
  now = datetime.now(timezone.utc)
  expires = now + expires_delta
  payload = TokenPayload(
    sub=id,
    type=token_type,
    iat=int(now.timestamp()),
    exp=int(expires.timestamp())
  )
  return jwt.encode(
    payload=payload.model_dump(),
    key=settings.jwt_secret,
    algorithm=settings.jwt_algorithm
  )

def decode_token(token: str) -> TokenPayload | None:
  try:
    payload_dict = jwt.decode(
      token,
      settings.jwt_secret,
      algorithms=[settings.jwt_algorithm]
    )
    return TokenPayload(**payload_dict)
  except ExpiredSignatureError:
    return None
  except InvalidTokenError:
    return None