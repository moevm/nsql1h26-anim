from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, 
        populate_by_name=True, 
        from_attributes=True
    )