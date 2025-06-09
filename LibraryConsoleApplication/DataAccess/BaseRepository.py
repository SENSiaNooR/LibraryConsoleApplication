from Connection import DatabaseConnector
from psycopg2.extensions import connection as PgConnection, cursor as PgCursor
from typing import Type, TypeVar, Callable, Union
from functools import wraps
from Exceptions.Exceptions import MultipleRowsReturnedError

T = TypeVar("T")

class BaseRepository:
    _db = DatabaseConnector()

    @classmethod
    def _get_connection(cls) -> PgConnection:
        return cls._db.get_connection()    

    @classmethod
    def _get_cursor(cls) -> PgCursor:
        return cls._db.get_cursor()


def map_to_model(model_class: Type[T]):
    def decorator(func: Callable[..., list[tuple]]) -> Callable[..., list[T]]:
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> list[T]:
            
            rows = func(*args, **kwargs)
            
            return [model_class(*row) for row in rows]
        
        return wrapper
    
    return decorator

def map_to_single_model(model_class: Type[T]):
    def decorator(func: Callable[..., Union[tuple, None]]) -> Callable[..., Union[T, None]]:
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> Union[T, None]:
            
            row = func(*args, **kwargs)

            if row is None:
                return None
            
            if isinstance(row, list):
                raise MultipleRowsReturnedError("Expected a single row (tuple), but got a list.")
            
            return model_class(*row)
        
        return wrapper
    
    return decorator
