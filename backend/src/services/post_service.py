from repositories.post_repository import PostRepository
from models.post import PostType
from schemas.post import PostCreate, PostUpdate, PostResponse, PostDetailResponse
from schemas.pagination import PostPaginationParams, PaginatedResponse
from core.exceptions import NotFoundException
from core.utils import generate_uid, get_now


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def create_post(self, schema: PostCreate, author_id: str) -> PostResponse:
        data = schema.model_dump(exclude_unset=True)
        tags = data.pop("tags", [])
        animal_data = data.pop("animal", None)

        now = get_now()
        props = {**data, "id": generate_uid(), "created_at": now, "updated_at": now}

        animal_props = None
        if schema.type == PostType.ANIMAL and animal_data:
            animal_props = {**animal_data, "id": generate_uid()}

        raw = await self.repo.create_post(
            props=props,
            author_id=author_id,
            tags=tags or None,
            animal_props=animal_props,
        )
        return PostResponse.model_validate(raw)


    async def get_post(self, post_id: str, current_user_id: str | None = None) -> PostDetailResponse:
        raw = await self.repo.get_post(post_id, current_user_id)
        if not raw:
            raise NotFoundException(entity="Post")
        return PostDetailResponse.model_validate(raw)


    async def get_feed(
        self,
        params: PostPaginationParams,
        current_user_id: str | None = None,
    ) -> PaginatedResponse[PostResponse]:
        paginated = await self.repo.get_feed(params, current_user_id)
        return PaginatedResponse(
            items=[PostResponse.model_validate(item) for item in paginated.items],
            total=paginated.total,
            limit=paginated.limit,
            offset=paginated.offset,
            has_more=paginated.has_more,
        )


    async def update_post(
        self, 
        post_id: str, 
        schema: PostUpdate, 
        current_user_id: str
    ) -> PostResponse:
        data = schema.model_dump(exclude_unset=True)
        tags = data.pop("tags", None)
        animal_data = data.pop("animal", None)

        props = {**data, "updated_at": get_now()}

        animal_props = None
        detach_animal = False
        if "animal" in schema.model_fields_set:
            if animal_data is None:
                detach_animal = True
            else:
                animal_props = {k: v for k, v in animal_data.items() if v is not None}
                if "scientific_name" not in animal_props:
                    animal_props["scientific_name"] = animal_props.get("name", generate_uid())

        raw = await self.repo.update_post_safe(
            post_id=post_id,
            props=props,
            current_user_id=current_user_id,
            tags=tags,
            animal_props=animal_props,
            detach_animal=detach_animal,
        )
        if not raw:
            raise NotFoundException(entity="Post")
        return PostResponse.model_validate(raw)


    async def delete_post(self, post_id: str, current_user_id: str) -> bool:
        return await self.repo.delete_post_safe(post_id, current_user_id)


    async def toggle_like(self, post_id: str, user_id: str) -> bool:
        result = await self.repo.toggle_like(post_id, user_id)
        if not result:
            raise NotFoundException(entity="Post")
        return result