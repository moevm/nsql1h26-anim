from pydantic import field_validator
from .base import BaseSchema, PostType, TaxonRank

class LoginRequest(BaseSchema):
  identifier: str
  password: str

class RegisterRequest(BaseSchema):
  username: str
  email: str
  password: str
  first_name: str
  last_name: str

class UserUpdate(BaseSchema):
  email: str | None = None
  username: str | None = None
  first_name: str | None = None
  last_name: str | None = None
  avatar_url: str | None = None
  avatar_background_color: str | None = None
  bio: str | None = None

class TaxonCreate(BaseSchema):
  name: str
  rank: TaxonRank
  parent_name: str | None = None

class AnimalCreate(BaseSchema):
  name: str
  scientific_name: str

class CommentCreate(BaseSchema):
  content: str
  parent_comment_id: str | None = None

class PostCreate(BaseSchema):
  title: str
  content: str
  image_url: str | None = None
  location: str | None = None
  type: PostType
  animal: AnimalCreate | None = None
  taxon: TaxonCreate | None = None
  tags: list[str] = []

  @field_validator("tags", mode="before")
  @classmethod
  def lowercase_tags(cls, v: list[str]) -> list[str]:
    return [tag.lower() for tag in v]

class PostUpdate(BaseSchema):
  title: str | None = None
  content: str | None = None
  image_url: str | None = None
  location: str | None = None
  type: PostType | None = None
  animal: AnimalCreate | None = None
  taxon: TaxonCreate | None = None
  tags: list | None = None