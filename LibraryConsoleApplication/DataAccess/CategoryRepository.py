from typing import Optional
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from Models.Models import CategoryModel, CategoryViewModel
from Models.Schema import DBTableColumns, DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor


class CategoryRepository(CommonQueriesRepository):
    
    table_name = DBTables.CATEGORY
    view_name = DBViews.CATEGORY_VIEW
    model_class = CategoryModel
    view_model_class = CategoryViewModel
    insert_clause_exclude = {
        DBTableColumns.Category.ID
    }
    set_clause_exclude = {
        DBTableColumns.Category.ID
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
        pass
    
    @classmethod
    @forbidden_method
    def clear(cls, cursor: Optional[PgCursor] = None):
        pass
 
    

if __name__ == '__main__':
    model1 = CategoryModel(name= 'جنگ')
    model2 = CategoryModel(description='آثاری')
    
    model3 = CategoryViewModel(name='داستان کوتاه')
    model4 = CategoryViewModel(books='ریاضی یازدهم')
    
    model5 = CategoryModel(name = 'دینی',description= 'توضیحات مربوطه...')
    
    res1 = CategoryRepository.get_category(model1)
    print(f'res1 = {res1}\n')
    
    res2 = CategoryRepository.get_categories(model2)
    print('res2 = [')
    for row in res2:
        print(f'\t{row}')
    print(']\n')

    res3 = CategoryRepository.get_category_view(model3)
    print(f'res3 = {res3}\n')
    
    res4 = CategoryRepository.get_categories_view(model4)
    print('res4 = [')
    for row in res4:
        print(f'\t{row}')
    print(']\n')
    
    res5 = CategoryRepository.add_category(model5)
    print(f'res5 = {res5}\n')
    
    model6 = CategoryModel(id = res5.id, name='دینی و الهی', description='توضیحات مربوطه جدید...')
    
    CategoryRepository.update_category(model6)
    res6 = CategoryRepository.get_category(model6)
    print(f'res6 = {res6}\n')
    
    res7 = CategoryRepository.get_categories(CategoryModel())
    print('res7 = [')
    for row in res7:
        print(f'\t{row}')
    print(']\n')
        
    CategoryRepository.delete_category(id = res5.id)