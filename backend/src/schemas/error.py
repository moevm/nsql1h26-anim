from schemas.base import BaseSchema

class ErrorDetail(BaseSchema):
    message: str
    code: str
    field: str | None = None
    reason: str | None = None


class ErrorResponse(BaseSchema):
    error: ErrorDetail