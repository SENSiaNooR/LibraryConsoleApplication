from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.MemberRepository import MemberRepository
from DataAccess.BookRepository import BookRepository
from DataAccess.LibrarianRepository import LibrarianRepository
from Exceptions.Exceptions import BookOutOfStockError, NotSuchModelInDataBaseError
from Models.Models import BookModel, BorrowRequestModel, BorrowRequestStatus, LibrarianModel, MemberModel, MembersBorrowRequestViewModel
from Models.Schema import DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor


class BorrowRequestRepository(BaseRepository):

    @classmethod
    @map_to_single_model(BorrowRequestModel)
    def get_borrow_request(cls, model : BorrowRequestModel, cursor : Optional[PgCursor] = None) -> BorrowRequestModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBTables.BORROW_REQUEST,
            cursor=cursor
        )
        
    @classmethod
    @map_to_single_model(MembersBorrowRequestViewModel)
    def get_borrow_request_view(cls, model : MembersBorrowRequestViewModel, cursor : Optional[PgCursor] = None) -> MembersBorrowRequestViewModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBViews.MEMBERS_BORROW_REQUEST_VIEW,
            cursor=cursor
        )
       
    @classmethod
    @map_to_model(BorrowRequestModel)
    def get_borrow_requests(cls, model : BorrowRequestModel, cursor : Optional[PgCursor] = None) -> list[BorrowRequestModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBTables.BORROW_REQUEST,
            cursor=cursor
        )
        
    @classmethod
    @map_to_model(MembersBorrowRequestViewModel)
    def get_borrow_requests_view(cls, model : MembersBorrowRequestViewModel, cursor : Optional[PgCursor] = None) -> list[MembersBorrowRequestViewModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBViews.MEMBERS_BORROW_REQUEST_VIEW,
            cursor=cursor
        )

    @classmethod
    @map_to_single_model(BorrowRequestModel)
    def add_borrow_request(cls, member_model : MemberModel, book_model : BookModel, cursor : Optional[PgCursor] = None) -> BorrowRequestModel:
                
        member_db_model = MemberRepository.get_member(member_model, cursor)
        book_db_model = BookRepository.get_book(book_model, cursor)
        
        if member_db_model is None:
            raise NotSuchModelInDataBaseError('can not find member', member_model)
        
        if book_db_model is None:
            raise NotSuchModelInDataBaseError('can not find book', book_model)

        if book_db_model.available_copies == 0:
            raise BookOutOfStockError()

        now = datetime.now(ZoneInfo("Asia/Tehran"))
        status = BorrowRequestStatus.pending

        model = BorrowRequestModel(
            member_id=member_db_model.id,
            book_id=book_db_model.id,
            request_timestamp=now,
            status=status
        )

        return CommonQueriesRepository.add_record(
            model=model,
            table=DBTables.BORROW_REQUEST,
            cursor=cursor
        )
    
    @classmethod
    def handle_borrow_request(
        cls,
        borrow_request_id : int,
        librarian_model : LibrarianModel,
        status : BorrowRequestStatus,
        note : str,
        cursor : Optional[PgCursor] = None
    ) -> None:
        
        borrow_request_db_model = cls.get_borrow_request(BorrowRequestModel(id=borrow_request_id), cursor)
        librarian_db_model = LibrarianRepository.get_librarian(librarian_model, cursor)
        
        if borrow_request_db_model is None:
            raise NotSuchModelInDataBaseError('can not find borrow request', BorrowRequestModel(id=borrow_request_id))
        
        if librarian_db_model is None:
            raise NotSuchModelInDataBaseError('can not find librarian', librarian_model)

        if status == BorrowRequestStatus.pending:
            raise ValueError('status must be accepted or rejected')

        now = datetime.now(ZoneInfo("Asia/Tehran"))

        model = BorrowRequestModel(
            id=borrow_request_db_model.id,
            status=status,
            handled_at=now,
            handled_by=librarian_db_model.id,
            note=note
        )

        return CommonQueriesRepository.update_record(
            model=model,
            table=DBTables.BORROW_REQUEST,
            cursor=cursor
        )
    
    @classmethod
    def delete_borrow_request(cls, id : int, cursor : Optional[PgCursor] = None) -> None:
        return CommonQueriesRepository.delete_record(
            id=id,
            table=DBTables.BORROW_REQUEST,
            cursor=cursor
        )

    @classmethod
    def clear_table(cls, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = f"""
            DELETE FROM {DBTables.BORROW_REQUEST}
        """
    
        cursor.execute(query)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
if __name__ == '__main__':
    pass