from .base import BaseSchema, PostType, TaxonRank

class UserResponse(BaseSchema):
  id: str
  username: str
  email: str
  first_name: str
  last_name: str
  role: str
  bio: str | None = None
  avatar_url: str | None = None
  avatar_background_color: str | None = None
  created_at: str | None = None

class TaxonResponse(BaseSchema):
  name: str
  rank: TaxonRank

class AnimalResponse(BaseSchema):
  name: str
  scientific_name: str

class AuthorResponse(BaseSchema):
  id: str
  first_name: str
  last_name: str
  username: str
  avatar_url: str | None = None
  avatar_background_color: str | None = None

class CommentResponse(BaseSchema):
  id: str
  content: str
  created_at: str
  author: AuthorResponse
  likes_count: int = 0
  is_liked: bool = False
  parent_id: str | None = None

class PostResponse(BaseSchema):
  id: str
  title: str
  content: str
  image_url: str | None = None
  location: str | None = None
  type: PostType
  author: AuthorResponse
  animal: AnimalResponse | None = None
  taxonomy_chain: list[TaxonResponse] = []
  tags: list[str] = []