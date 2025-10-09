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
        """
        Adds a new borrowing record and updates the related book availability.

        This method registers a new borrowing event in the database. It checks whether 
        the requested book exists and has available copies before creating the borrowing 
        record. Once the record is added, it decreases the book’s `available_copies` count 
        by one.

        If no database cursor is provided, the method opens a new connection, performs 
        the operation, commits the transaction, and closes the connection automatically.

        Workflow:
            1. Verify that the referenced book exists.
            2. Check that at least one copy of the book is available.
            3. Set borrowing metadata (start date, end date, returned flag).
            4. Insert a new borrowing record into the database.
            5. Decrease the book’s available copies.
            6. Commit and close the connection (if opened internally).

        Args:
            model (BorrowingModel): The borrowing record to be inserted into the database.
            cursor (Optional[PgCursor], optional): Database cursor to use. 
                If not provided, a new connection will be created automatically.

        Raises:
            NotSuchModelInDataBaseError: If the referenced book does not exist.
            BookOutOfStockError: If there are no available copies of the requested book.

        Returns:
            BorrowingModel: The newly added borrowing record, as stored in the database.
        """
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
        """
        Marks a borrowed book as returned and updates the related book record.

        This method finalizes the borrowing process by setting the `returned` field of 
        the borrowing record to `True` and assigning the current timestamp as the 
        `end_date`. It then increments the `available_copies` count of the corresponding 
        book in the `BookRepository`.

        If no database cursor is provided, the method opens a new connection and commits 
        the changes automatically before closing it.

        Workflow:
            1. Fetch the borrowing record from the database.
            2. Validate that the record exists and has not already been returned.
            3. Mark the record as returned and update the return date.
            4. Update the related book’s available copies.
            5. Commit and close the connection (if it was opened internally).

        Args:
            model (BorrowingModel): The borrowing record to be marked as returned.
            cursor (Optional[PgCursor], optional): Database cursor to use. 
                If not provided, a new connection will be created automatically.

        Raises:
            NotSuchModelInDataBaseError: If the borrowing record does not exist.
            AlreadyReturnedBookError: If the book was already marked as returned.

        Returns:
            None
        """
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
        """Disabled method. Not allowed for this repository."""
        pass
            
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

    @classmethod
    @forbidden_method
    def clear(cls, cursor: Optional[PgCursor] = None):
        """Disabled method. Not allowed for this repository."""
        pass

    
    
    
    
            
if __name__ == '__main__':
    pass
