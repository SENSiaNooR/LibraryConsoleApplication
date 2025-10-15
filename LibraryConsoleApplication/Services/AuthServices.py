from Core.JWT import JWTManager
from DataAccess.GuestRepository import GuestRepository
from DataAccess.MemberRepository import MemberRepository
from DataAccess.UserRepository import UserRepository
from Exceptions.Exceptions import AuthenticationError
from Models.Models import MemberModel, PlainUserModel, UserType, UserWithoutPasswordViewModel
from Services.LoginResultModel import LoginResult


class AuthServices:
    @classmethod
    def login(cls, plain_user: PlainUserModel) -> LoginResult:
        user = UserRepository.verify_user(plain_user)
        if user is None:
            raise AuthenticationError()

        jwt_manager = JWTManager()

        token = jwt_manager.create_token(user.__dict__)

        return LoginResult(token, user)
    
    @classmethod
    def login_as_guest(cls) -> str:
        guest = GuestRepository.add()
        
        jwt_manager = JWTManager()
        
        user = UserWithoutPasswordViewModel(
            id = guest.id,
            username = None,
            name = None,
            user_type = UserType.guest
        )
        
        token = jwt_manager.create_token(user.__dict__)
        
        return token
    
    @classmethod
    def signup(cls, plain_user: PlainUserModel, member_model: MemberModel) -> LoginResult:
        member = MemberRepository.add(plain_user, member_model)
        return cls.login(plain_user)