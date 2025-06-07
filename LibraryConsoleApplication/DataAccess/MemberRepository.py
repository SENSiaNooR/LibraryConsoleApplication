from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from DataAccess.BaseRepository import BaseRepository, map_to_single_model
from DataAccess.Exceptions import MemberAlreadyDeactivatedError
from DataAccess.Models import MemberModel, MemberWithoutPasswordViewModel, UserModel, UserType
from DataAccess.Schema import DBTableColumns, DBTables, DBViewColumns, DBViews
from psycopg2.extensions import cursor as PgCursor
from DataAccess.UserRepository import UserRepository


class MemberRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(MemberWithoutPasswordViewModel)
    def get_member_without_password(cls, username : str, cursor : Optional[PgCursor] = None) -> MemberWithoutPasswordViewModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = (
            f"""
            SELECT * FROM {DBViews.MEMBER_WITHOUT_PASSWORD_VIEW} 
            WHERE {DBViewColumns.MemberWithoutPasswordView.USERNAME} = %s
            """
        )
        
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    def deactivate_member(cls, username : str, cursor : Optional[PgCursor] = None):
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        member_without_password_model = cls.get_member_without_password(username, cursor)
        
        if member_without_password_model is None:
            raise ValueError('no any member with this username')
        
        if member_without_password_model.active == False:
            raise MemberAlreadyDeactivatedError(f'member {member_without_password_model.name} is already deactive.')
        
        query = (
            f"""
            UPDATE {DBTables.MEMBER}
            SET 
	            {DBTableColumns.Member.ACTIVE} = %s
            WHERE
	            {DBTableColumns.Member.USER_ID} = %s
            """
        )
        
        cursor.execute(query, (False, member_without_password_model.id))
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def activate_member(cls, username : str, cursor : Optional[PgCursor] = None):
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        member_without_password_model = cls.get_member_without_password(username, cursor)
        
        if member_without_password_model is None:
            raise ValueError('no any member with this username')
        
        if member_without_password_model.active == True:
            raise MemberAlreadyDeactivatedError(f'member {member_without_password_model.name} is already active.')
        
        query = (
            f"""
            UPDATE {DBTables.MEMBER}
            SET 
	            {DBTableColumns.Member.ACTIVE} = %s
            WHERE
	            {DBTableColumns.Member.USER_ID} = %s
            """
        )
        
        cursor.execute(query, (True, member_without_password_model.id))
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def update_member_password(cls, username : str, new_hashed_password : str, cursor : Optional[PgCursor] = None):
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        user_model = UserRepository.get_user(username, UserType.member, cursor)
        
        if user_model is None:
            raise ValueError('no any member with this username')
        

        query = (
            f"""
            UPDATE {DBTables.USER}
            SET 
	            {DBTableColumns.User.HASHED_PASSWORD} = %s
            WHERE
	            {DBTableColumns.User.ID} = %s and
	            {DBTableColumns.User.USERNAME} = %s
            """
        )
        
        cursor.execute(query, (new_hashed_password, user_model.id, user_model.username))
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    @map_to_single_model(MemberModel)
    def add_member(cls, username : str, hashed_password : str, name : str, email : str, cursor : Optional[PgCursor] = None) -> MemberModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        user_model = UserRepository.add_user(username, hashed_password, cursor)
              
        query = (
            f"""
            INSERT INTO {DBTables.MEMBER} (
                {DBTableColumns.Member.USER_ID},
                {DBTableColumns.Member.NAME},
                {DBTableColumns.Member.EMAIL},
                {DBTableColumns.Member.JOIN_DATE},
                {DBTableColumns.Member.ACTIVE}
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


