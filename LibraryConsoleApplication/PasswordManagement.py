import os
import re
from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

class PasswordManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PasswordManager, cls).__new__(cls)
            cls._instance._init_once()
        return cls._instance

    def _init_once(self):
        load_dotenv()

        self.ph = PasswordHasher(
            time_cost = int(os.getenv("HASH_TIME_COST")),
            memory_cost = int(os.getenv("HASH_MEMORY_COST")),
            parallelism = int(os.getenv("HASH_PARALLELISM"))
        )

        self.check_length = os.getenv("CHECK_LENGTH") == "True"
        self.min_length = int(os.getenv("MIN_LENGTH"))
        self.check_letter = os.getenv("CHECK_LETTER") == "True"
        self.check_digit = os.getenv("CHECK_DIGIT") == "True"
        self.check_upper = os.getenv("CHECK_UPPER") == "True"
        self.check_lower = os.getenv("CHECK_LOWER") == "True"
        self.check_special = os.getenv("CHECK_SPECIAL") == "True"

    def hash_password(self, plain_password: str) -> str:
        return self.ph.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return self.ph.verify(hashed_password, plain_password)
        except (VerifyMismatchError, VerificationError):
            return False

    def needs_rehash(self, hashed_password: str) -> bool:
        return self.ph.check_needs_rehash(hashed_password)
    
    def is_valid_password(self, password: str) -> bool:
        checks = []

        if self.check_length:
            checks.append(len(password) >= self.min_length)

        if self.check_letter:
            checks.append(bool(re.search(r'[A-Za-z]', password)))

        if self.check_digit:
            checks.append(bool(re.search(r'\d', password)))

        if self.check_upper:
            checks.append(bool(re.search(r'[A-Z]', password)))

        if self.check_lower:
            checks.append(bool(re.search(r'[a-z]', password)))

        if self.check_special:
            checks.append(bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)))

        return all(checks)

