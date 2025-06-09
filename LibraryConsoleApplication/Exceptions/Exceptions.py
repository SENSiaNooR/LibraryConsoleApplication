

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