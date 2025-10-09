from DataAccess.Connection import DatabaseConnector
from psycopg2.extensions import connection as PgConnection, cursor as PgCursor
from typing import Optional, Type
from abc import ABC
from Models.Models import BaseTableModel, BaseViewModel


class BaseRepository(ABC):
    """Abstract base class for database repositories.

    This class provides a unified interface for managing connections
    to the PostgreSQL database through a `DatabaseConnector` instance.
    It also defines metadata for the associated table, view, and model
    classes used for ORM-like operations.

    Attributes:
        _db (DatabaseConnector): Object responsible for managing the database connection.
        table_name (str): The name of the table in the PostgreSQL database.
        view_name (Optional[str]): The name of the view in PostgreSQL related to the table.
        model_class (Type[BaseTableModel]): The model class used to represent table records.
        view_model_class (Optional[Type[BaseViewModel]]): The model class used to represent view records.
        insert_clause_exclude (Set[str]): Columns that cannot be specified in INSERT queries.
        set_clause_exclude (Set[str]): Columns that cannot be specified in UPDATE queries.
        where_clause_exclude (Set[str]): Columns that cannot be specified in WHERE (filtering) queries.
    """
    
    _db = DatabaseConnector()

    table_name : str
    view_name : Optional[str] = None
    model_class : Type[BaseTableModel]
    view_model_class : Optional[Type[BaseViewModel]] = None
    insert_clause_exclude : set = {'id'}
    set_clause_exclude : set = {'id'}
    where_clause_exclude : set = set()

    @classmethod
    def _get_connection(cls) -> PgConnection:
        """Get a database connection object.

        Returns:
            PgConnection: An active PostgreSQL connection instance obtained from the DatabaseConnector.
        """
        return cls._db.get_connection()    

    @classmethod
    def _get_cursor(cls) -> PgCursor:
        """Get a database cursor object.

        Returns:
            PgCursor: A PostgreSQL cursor instance for executing SQL queries.
        """
        return cls._db.get_cursor()
    


