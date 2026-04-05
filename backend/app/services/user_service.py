from uuid import uuid4
from datetime import datetime, timezone
from neo4j import AsyncSession
from ..repositories.user_repository import UserRepository
from ..http.schemas.request import UserRegisterRequest, UserUpdateRequest
from ..http.schemas.response import UserResponse

class UserService:

    def __init__(self, session: AsyncSession):
      self.repo = UserRepository(session)

    def _to_response(self, node) -> UserResponse:
      return UserResponse(
        id=node['id'],
        username=node['username'],
        email=node['email'],
        first_name=node['first_name'],
        last_name=node['last_name'],
        avatar_url=node['avatar_url'],
        bio=node['bio'],
        created_at=node['created_at']
      )

    async def create(self, data: UserRegisterRequest) -> None:
      flat_data = {
        'id': str(uuid4()),
        'email': data.email,
        'password': data.password,  # TODO: хешировать
        'username': data.username,
        'first_name': data.first_name,
        'last_name': data.last_name,
        'avatar_url': None,
        'bio': None,
        'role': 'user',
        'created_at': datetime.now(timezone.utc).isoformat(),
      }

      await self.repo.create([flat_data])

    async def get(self, id: str) -> UserResponse | None:
      node = await self.repo.get(id)
      return self._to_response(node) if node else None

    async def get_all(self) -> list[UserResponse]:
      nodes = await self.repo.get_all()
      return [self._to_response(node) for node in nodes]

    async def update(self, id: str, data: UserUpdateRequest) -> None:
      props = data.model_dump(exclude_none=True)
      props['updated_at'] = datetime.now(timezone.utc).isoformat()
      await self.repo.update(id, props)

    async def delete(self, id: str) -> None:
      await self.repo.delete(id)