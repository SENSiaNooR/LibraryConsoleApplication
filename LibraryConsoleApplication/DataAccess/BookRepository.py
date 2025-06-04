
from typing import Optional, Union
from DataAccess.BaseRepository import BaseRepository, map_to_single_model
from DataAccess.Models import BookModel, MemberWithoutPasswordViewModel
from psycopg2.extensions import cursor as PgCursor


class BookRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(BookModel)
    def create_book(
        cls,
        title : str,
        publisher : str,
        categories : Union[list[str], str],
        authors : Union[list[str], str],
        total_copies : int,
        auto_create_relations : bool = False,
        cursor : Optional[PgCursor] = None
    ) -> BookModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = (
            f"""
            SELECT 
                *
            FROM
                {DBViews.MEMBER_WITHOUT_PASSWORD_VIEW} 
            WHERE
                {DBViewColumns.MemberWithoutPasswordView.USERNAME} = %s
            """
        )
        
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result