from enum import StrEnum
from typing import Any

class ErrorCode(StrEnum):
    NOT_FOUND = "not_found"
    VALIDATION_ERROR = "validation_error"
    BUSINESS_RULE_VIOLATION = "business_rule_violation"
    CONFLICT = "conflict"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"

class AppException(Exception):
    def __init__(
        self, 
        detail: str, 
        code: str, 
        status: int, 
        context: dict[str, Any] | None = None
    ):
        self.detail = detail
        self.code = code
        self.status = status
        self.context = context or {}
        super().__init__(self.detail)

class NotFoundException(AppException):
    def __init__(
        self, entity: str, 
        context: dict[str, Any] | None = None
    ):
        super().__init__(
            detail=f"{entity} not found",
            code=f"{entity.lower()}_{ErrorCode.NOT_FOUND}",
            status=404,
            context=context
        )

class ValidationException(AppException):
    def __init__(
        self, detail: str, 
        context: dict[str, Any] | None = None
    ):
        super().__init__(
            detail=detail,
            code=ErrorCode.VALIDATION_ERROR,
            status=422,
            context=context
        )

class BusinessRuleException(AppException):
    def __init__(
        self, detail: str, 
        code: str = ErrorCode.BUSINESS_RULE_VIOLATION, 
        context: dict[str, Any] | None = None
    ):
        super().__init__(
            detail=detail,
            code=code,
            status=400,
            context=context
        )

class ConflictException(AppException):
    def __init__(
        self, entity: str, 
        context: dict[str, Any] | None = None
    ):
        super().__init__(
            detail=f"{entity} already exists",
            code=f"{entity.lower()}_{ErrorCode.CONFLICT}",
            status=409,
            context=context
        )