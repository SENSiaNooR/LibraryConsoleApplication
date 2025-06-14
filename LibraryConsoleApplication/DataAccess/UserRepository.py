from typing import Optional
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from Exceptions.Exceptions import AuthenticationFailed, NotSuchModelInDataBaseError
from Models.Models import PlainUserModel, UserModel, UserType, UserViewModel
from Models.Schema import DBTableColumns, DBTables, DBViewColumns, DBViews
from psycopg2.extensions import cursor as PgCursor
from PasswordManagement import PasswordManager


class UserRepository(BaseRepository):
    
    @classmethod
    def verify_user(cls, plain_user_model : PlainUserModel, cursor : Optional[PgCursor] = None) -> bool:
        
        if (not isinstance(plain_user_model.username, str)) or (not isinstance(plain_user_model.password, str)):
            raise ValueError('username and password must be string')

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
        
        cursor.execute(query, (plain_user_model.username,))
        
        if cursor.rowcount == 0:
            return False
     
        user = cursor.fetchone()
        user_model = UserModel(*user)
        
        password_manager = PasswordManager()
        
        verification = password_manager.verify_password(
            plain_password=plain_user_model.password,
            hashed_password=user_model.hashed_password
        )
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return verification

    @classmethod
    @map_to_single_model(UserModel)
    def get_user(cls, model : UserModel, cursor : Optional[PgCursor] = None) -> UserModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBTables.USER,
            exclude={DBTableColumns.User.HASHED_PASSWORD},
            cursor=cursor
        )
        
    @classmethod
    @map_to_single_model(UserViewModel)
    def get_user_view(cls, model : UserViewModel, cursor : Optional[PgCursor] = None) -> UserViewModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBViews.USER_VIEW,
            exclude={DBViewColumns.UserView.HASHED_PASSWORD},
            cursor=cursor
        )
       
    @classmethod
    @map_to_model(UserModel)
    def get_users(cls, model : UserModel, cursor : Optional[PgCursor] = None) -> list[UserModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBTables.USER,
            exclude={DBTableColumns.User.HASHED_PASSWORD},
            cursor=cursor
        )
    
    @classmethod
    @map_to_model(UserViewModel)
    def get_users_view(cls, model : UserViewModel, cursor : Optional[PgCursor] = None) -> list[UserViewModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBViews.USER_VIEW,
            exclude={DBViewColumns.UserView.HASHED_PASSWORD},
            cursor=cursor
        )

    @classmethod
    def hash_password_and_add_user(cls, plain_user_model : PlainUserModel, cursor : Optional[PgCursor] = None) -> UserModel:
        if (not isinstance(plain_user_model.username, str)) or (not isinstance(plain_user_model.password, str)):
            raise ValueError('username and password must be string')
        
        password_manager = PasswordManager()
        hashed_password = password_manager.hash_password(plain_password=plain_user_model.password)
        model = UserModel(
            username=plain_user_model.username,
            hashed_password=hashed_password
        )
        return cls.add_user(model,cursor)

    @classmethod
    @map_to_single_model(UserModel)
    def add_user(cls, model : UserModel, cursor : Optional[PgCursor] = None) -> UserModel:
        return CommonQueriesRepository.add_record(
            model=model,
            table=DBTables.USER,
            cursor=cursor
        )
    
    @classmethod
    def change_password(cls, plain_user_model : PlainUserModel, new_password : str, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        verification = cls.verify_user(plain_user_model, cursor)
        
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
        
        cursor.execute(query, (new_hashed_password, plain_user_model.username))
        
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
    def change_username(cls, plain_user_model : PlainUserModel, new_username : str, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        verification = cls.verify_user(plain_user_model, cursor)
        
        if not verification:
            raise AuthenticationFailed('Username or password is wrong')

        query = (
            f"""
            UPDATE {DBTables.USER} 
            SET {DBTableColumns.User.USERNAME} = %s
            WHERE {DBTableColumns.User.USERNAME} = %s
            """
        )
        
        cursor.execute(query, (new_username, plain_user_model.username))
        
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
    
    res4 = UserRepository.verify_user(PlainUserModel('sensian', '82sen82abc'))
    print(f'res4 = {res4}\n\n')
    
    res5 = UserRepository.verify_user(PlainUserModel('sensian', '82SEN82ABC'))
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
    
    res7 = UserRepository.hash_password_and_add_user(PlainUserModel(username='hajhaj4343', password='12121212'))
    print(f'res7 = {res7}\n\n')
    
    res8 = UserRepository.verify_user(PlainUserModel('hajhaj4343', password='12121211'))
    res9 = UserRepository.verify_user(PlainUserModel('hajhaj4343', password='12121212'))
    
    print(f'res8 = {res8}\n\n')
    print(f'res9 = {res9}\n\n')
    
    ##############################################################################################################################

    try:
        UserRepository.change_password(PlainUserModel('hajhaj4343', '12121211'), '87654321')
    except Exception as ex:
        print(f'{ex}\n\n')
     
    UserRepository.change_password(PlainUserModel('hajhaj4343', '12121212'), '87654321')
    
    res10 = UserRepository.verify_user(PlainUserModel('hajhaj4343', password='87654321'))
    print(f'res10 = {res10}\n\n')
    
    ##############################################################################################################################
    
    try:
        UserRepository.change_member_password(username='hajhaj4343', new_password='88776655')
    except Exception as ex:
        print(f'{ex}\n\n')
        
    ##############################################################################################################################
    
    UserRepository.change_username(PlainUserModel('hajhaj4343', '87654321'), 'hajhaj5454')
    res11 = UserRepository.get_user_view(UserViewModel(username='hajhaj5454'))
    
    print(f'res11 = {res11}\n\n')
    
    ##############################################################################################################################
