from Connection import DatabaseConnector
from typing import Type, TypeVar, Callable
from functools import wraps

T = TypeVar("T")

class BaseRepository:
    def __init__(self):
        self.db = DatabaseConnector()

    def get_cursor(self):
        return self.db.get_cursor()


def map_to_model(model_class: Type[T]):
    def decorator(func: Callable[..., list[tuple]]) -> Callable[..., list[T]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> list[T]:
            rows = func(*args, **kwargs)
            return [model_class(*row) for row in rows]
        return wrapper
    return decorator
