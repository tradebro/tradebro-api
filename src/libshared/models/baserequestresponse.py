from humps import camelize
from pydantic import BaseModel


class BaseRequestResponse(BaseModel):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        alias_generator = camelize


class ErrorResponse(BaseRequestResponse):
    detail: str | None = None
