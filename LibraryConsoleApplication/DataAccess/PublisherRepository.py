from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.Models import CategoryModel, CategoryViewModel, MemberModel, MemberWithoutPasswordViewModel, PublisherModel, PublisherViewModel, UserModel, UserType
from DataAccess.Schema import DBTableColumns, DBTables, DBViewColumns, DBViews
from psycopg2.extensions import cursor as PgCursor
from DataAccess.SqlBuilder import build_insert_clause, build_set_clause, build_where_clause
from DataAccess.UserRepository import UserRepository


class PublisherRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(PublisherModel)
    def get_publisher(cls, model : PublisherModel, cursor : Optional[PgCursor] = None) -> PublisherModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        where_clause, values = build_where_clause(model)

        query = (
            f"""
            SELECT * FROM {DBTables.PUBLISHER} 
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
    @map_to_single_model(PublisherViewModel)
    def get_publisher_with_books(cls, model : PublisherModel, cursor : Optional[PgCursor] = None) -> PublisherViewModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model)

        query = (
            f"""
            SELECT * FROM {DBViews.PUBLISHER_VIEW} 
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
    @map_to_model(PublisherModel)
    def get_all_publishers(cls, cursor : Optional[PgCursor] = None) -> list[PublisherModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = (
            f"""
            SELECT * FROM {DBTables.PUBLISHER} 
            """
        )
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    @map_to_model(PublisherViewModel)
    def get_all_publishers_with_books(cls, cursor : Optional[PgCursor] = None) -> list[PublisherViewModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = (
            f"""
            SELECT * FROM {DBViews.PUBLISHER_VIEW} 
            """
        )
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result

    @classmethod
    @map_to_single_model(PublisherModel)
    def add_publisher(cls, model : PublisherModel, cursor : Optional[PgCursor] = None) -> PublisherModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        columns_clause, placeholders_clause, values = build_insert_clause(model)

        query = (
            f"""
            INSERT INTO {DBTables.PUBLISHER} (
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
    def update_publisher(cls, model: PublisherModel, cursor: Optional[PgCursor] = None) -> None:
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
            UPDATE {DBTables.PUBLISHER}
            SET {set_clause}
            WHERE {DBTableColumns.Publisher.ID} = %s
        """
    
        values.append(model.id)
        cursor.execute(query, values)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def delete_publisher(cls, id: int, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = f"""
            DELETE FROM {DBTables.PUBLISHER}
            WHERE {DBTableColumns.Publisher.ID} = %s
        """
    
        cursor.execute(query, (id,))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
    
if __name__ == '__main__':
    #p = PublisherModel(phone = '071-32223344')
    #res1 = PublisherRepository.get_publisher(p)
    #print(res1)
    #res2 = PublisherRepository.get_publisher_with_books(p)
    #print(res2)
    #p = PublisherModel(name = 'نشر پوران هپروت', address = 'کرج', contact_email= 'pooran@gmail.com', phone= '0453-31233145')
    #res = PublisherRepository.add_publisher(p)
    #print(res)
    #p = PublisherModel(id = 27, name='نشر پوران هپروت پلاس', contact_email= 'parro@gmail.com')
    #PublisherRepository.update_publisher(p)
    pass 

