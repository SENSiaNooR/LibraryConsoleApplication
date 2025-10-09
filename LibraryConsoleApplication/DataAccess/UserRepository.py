from typing import Optional
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from Exceptions.Exceptions import AuthenticationFailed, NotSuchModelInDataBaseError
from Models.Models import PlainUserModel, UserModel, UserType, UserViewModel
from Models.Schema import DBTableColumns, DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor
from Core.PasswordManagement import PasswordManager


class UserRepository(CommonQueriesRepository):
    
    table_name = DBTables.USER
    view_name = DBViews.USER_VIEW
    model_class = UserModel
    view_model_class = UserViewModel
    insert_clause_exclude = {
        DBTableColumns.User.ID    
    }
    set_clause_exclude = {
        DBTableColumns.User.ID    
    }
    where_clause_exclude = {
        DBTableColumns.User.HASHED_PASSWORD    
    }
    

    # Methods
    
    @classmethod
    def verify_user(cls, plain_user_model : PlainUserModel, cursor : Optional[PgCursor] = None) -> bool:
        """
        Verifies a user's credentials by comparing the provided plain password with the stored hash.

        This method retrieves the user record from the database using the provided username,
        then verifies whether the given plain-text password matches the stored hashed password.
        It is typically used during the login process.

        Args:
            plain_user_model (PlainUserModel):
                The plain user data containing the username and password to verify.
            cursor (Optional[PgCursor], optional):
                Existing database cursor. If not provided, a new one will be created automatically.

        Returns:
            bool:
                True if the provided credentials are valid; False otherwise.

        Raises:
            ValueError:
                If the username or password is not a string.
            NotSuchModelInDataBaseError:
                If the user with the specified username does not exist in the database.
            DatabaseError:
                If any database operation fails.
        """
        if (not isinstance(plain_user_model.username, str)) or (not isinstance(plain_user_model.password, str)):
            raise ValueError('username and password must be string')

        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        model = UserModel(username = plain_user_model.username)
        db_model = cls.get_one(model, cursor)
    
        password_manager = PasswordManager()
        
        verification = password_manager.verify_password(
            plain_password=plain_user_model.password,
            hashed_password=db_model.hashed_password
        )
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return verification

    @classmethod
    def hash_password_and_add_user(cls, plain_user_model : PlainUserModel, cursor : Optional[PgCursor] = None) -> UserModel:
        """
        Hashes a user's plain-text password and adds the new user to the database.

        This method takes a plain user model containing a raw (unhashed) password,
        hashes it securely using the `PasswordManager`, and creates a new `UserModel`
        record with the hashed password.  
        It is used internally by repositories (e.g., `LibrarianRepository`, `MemberRepository`)
        when creating new user accounts.

        Args:
            plain_user_model (PlainUserModel):
                The plain user data containing the username and raw password.
            cursor (Optional[PgCursor], optional):
                Existing database cursor. If not provided, a new one will be created automatically.

        Returns:
            UserModel:
                The created user model containing the hashed password, suitable for storage in the database.

        Raises:
            ValueError:
                If the username or password is not a string.
            DatabaseError:
                If the insert operation fails.
        """
        if (not isinstance(plain_user_model.username, str)) or (not isinstance(plain_user_model.password, str)):
            raise ValueError('username and password must be string')
        
        password_manager = PasswordManager()
        hashed_password = password_manager.hash_password(plain_password=plain_user_model.password)
        model = UserModel(
            username=plain_user_model.username,
            hashed_password=hashed_password
        )
        return cls.add(model,cursor)

    @classmethod
    def change_password(cls, plain_user_model : PlainUserModel, new_password : str, cursor : Optional[PgCursor] = None) -> None:
        """
        Change the password of a user after verifying their current credentials.

        The user must provide a valid username and current password to confirm identity.
        After successful verification, the password is securely re-hashed and updated in the database.

        Args:
            plain_user_model (PlainUserModel): 
                A model containing the user's current username and password.
            new_password (str): 
                The new password to be set for the user.
            cursor (Optional[PgCursor], optional): 
                An existing PostgreSQL cursor for transactional use. 
                If not provided, a new one will be created and committed automatically.

        Raises:
            AuthenticationFailed: If the provided username or password is incorrect.

        Returns:
            None
        """
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
        """
        Change a user's password based on their role (used internally by admin or librarian operations).

        This method bypasses direct credential verification and allows role-authorized
        password resets. It is mainly used by higher-privilege users (e.g., Admin for librarians,
        Librarian for members).

        Args:
            username (str): 
                Username of the target user.
            new_password (str): 
                The new password to assign.
            user_type (UserType): 
                The role of the user whose password is being changed.
            cursor (Optional[PgCursor], optional): 
                An existing PostgreSQL cursor. If not provided, a new one will be created.

        Raises:
            NotSuchModelInDataBaseError: If the specified user does not exist in the database.

        Returns:
            None
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        model = UserViewModel(username=username, user_type=user_type)
        user = cls.view_one(model, cursor=cursor)
    
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
        """
        Change a member's password (used by librarians).

        This method allows a librarian to reset a member’s password without requiring the old one.
        Internally delegates to `_change_password_by_role`.

        Args:
            username (str): Username of the member.
            new_password (str): New password to assign.
            cursor (Optional[PgCursor], optional): Database cursor for transactional use.

        Returns:
            None
        """
        cls._change_password_by_role(username, new_password, UserType.member, cursor)

    @classmethod
    def change_librarian_password(cls, username: str, new_password: str, cursor: Optional[PgCursor] = None) -> None:
        """
        Change a librarian's password (used by administrators).

        Allows an admin to reset a librarian’s password without requiring old credentials.
        Internally uses `_change_password_by_role`.

        Args:
            username (str): Username of the librarian.
            new_password (str): New password to assign.
            cursor (Optional[PgCursor], optional): Database cursor for transactional use.

        Returns:
            None
        """
        cls._change_password_by_role(username, new_password, UserType.librarian, cursor)
    
    @classmethod
    def change_username(cls, plain_user_model : PlainUserModel, new_username : str, cursor : Optional[PgCursor] = None) -> None:
        """
        Change a user's username after verifying their current credentials.

        The user must authenticate with their existing username and password before changing it.
        The change is then persisted in the database.

        Args:
            plain_user_model (PlainUserModel): 
                The current username and password of the user.
            new_username (str): 
                The desired new username.
            cursor (Optional[PgCursor], optional): 
                Database cursor for transactional use. 
                If not provided, a new cursor will be created and committed automatically.

        Raises:
            AuthenticationFailed: If the current username or password is invalid.

        Returns:
            None
        """
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


    # Inherited Methods

    @classmethod
    def get_one(cls, model : model_class, cursor : Optional[PgCursor] = None) -> Optional[model_class]:
        return super().get_one(model, cursor)
       
    @classmethod
    def get_many(cls, model : model_class, cursor : Optional[PgCursor] = None) -> list[model_class]:
        return super().get_many(model, cursor)
    
    @classmethod
    def view_one(cls, model : view_model_class, cursor : Optional[PgCursor] = None) -> Optional[view_model_class]:
        return super().view_one(model, cursor)
       
    @classmethod
    def view_many(cls, model : view_model_class, cursor : Optional[PgCursor] = None) -> list[view_model_class]:
        return super().view_many(model, cursor)
    
    @classmethod
    def add(cls, model : model_class, cursor : Optional[PgCursor] = None) -> model_class:
        return super().add(model, cursor)
                
    @classmethod
    def delete(cls, id : int, cursor: Optional[PgCursor] = None) -> None:
        return super().delete(id, cursor)
    

    # Forbidden Methods
           
    @classmethod
    @forbidden_method
    def update(cls, model, cursor: Optional[PgCursor] = None):
        """Disabled method. Not allowed for this repository."""
        pass
                
    @classmethod
    @forbidden_method
    def remove(cls, model, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None):
        """Disabled method. Not allowed for this repository."""
        pass

    @classmethod
    @forbidden_method
    def clear(cls, cursor: Optional[PgCursor] = None):
        """Disabled method. Not allowed for this repository."""
        pass







    


    

        
    
    



    
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
