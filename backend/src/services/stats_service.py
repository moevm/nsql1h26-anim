from repositories.stats_repository import StatsRepository
from core.exceptions import AppException

POSTS_X_OPTIONS = ["type", "tag", "taxon", "author", "date"]
POSTS_Y_OPTIONS = ["likes_count", "comments_count", "count"]

USERS_X_OPTIONS = ["role", "username", "first_name", "last_name", "date"]
USERS_Y_OPTIONS = ["followers_count", "following_count", "posts_count", "likes_count", "comments_count", "count"]

COMMENTS_X_OPTIONS = ["author", "date"]
COMMENTS_Y_OPTIONS = ["likes_count", "count"]


def _validate_fields(x_field: str, y_field: str, x_options: list, y_options: list):
    if x_field not in x_options:
        raise AppException(
            detail=f"Недопустимое поле X: {x_field}. Допустимые: {x_options}",
            code="invalid_x_field",
            status=400,
        )
    if y_field not in y_options:
        raise AppException(
            detail=f"Недопустимое поле Y: {y_field}. Допустимые: {y_options}",
            code="invalid_y_field",
            status=400,
        )


class StatsService:
    def __init__(self, repo: StatsRepository):
        self.repo = repo

    async def get_posts_stats(self, x_field: str, y_field: str, filters: dict) -> dict:
        _validate_fields(x_field, y_field, POSTS_X_OPTIONS, POSTS_Y_OPTIONS)
        
        cleaned_filters = {k: v for k, v in filters.items() if v is not None and v != ""}
        rows = await self.repo.get_posts_stats(x_field, y_field, cleaned_filters)
        return self._build_response(rows, x_field, y_field, entity="posts")

    async def get_users_stats(self, x_field: str, y_field: str, filters: dict) -> dict:
        _validate_fields(x_field, y_field, USERS_X_OPTIONS, USERS_Y_OPTIONS)
        cleaned_filters = {k: v for k, v in filters.items() if v is not None and v != ""}
        rows = await self.repo.get_users_stats(x_field, y_field, cleaned_filters)
        return self._build_response(rows, x_field, y_field, entity="users")

    async def get_comments_stats(self, x_field: str, y_field: str, filters: dict) -> dict:
        _validate_fields(x_field, y_field, COMMENTS_X_OPTIONS, COMMENTS_Y_OPTIONS)
        cleaned_filters = {k: v for k, v in filters.items() if v is not None and v != ""}
        rows = await self.repo.get_comments_stats(x_field, y_field, cleaned_filters)
        return self._build_response(rows, x_field, y_field, entity="comments")
    
    def _build_response(self, rows: list[dict], x_field: str, y_field: str, entity: str) -> dict:
        return {
            "entity": entity,
            "x_field": x_field,
            "y_field": y_field,
            "rows": rows,
        }