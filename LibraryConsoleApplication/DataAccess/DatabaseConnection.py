import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extensions import cursor as PgCursor
from pathlib import Path


class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._connection:
            
            current_dir = Path(__file__).resolve().parent
            dotenv_path = current_dir.parent / ".env"
            load_dotenv(dotenv_path=dotenv_path)  # بارگذاری فایل .env

            try:
                self._connection = psycopg2.connect(
                    dbname=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT")
                )
            except Exception as e:
                print("Connection error:", e)

    def get_cursor(self) -> PgCursor:
        if self._connection:
            return self._connection.cursor()
        else:
            raise Exception("No active database connection")

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            print("Connection closed")
