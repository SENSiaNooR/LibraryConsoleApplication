from typing import Optional
from DataAccess.Schema import DBTables
from Models import AuthorModel
from BaseRepository import BaseRepository
from BaseRepository import map_to_model
from psycopg2.extensions import cursor as PgCursor

class AuthorRepository(BaseRepository):

    @classmethod
    @map_to_model(AuthorModel)
    def get_all_authors(cls, cursor : Optional[PgCursor] = None) -> list[AuthorModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
            
        query = (
            f"""
            SELECT
                *
            FROM {DBTables.AUTHOR}
            """
        )

        cursor.execute(query)
        
        result = cursor.fetchall()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result


if __name__ == '__main__':

    a = AuthorRepository.get_all_authors()
    for item in a:
        print(item)