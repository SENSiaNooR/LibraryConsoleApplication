from typing import Optional
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from Models.Models import LibrarianModel, LibrarianViewModel, PlainUserModel
from Models.Schema import DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor
from DataAccess.UserRepository import UserRepository


class LibrarianRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(LibrarianModel)
    def get_librarian(cls, model : LibrarianModel, cursor : Optional[PgCursor] = None) -> LibrarianModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBTables.LIBRARIAN,
            cursor=cursor
        )
    
    @classmethod
    @map_to_model(LibrarianModel)
    def get_all_librarians(cls, cursor : Optional[PgCursor] = None) -> list[LibrarianModel]:
        return CommonQueriesRepository.get_records(
            model=LibrarianModel(),
            table=DBTables.LIBRARIAN,
            cursor=cursor
        )

    @classmethod
    @map_to_single_model(LibrarianViewModel)
    def get_librarian_view(cls, model : LibrarianViewModel, cursor : Optional[PgCursor] = None) -> LibrarianViewModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBViews.LIBRARIAN_VIEW,
            cursor=cursor
        )
    
    @classmethod
    @map_to_model(LibrarianViewModel)
    def get_all_librarians_view(cls, cursor : Optional[PgCursor] = None) -> list[LibrarianViewModel]:
        return CommonQueriesRepository.get_records(
            model=LibrarianViewModel(),
            table=DBViews.LIBRARIAN_VIEW,
            cursor=cursor
        )
          
    @classmethod
    @map_to_single_model(LibrarianModel)
    def add_librarian(cls, plain_user_model : PlainUserModel, name : str, cursor : Optional[PgCursor] = None) -> LibrarianModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        user_model = UserRepository.hash_password_and_add_user(plain_user_model, cursor)
         
        librarian_model = LibrarianModel(
            id=user_model.id,
            name=name
        )

        result = CommonQueriesRepository.add_record(
            model=librarian_model,
            table=DBTables.LIBRARIAN,
            exclude=set(),
            cursor=cursor
        )
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result

    @classmethod
    def change_name(cls, model: LibrarianModel, cursor: Optional[PgCursor] = None) -> None:  
        return CommonQueriesRepository.update_record(
            model=model,
            table=DBTables.LIBRARIAN,
            cursor=cursor
        )
 
if __name__ == '__main__':
    pass
    


        
    