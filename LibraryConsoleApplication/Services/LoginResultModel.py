from dataclasses import dataclass

from Models.Models import UserWithoutPasswordViewModel

@dataclass
class LoginResult:
    """
    Represents the result of a successful authentication process.
    
    Attributes:
        token (str): The generated JWT token for subsequent requests.
        user_info (UserWithoutPasswordViewModel) : User information that include id, username, name, user_type.
    """
    token: str
    user_info: UserWithoutPasswordViewModel
