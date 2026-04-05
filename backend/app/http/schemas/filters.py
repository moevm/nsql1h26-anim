from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Union, List, Optional, Literal
from datetime import datetime

class BasePostFilters(BaseModel):
  search_query: Optional[str] = None 
  author_username: Optional[str] = None
  tag: Optional[str] = None
  start_date: Optional[datetime] = None
  end_date: Optional[datetime] = None

class AnimalFilter(BasePostFilters):
  taxon_name: Optional[str] = None
  habitat: Optional[str] = None