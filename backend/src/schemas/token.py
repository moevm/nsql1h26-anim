from .base import BaseSchema

class TokenPayload(BaseSchema):
  sub: str
  type: str
  iat: int
  exp: int