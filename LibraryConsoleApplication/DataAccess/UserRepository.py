from typing import Optional
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.Exceptions import AuthenticationFailed, MultipleRowsReturnedError, NotSuchModelInDataBaseError
from DataAccess.Models import MemberModel, UserModel, UserType, UserViewModel
from DataAccess.Schema import DBTableColumns, DBTables, DBTypes, DBViewColumns, DBViews
from psycopg2.extensions import cursor as PgCursor

from DataAccess.SqlBuilder import build_insert_clause, build_set_clause, build_where_clause
from PasswordManagement import PasswordManager


class UserRepository(BaseRepository):
    
    @classmethod
    def verify_user(cls, username : str, password : str, cursor : Optional[PgCursor] = None) -> bool:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = (
            f"""
            SELECT * FROM {DBTables.USER} 
            WHERE {DBTableColumns.User.USERNAME} = %s
            """
        )
        
        cursor.execute(query, (username,))
        
        if cursor.rowcount == 0:
            return False
     
        user = cursor.fetchone()
        user_model = UserModel(*user)
        
        password_manager = PasswordManager()
        
        verification = password_manager.verify_password(
            plain_password=password,
            hashed_password=user_model.hashed_password
        )
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return verification

    @classmethod
    @map_to_single_model(UserModel)
    def get_user(cls, model : UserModel, cursor : Optional[PgCursor] = None) -> UserModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(model, exclude={DBTableColumns.User.HASHED_PASSWORD})
        
        if not where_clause:
            raise ValueError("At least one non-null attribute must be provided for filtering.")

        query = (
            f"""
            SELECT * FROM {DBTables.USER} 
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
    @map_to_single_model(UserViewModel)
    def get_user_view(cls, model : UserViewModel, cursor : Optional[PgCursor] = None) -> UserViewModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
            
        where_clause, values = build_where_clause(model, exclude={DBViewColumns.UserView.HASHED_PASSWORD})
        
        if not where_clause:
            raise ValueError("At least one non-null attribute must be provided for filtering.")

        query = (
            f"""
            SELECT * FROM {DBViews.USER_VIEW} 
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
    @map_to_model(UserModel)
    def get_users(cls, model : UserModel, cursor : Optional[PgCursor] = None) -> list[UserModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(
            model=model, 
            use_like_for_strings=True, 
            exclude={DBTableColumns.User.HASHED_PASSWORD}
        )
        
        if not where_clause:
            query = (
                f"""
                SELECT * FROM {DBTables.USER} 
                """
            )
            cursor.execute(query)
            
        else:
            query = (
                f"""
                SELECT * FROM {DBTables.USER}
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
    @map_to_model(UserViewModel)
    def get_users_view(cls, model : UserViewModel, cursor : Optional[PgCursor] = None) -> list[UserViewModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        where_clause, values = build_where_clause(
            model=model, 
            use_like_for_strings=True,
            exclude={DBViewColumns.UserView.HASHED_PASSWORD}
        )
        
        if not where_clause:
            query = (
                f"""
                SELECT * FROM {DBViews.USER_VIEW} 
                """
            )
            cursor.execute(query)
            
        else:
            query = (
                f"""
                SELECT * FROM {DBViews.USER_VIEW}
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
    def hash_password_and_add_user(cls, username : str, password : str, cursor : Optional[PgCursor] = None) -> UserModel:
        
        password_manager = PasswordManager()
        hashed_password = password_manager.hash_password(plain_password=password)
        model = UserModel(
            username=username,
            hashed_password=hashed_password
        )
        return cls.add_user(model,cursor)

    @classmethod
    @map_to_single_model(UserModel)
    def add_user(cls, model : UserModel, cursor : Optional[PgCursor] = None) -> UserModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        columns_clause, placeholders_clause, values = build_insert_clause(model)

        query = (
            f"""
            INSERT INTO {DBTables.USER} (
                {columns_clause}
            )
            VALUES ({placeholders_clause})
            RETURNING *
            """
        )
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    def change_password(cls, username : str, password : str, new_password : str, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        verification = cls.verify_user(username, password, cursor)
        
        if not verification:
            raise AuthenticationFailed('Username or password is wrong')

        password_manager = PasswordManager()
        new_hashed_password = password_manager.hash_password(new_password)

        query = (
            f"""
            UPDATE {DBTables.USER} 
            SET {DBTableColumns.User.HASHED_PASSWORD} = %s
            WHERE {DBTableColumns.User.USERNAME} = %s
            """
        )
        
        cursor.execute(query, (new_hashed_password, username))
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

    @classmethod
    def _change_password_by_role(cls, username: str, new_password: str, user_type: UserType, cursor: Optional[PgCursor] = None) -> None:
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        model = UserViewModel(username=username, user_type=user_type)
        user = cls.get_user_view(model, cursor=cursor)
    
        if not user:
            raise NotSuchModelInDataBaseError(f"Cannot find {user_type.value}", model)

        password_manager = PasswordManager()
        new_hashed_password = password_manager.hash_password(new_password)

        query = f"""
            UPDATE {DBTables.USER}
            SET {DBTableColumns.User.HASHED_PASSWORD} = %s
            WHERE {DBTableColumns.User.USERNAME} = %s
        """
        cursor.execute(query, (new_hashed_password, username))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
        
    @classmethod
    def change_member_password(cls, username: str, new_password: str, cursor: Optional[PgCursor] = None) -> None:
        cls._change_password_by_role(username, new_password, UserType.member, cursor)

    @classmethod
    def change_librarian_password(cls, username: str, new_password: str, cursor: Optional[PgCursor] = None) -> None:
        cls._change_password_by_role(username, new_password, UserType.librarian, cursor)
    
    @classmethod
    def change_username(cls, username : str, password : str, new_username : str, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        verification = cls.verify_user(username, password, cursor)
        
        if not verification:
            raise AuthenticationFailed('Username or password is wrong')

        query = (
            f"""
            UPDATE {DBTables.USER} 
            SET {DBTableColumns.User.USERNAME} = %s
            WHERE {DBTableColumns.User.USERNAME} = %s
            """
        )
        
        cursor.execute(query, (new_username, username))
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
    
    @classmethod
    def delete_user(cls, username: str, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = f"""
            DELETE FROM {DBTables.USER}
            WHERE {DBTableColumns.User.USERNAME} = %s
        """
    
        cursor.execute(query, (username,))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
    
if __name__ == '__main__':
    
    UserRepository.delete_user('hajhaj3232')
    UserRepository.delete_user('hajhaj4343')
    UserRepository.delete_user('hajhaj5454')

    ##############################################################################################################################

    model1 = UserModel(username='omidzzz')
    model2 = UserModel(hashed_password='$argon2id$v=19$m=102400,t=2,p=8$jEtzc2L7BKyAQxfB62w/rQ$iJMtBhsaDqiqERerdkLbu33i+ERUxgjd4UbXRa54Mno')
    model3 = UserModel(id = 10)

    res1 = UserRepository.get_user(model1)
    print(f'res1 = {res1}\n\n')
    
    try:
        res2 = UserRepository.get_user(model2)
        print(f'res2 = {res2}\n\n')
    except Exception as ex:
        print(f'res2 = {ex}\n\n')
        
    res3 = UserRepository.get_user(model3)
    print(f'res3 = {res3}\n\n')
    
    ##############################################################################################################################
    
    res4 = UserRepository.verify_user('sensian', '82sen82abc')
    print(f'res4 = {res4}\n\n')
    
    res5 = UserRepository.verify_user('sensian', '82SEN82ABC')
    print(f'res5 = {res5}\n\n')

    ##############################################################################################################################
    
    models1 = UserRepository.get_users(UserModel())
    models2 = UserRepository.get_users_view(UserViewModel())
    models3 = UserRepository.get_users_view(UserViewModel(user_type=UserType.member))
    
    print('models1 = [')
    for model in models1:
        print(f'\t{model}')
    print(']\n\n')

    print('models2 = [')
    for model in models2:
        print(f'\t{model}')
    print(']\n\n')

    print('models3 = [')
    for model in models3:
        print(f'\t{model}')
    print(']\n\n')
    
    ##############################################################################################################################
    
    model4 = UserModel(id = 1, username='hajhaj3232', hashed_password='hashed_password example dwsncksdjcndkc')
    
    res6 = UserRepository.add_user(model4)
    print(f'res6 = {res6}\n\n')
    
    res7 = UserRepository.hash_password_and_add_user(username='hajhaj4343', password='12121212')
    print(f'res7 = {res7}\n\n')
    
    res8 = UserRepository.verify_user('hajhaj4343', password='12121211')
    res9 = UserRepository.verify_user('hajhaj4343', password='12121212')
    
    print(f'res8 = {res8}\n\n')
    print(f'res9 = {res9}\n\n')
    
    ##############################################################################################################################

    try:
        UserRepository.change_password('hajhaj4343', '12121211', '87654321')
    except Exception as ex:
        print(f'{ex}\n\n')
     
    UserRepository.change_password('hajhaj4343', '12121212', '87654321')
    
    res10 = UserRepository.verify_user('hajhaj4343', password='87654321')
    print(f'res10 = {res10}\n\n')
    
    ##############################################################################################################################
    
    try:
        UserRepository.change_member_password(username='hajhaj4343', new_password='88776655')
    except Exception as ex:
        print(f'{ex}\n\n')
        
    ##############################################################################################################################
    
    UserRepository.change_username('hajhaj4343', '87654321', 'hajhaj5454')
    res11 = UserRepository.get_user_view(UserViewModel(username='hajhaj5454'))
    
    print(f'res11 = {res11}\n\n')
    
    ##############################################################################################################################