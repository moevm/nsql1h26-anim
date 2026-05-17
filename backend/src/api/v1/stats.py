from fastapi import APIRouter, Query, Depends
from typing import Annotated
from api.deps import get_stats_service
from services.stats_service import (
    StatsService,
    POSTS_X_OPTIONS, POSTS_Y_OPTIONS,
    USERS_X_OPTIONS, USERS_Y_OPTIONS,
    COMMENTS_X_OPTIONS, COMMENTS_Y_OPTIONS,
)

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/meta")
async def get_meta():
    return {
        "posts": {
            "x_options": POSTS_X_OPTIONS,
            "y_options": POSTS_Y_OPTIONS,
            "filters": ["author", "tag", "taxon", "type"],
        },
        "users": {
            "x_options": USERS_X_OPTIONS,
            "y_options": USERS_Y_OPTIONS,
            "filters": ["first_name", "last_name", "username", "role"],
        },
        "comments": {
            "x_options": COMMENTS_X_OPTIONS,
            "y_options": COMMENTS_Y_OPTIONS,
            "filters": ["author"],
        },
    }


@router.get("/posts")
async def posts_stats(
    service: Annotated[StatsService, Depends(get_stats_service)],
    x_field: str = Query(...),
    y_field: str = Query(...),
    author: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    taxon: str | None = Query(default=None),
    type: str | None = Query(default=None),
):
    filters = {
        "author": author,
        "tag": tag,
        "taxon": taxon,
        "type": type,
    }
    return await service.get_posts_stats(x_field, y_field, filters)


@router.get("/users")
async def users_stats(
    service: Annotated[StatsService, Depends(get_stats_service)],
    x_field: str = Query(...),
    y_field: str = Query(...),
    first_name: str | None = Query(default=None),
    last_name: str | None = Query(default=None),
    username: str | None = Query(default=None),
    role: str | None = Query(default=None),
):
    filters = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "role": role,
    }
    return await service.get_users_stats(x_field, y_field, filters)


@router.get("/comments")
async def comments_stats(
    service: Annotated[StatsService, Depends(get_stats_service)],
    x_field: str = Query(...),
    y_field: str = Query(...),
    author: str | None = Query(default=None),
):
    filters = {
        "author": author,
    }
    return await service.get_comments_stats(x_field, y_field, filters)