from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from Exceptions.Exceptions import NotSuchModelInDataBaseError
from Models.Models import GuestModel
from Models.Schema import DBTableColumns, DBTables
from psycopg2.extensions import cursor as PgCursor
import psycopg2.extras

psycopg2.extras.register_uuid()


class GuestRepository(CommonQueriesRepository):

    table_name = DBTables.GUEST
    model_class = GuestModel
    insert_clause_exclude = set()
    set_clause_exclude = {
        DBTableColumns.Guest.ID,
        DBTableColumns.Guest.CREATED_TIME
    }
    where_clause_exclude = {
        DBTableColumns.Guest.CREATED_TIME,
        DBTableColumns.Guest.REQUEST_COUNT
    }
    

    # Methods
    
    @classmethod
    def add(cls, cursor : Optional[PgCursor] = None) -> model_class:
        id = uuid4()
        now = datetime.now(ZoneInfo("Asia/Tehran"))
        model = GuestModel(
            id=id,
            created_time=now,
            request_count=0
        )
        return super().add(model, cursor)
    
    @classmethod
    def increase_request(cls, model : model_class, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
            
        db_model = cls.get_one(model, cursor)
        
        if db_model is None:
            raise NotSuchModelInDataBaseError('can not find guest', model)
        
        db_model.request_count += 1
        
        super().update(db_model, cursor)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

    @classmethod
    def can_guest_request(cls, model : model_class, max_requests: int, max_minutes: int, cursor: Optional[PgCursor] = None) -> bool:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        guest = cls.get_one(model, cursor)

        if guest is None:
            raise NotSuchModelInDataBaseError('can not find guest', GuestModel(id=uuid))

        now = datetime.now(ZoneInfo("Asia/Tehran"))
        delta_minutes = (now - guest.created_time).total_seconds() / 60

        result : bool = True
        
        if guest.request_count >= max_requests or delta_minutes >= max_minutes:
            result = False
    
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result


    # Inherited Methods

    @classmethod
    def get_one(cls, model : model_class, cursor : Optional[PgCursor] = None) -> Optional[model_class]:
        return super().get_one(model, cursor)
                
    @classmethod
    def delete(cls, id : UUID, cursor: Optional[PgCursor] = None) -> None:
        return super().delete(id, cursor)

    @classmethod
    def clear(cls, cursor: Optional[PgCursor] = None) -> None:
        return super().clear(cursor)
    

    # Forbidden Methods
          
    @classmethod
    @forbidden_method
    def get_many(cls, model, cursor : Optional[PgCursor] = None):
        pass
    
    @classmethod
    @forbidden_method
    def view_one(cls, model, cursor : Optional[PgCursor] = None):
        pass
       
    @classmethod
    @forbidden_method
    def view_many(cls, model, cursor : Optional[PgCursor] = None):
        pass
    
    @classmethod
    @forbidden_method
    def update(cls, model, cursor: Optional[PgCursor] = None):
        pass
   
    @classmethod
    @forbidden_method
    def remove(cls, model, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None):
        pass

            
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
            
