from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import jwt
from argon2 import PasswordHasher
from core.config import settings

ph = PasswordHasher()

class TokenPayload(BaseModel):
    sub: str
    type: str
    iat: int
    exp: int


def hash_password(value: str) -> str:
    return ph.hash(value)

def verify_password(plain_value: str, hashed_value: str) -> bool:
    try:
        return ph.verify(hashed_value, plain_value)
    except Exception:
        return False

def create_token(user_id: str, expires_delta: timedelta, token_type: str = "access") -> str:
    now = datetime.now(timezone.utc)
    expires = now + expires_delta
    payload = TokenPayload(
        sub=user_id, 
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
        payload_dict = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return TokenPayload(**payload_dict)
    except Exception:
        return None