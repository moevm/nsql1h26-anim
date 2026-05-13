from pydantic import Field
from models.base import BaseNode
from models.user import User
from models.animal import Animal
from models.comment import CommentTree

from enum import Enum

class PostType(str, Enum):
    NOTE = "note"
    ANIMAL = "animal"

class PostBase(BaseNode):
    title: str
    content: str
    image_url: str | None = None
    location: str | None = None
    type: PostType
    author: User | None = None
    animal: Animal | None = None
    likes_count: int = 0
    is_liked: bool = False
    tags: list[str] = Field(default_factory=list)
    comments: list[CommentTree] = Field(default_factory=list)
    comments_count: int = 0