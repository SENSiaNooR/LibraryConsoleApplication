from Exceptions.Exceptions import InappropriateRoleError
from Services.BaseServices import BaseServices


class AdminServices(BaseServices):
    def __init__(self, token):
        super().__init__(token)
        if self.user_model.user_type != 'admin':
            raise InappropriateRoleError()