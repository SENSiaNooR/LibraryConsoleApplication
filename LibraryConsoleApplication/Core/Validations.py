import re
from PasswordManagement import PasswordManager

class Validations:
    
    @staticmethod
    def email_validation(email : str) -> bool:
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)
    
    @staticmethod
    def username_validation(username : str) -> bool:
        return re.match(r"^[a-zA-Z][a-zA-Z0-9_]{2,15}$", username)
    
    @staticmethod
    def password_validation(password : str) -> bool:
        pass_manager = PasswordManager()
        return pass_manager.is_valid_password(password)
    
    @staticmethod
    def landline_number_validation(phone : str) -> bool:
        return re.match(r"^0\d{2,3}-?\d{8}$", phone)

    @staticmethod
    def mobile_number_validation(phone : str) -> bool:
        return re.match(r"^(?:\+98|0098|98|0)?9\d{9}$", phone)