from typing import Annotated
from fastapi import Depends, Request, Cookie

from database.db import db
from core.security import decode_token
from core.exceptions import AppException, NotFoundException, ErrorCode

from repositories.user_repository import UserRepository
from repositories.post_repository import PostRepository
from repositories.comment_repository import CommentRepository
from repositories.tag_repository import TagRepository
from repositories.animal_repository import AnimalRepository

from services.auth_service import AuthService
from services.user_service import UserService
from services.post_service import PostService
from services.comment_service import CommentService

from models.user import User


def get_user_repo() -> UserRepository:
    return UserRepository(db)

def get_post_repo() -> PostRepository:
    return PostRepository(db)

def get_comment_repo() -> CommentRepository:
    return CommentRepository(db)

def get_tag_repo() -> TagRepository:
    return TagRepository(db)

def get_animal_repo() -> AnimalRepository:
    return AnimalRepository(db)


def get_auth_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)]
) -> AuthService:
    return AuthService(repo)


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)]
) -> UserService:
    return UserService(repo)


def get_post_service(
    repo: Annotated[PostRepository, Depends(get_post_repo)]
) -> PostService:
    return PostService(repo)


def get_comment_service(
    repo: Annotated[CommentRepository, Depends(get_comment_repo)]
) -> CommentService:
    return CommentService(repo)


async def get_current_user(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
    access_token: Annotated[str | None, Cookie()] = None
) -> User:
    if not access_token:
        raise AppException(
            detail="Not authenticated", 
            code="not_authenticated", 
            status=401
        )

    payload = decode_token(access_token)
    if not payload or payload.type != "access":
        raise AppException(
            detail="Invalid or expired token", 
            code=ErrorCode.UNAUTHORIZED, 
            status=401
        )

    user = await repo.get_by_id(payload.sub)
    if not user:
        raise NotFoundException(entity="User")

    return user


async def get_current_user_id(
    user: Annotated[User, Depends(get_current_user)]
) -> str:
    return user.id