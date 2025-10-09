from typing import Optional
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from Models.Schema import DBTableColumns, DBTables, DBViews
from Models.Models import AuthorModel, AuthorViewModel
from psycopg2.extensions import cursor as PgCursor

class AuthorRepository(CommonQueriesRepository):

    table_name = DBTables.AUTHOR
    view_name = DBViews.AUTHOR_VIEW
    model_class = AuthorModel
    view_model_class = AuthorViewModel
    insert_clause_exclude = {
        DBTableColumns.Author.ID    
    }
    set_clause_exclude = {
        DBTableColumns.Author.ID    
    }
    where_clause_exclude = set()


    # Inherited Methods

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
    

    # Forbidden Methods
    
    @classmethod
    @forbidden_method
    def remove(cls, model, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None):
        pass
    
    @classmethod
    @forbidden_method
    def clear(cls, cursor: Optional[PgCursor] = None):
        pass
    

    
    


if __name__ == '__main__':
    

    #model = AuthorModel(name = 'ندا عابد')
    #db_model = AuthorRepository.get_one(model)
    #print(db_model)

    #db_model.name = 'رها عابد'
    #AuthorRepository.update(db_model)
    
    print(AuthorRepository.view_many(AuthorViewModel()))
