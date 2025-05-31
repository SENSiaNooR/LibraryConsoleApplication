import os
from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

class PasswordManager:
    def __init__(self):
        load_dotenv()

        self.ph = PasswordHasher(
            time_cost = int(os.getenv("HASH_TIME_COST")),
            memory_cost = int(os.getenv("HASH_MEMORY_COST")),
            parallelism = int(os.getenv("HASH_PARALLELISM"))
        )

    def hash_password(self, plain_password: str) -> str:
        return self.ph.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return self.ph.verify(hashed_password, plain_password)
        except (VerifyMismatchError, VerificationError):
            return False

    def needs_rehash(self, hashed_password: str) -> bool:
        return self.ph.check_needs_rehash(hashed_password)

