from pydantic import BaseModel
from schemas.base import TaxonRank, PostType

class User(BaseModel):
  id: str
  username: str
  email: str
  password: str
  first_name: str
  last_name: str
  bio: str | None = None
  avatar_url: str | None = None
  avatar_background_color: str | None = None
  role: str = 'user'
  created_at: str
  updated_at: str

class Taxon(BaseModel):
  id: str
  name: str
  rank: TaxonRank

class Animal(BaseModel):
  id: str
  name: str
  scientific_name: str
  created_at: str
  updated_at: str

class Tag(BaseModel):
  id: str
  name: str

class Comment(BaseModel):
  id: str
  content: str
  created_at: str
  updated_at: str
  parent_id: str | None = None

class CommentFull(Comment):
  author: User
  likes_count: int = 0
  is_liked: bool = False

class Post(BaseModel):
  id: str
  title: str
  content: str
  image_url: str | None = None
  location: str | None = None
  updated_at: str
  created_at: str 
  type: PostType

class PostFull(Post):
  author: User
  animal: Animal | None = None
  taxonomy_chain: list[Taxon] = []
  tags: list[str] = []
  comments: list[CommentFull] = []
  likes_count: int = 0
  is_liked: bool = False 