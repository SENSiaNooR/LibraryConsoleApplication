import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from dotenv import load_dotenv

class JWTManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JWTManager, cls).__new__(cls)
            cls._instance._init_once()
        return cls._instance

    def _init_once(self):
        load_dotenv()

        self.secret_key = os.getenv("JWT_SECRET_KEY")
        self.algorithm = os.getenv("JWT_ALGORITHM")
        min = int(os.getenv("JWT_EXP_MINUTES"))
        self.exp = timedelta(minutes=min)

    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + self.exp
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid Token.")

    def is_token_expired(self, token: str) -> bool:
        try:
            jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": True})
            return False
        except jwt.ExpiredSignatureError:
            return True
        except jwt.InvalidTokenError:
            raise ValueError("Invalid Token.")
