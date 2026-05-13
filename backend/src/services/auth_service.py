from datetime import timedelta
from fastapi import Response
from core.config import settings
from core.security import create_token, verify_password, hash_password, decode_token
from core.exceptions import NotFoundException, BusinessRuleException, AppException, ErrorCode
from repositories.user_repository import UserRepository
from models.user import User
from schemas.identity import RegisterRequest, LoginRequest

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo


    async def _generate_auth_response(self, user: User, response: Response) -> User:
        access_token = create_token(
            user_id=user.id,
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
            token_type="access",
        )
        refresh_token = create_token(
            user_id=user.id,
            expires_delta=timedelta(days=settings.refresh_token_expire_days),
            token_type="refresh",
        )

        params = {"httponly": True, "secure": True, "samesite": "lax"}
        
        response.set_cookie(
            key="refresh_token", value=refresh_token, path="/api/v1/auth",
            max_age=settings.refresh_token_expire_days * 86400, **params
        )
        response.set_cookie(
            key="access_token", value=access_token, path="/",
            max_age=settings.access_token_expire_minutes * 60, **params
        )
        return user


    async def register(self, data: RegisterRequest, response: Response) -> User:
        user_node = User(
            **data.model_dump(exclude={"password"}),
            password=hash_password(data.password)
        )
        props = user_node.model_dump(exclude={
            "is_followed", 
            "followers_count", 
            "following_count",
            
        })
        user = await self.repo.create(user_node.model_dump())
        return await self._generate_auth_response(user, response)


    async def login(self, data: LoginRequest, response: Response) -> User:
        user = await self.repo.get_by_identifier(data.identifier)
        if not user or not verify_password(data.password, user.password):
            raise BusinessRuleException(detail="Invalid credentials", code=ErrorCode.UNAUTHORIZED)
        
        return await self._generate_auth_response(user, response)


    async def logout(response: Response):
        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            path="/api/v1/auth",
            samesite="lax",
            secure=True
        )
        
        response.delete_cookie(
            key="access_token",
            httponly=True,
            path="/",
            samesite="lax",
            secure=True
        )

    async def refresh(self, token: str | None, response: Response) -> User:
        if not token:
            raise AppException(detail="Token missing", code="missing_token", status=401)
        
        payload = decode_token(token)
        if not payload or payload.type != "refresh":
            raise AppException(detail="Invalid token", code="invalid_token", status=401)

        user = await self.repo.get_by_id(payload.sub)
        if not user:
            raise NotFoundException(entity="user")
            
        return await self._generate_auth_response(user, response)