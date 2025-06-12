from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.MemberRepository import MemberRepository
from DataAccess.BookRepository import BookRepository
from DataAccess.LibrarianRepository import LibrarianRepository
from Exceptions.Exceptions import BookOutOfStockError, NotSuchModelInDataBaseError
from Models.Models import BookModel, BorrowRequestModel, BorrowRequestStatus, BorrowingModel, BorrowingViewModel, LibrarianModel, MemberModel, MembersBorrowRequestViewModel
from Models.Schema import DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor


class BorrowingRepository(BaseRepository):

    @classmethod
    @map_to_single_model(BorrowingModel)
    def get_borrowing(cls, model : BorrowingModel, cursor : Optional[PgCursor] = None) -> BorrowingModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBTables.BORROWING,
            cursor=cursor
        )
        
    @classmethod
    @map_to_single_model(BorrowingViewModel)
    def get_borrowing_view(cls, model : BorrowingViewModel, cursor : Optional[PgCursor] = None) -> BorrowingViewModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBViews.BORROWING_VIEW,
            cursor=cursor
        )
       
    @classmethod
    @map_to_model(BorrowingModel)
    def get_borrowings(cls, model : BorrowingModel, cursor : Optional[PgCursor] = None) -> list[BorrowingModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBTables.BORROWING,
            cursor=cursor
        )
        
    @classmethod
    @map_to_model(BorrowingViewModel)
    def get_borrowings_view(cls, model : BorrowingViewModel, cursor : Optional[PgCursor] = None) -> list[BorrowingViewModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBViews.BORROWING_VIEW,
            cursor=cursor
        )

    @classmethod
    @map_to_single_model(BorrowingModel)
    def add_borrowing(cls, member_model : MemberModel, book_model : BookModel, cursor : Optional[PgCursor] = None) -> BorrowingModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        member_db_model = MemberRepository.get_member(member_model, cursor)
        book_db_model = BookRepository.get_book(book_model, cursor)
        
        if member_db_model is None:
            raise NotSuchModelInDataBaseError('can not find member', member_model)
        
        if book_db_model is None:
            raise NotSuchModelInDataBaseError('can not find book', book_model)
        
        if book_db_model.available_copies == 0:
            raise BookOutOfStockError()

        now = datetime.now(ZoneInfo("Asia/Tehran"))

        model = BorrowingModel(
            member_id=member_db_model.id,
            book_id=book_db_model.id,
            start_date=now,
            end_date=None,
            returned=False
        )

        result = CommonQueriesRepository.add_record(
            model=model,
            table=DBTables.BORROWING,
            cursor=cursor
        )
        
        book_db_model.available_copies -= 1
        BookRepository.update_book(book_db_model, cursor=cursor)
    
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
         
        return result
    
    @classmethod
    def return_book(cls, borrowing_model : BorrowingModel, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
            
        borrowing_db_model = cls.get_borrowing(borrowing_model,cursor)
        
        if borrowing_db_model is None:
            raise NotSuchModelInDataBaseError('can not find borrowing record', borrowing_model)
        
        borrowing_db_model.returned = True
        borrowing_db_model.end_date = datetime.now(ZoneInfo("Asia/Tehran"))

        result = CommonQueriesRepository.update_record(
            model=borrowing_db_model,
            table=DBTables.BORROWING,
            cursor=cursor
        )
        
        book_db_model = BookRepository.get_book(BookModel(id=borrowing_db_model.book_id),cursor=cursor)
        book_db_model.available_copies += 1
        BookRepository.update_book(book_db_model,cursor=cursor)
    
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    
            
if __name__ == '__main__':
    pass
