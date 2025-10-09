import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path
from psycopg2.extensions import connection as PgConnection, cursor as PgCursor


class DatabaseConnector:
    """Singleton class for managing PostgreSQL database connections.

    This class provides a centralized interface to load environment
    variables from a `.env` file and create connections and cursors
    for PostgreSQL using the `psycopg2` library. Ensures only one
    instance of the connector exists across the application.

    Attributes:
        _instance (Optional[DatabaseConnector]): Singleton instance of the connector.
        _env_loaded (bool): Flag indicating whether environment variables have been loaded.
    """

    _instance = None
    _env_loaded = False

    def __new__(cls):
        """Create or return the singleton instance.

        Returns:
            DatabaseConnector: The single existing instance of the connector.
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the connector and load environment variables if not already loaded."""
        if not DatabaseConnector._env_loaded:
            current_dir = Path(__file__).resolve().parent
            dotenv_path = current_dir.parent / ".env"
            load_dotenv(dotenv_path=dotenv_path)
            DatabaseConnector._env_loaded = True

    def get_connection(self) -> PgConnection:
        """Create and return a new PostgreSQL connection.

        Reads database credentials from environment variables loaded
        from the `.env` file and creates a connection using psycopg2.

        Returns:
            PgConnection: A new connection object to the PostgreSQL database.

        Raises:
            psycopg2.OperationalError: If the connection to the database fails.
        """
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

    def get_cursor(self) -> PgCursor:
        """Create and return a new database cursor.

        Opens a new connection via `get_connection()` and returns
        a cursor object for executing SQL statements.

        Returns:
            PgCursor: A cursor object used to interact with the PostgreSQL database.
        """
        conn = self.get_connection()
        return conn.cursor()
