from repositories.user_repository import UserRepository
from core.exceptions import NotFoundException, BusinessRuleException
from schemas.pagination import PaginatedResponse, UserPaginationParams
from schemas.identity import UserUpdate
from models.user import User


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user(self, user_id: str, current_user_id: str | None = None) -> User:
        user = await self.repo.get_by_id(user_id, current_user_id)
        if not user:
            raise NotFoundException(entity="User")
        return user

    async def list_users(self, params: UserPaginationParams, current_user_id: str | None = None) -> PaginatedResponse[User]:
        return await self.repo.list_users(params, current_user_id)

    async def update_profile(self, user_id: str, data: UserUpdate) -> User:
        update_data = data.model_dump(exclude_none=True)
        if not update_data:
            return await self.get_user(user_id)
            
        updated_raw = await self.repo.update(user_id, update_data)
        if not updated_raw:
            raise NotFoundException(entity="User")
        
        return await self.get_user(user_id)

    async def remove_account(self, user_id: str) -> bool:
        if not await self.repo.delete(user_id):
            raise NotFoundException(entity="User")
        return True

    async def follow_user(self, user_id: str, target_id: str) -> bool:
        if user_id == target_id:
            raise BusinessRuleException(
                detail="You cannot follow yourself",
                code="self_follow_forbidden"
            )
            
        target_exists = await self.repo.get_by_id(target_id)
        if not target_exists:
            raise NotFoundException(entity="TargetUser")
            
        return await self.repo.toggle_follow(user_id, target_id)
    
    async def get_followers(self, user_id: str, current_user_id: str | None = None) -> PaginatedResponse[User]:
        return await self.repo.get_followers(user_id, current_user_id)

    async def get_following(self, user_id: str, current_user_id: str | None = None) -> PaginatedResponse[User]:
        return await self.repo.get_following(user_id, current_user_id)