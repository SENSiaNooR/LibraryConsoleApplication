from typing import Type, Callable, TypeVar, Union
from functools import wraps
from Exceptions.Exceptions import MultipleRowsReturnedError, RepositoryMethodNotAllowedError

T = TypeVar("T")

def map_to_model(model_class: Type[T]):
    """
    Decorator that maps a list of database result tuples to a list of model instances.

    This decorator is intended for repository methods that return multiple rows 
    (as a list of tuples). It automatically converts each row into an instance 
    of the specified model class.

    Example:
        @map_to_model(UserModel)
        def get_many_users(...):
            return [(1, "John"), (2, "Alice")]  # Returned from DB

        # → The result will be: [UserModel(1, "John"), UserModel(2, "Alice")]

    Args:
        model_class (Type[T]): The model class used to instantiate objects 
                               from the returned tuples.

    Returns:
        Callable[..., list[T]]: A decorator that transforms a list of tuples 
                                into a list of `model_class` instances.
    """
    def decorator(func: Callable[..., list[tuple]]) -> Callable[..., list[T]]:
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> list[T]:
            
            rows = func(*args, **kwargs)
            
            return [model_class(*row) for row in rows]
        
        return wrapper
    
    return decorator

def map_to_single_model(model_class: Type[T]):
    """
    Decorator that maps a single database result tuple to a model instance.

    This decorator is used for repository methods that return a single row 
    (as a tuple) or None. It converts that tuple into an instance of the 
    specified model class. If the function returns a list instead of a tuple, 
    it raises a `MultipleRowsReturnedError`.

    Example:
        @map_to_single_model(UserModel)
        def get_user_by_id(...):
            return (1, "John")  # Returned from DB

        # → The result will be: UserModel(1, "John")

    Args:
        model_class (Type[T]): The model class used to instantiate the object 
                               from the returned tuple.

    Returns:
        Callable[..., Union[T, None]]: A decorator that transforms a tuple 
                                       into a `model_class` instance or returns None.

    Raises:
        MultipleRowsReturnedError: If the wrapped function returns a list 
                                   instead of a single tuple.
    """
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

def forbidden_method(func):
    """
    Decorator to explicitly disable a repository method.

    This decorator is used to mark certain repository methods as forbidden 
    for specific tables or repositories. When the decorated method is called, 
    it raises a `RepositoryMethodNotAllowedError` with details about 
    the method and repository name.

    Example:
        @classmethod
        @forbidden_method
        def remove(cls, model, ...):
            "Forbidden Method. Do not use this method."
            pass

    Raises:
        RepositoryMethodNotAllowedError: Always raised when the decorated method is called.
    """
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        raise RepositoryMethodNotAllowedError(func.__name__, cls.__name__)
    return wrapper
