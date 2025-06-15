
from datetime import datetime
from os import name
from typing import Optional
from zoneinfo import ZoneInfo
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from Models.Models import LibrarianActivityLogModel, LibrarianActivityLogViewModel, PublisherModel, PublisherViewModel
from Models.Schema import DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor


class LibrarianActivityLogRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(LibrarianActivityLogModel)
    def get_log(cls, model : LibrarianActivityLogModel, cursor : Optional[PgCursor] = None) -> LibrarianActivityLogModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBTables.LIBRARIAN_ACTIVITY_LOG,
            cursor=cursor
        )
    
    @classmethod
    @map_to_single_model(LibrarianActivityLogViewModel)
    def get_log_view(cls, model : LibrarianActivityLogViewModel, cursor : Optional[PgCursor] = None) -> LibrarianActivityLogViewModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBViews.LIBRARIAN_ACTIVITY_LOG_VIEW,
            cursor=cursor
        )
       
    @classmethod
    @map_to_model(LibrarianActivityLogModel)
    def get_logs(cls, model : LibrarianActivityLogModel, cursor : Optional[PgCursor] = None) -> list[LibrarianActivityLogModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBTables.LIBRARIAN_ACTIVITY_LOG,
            cursor=cursor
        )
    
    @classmethod
    @map_to_model(LibrarianActivityLogViewModel)
    def get_logs_view(cls, model : LibrarianActivityLogViewModel, cursor : Optional[PgCursor] = None) -> list[LibrarianActivityLogViewModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBViews.LIBRARIAN_ACTIVITY_LOG_VIEW,
            cursor=cursor
        )

    @classmethod
    @map_to_single_model(LibrarianActivityLogModel)
    def add_log(cls, model : LibrarianActivityLogModel, cursor : Optional[PgCursor] = None) -> LibrarianActivityLogModel:
        now = datetime.now(ZoneInfo('Asia/Tehran'))
        model.timestamp = now

        return CommonQueriesRepository.add_record(
            model=model,
            table=DBTables.LIBRARIAN_ACTIVITY_LOG,
            cursor=cursor
        )
            
    @classmethod
    def clear_table(cls, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = f"""
            DELETE FROM {DBTables.LIBRARIAN_ACTIVITY_LOG}
        """
    
        cursor.execute(query)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
  

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