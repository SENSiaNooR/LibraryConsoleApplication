from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from DataAccess.UserRepository import UserRepository
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.Models import MemberModel, UserModel
from DataAccess.Schema import DBColumns, DBTables
from psycopg2.extensions import cursor as PgCursor


class LibrarianRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(MemberModel)
    def create_member(cls, username : str, hashed_password : str, name : str, email : str, cursor : Optional[PgCursor] = None) -> MemberModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        user_model = UserRepository.create_user(username, hashed_password, cursor)
              
        query = (
            f"""
            INSERT INTO {DBTables.MEMBER} (
                {DBColumns.Member.USER_ID},
                {DBColumns.Member.NAME},
                {DBColumns.Member.EMAIL},
                {DBColumns.Member.JOIN_DATE},
                {DBColumns.Member.ACTIVE}
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
            """
        )
        
        now = datetime.now(ZoneInfo("Asia/Tehran"))
        active = True

        cursor.execute(query, (user_model.id, name, email, now, active))
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
if __name__ == '__main__':
    print(LibrarianRepository.create_member('alkasx12','uisvdfjk','مهدی رضویان کرجی','mahdi454@gmail.com'))

        
    