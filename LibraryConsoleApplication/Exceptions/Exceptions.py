

class NotSuchModelInDataBaseError(Exception):
    """Exception raised for custom error in the application."""

    def __init__(self, message, model):
        super().__init__(message)
        self.model = model


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