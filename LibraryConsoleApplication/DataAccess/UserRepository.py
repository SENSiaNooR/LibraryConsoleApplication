from typing import Optional
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.Models import MemberModel, UserModel
from DataAccess.Schema import DBColumns, DBTables
from psycopg2.extensions import cursor as PgCursor


class UserRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(UserModel)
    def create_user(cls, username : str, hashed_password : str, cursor : Optional[PgCursor] = None) -> UserModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = (
            f"""
            INSERT INTO {DBTables.USER} (
                {DBColumns.User.USERNAME},
                {DBColumns.User.HASHED_PASSWORD}
            ) 
            VALUES (%s, %s)
            RETURNING *
            """
        )
        
        cursor.execute(query, (username, hashed_password))
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
if __name__ == '__main__':
    print(UserRepository.create_user('alkasx32','uisvdfjk'))
