from schemas.base import BaseSchema
from datetime import datetime

class AuthorResponse(BaseSchema):
    id: str
    first_name: str | None = None
    last_name: str | None = None
    username: str
    avatar_url: str | None = None
    avatar_background_color: str | None = None
    is_followed: bool = False


class UserResponse(AuthorResponse):
    id: str
    first_name: str
    last_name: str
    created_at: datetime
    bio: str | None = None
    role: str = "user"
    is_followed: bool = False
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    likes_count: int = 0
    comments_count: int = 0
    

class RegisterRequest(BaseSchema):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


class LoginRequest(BaseSchema):
    identifier: str
    password: str


class UserUpdate(BaseSchema):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    avatar_background_color: str | None = None


class ChangePasswordRequest(BaseSchema):
    old_password: str
    new_password: str