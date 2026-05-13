from repositories.comment_repository import CommentRepository
from models.comment import CommentTree
from schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from schemas.pagination import CommentPaginationParams, PaginatedResponse
from core.utils import get_now, generate_uid
from core.exceptions import NotFoundException


def build_comment_tree(comments: list[CommentTree]) -> list[CommentTree]:
    by_id = {c.id: c for c in comments}
    roots = []

    for c in comments:
        c.replies = []

    for c in comments:
        if getattr(c, "parent_id", None) and c.parent_id in by_id:
            by_id[c.parent_id].replies.append(c)
        else:
            roots.append(c)

    return roots


class CommentService:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def create_comment(self, schema: CommentCreate, author_id: str) -> CommentResponse:
        comment_props = {
            "id": generate_uid(),
            "content": schema.content,
            "created_at": get_now(),
            "updated_at": get_now(),
            "likes_count": 0,
            "is_liked": False,
            "parent_id": schema.parent_id,
        }

        raw_data = await self.repo.create_comment(
            props=comment_props,
            author_id=author_id,
            post_id=schema.target_id,
            parent_id=schema.parent_id
        )

        return CommentResponse.model_validate(raw_data)

    async def get_comment_tree(
        self,
        post_id: str,
        params: CommentPaginationParams,
        current_user_id: str | None = None,
    ) -> PaginatedResponse[CommentResponse]:

        result = await self.repo.get_comments_tree(
            post_id=post_id,
            params=params,
            current_user_id=current_user_id
        )

        tree = build_comment_tree(result.items)

        return PaginatedResponse(
            items=[CommentResponse.model_validate(c) for c in tree],
            total=result.total,
            limit=result.limit,
            offset=result.offset,
            has_more=result.has_more
        )

    async def update_comment(
        self,
        comment_id: str,
        schema: CommentUpdate,
        current_user_id: str,
    ) -> CommentResponse | None:

        props = {
            "content": schema.content,
            "updated_at": get_now()
        }

        updated_raw = await self.repo.update_comment(
            comment_id=comment_id,
            props=props,
            current_user_id=current_user_id
        )

        if not updated_raw:
            raise NotFoundException(entity="Comment")

        return CommentResponse.model_validate(updated_raw)

    async def delete_comment(self, comment_id: str, current_user_id: str) -> bool:
        return await self.repo.delete_comment_safe(comment_id, current_user_id)

    async def toggle_like(self, comment_id: str, user_id: str) -> bool:
        result = await self.repo.toggle_like(comment_id, user_id)
        if result is None:
            raise NotFoundException(entity="Comment")
        return result