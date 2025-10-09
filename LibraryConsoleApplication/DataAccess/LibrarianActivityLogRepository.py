
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from Models.Models import LibrarianActivityLogModel, LibrarianActivityLogViewModel
from Models.Schema import DBTableColumns, DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor


class LibrarianActivityLogRepository(CommonQueriesRepository):
    
    table_name = DBTables.LIBRARIAN_ACTIVITY_LOG
    view_name = DBViews.LIBRARIAN_ACTIVITY_LOG_VIEW
    model_class = LibrarianActivityLogModel
    view_model_class = LibrarianActivityLogViewModel
    insert_clause_exclude = {
        DBTableColumns.LibrarianActivityLog.ID
    }
    set_clause_exclude = {
        DBTableColumns.LibrarianActivityLog.ID,
        DBTableColumns.LibrarianActivityLog.LIBRARIAN_ID,
        DBTableColumns.LibrarianActivityLog.ACTION_TYPE,
        DBTableColumns.LibrarianActivityLog.MEMBER_ID,
        DBTableColumns.LibrarianActivityLog.BOOK_ID,
        DBTableColumns.LibrarianActivityLog.TIMESTAMP
    }
    where_clause_exclude = set()


    # Methods
    
    @classmethod
    def add(cls, model : model_class, cursor : Optional[PgCursor] = None) -> model_class:
        now = datetime.now(ZoneInfo("Asia/Tehran"))
        model.timestamp = now
        return super().add(model, cursor)



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
  


if __name__ == '__main__':
    
    from Models.Models import LibrarianModel, MemberModel, LibrarianAction
    from LibrarianRepository import LibrarianRepository
    from MemberRepository import MemberRepository
    
    librarian1 = LibrarianModel(name='مصطفی هدایتی')
    librarian1_db = LibrarianRepository.get_librarian(librarian1)
    
    member1 = MemberModel(name='حامد کلانتری')
    member1_db = MemberRepository.get_member(member1)
    
    action = LibrarianAction.send_message
    
    log1 = LibrarianActivityLogModel(
        librarian_id=librarian1_db.id,
        action_type=action,
        member_id=member1_db.id,
    )
    
    log1_db = LibrarianActivityLogRepository.add_log(log1)
    
    log1_get = LibrarianActivityLogRepository.get_log(log1)
    
    print(f'{log1_get=}')
    
    log1_view = LibrarianActivityLogViewModel(id = log1_get.id)
    
    log1_view_db = LibrarianActivityLogRepository.get_log_view(log1_view)
    
    print(f'{log1_view_db=}')

    log2_view = LibrarianActivityLogViewModel(librarian_name = 'مصطفی')
    
    res2 = LibrarianActivityLogRepository.get_logs_view(log2_view)
    
    print('res2 = [')
    for row in res2:
        print(f'\t{row}')
    print(']')