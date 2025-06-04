import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path
from psycopg2.extensions import connection as PgConnection, cursor as PgCursor


class DatabaseConnector:
    _instance = None
    _env_loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not DatabaseConnector._env_loaded:
            current_dir = Path(__file__).resolve().parent
            dotenv_path = current_dir.parent / ".env"
            load_dotenv(dotenv_path=dotenv_path)
            DatabaseConnector._env_loaded = True

    def get_connection(self) -> PgConnection:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

    def get_cursor(self) -> PgCursor:
        conn = self.get_connection()
        return conn.cursor()
