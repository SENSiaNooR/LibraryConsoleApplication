from typing import Optional
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from Models.Models import LibrarianModel, LibrarianViewModel, PlainUserModel
from Models.Schema import DBTableColumns, DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor
from DataAccess.UserRepository import UserRepository


class LibrarianRepository(CommonQueriesRepository):
    
    table_name = DBTables.LIBRARIAN
    view_name = DBViews.LIBRARIAN_VIEW
    model_class = LibrarianModel
    view_model_class = LibrarianViewModel
    insert_clause_exclude = set()
    set_clause_exclude = {
        DBTableColumns.Librarian.ID    
    }
    where_clause_exclude = set()
    

    # Methods
        
    @classmethod
    def add(cls, plain_user_model : PlainUserModel, model : model_class, cursor : Optional[PgCursor] = None) -> model_class:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        user_model = UserRepository.hash_password_and_add_user(plain_user_model, cursor) 
        model.id = user_model.id

        result = super().add(model, cursor)
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result    


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
    def update(cls, model : model_class, cursor: Optional[PgCursor] = None) -> None:
        return super().update(model, cursor)
    

    # Forbidden Methods

    @classmethod
    @forbidden_method
    def delete(cls, id : int, cursor: Optional[PgCursor] = None):
        pass
    
    @classmethod
    @forbidden_method
    def remove(cls, model, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None):
        pass

    @classmethod
    @forbidden_method
    def clear(cls, cursor: Optional[PgCursor] = None):
        pass


 
if __name__ == '__main__':
    pass
    


        
    