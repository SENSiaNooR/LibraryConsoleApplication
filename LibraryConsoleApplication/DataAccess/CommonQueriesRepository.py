from typing import Optional
from DataAccess.BaseRepository import BaseRepository
from Exceptions.Exceptions import MultipleRowsReturnedError
from psycopg2.extensions import cursor as PgCursor
from DataAccess.SqlBuilder import build_insert_clause, build_set_clause, build_where_clause


class CommonQueriesRepository(BaseRepository):
    
    @classmethod
    def get_record(cls, model, table : str, exclude : set = set(), cursor : Optional[PgCursor] = None) -> tuple:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        where_clause, values = build_where_clause(model, exclude=exclude)

        query = (
            f"""
            SELECT * FROM {table} 
            WHERE {where_clause}
            """
        )
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 1:
            raise MultipleRowsReturnedError()
        
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
       
    @classmethod
    def get_records(cls, model, table : str, exclude : set = set(),cursor : Optional[PgCursor] = None) -> list[tuple]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model, use_like_for_strings=True, exclude=exclude)
        
        if not where_clause:
            query = (
                f"""
                SELECT * FROM {table} 
                """
            )
            cursor.execute(query)
            
        else:
            query = (
                f"""
                SELECT * FROM {table}
                WHERE {where_clause}
                """
            )
            cursor.execute(query, values)
            
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    def add_record(cls, model, table : str, exclude : set = {'id'}, cursor : Optional[PgCursor] = None) -> tuple:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        columns_clause, placeholders_clause, values = build_insert_clause(model, exclude)

        query = (
            f"""
            INSERT INTO {table} (
                {columns_clause}
            )
            VALUES ({placeholders_clause})
            RETURNING *
            """
        )
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    def update_record(cls, model, table : str, cursor: Optional[PgCursor] = None) -> None:
        if model.id is None:
            raise ValueError("Model must have an 'id' to perform update.")
    
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        set_clause, values = build_set_clause(model)

        if not set_clause:
            return  # Nothing to update

        query = f"""
            UPDATE {table}
            SET {set_clause}
            WHERE id = %s
        """
    
        values.append(model.id)
        cursor.execute(query, values)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def delete_record(cls, id : int, table : str, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = f"""
            DELETE FROM {table}
            WHERE id = %s
        """
    
        cursor.execute(query, (id,))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def delete_records(cls, model, table : str, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model, use_like_for_strings)

        query = f"""
            DELETE FROM {table}
            WHERE {where_clause}
        """
    
        cursor.execute(query, values)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
