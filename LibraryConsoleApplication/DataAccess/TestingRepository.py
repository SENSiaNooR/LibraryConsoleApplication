from typing import Optional
from psycopg2.extensions import cursor as PgCursor
from Models.Models import TestingModel, TestingViewModel
from Models.Schema import DBTableColumns, DBTables, DBViews 
from DataAccess.CommonQueriesRepository import CommonQueriesRepository

class TestingRepository(CommonQueriesRepository):

    table_name = DBTables.TESTING
    view_name = DBViews.TESTING_VIEW
    model_class = TestingModel
    view_model_class = TestingViewModel
    insert_clause_exclude = {
        DBTableColumns.Testing.ID    
    }
    set_clause_exclude = {
        DBTableColumns.Testing.ID    
    }
    where_clause_exclude = set()

    @classmethod
    def get_one(cls, model : model_class, cursor : Optional[PgCursor] = None) -> Optional[model_class]:
        return super().get_one(model, cursor)
       
    @classmethod
    def get_many(cls, model : model_class, cursor : Optional[PgCursor] = None) -> list[model_class]:
        return super().get_many(model, cursor)
    
    @classmethod
    def view_one(cls, model : view_model_class, cursor : Optional[PgCursor] = None) -> Optional[view_model_class]:
        return super().view_one(model, cursor)
       
    @classmethod
    def view_many(cls, model : view_model_class, cursor : Optional[PgCursor] = None) -> list[view_model_class]:
        return super().view_many(model, cursor)
    
    @classmethod
    def add(cls, model : model_class, cursor : Optional[PgCursor] = None) -> model_class:
        return super().add(model, cursor)
    
    @classmethod
    def update(cls, model : model_class, cursor: Optional[PgCursor] = None) -> None:
        return super().update(model, cursor)
            
    @classmethod
    def delete(cls, id : int, cursor: Optional[PgCursor] = None) -> None:
        return super().delete(id, cursor)

    @classmethod
    def remove(cls, model : model_class, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None):
        return super().remove(model, use_like_for_strings, cursor)
    
    @classmethod
    def clear(cls, cursor: Optional[PgCursor] = None):
        return super().clear(cursor)
    