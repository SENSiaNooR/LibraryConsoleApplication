from typing import Optional
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from Models.Schema import DBTables, DBViews
from Models.Models import AuthorModel, AuthorViewModel
from BaseRepository import BaseRepository, map_to_single_model
from BaseRepository import map_to_model
from psycopg2.extensions import cursor as PgCursor

class AuthorRepository(BaseRepository):

    @classmethod
    @map_to_single_model(AuthorModel)
    def get_category(cls, model : AuthorModel, cursor : Optional[PgCursor] = None) -> AuthorModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBTables.AUTHOR,
            cursor=cursor
        )
        
    @classmethod
    @map_to_single_model(AuthorViewModel)
    def get_category_view(cls, model : AuthorViewModel, cursor : Optional[PgCursor] = None) -> AuthorViewModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBViews.AUTHOR_VIEW,
            cursor=cursor
        )
       
    @classmethod
    @map_to_model(AuthorModel)
    def get_categories(cls, model : AuthorModel, cursor : Optional[PgCursor] = None) -> list[AuthorModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBTables.AUTHOR,
            cursor=cursor
        )
    
    @classmethod
    @map_to_model(AuthorViewModel)
    def get_categories_view(cls, model : AuthorViewModel, cursor : Optional[PgCursor] = None) -> list[AuthorViewModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBViews.AUTHOR_VIEW,
            cursor=cursor
        )

    @classmethod
    @map_to_single_model(AuthorModel)
    def add_category(cls, model : AuthorModel, cursor : Optional[PgCursor] = None) -> AuthorModel:
        return CommonQueriesRepository.add_record(
            model=model,
            table=DBTables.AUTHOR,
            cursor=cursor
        )
    
    @classmethod
    def update_category(cls, model: AuthorModel, cursor: Optional[PgCursor] = None) -> None:
        return CommonQueriesRepository.update_record(
            model=model,
            table=DBTables.AUTHOR,
            cursor=cursor
        )

    @classmethod
    def delete_category(cls, id: int, cursor: Optional[PgCursor] = None) -> None:
        return CommonQueriesRepository.delete_record(
            id=id,
            table=DBTables.AUTHOR,
            cursor=cursor
        )
    


if __name__ == '__main__':

    pass