from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from DataAccess.BookRepository import BookRepository
from Exceptions.Exceptions import AlreadyReturnedBookError, BookOutOfStockError, NotSuchModelInDataBaseError
from Models.Models import BookModel, BorrowingModel, BorrowingViewModel
from Models.Schema import DBTableColumns, DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor


class BorrowingRepository(CommonQueriesRepository):

    table_name = DBTables.BORROWING
    view_name = DBViews.BORROWING_VIEW
    model_class = BorrowingModel
    view_model_class = BorrowingViewModel
    insert_clause_exclude = {
        DBTableColumns.Borrowing.ID
    }
    set_clause_exclude = {
        DBTableColumns.Borrowing.ID,
        DBTableColumns.Borrowing.MEMBER_ID,
        DBTableColumns.Borrowing.BOOK_ID,
        DBTableColumns.Borrowing.START_DATE
    }
    where_clause_exclude = set()


    # Methods

    @classmethod
    def add(cls, model : model_class, cursor : Optional[PgCursor] = None) -> model_class:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        book_model = BookModel(id = model.book_id)
        book_db_model = BookRepository.get_one(book_model, cursor)
        
        if book_db_model is None:
            raise NotSuchModelInDataBaseError('can not find book', book_model)
        
        if book_db_model.available_copies == 0:
            raise BookOutOfStockError()

        now = datetime.now(ZoneInfo("Asia/Tehran"))

        model.start_date=now
        model.end_date=None
        model.returned=False

        result = super().add(model, cursor)
        
        book_db_model.available_copies -= 1
        BookRepository.update(book_db_model, cursor)
    
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
         
        return result

    @classmethod
    def return_book(cls, model : BorrowingModel, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
            
        borrowing_db_model = cls.get_one(model,cursor)
        
        if borrowing_db_model is None:
            raise NotSuchModelInDataBaseError('can not find borrowing record', model)
        
        if borrowing_db_model.returned is True:
            raise AlreadyReturnedBookError()
        
        borrowing_db_model.returned = True
        borrowing_db_model.end_date = datetime.now(ZoneInfo("Asia/Tehran"))

        super().update(borrowing_db_model, cursor)
        
        book_db_model = BookRepository.get_one(BookModel(id=borrowing_db_model.book_id),cursor=cursor)
        book_db_model.available_copies += 1
        BookRepository.update(book_db_model,cursor=cursor)
    
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()


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


    # Forbidden Methods
            
    @classmethod
    @forbidden_method
    def update(cls, model, cursor: Optional[PgCursor] = None):
        pass
            
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
