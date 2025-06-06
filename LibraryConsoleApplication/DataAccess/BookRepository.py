
from typing import Any, Optional, Union
from DataAccess.CategoryRepository import CategoryRepository
from DataAccess.AuthorRepository import AuthorRepository
from DataAccess.Exceptions import MultipleRowsReturnedError, NotSuchModelInDataBaseError
from DataAccess.PublisherRepository import PublisherRepository
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.Models import AuthorModel, BookAuthorModel, BookCategoryModel, BookModel, BookViewModel, CategoryModel, CategoryViewModel, MemberWithoutPasswordViewModel, PublisherModel, UnsetType
from psycopg2.extensions import cursor as PgCursor
from DataAccess.Schema import DBTableColumns, DBTables, DBViews
from DataAccess.SqlBuilder import build_insert_clause, build_set_clause, build_where_clause


    

class BookRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(BookModel)
    def add_book(
        cls,
        book_model : BookModel,
        authors_model : list[AuthorModel],
        categories_model : list[CategoryModel],
        publisher_model : Optional[PublisherModel] = None,
        auto_create_relation : bool = False,
        cursor : Optional[PgCursor] = None
    ) -> BookModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        p_model : PublisherModel
        a_models : list[AuthorModel] = []
        c_models : list[CategoryModel] = []
        
        if publisher_model is None:
            if (book_model.publisher_id is None) or isinstance(book_model.publisher_id, UnsetType):
                raise ValueError('Must set publisher.')
            
            publisher_model = PublisherModel(id = book_model.publisher_id)
        

        p_model = PublisherRepository.get_publisher(publisher_model, cursor)
        
        if p_model is None:
            if auto_create_relation:
                p_model = PublisherRepository.add_publisher(publisher_model, cursor)
            
            else:
                raise NotSuchModelInDataBaseError('Not such record in Publisher table', publisher_model)
            
        book_model.publisher_id = p_model.id
            
        if not authors_model:
            raise ValueError('at least one author need')
        
        for model in authors_model:
            a_model = AuthorRepository.get_author(model, cursor)
            
            if a_model is None:
                if auto_create_relation:
                    a_model = AuthorRepository.add_author(model, cursor)
                else:
                    raise NotSuchModelInDataBaseError('Not such record in Author table', model)
            
            a_models.append(a_model)
         

        if not categories_model:
            raise ValueError('at least one category need')
            
        for model in categories_model:
            c_model = CategoryRepository.get_category(model, cursor)
            
            if c_model is None:
                if auto_create_relation:
                    c_model = CategoryRepository.add_category(model, cursor)
                else:
                    raise NotSuchModelInDataBaseError('Not such record in Category table', model)
            
            c_models.append(c_model)
         
        columns_clause, placeholders_clause, values = build_insert_clause(book_model)
            
        query = (
            f"""
            INSERT INTO {DBTables.BOOK} (
                {columns_clause}
            ) 
            VALUES({placeholders_clause})
            RETURNING *
            """
        )
        
        cursor.execute(query, values)
        book_result = cursor.fetchone()
        
        b_model = BookModel(*book_result)
        
        for model in a_models:
            cls.add_author_to_book(b_model, model, cursor)
            
        for model in c_models:
            cls.add_category_to_book(b_model, model, cursor)
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return book_result
    
    @classmethod
    @map_to_single_model(BookModel)
    def get_book(cls, model : BookModel, cursor : Optional[PgCursor] = None) -> BookModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model)
        
        if not where_clause:
            raise ValueError("At least one non-null attribute must be provided for filtering.")

        query = (
            f"""
            SELECT * FROM {DBTables.BOOK} 
            WHERE {where_clause}
            """
        )
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 1:
            raise MultipleRowsReturnedError()
        
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    @map_to_single_model(BookViewModel)
    def get_book_view(cls, model : BookViewModel, cursor : Optional[PgCursor] = None) -> BookViewModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model)
        
        if not where_clause:
            raise ValueError("At least one non-null attribute must be provided for filtering.")

        query = (
            f"""
            SELECT * FROM {DBViews.BOOK_VIEW} 
            WHERE {where_clause}
            """
        )
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 1:
            raise MultipleRowsReturnedError()
        
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    @map_to_model(BookModel)
    def get_books(cls, model : BookModel, cursor : Optional[PgCursor] = None) -> list[BookModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model, use_like_for_strings=True)
        
        query : str

        if not where_clause:
            query = (
                f"""
                SELECT * FROM {DBTables.BOOK} 
                """
            )
            cursor.execute(query)
        else:
            query = (
                f"""
                SELECT * FROM {DBTables.BOOK} 
                WHERE {where_clause}
                """
            )
            cursor.execute(query, values)

        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    @map_to_model(BookViewModel)
    def get_books_view(cls, model : BookViewModel, cursor : Optional[PgCursor] = None) -> list[BookViewModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model, use_like_for_strings=True)
        
        query : str

        if not where_clause:
            query = (
                f"""
                SELECT * FROM {DBViews.BOOK_VIEW} 
                """
            )
            cursor.execute(query)
        else:
            query = (
                f"""
                SELECT * FROM {DBViews.BOOK_VIEW} 
                WHERE {where_clause}
                """
            )
            cursor.execute(query, values)
        
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result

    @classmethod
    @map_to_single_model(BookAuthorModel)
    def add_author_to_book(cls, book_model : BookModel, author_model : AuthorModel, cursor : Optional[PgCursor] = None) -> BookAuthorModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
            
        b_model = cls.get_book(book_model, cursor)
        a_model = AuthorRepository.get_author(author_model, cursor)
        
        if b_model is None:
            raise NotSuchModelInDataBaseError('book not found', book_model)
        
        if a_model is None:
            raise NotSuchModelInDataBaseError('author not found', author_model)
                   
        query = (
            f"""
            INSERT INTO {DBTables.BOOK_AUTHOR} (
                {DBTableColumns.BookAuthor.BOOK_ID},
                {DBTableColumns.BookAuthor.AUTHOR_ID}
            ) 
            VALUES(%s, %s)
            RETURNING *
            """
        )
        
        cursor.execute(query, (b_model.id, a_model.id))
        result = cursor.fetchone()

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result

    @classmethod
    @map_to_single_model(BookCategoryModel)
    def add_category_to_book(cls, book_model : BookModel, category_model : CategoryModel, cursor : Optional[PgCursor] = None) -> BookCategoryModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
            
        b_model = cls.get_book(book_model, cursor)
        c_model = CategoryRepository.get_category(category_model, cursor)
        
        if b_model is None:
            raise NotSuchModelInDataBaseError('book not found', book_model)
        
        if c_model is None:
            raise NotSuchModelInDataBaseError('category not found', category_model)
                   
        query = (
            f"""
            INSERT INTO {DBTables.BOOK_CATEGORY} (
                {DBTableColumns.BookCategory.BOOK_ID},
                {DBTableColumns.BookCategory.CATEGORY_ID}
            ) 
            VALUES(%s, %s)
            RETURNING *
            """
        )
        
        cursor.execute(query, (b_model.id, c_model.id))
        result = cursor.fetchone()

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    def _delete_book_categories(cls, book_id: int, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
                    
        query = (
            f"""
            DELETE FROM {DBTables.BOOK_CATEGORY} 
            WHERE {DBTableColumns.BookCategory.BOOK_ID} = %s
            """
        )
        
        cursor.execute(query, (book_id,))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

    @classmethod
    def _delete_book_authors(cls, book_id: int, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
                   
        query = (
            f"""
            DELETE FROM {DBTables.BOOK_AUTHOR} 
            WHERE {DBTableColumns.BookAuthor.BOOK_ID} = %s
            """
        )
        
        cursor.execute(query, (book_id,))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

    @classmethod
    def _replace_authors(cls, book_id: int, authors : list[AuthorModel], auto_create : bool = False, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
            
        cls._delete_book_authors()
        for a in authors:
            author = AuthorRepository.get_author(a, cursor)
            if not author:
                if auto_create:
                    author = AuthorRepository.add_author(a, cursor)
                else:
                    raise NotSuchModelInDataBaseError("Author not found", a)
            cls.add_author_to_book(BookModel(id=book_id), author, cursor)
            
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def _replace_categories(cls, book_id: int, categories : list[CategoryModel], auto_create : bool = False, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
          
        cls._delete_book_categories()
        for c in categories:
            category = CategoryRepository.get_category(c, cursor)
            if not category:
                if auto_create:
                    category = CategoryRepository.add_category(c, cursor)
                else:
                    raise NotSuchModelInDataBaseError("Category not found", c)
            cls.add_category_to_book(BookModel(id=book_id), category, cursor)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

    @classmethod
    def update_book(
        cls,
        book_model: BookModel,
        publisher_model: Optional[PublisherModel] = None,
        authors_model: Optional[list[AuthorModel]] = None,
        categories_model: Optional[list[CategoryModel]] = None,
        auto_create_relation: bool = False,
        cursor: Optional[PgCursor] = None
    ) -> None:
        
        if book_model.id is None:
            raise ValueError('Book id is required')

        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        p_model : Optional[PublisherModel] = None
        
        if publisher_model is not None:
            p_model = PublisherRepository.get_publisher(publisher_model, cursor)
            
            if p_model is None:
                if auto_create_relation:
                    p_model = PublisherRepository.add_publisher(publisher_model, cursor)
                
                else:
                    raise NotSuchModelInDataBaseError('Not such record in Publisher table', publisher_model)
 
        elif book_model.publisher_id is None:
            raise ValueError('Book must have publisher')
        
        elif not isinstance(book_model.publisher_id, UnsetType):
            p_model = PublisherRepository.get_publisher(PublisherModel(id = book_model.publisher_id), cursor)
            
            if p_model is None:
                 raise NotSuchModelInDataBaseError('Not such record in Publisher table', publisher_model)
            
        if p_model is not None:
            book_model.publisher_id = p_model.id
        
        set_clause, values = build_set_clause(book_model)

        query = f"""
            UPDATE {DBTables.BOOK}
            SET {set_clause}
            WHERE {DBTableColumns.Publisher.ID} = %s
        """
        values.append(book_model.id)
        
        cursor.execute(query, values)
        
        if authors_model:
            cls._replace_authors(book_model.id, authors_model, auto_create_relation, cursor)


        if categories_model:
            cls._replace_categories(book_model.id, categories_model, auto_create_relation, cursor)
            
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
       
    @classmethod
    def delete_book(cls, id: int, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        query = f"""
            DELETE FROM {DBTables.BOOK}
            WHERE {DBTableColumns.Book.ID} = %s
        """
        cursor.execute(query, (id,))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()


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

