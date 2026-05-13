from models.base import BaseNode
from models.user import User

class Comment(BaseNode):
    content: str
    author: User
    likes_count: int = 0
    is_liked: bool = False
    parent_id: str | None = None

class CommentTree(Comment):
    replies: list["CommentTree"] = []

CommentTree.model_rebuild()