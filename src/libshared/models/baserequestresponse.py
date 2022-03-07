import functools
import inspect

from humps import camelize
from pydantic import BaseModel


def _bind_wrapper(func):
    spec = inspect.getfullargspec(func)

    @functools.wraps(func)
    def wrapper(self):
        real_args = []
        d = self.dict()

        for arg in spec.args:
            real_args.append(d[arg])
            del d[arg]

        if not spec.varkw:
            d = {}

        return func(*real_args, **d)

    return wrapper


class BaseRequestResponse(BaseModel):
    def dump(self, exclude_unset: bool = True):
        return self.dict(by_alias=True, exclude_unset=exclude_unset)

    @classmethod
    def bind(cls, func):
        setattr(cls, func.__name__, _bind_wrapper(func))

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        alias_generator = camelize
