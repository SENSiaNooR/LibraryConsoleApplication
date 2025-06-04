from dataclasses import asdict
from typing import Optional
from unicodedata import category
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.Models import CategoryModel, CategoryViewModel
from DataAccess.Schema import DBTableColumns, DBTables, DBViewColumns, DBViews
from psycopg2.extensions import cursor as PgCursor
from DataAccess.SqlBuilder import build_set_clause, build_where_clause


class CategoryRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(CategoryModel)
    def get_category(cls, model : CategoryModel, cursor : Optional[PgCursor] = None) -> CategoryModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model)
        
        if not where_clause:
            raise ValueError("At least one non-null attribute must be provided for filtering.")

        query = (
            f"""
            SELECT * FROM {DBTables.CATEGORY} 
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
    @map_to_single_model(CategoryViewModel)
    def get_category_with_books(cls, model : CategoryModel, cursor : Optional[PgCursor] = None) -> CategoryViewModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
            
        where_clause, values = build_where_clause(model)
        
        if not where_clause:
            raise ValueError("At least one non-null attribute must be provided for filtering.")

        query = (
            f"""
            SELECT * FROM {DBViews.CATEGORY_VIEW} 
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
    @map_to_model(CategoryModel)
    def get_all_categories(cls, cursor : Optional[PgCursor] = None) -> list[CategoryModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = (
            f"""
            SELECT 
                *
            FROM
                {DBTables.CATEGORY} 
            """
        )
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    @map_to_model(CategoryViewModel)
    def get_all_categories_with_books(cls, cursor : Optional[PgCursor] = None) -> list[CategoryViewModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = (
            f"""
            SELECT 
                *
            FROM
                {DBViews.CATEGORY_VIEW} 
            """
        )
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result

    @classmethod
    @map_to_single_model(CategoryModel)
    def add_category(cls, model : CategoryModel, cursor : Optional[PgCursor] = None) -> CategoryModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = (
            f"""
            INSERT INTO {DBTables.CATEGORY} (
                {DBTableColumns.Category.NAME},
                {DBTableColumns.Category.DESCRIPTION}
            )
            VALUES (%s, %s)
            RETURNING *
            """
        )
        
        cursor.execute(query, (model.name, model.description))
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    def update_category(cls, model: CategoryModel, cursor: Optional[PgCursor] = None) -> None:
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
            UPDATE {DBTables.CATEGORY}
            SET {set_clause}
            WHERE {DBTableColumns.Category.ID} = %s
        """
    
        values.append(model.id)
        cursor.execute(query, values)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

    @classmethod
    def delete_category(cls, id: int, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = f"""
            DELETE FROM {DBTables.CATEGORY}
            WHERE {DBTableColumns.Category.ID} = %s
        """
    
        cursor.execute(query, (id,))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
    
if __name__ == '__main__':
    #category = CategoryModel(name = 'کمک درسی', description= 'توضیحات')
    #res = CategoryRepository.add_category(category)
    #print(res)
    #category = CategoryModel(id = 49, description= 'توضیحات جدید')
    #CategoryRepository.update_category(category)
    #CategoryRepository.delete_category(49)
    pass