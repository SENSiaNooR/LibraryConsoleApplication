from typing import Optional
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.Models import MemberModel, UserModel, UserType, UserViewModel
from DataAccess.Schema import DBTableColumns, DBTables, DBTypes, DBViewColumns, DBViews
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
                {DBTableColumns.User.USERNAME},
                {DBTableColumns.User.HASHED_PASSWORD}
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


    @classmethod
    @map_to_single_model(UserViewModel)
    def get_user(cls, username : str, role : Optional[UserType] = None, cursor : Optional[PgCursor] = None) -> UserViewModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        query : str

        if role is None:
            query = (
                f"""
                SELECT
                    *
                FROM {DBViews.USER_VIEW}
                WHERE
                    {DBViewColumns.UserView.USERNAME} = %s
                """
            )
            cursor.execute(query, (username,))
            
        else:
            query = (
                f"""
                SELECT
                    *
                FROM {DBViews.USER_VIEW}
                WHERE
                    {DBViewColumns.UserView.USERNAME} = %s AND
                    {DBViewColumns.UserView.USER_TYPE} = %s :: {DBTypes.USER_TYPE}
                """
            ) 
            cursor.execute(query, (username, role.value))
        
        
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
if __name__ == '__main__':
    #print(UserRepository.create_user('alkasx1','uisvdfjk'))
    
    res = UserRepository.get_user(username = 'omidzzz', role = UserType.admin)
    
    print(res)
