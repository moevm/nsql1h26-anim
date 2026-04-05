from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Union, List, Optional, Literal

# TODO: На следующую итерацию продумать ограничения для каждого из полей
# UserNameString = Annotated[str, Field(min_length=2, max_length=50)]
# NameString = Annotated[str, Field(min_length=2, max_length=50)]
# PasswordString = Annotated[str, Field(min_length=2)]
# BioString = Annotated[str, Field(max_length=500)]

class UserRegisterRequest(BaseModel):
  email: EmailStr
  password: str
  username: str
  first_name: str
  last_name: str

class UserLoginRequest(BaseModel):
  username: str
  password: str

class UserUpdateRequest(BaseModel):
  email: Optional[EmailStr] = None
  username: Optional[str] = None
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  avatar_url: Optional[str] = None
  bio: Optional[str] = None

class GeneralObservation(BaseModel):
  type: Literal['general'] = 'general'

class AnimalObservation(BaseModel):
  type: Literal['animal'] = 'animal'
  taxon_name: str
  taxon_rank: str
  species: str
  habitat: str
  
class PostCreateRequest(BaseModel):
  author_id: str  # временно, потом убрать когда будет JWT
  title: str
  content: str
  image_url: Optional[str] = None
  location: Optional[str] = None
  observation: Optional[
    Union[
      AnimalObservation, 
      GeneralObservation
    ]
  ] = Field(..., discriminator='type')
  tags: List[str] = Field(default_factory=list)

class PostUpdateRequest(BaseModel):
  title: Optional[str] = None
  content: Optional[str] = None
  image_url: Optional[str] = None
  location: Optional[str] = None
  observation: Optional[
    Union[
      AnimalObservation, 
      GeneralObservation
    ]
  ] = Field(None, discriminator='type')
  tags: Optional[List[str]] = None

class CommentCreateRequest(BaseModel):
  content: str
  reply_to_id: Optional[str] = None

class CommentUpdateRequest(BaseModel):
  content: Optional[str] = None