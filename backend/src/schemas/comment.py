from schemas.base import BaseSchema
from schemas.identity import AuthorResponse
from datetime import datetime

class CommentCreate(BaseSchema):
    content: str
    target_id: str
    parent_id: str | None = None


class CommentUpdate(BaseSchema):
    content: str


class CommentResponse(BaseSchema):
    id: str
    content: str
    created_at: datetime
    author: AuthorResponse
    likes_count: int = 0
    is_liked: bool = False
    parent_id: str | None = None 
    replies: list["CommentResponse"] = []


CommentResponse.model_rebuild()