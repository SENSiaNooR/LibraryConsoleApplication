
from typing import Optional
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from Models.Models import AuthorModel, BookModel, BookViewModel, CategoryModel, PublisherModel
from psycopg2.extensions import cursor as PgCursor
from Models.Schema import DBTableColumns, DBTables, DBViews


class BookRepository(CommonQueriesRepository):
    
    table_name = DBTables.BOOK
    view_name = DBViews.BOOK_VIEW
    model_class = BookModel
    view_model_class = BookViewModel
    insert_clause_exclude = {
        DBTableColumns.Book.ID
    }
    set_clause_exclude = {
        DBTableColumns.Book.ID
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
    
    book_model = BookModel(
        title='ریاضی یازدهم',
        total_copies=20,
        available_copies=20
    )
    
    publisher_model = PublisherModel(
        name='خیلی سبز',
        address='تهران، انقلاب، روبروی دانشگاه تهران',
        contact_email='kheilisabz@gmail.com',
        phone='021-33433343'
    )
    
    author_models = [
        AuthorModel(
            name='احسان منصوری',
            biography='یه جوان 27 ساله از تهران، ارشد مهندسی برق از دانشگاه تهران'
        ),
        AuthorModel(
            name='مجید کمالی',
            biography='دکتر مجید کمالی، عضو هیئت علمی دانشگاه امیرکبیر'
        )        
    ]
    
    category_models = [
        CategoryModel(
            name='کمک درسی',
            description='کتاب های کمک درسی آموزش و پرورش'
        ), 
        CategoryModel(
            name='ریاضیات',
            description='کتاب های مرتبط با علوم ریاضی'
        ),
        CategoryModel(
            name='نمونه سوال',
            description='کتاب های حاوی نمونه سوالات کنکوری و امتحانی'
        )
    ]

    #res = BookRepository.add_book(
    #    book_model=book_model,
    #    authors_model=author_models,
    #    categories_model=category_models,
    #    publisher_model=publisher_model,
    #    auto_create_relation=True
    #)
    #print(res)

    #res = BookRepository.get_books_full_info(BookViewModel(title='س'))
    #for row in res:
    #    print(row)
    
    #book = BookRepository.get_book(BookModel(title = 'ریاضی یازدهم'))

    #book.available_copies -= 3
    
    #publisher = PublisherModel(name = 'گاج',phone= '021-55443344')

    #BookRepository.update_book(
    #    book_model=book,
    #    publisher_model=publisher,
    #    authors_model=[
    #        AuthorModel(name='کاظم قلمچی'),
    #        AuthorModel(name='رها جهانشاهی')
    #    ],
    #    auto_create_relation=True
    #)
    
    res = BookRepository.get_book(BookModel(available_copies=28))
    print(res)

