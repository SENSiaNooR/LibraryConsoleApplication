from Core.JWT import JWTManager
from Models.Models import UserWithoutPasswordViewModel
from functools import wraps

def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        jwt_manager = JWTManager()
        payload = jwt_manager.decode_token(self.token)
        self.user_model = UserWithoutPasswordViewModel(**payload)
        return func(self, *args, **kwargs)
    return wrapper