
from Exceptions.Exceptions import InappropriateRoleError
from Services.BaseServices import BaseServices


class MemberServices(BaseServices):
    def __init__(self, token):
        super().__init__(token)
        if self.user_model.user_type != 'member':
            raise InappropriateRoleError()