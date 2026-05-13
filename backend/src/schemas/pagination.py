from core.constants import PaginationConst, PostConst, CommentCost, AnimalConst, UserConst
from schemas.base import BaseSchema
from typing import ClassVar
from datetime import date
from pydantic import Field, model_validator

class PaginationParams(BaseSchema):
    limit: int = PaginationConst.DEFAULT_LIMIT
    offset: int = 0

    MAX_LIMIT: ClassVar[int] = PaginationConst.MAX_LIMIT

    @model_validator(mode='after')
    def check_pagination_bounds(self) -> 'PaginationParams':
        self.limit = max(1, min(self.limit, self.MAX_LIMIT))
        self.offset = max(0, self.offset)        
        return self


class PaginatedResponse[T](BaseSchema):
    items: list[T]
    total: int
    limit: int
    offset: int
    has_more: bool


class PostPaginationParams(PaginationParams):
    limit: int = PostConst.DEFAULT_LIMIT
    MAX_LIMIT: ClassVar[int] = PostConst.MAX_LIMIT
    search: str | None = None       
    type: str | None = None          
    tag: str | None = None          
    author: str | None = None
    taxon: str | None = None
    scientific_name: str | None = None       
    date_from: date | None = Field(None, alias="dateFrom")
    date_to: date | None = Field(None, alias="dateTo")
    only_followed: bool = Field(False, alias="onlyFollowed")   
    sort: str = 'newest' 


class CommentPaginationParams(PaginationParams):
    limit: int = CommentCost.DEFAULT_LIMIT
    MAX_LIMIT: ClassVar[int] = CommentCost.MAX_LIMIT


class AnimalPaginationParams(PaginationParams):
    limit: int = AnimalConst.DEFAULT_LIMIT
    MAX_LIMIT: ClassVar[int] = AnimalConst.MAX_LIMIT


class UserPaginationParams(PaginationParams):
    limit: int = UserConst.DEFAULT_LIMIT
    MAX_LIMIT: ClassVar[int] = UserConst.MAX_LIMIT
    search: str | None = None