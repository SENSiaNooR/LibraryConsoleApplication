from abc import ABC
from uuid import UUID
from Core.JWT import JWTManager
from Models.Models import UserWithoutPasswordViewModel

from Services.Decorators import token_required


class BaseServices(ABC):
    
    def __init__(self, token):
        self.token = token
        jwt_manager = JWTManager()
        payload = jwt_manager.decode_token(self.token)
        try:
            payload["id"] = UUID(payload["id"])
        except:
            pass
        self.user_model = UserWithoutPasswordViewModel(payload['id'], payload['username'], payload['name'], payload['user_type'])
        
    @token_required
    def my_info(self):
        return f'hi {self.user_model.name}. your username is {self.user_model.username} and your role is {self.user_model.user_type}'
    

    

        
