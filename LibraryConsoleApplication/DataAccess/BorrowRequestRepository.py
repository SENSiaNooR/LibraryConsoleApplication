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
        """
        Adds a new borrow request record after validating member and book conditions.

        This method registers a new borrow request in the database. It ensures that:
        - The requesting member exists and is active.
        - The requested book exists and has at least one available copy.
    
        The method then assigns the current timestamp as the request time and 
        sets the request status to `pending` before inserting the record into the database.

        If no database cursor is provided, a new connection will be created, 
        and the transaction will be committed and closed automatically.

        Workflow:
            1. Fetch and validate the member and book records.
            2. Ensure the member is active and the book is available.
            3. Assign metadata (request timestamp, status = pending).
            4. Insert the borrow request record into the database.
            5. Commit and close the connection (if opened internally).

        Args:
            model (BorrowRequestModel): The borrow request record to insert.
            cursor (Optional[PgCursor], optional): Database cursor to use.
                If not provided, a new connection will be opened automatically.

        Raises:
            NotSuchModelInDataBaseError: If the referenced member or book does not exist.
            InactiveMemberBorrowRequestError: If the requesting member is inactive.
            BookOutOfStockError: If the requested book has no available copies.

        Returns:
            BorrowRequestModel: The newly inserted borrow request record.
        """
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
        """
        Updates the status of a borrow request after validating its current state.

        This method allows changing the status of a borrow request to either 
        `accepted` or `rejected`. It performs the following validations:
          - The borrow request exists in the database.
          - The request is currently in `pending` status.
          - The new status is either `accepted` or `rejected`.

        Upon successful validation, it sets the `handled_at` timestamp to the 
        current datetime and updates the record in the database.

        If no cursor is provided, the method will open a new database connection,
        commit the transaction, and close it automatically.

        Args:
            model (BorrowRequestModel): The borrow request model containing the updated status.
            cursor (Optional[PgCursor], optional): Database cursor to use. 
                If not provided, a new connection will be created automatically.

        Raises:
            NotSuchModelInDataBaseError: If the borrow request does not exist.
            BorrowRequestAlreadyHandledError: If the request status is not `pending`.
            ValueError: If the new status is not `accepted` or `rejected`.

        Returns:
            None
        """
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
        """Disabled method. Not allowed for this repository."""
        pass
    
    @classmethod
    @forbidden_method
    def remove(cls, model, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None):
        """Disabled method. Not allowed for this repository."""
        pass
            

if __name__ == '__main__':
    pass