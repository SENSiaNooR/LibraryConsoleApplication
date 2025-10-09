from typing import Optional
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from Models.Models import BookAuthorModel
from Models.Schema import DBTables
from psycopg2.extensions import cursor as PgCursor


class BookAuthorRepository(CommonQueriesRepository):
    
    table_name = DBTables.BOOK_AUTHOR
    model_class = BookAuthorModel
    insert_clause_exclude = set()
    set_clause_exclude = set()
    where_clause_exclude = set()
    
    # Inherited Methods
    
    @classmethod
    def add(cls, model : model_class, cursor : Optional[PgCursor] = None) -> model_class:
        return super().add(model, cursor)

    @classmethod
    def remove(cls, model : model_class, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None) -> None:
        return super().remove(model, use_like_for_strings, cursor)


    # Forbidden Methods
    
    @classmethod
    @forbidden_method
    def get_one(cls, model, cursor : Optional[PgCursor] = None):
        pass
       
    @classmethod
    @forbidden_method
    def get_many(cls, model, cursor : Optional[PgCursor] = None):
        pass
    
    @classmethod
    @forbidden_method
    def view_one(cls, model, cursor : Optional[PgCursor] = None):
        pass
       
    @classmethod
    @forbidden_method
    def view_many(cls, model, cursor : Optional[PgCursor] = None):
        pass
    
    @classmethod
    @forbidden_method
    def update(cls, model, cursor: Optional[PgCursor] = None):
        pass
            
    @classmethod
    @forbidden_method
    def delete(cls, id, cursor: Optional[PgCursor] = None):
        pass
    
    @classmethod
    @forbidden_method
    def clear(cls, cursor: Optional[PgCursor] = None):
        pass


if __name__ == '__main__':
    pass
