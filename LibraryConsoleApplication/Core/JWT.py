import os
from time import sleep
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from dotenv import load_dotenv
from pathlib import Path

class JWTManager:
    _instance = None
    _env_loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JWTManager, cls).__new__(cls)
            cls._instance._init_once()
        return cls._instance

    def _init_once(self):
        
        if not JWTManager._env_loaded:
            current_dir = Path(__file__).resolve().parent
            dotenv_path = current_dir.parent / ".env"
            load_dotenv(dotenv_path=dotenv_path)
            JWTManager._env_loaded = True

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

if __name__ == "__main__":
    jwt_mgr = JWTManager()
    token = jwt_mgr.create_token({"user_id": 1, "username": "admin"})
    print("توکن:", token)

    try:
        data = jwt_mgr.decode_token(token)
        print("داده:", data)
    except ValueError as e:
        print("خطا:", e)