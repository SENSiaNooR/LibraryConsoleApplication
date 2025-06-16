from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from DataAccess.MemberRepository import MemberRepository
from DataAccess.BookRepository import BookRepository
from Exceptions.Exceptions import BookOutOfStockError, BorrowRequestAlreadyHandledError, InactiveMemberBorrowRequestError, NotSuchModelInDataBaseError
from Models.Models import BookModel, BorrowRequestModel, BorrowRequestStatus, MemberModel, MembersBorrowRequestViewModel, UnsetType
from Models.Schema import DBTableColumns, DBTables, DBViewColumns, DBViews
from psycopg2.extensions import cursor as PgCursor


class BorrowRequestRepository(CommonQueriesRepository):

    table_name = DBTables.BORROW_REQUEST
    view_name = DBViews.MEMBERS_BORROW_REQUEST_VIEW
    model_class = BorrowRequestModel
    view_model_class = MembersBorrowRequestViewModel
    insert_clause_exclude = {
        DBTableColumns.BorrowRequest.ID,
        DBTableColumns.BorrowRequest.HANDLED_AT,
        DBTableColumns.BorrowRequest.HANDLED_BY,
        DBTableColumns.BorrowRequest.NOTE
    }
    set_clause_exclude = {
        DBTableColumns.BorrowRequest.ID,
        DBTableColumns.BorrowRequest.BOOK_ID,
        DBTableColumns.BorrowRequest.MEMBER_ID,
        DBTableColumns.BorrowRequest.REQUEST_TIMESTAMP
    }
    where_clause_exclude = set()
    
    # Methods
    
    @classmethod
    def add(cls, model : model_class, cursor : Optional[PgCursor] = None) -> model_class:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        member_model = MemberModel(id=model.member_id)
        book_model = BookModel(id=model.book_id)
        
        member_db_model = MemberRepository.get_one(member_model, cursor)
        book_db_model = BookRepository.get_one(book_model, cursor)
        
        if member_db_model is None:
            raise NotSuchModelInDataBaseError('can not find member', member_model)
        
        if book_db_model is None:
            raise NotSuchModelInDataBaseError('can not find book', book_model)

        if member_db_model.active is False:
            raise InactiveMemberBorrowRequestError()

        if book_db_model.available_copies == 0:
            raise BookOutOfStockError()

        now = datetime.now(ZoneInfo("Asia/Tehran"))
        status = BorrowRequestStatus.pending

        model.request_timestamp = now
        model.status = status

        result = super().add(model, cursor)
    
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    def update(cls, model : model_class, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        db_model = cls.get_one(BorrowRequestModel(id=model.id), cursor)
        
        if db_model is None:
            raise NotSuchModelInDataBaseError('can not find borrow request', BorrowRequestModel(id=model.id))
        
        if not db_model.status == BorrowRequestStatus.pending:
            raise BorrowRequestAlreadyHandledError()

        if not model.status in [BorrowRequestStatus.accepted, BorrowRequestStatus.rejected]:
            raise ValueError('status must be accepted or rejected')

        now = datetime.now(ZoneInfo("Asia/Tehran"))
        model.handled_at = now
        
        super().update(model, cursor)
        
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

    @classmethod
    def clear(cls, cursor: Optional[PgCursor] = None) -> None:
        return super().clear(cursor)
    

    # Forbidden Methods
    
    @classmethod
    @forbidden_method
    def delete(cls, id : int, cursor: Optional[PgCursor] = None):
        pass
    
    @classmethod
    @forbidden_method
    def remove(cls, model, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None):
        pass
            

if __name__ == '__main__':
    pass