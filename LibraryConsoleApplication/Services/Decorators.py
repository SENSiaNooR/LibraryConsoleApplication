from uuid import UUID
from Core.JWT import JWTManager
from Exceptions.Exceptions import ReachedToRequestLimitError
from Models.Models import UserWithoutPasswordViewModel
from functools import wraps

def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        jwt_manager = JWTManager()
        payload = jwt_manager.decode_token(self.token)
        try:
            payload["id"] = UUID(payload["id"])
        except:
            pass
        self.user_model = UserWithoutPasswordViewModel(payload['id'], payload['username'], payload['name'], payload['user_type'])
        return func(self, *args, **kwargs)
    return wrapper


def guest_request_limit(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.can_guest_request():
            raise ReachedToRequestLimitError()
        self.increase_guest_request()
        return func(self, *args, **kwargs)
    return wrapper