import neo4j.time
from pydantic import BaseModel,Field, ConfigDict, field_validator
from datetime import datetime
from core.utils import generate_uid, get_now

class BaseNode(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    @field_validator("created_at", "updated_at", mode="before", check_fields=False)
    @classmethod
    def parse_neo4j_datetime(cls, v):
        if isinstance(v, (neo4j.time.DateTime, neo4j.time.Date)):
            return v.to_native()
        return v

    id: str = Field(default_factory=generate_uid)
    created_at: datetime = Field(default_factory=get_now)
    updated_at: datetime = Field(default_factory=get_now)