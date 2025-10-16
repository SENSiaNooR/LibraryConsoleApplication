

class NotSuchModelInDataBaseError(Exception):
    """Exception raised for custom error in the application."""

    def __init__(self, message, model):
        super().__init__(message)
        self.model = model

class EmptyModelError(ValueError):
    """Raised when attempting to query or update using an empty model."""
    def __init__(self, message: str = "Model has no populated fields for building a WHERE clause."):
        super().__init__(message)

class MultipleRowsReturnedError(Exception):
    """Raised when more than one row is returned in a single-row query."""
    pass

class MemberAlreadyDeactivatedError(Exception):
    """Raised when trying to deactivate a member who is already inactive."""
    pass

class MemberAlreadyActivatedError(Exception):
    """Raised when trying to activate a member who is already active."""
    pass

class AuthenticationFailed(Exception):
    def __init__(self, message="Authentication failed"):
        super().__init__(message)
        
class BookOutOfStockError(Exception):
    """Raise when book is out of stock"""
    pass

class AlreadyReturnedBookError(Exception):
    """Raise when book is already returned to library"""  
    pass
    
class RepositoryMethodNotAllowedError(Exception):
    def __init__(self, method_name: str, repository_name: str):
        message = f"The method '{method_name}' is not allowed in repository '{repository_name}'."
        super().__init__(message)
        
class InactiveMemberBorrowRequestError(Exception):
    """Raised when an inactive member attempts to borrow a book."""
    pass

class BorrowRequestAlreadyHandledError(Exception):
    """Raised when try handle (update) borrow request that already handled before."""
    pass

class AuthenticationError(Exception):
    """
    Raised when user authentication fails, 
    e.g., invalid username/password or token issues.
    """
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)
        
class ReachedToRequestLimitError(Exception):
    """Raised when guest request more than limitation."""
    pass

class InappropriateRoleError(Exception):
    """Raised when try to get instance of Service classes (such as MemberServices) by token of other roles (such as guest)."""