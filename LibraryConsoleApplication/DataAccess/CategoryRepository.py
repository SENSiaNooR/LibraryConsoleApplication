from typing import Optional
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from Models.Models import CategoryModel, CategoryViewModel
from Models.Schema import DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor


class CategoryRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(CategoryModel)
    def get_category(cls, model : CategoryModel, cursor : Optional[PgCursor] = None) -> CategoryModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBTables.CATEGORY,
            cursor=cursor
        )
        
    @classmethod
    @map_to_single_model(CategoryViewModel)
    def get_category_view(cls, model : CategoryViewModel, cursor : Optional[PgCursor] = None) -> CategoryViewModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBViews.CATEGORY_VIEW,
            cursor=cursor
        )
       
    @classmethod
    @map_to_model(CategoryModel)
    def get_categories(cls, model : CategoryModel, cursor : Optional[PgCursor] = None) -> list[CategoryModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBTables.CATEGORY,
            cursor=cursor
        )
    
    @classmethod
    @map_to_model(CategoryViewModel)
    def get_categories_view(cls, model : CategoryViewModel, cursor : Optional[PgCursor] = None) -> list[CategoryViewModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBViews.CATEGORY_VIEW,
            cursor=cursor
        )

    @classmethod
    @map_to_single_model(CategoryModel)
    def add_category(cls, model : CategoryModel, cursor : Optional[PgCursor] = None) -> CategoryModel:
        return CommonQueriesRepository.add_record(
            model=model,
            table=DBTables.CATEGORY,
            cursor=cursor
        )
    
    @classmethod
    def update_category(cls, model: CategoryModel, cursor: Optional[PgCursor] = None) -> None:
        return CommonQueriesRepository.update_record(
            model=model,
            table=DBTables.CATEGORY,
            cursor=cursor
        )

    @classmethod
    def delete_category(cls, id: int, cursor: Optional[PgCursor] = None) -> None:
        return CommonQueriesRepository.delete_record(
            id=id,
            table=DBTables.CATEGORY,
            cursor=cursor
        )
    
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