from schemas.base import BaseSchema
from schemas.identity import AuthorResponse
from schemas.animal import AnimalResponse, AnimalCreate, AnimalUpdate
from schemas.comment import CommentResponse
from models.post import PostType
from datetime import datetime

class PostCreate(BaseSchema):
    title: str
    content: str
    type: PostType
    image_url: str | None = None
    location: str | None = None
    tags: list[str] = []
    animal: AnimalCreate | None = None


class PostUpdate(BaseSchema):
    title: str | None = None
    content: str | None = None
    image_url: str | None = None
    location: str | None = None
    tags: list[str] | None = None
    animal: AnimalUpdate | None = None
    type: PostType | None = None


class PostResponse(BaseSchema):
    id: str
    title: str
    content: str
    image_url: str | None = None
    location: str | None = None
    type: PostType
    author: AuthorResponse
    animal: AnimalResponse | None = None
    likes_count: int = 0
    is_liked: bool = False
    tags: list[str] = []
    comments_count: int = 0
    created_at: datetime

class PostDetailResponse(PostResponse):
    comments: list[CommentResponse] = []