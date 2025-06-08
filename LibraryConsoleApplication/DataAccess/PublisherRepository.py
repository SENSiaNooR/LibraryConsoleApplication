from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Exceptions import MultipleRowsReturnedError
from DataAccess.Models import CategoryModel, CategoryViewModel, MemberModel, MemberWithoutPasswordViewModel, PublisherModel, PublisherViewModel, UserModel, UserType
from DataAccess.Schema import DBTableColumns, DBTables, DBViewColumns, DBViews
from psycopg2.extensions import cursor as PgCursor
from DataAccess.SqlBuilder import build_insert_clause, build_set_clause, build_where_clause
from DataAccess.UserRepository import UserRepository


class PublisherRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(PublisherModel)
    def get_publisher(cls, model : PublisherModel, cursor : Optional[PgCursor] = None) -> PublisherModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBTables.PUBLISHER,
            cursor=cursor
        )
    
    @classmethod
    @map_to_single_model(PublisherViewModel)
    def get_publisher_view(cls, model : PublisherViewModel, cursor : Optional[PgCursor] = None) -> PublisherViewModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBViews.PUBLISHER_VIEW,
            cursor=cursor
        )
       
    @classmethod
    @map_to_model(PublisherModel)
    def get_publishers(cls, model : PublisherModel, cursor : Optional[PgCursor] = None) -> list[PublisherModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBTables.PUBLISHER,
            cursor=cursor
        )
    
    @classmethod
    @map_to_model(PublisherViewModel)
    def get_publishers_view(cls, model : PublisherViewModel, cursor : Optional[PgCursor] = None) -> list[PublisherViewModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBViews.PUBLISHER_VIEW,
            cursor=cursor
        )

    @classmethod
    @map_to_single_model(PublisherModel)
    def add_publisher(cls, model : PublisherModel, cursor : Optional[PgCursor] = None) -> PublisherModel:
        return CommonQueriesRepository.add_record(
            model=model,
            table=DBTables.PUBLISHER,
            cursor=cursor
        )
    
    @classmethod
    def update_publisher(cls, model: PublisherModel, cursor: Optional[PgCursor] = None) -> None:
        return CommonQueriesRepository.update_record(
            model=model,
            table=DBTables.PUBLISHER,
            cursor=cursor
        )
            
    @classmethod
    def delete_publisher(cls, id: int, cursor: Optional[PgCursor] = None) -> None:
        return CommonQueriesRepository.delete_record(
            id=id,
            table=DBTables.PUBLISHER,
            cursor=cursor
        )
    
if __name__ == '__main__':
    
    model1 = PublisherModel(phone = '071-32223344')
    model2 = PublisherModel(name='ان')
    
    model3 = PublisherViewModel(name= 'نشر نی')
    model4 = PublisherViewModel(books='خط سوم')
    
    model5 = PublisherModel(name = 'نشر پوران هپروت', address = 'کرج', contact_email= 'pooran@gmail.com', phone= '0453-31233145')
    
    res1 = PublisherRepository.get_publisher(model1)
    print(f'res1 = {res1}\n')
    
    res2 = PublisherRepository.get_publishers(model2)
    print('res2 = [')
    for row in res2:
        print(f'\t{row}')
    print(']\n')

    res3 = PublisherRepository.get_publisher_view(model3)
    print(f'res3 = {res3}\n')
    
    res4 = PublisherRepository.get_publishers_view(model4)
    print('res4 = [')
    for row in res4:
        print(f'\t{row}')
    print(']\n')
    
    res5 = PublisherRepository.add_publisher(model5)
    print(f'res5 = {res5}\n')
    
    model6 = PublisherModel(id = res5.id, name='نشر پوران هپروت پلاس', contact_email= 'parro@gmail.com')
    PublisherRepository.update_publisher(model6)
    res6 = PublisherRepository.get_publisher(model6)
    print(f'res6 = {res6}\n')
    
    res7 = PublisherRepository.get_publishers(PublisherModel())
    print('res7 = [')
    for row in res7:
        print(f'\t{row}')
    print(']\n')
        
    PublisherRepository.delete_publisher(id = res5.id)
    


