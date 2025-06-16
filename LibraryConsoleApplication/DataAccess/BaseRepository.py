from Connection import DatabaseConnector
from psycopg2.extensions import connection as PgConnection, cursor as PgCursor
from typing import Optional, Type
from abc import ABC
from Models.Models import BaseTableModel, BaseViewModel

class BaseRepository(ABC):
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
        return cls._db.get_connection()    

    @classmethod
    def _get_cursor(cls) -> PgCursor:
        return cls._db.get_cursor()
    


