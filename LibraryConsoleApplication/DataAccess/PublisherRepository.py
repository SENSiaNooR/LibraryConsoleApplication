from typing import Optional
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from Models.Models import PublisherModel, PublisherViewModel
from Models.Schema import DBTableColumns, DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor


class PublisherRepository(CommonQueriesRepository):
    
    table_name = DBTables.PUBLISHER
    view_name = DBViews.PUBLISHER_VIEW
    model_class = PublisherModel
    view_model_class = PublisherViewModel
    insert_clause_exclude = {
        DBTableColumns.Publisher.ID    
    }
    set_clause_exclude = {
        DBTableColumns.Publisher.ID    
    }
    where_clause_exclude = set()


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
    def add(cls, model : model_class, cursor : Optional[PgCursor] = None) -> model_class:
        return super().add(model, cursor)
    
    @classmethod
    def update(cls, model : model_class, cursor: Optional[PgCursor] = None) -> None:
        return super().update(model, cursor)
            
    @classmethod
    def delete(cls, id : int, cursor: Optional[PgCursor] = None) -> None:
        return super().delete(id, cursor)
    

    # Forbidden Methods
    
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
    


