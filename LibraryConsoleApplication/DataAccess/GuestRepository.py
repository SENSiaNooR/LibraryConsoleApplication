from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo
from DataAccess.BaseRepository import BaseRepository, map_to_single_model
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from Exceptions.Exceptions import NotSuchModelInDataBaseError
from Models.Models import GuestModel
from Models.Schema import DBTables
from psycopg2.extensions import cursor as PgCursor
import psycopg2.extras

psycopg2.extras.register_uuid()


class GuestRepository(BaseRepository):

    @classmethod
    @map_to_single_model(GuestModel)
    def get_guest(cls, uuid : UUID, cursor : Optional[PgCursor] = None) -> GuestModel:
        model = GuestModel(id = uuid)
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBTables.GUEST,
            cursor=cursor
        )

    @classmethod
    @map_to_single_model(GuestModel)
    def add_guest(cls, cursor : Optional[PgCursor] = None) -> GuestModel:
                
        id = uuid4()
        now = datetime.now(ZoneInfo("Asia/Tehran"))
        
        guest_model = GuestModel(
            id=id,
            created_time=now,
            request_count=0
        )
        
        return CommonQueriesRepository.add_record(
            model=guest_model,
            table=DBTables.GUEST,
            exclude=set(),
            cursor=cursor
        )
    
    @classmethod
    def increase_request(cls, uuid : UUID, cursor : Optional[PgCursor] = None) -> None:
        
        guest_db_model = cls.get_guest(uuid, cursor=cursor)
        
        if guest_db_model is None:
            raise NotSuchModelInDataBaseError('can not find guest', GuestModel(id=uuid))
        
        guest_db_model.request_count += 1

        return CommonQueriesRepository.update_record(
            model=guest_db_model,
            table=DBTables.GUEST,
            cursor=cursor
        )
    
    @classmethod
    def can_guest_request(cls, uuid: UUID, max_requests: int, max_minutes: int, cursor: Optional[PgCursor] = None) -> bool:
        guest = cls.get_guest(uuid, cursor)

        if guest is None:
            raise NotSuchModelInDataBaseError('can not find guest', GuestModel(id=uuid))

        now = datetime.now(ZoneInfo("Asia/Tehran"))
        delta_minutes = (now - guest.created_time).total_seconds() / 60

        if guest.request_count >= max_requests:
            return False
    
        if delta_minutes >= max_minutes:
            return False

        return True

    @classmethod
    def delete_guest(cls, uuid : UUID, cursor : Optional[PgCursor] = None) -> None:
        return CommonQueriesRepository.delete_record(
            id=uuid,
            table=DBTables.GUEST,
            cursor=cursor
        )

    @classmethod
    def clear_table(cls, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = f"""
            DELETE FROM {DBTables.GUEST}
        """
    
        cursor.execute(query)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
if __name__ == '__main__':
    
    g1 = GuestRepository.add_guest()
    g2 = GuestRepository.add_guest()
    
    print(f'{g1=}')
    print(f'{g2=}')
    
    g1_get = GuestRepository.get_guest(uuid = g1.id)
    g2_get = GuestRepository.get_guest(uuid = g2.id)
    
    print(f'{g1_get=}')
    print(f'{g2_get=}')
    
    for _ in range(10):
        GuestRepository.increase_request(g1_get.id)
        
    g1_get = GuestRepository.get_guest(uuid = g1_get.id)
    
    print(f'after requests: {g1_get=}')
    
    GuestRepository.delete_guest(uuid=g2_get.id)
    g2_get = GuestRepository.get_guest(uuid=g2_get.id)
    
    print(f'after delete: {g2_get=}')
    
    g3_uuid = '1c9bc47c-6103-4009-a540-9d518d2b9dfe'
    g3 = GuestRepository.get_guest(g3_uuid)
    print(f'{g3=}')
    
    can_request1 = GuestRepository.can_guest_request(uuid=g3.id, max_requests=20, max_minutes=15)
    print(f'{can_request1=}')
    
    can_request2 = GuestRepository.can_guest_request(uuid=g3.id, max_requests=10, max_minutes=40)
    print(f'{can_request2=}')
    
    can_request3 = GuestRepository.can_guest_request(uuid=g3.id, max_requests=20, max_minutes=40)
    print(f'{can_request3=}')
            
