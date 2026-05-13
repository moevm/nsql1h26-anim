from models.base import BaseNode

class User(BaseNode):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    bio: str | None = None
    avatar_url: str | None = None
    avatar_background_color: str | None = None
    role: str = "user"
    is_followed: bool = False
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0      
    likes_count: int = 0     
    comments_count: int = 0 