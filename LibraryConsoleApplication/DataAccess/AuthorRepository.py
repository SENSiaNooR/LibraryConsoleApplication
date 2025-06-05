from typing import Optional
from DataAccess.Schema import DBTableColumns, DBTables, DBViews
from DataAccess.SqlBuilder import build_insert_clause, build_set_clause, build_where_clause
from Models import AuthorModel, AuthorViewModel
from BaseRepository import BaseRepository, map_to_single_model
from BaseRepository import map_to_model
from psycopg2.extensions import cursor as PgCursor

class AuthorRepository(BaseRepository):

    @classmethod
    @map_to_single_model(AuthorModel)
    def get_author(cls, model : AuthorModel, cursor : Optional[PgCursor] = None) -> AuthorModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model)

        query = (
            f"""
            SELECT * FROM {DBTables.AUTHOR} 
            WHERE {where_clause}
            LIMIT 1
            """
        )
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    @map_to_single_model(AuthorViewModel)
    def get_author_with_books(cls, model : AuthorModel, cursor : Optional[PgCursor] = None) -> AuthorViewModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model)

        query = (
            f"""
            SELECT * FROM {DBViews.AUTHOR_VIEW} 
            WHERE {where_clause}
            LIMIT 1
            """
        )
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
       
    @classmethod
    @map_to_model(AuthorModel)
    def get_all_authors(cls, cursor : Optional[PgCursor] = None) -> list[AuthorModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = (
            f"""
            SELECT * FROM {DBTables.AUTHOR} 
            """
        )
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    @map_to_model(AuthorViewModel)
    def get_all_authors_with_books(cls, cursor : Optional[PgCursor] = None) -> list[AuthorViewModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = (
            f"""
            SELECT * FROM {DBViews.AUTHOR_VIEW} 
            """
        )
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result

    @classmethod
    @map_to_single_model(AuthorModel)
    def add_author(cls, model : AuthorModel, cursor : Optional[PgCursor] = None) -> AuthorModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        columns_clause, placeholders_clause, values = build_insert_clause(model)

        query = (
            f"""
            INSERT INTO {DBTables.AUTHOR} (
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
    def update_author(cls, model: AuthorModel, cursor: Optional[PgCursor] = None) -> None:
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
            UPDATE {DBTables.AUTHOR}
            SET {set_clause}
            WHERE {DBTableColumns.Author.ID} = %s
        """
    
        values.append(model.id)
        cursor.execute(query, values)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def delete_author(cls, id: int, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = f"""
            DELETE FROM {DBTables.AUTHOR}
            WHERE {DBTableColumns.Author.ID} = %s
        """
    
        cursor.execute(query, (id,))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
    


if __name__ == '__main__':

    a = AuthorRepository.get_all_authors()
    for item in a:
        print(item)