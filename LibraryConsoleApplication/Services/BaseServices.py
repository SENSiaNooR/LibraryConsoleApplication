from abc import ABC
from Models.Models import UserWithoutPasswordViewModel

from Services.Decorators import token_required


class BaseServices(ABC):
    
    def __init__(self, token):
        self.token = token
        self.user_model = UserWithoutPasswordViewModel()
        
    @token_required
    def my_info(self):
        return f'hi {self.user_model.name}. your username is {self.user_model.username} and your role is {self.user_model.user_type}'
    

        
