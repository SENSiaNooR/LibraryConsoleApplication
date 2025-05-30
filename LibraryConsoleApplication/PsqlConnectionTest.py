import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extensions import cursor as PgCursor

class Database:
    _instance = None
    _connection = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._connection:
            load_dotenv()  # بارگذاری فایل .env

            try:
                self._connection = psycopg2.connect(
                    dbname=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT")
                )
                print("Connected to database successfully.")
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
            
            
db = Database()
c1 = db.get_cursor()
c1.execute('select * from public.\"User\"')
res = c1.fetchall()
print(res)