from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Union, List, Optional, Literal
from datetime import datetime
from .request import AnimalObservation, GeneralObservation

class UserResponse(BaseModel):
  id: str 
  username: str
  email: EmailStr
  first_name: str
  last_name: str
  avatar_url: Optional[str] = None
  bio: Optional[str] = None
  created_at: datetime

class AuthorResponse(BaseModel):
  id: str
  username: str
  first_name: str
  last_name: str
  avatar_url: Optional[str] = None

class PostResponse(BaseModel):
  id: str
  title: str
  content: str
  author: AuthorResponse
  observation: Union[AnimalObservation, GeneralObservation]
  tags: List[str]
  created_at: datetime

class CommentResponse(BaseModel):
  id: str
  content: str
  author: AuthorResponse
  reply_to_id: Optional[str] = None

