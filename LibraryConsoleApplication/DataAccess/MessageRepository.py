
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from DataAccess.Decorators import forbidden_method
from Exceptions.Exceptions import NotSuchModelInDataBaseError
from DataAccess.UserRepository import UserRepository
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.BaseRepository import map_to_model
from Models.Models import MessageModel, MessageViewModel, UserModel
from Models.Schema import DBTableColumns, DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor


class MessageRepository(CommonQueriesRepository):
    
    table_name = DBTables.MESSAGE
    view_name = DBViews.MESSAGE_VIEW
    model_class = MessageModel
    view_model_class = MessageViewModel
    insert_clause_exclude = {
        DBTableColumns.Message.ID,
        DBTableColumns.Message.SEEN
    }
    set_clause_exclude = {
        DBTableColumns.Message.ID,
        DBTableColumns.Message.USER_ID,
        DBTableColumns.Message.MESSAGE,
        DBTableColumns.Message.CREATED_TIME
    }
    where_clause_exclude = set()
    

    # Methods
    
    @classmethod
    def add(cls, model : model_class, cursor : Optional[PgCursor] = None) -> model_class:
        now = datetime.now(ZoneInfo("Asia/Tehran"))
        model.created_time = now
        return super().add(model, cursor)
    
    @classmethod
    def _update_seen(cls, user_model: UserModel, cursor: Optional[PgCursor] = None) -> None:
        """
        Marks all messages for a specific user as seen.

        This internal method updates the `seen` status of all messages
        belonging to the given user to `True`.  
        It is typically called after retrieving messages from a user's inbox.

        Args:
            user_model (UserModel):
                The user whose messages should be marked as seen.
            cursor (Optional[PgCursor], optional):
                Existing database cursor. If not provided, a new one will be created automatically.

        Raises:
            NotSuchModelInDataBaseError:
                If the specified user record cannot be found in the database.
            DatabaseError:
                If the update operation fails.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True 
        
        model = UserRepository.get_one(user_model, cursor)
        
        if model is None:
            raise NotSuchModelInDataBaseError('user not found', user_model)
        
        query = f"""
            UPDATE {DBTables.MESSAGE}
            SET {DBTableColumns.Message.SEEN} = %s
            WHERE {DBTableColumns.Message.USER_ID} = %s
        """

        cursor.execute(query, (True, model.id))

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

    @classmethod
    @map_to_model(MessageViewModel)
    def inbox(cls, user_model: UserModel, cursor: Optional[PgCursor] = None) -> list[MessageViewModel]:
        """
        Retrieves all messages received by the specified user and marks them as seen.

        This method fetches all messages where the recipient matches the given user's username.
        The returned messages are mapped to `MessageViewModel` instances.  
        After fetching, all retrieved messages are automatically marked as seen.

        Args:
            user_model (UserModel):
                The user whose inbox messages are being retrieved.
            cursor (Optional[PgCursor], optional):
                Existing database cursor. If not provided, a new one will be created automatically.

        Returns:
            list[MessageViewModel]:
                A list of message view models representing the user's inbox.

        Raises:
            NotSuchModelInDataBaseError:
                If the specified user record cannot be found in the database.
            DatabaseError:
                If the query or update operation fails.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        model = UserRepository.get_one(user_model, cursor)
        
        if model is None:
            raise NotSuchModelInDataBaseError('user not found', user_model)
        
        message_model = MessageViewModel(to=model.username)
        
        result = cls.view_many(message_model, cursor)
        
        cls._update_seen(user_model, cursor)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

        return result

    @classmethod
    @map_to_model(MessageViewModel)
    def unread_inbox(cls, user_model: UserModel, cursor: Optional[PgCursor] = None) -> list[MessageViewModel]:
        """
        Retrieves only unread messages for the specified user and marks them as seen.

        This method fetches all messages addressed to the given user
        that have not yet been marked as seen (`seen = False`).  
        After retrieving the messages, it automatically updates their `seen` status to `True`.

        Args:
            user_model (UserModel):
                The user whose unread messages are being retrieved.
            cursor (Optional[PgCursor], optional):
                Existing database cursor. If not provided, a new one will be created automatically.

        Returns:
            list[MessageViewModel]:
                A list of message view models for unread messages.

        Raises:
            NotSuchModelInDataBaseError:
                If the specified user record cannot be found in the database.
            DatabaseError:
                If the query or update operation fails.
        """
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        model = UserRepository.get_one(user_model, cursor)
        
        if model is None:
            raise NotSuchModelInDataBaseError('user not found', user_model)
        
        message_model = MessageViewModel(to=model.username, seen=False)
        
        result = cls.view_many(message_model, cursor)
        
        cls._update_seen(user_model, cursor)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

        return result


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
    def clear(cls, cursor: Optional[PgCursor] = None) -> None:
        return super().clear(cursor)
    

    # Forbidden Methods
    
    @classmethod
    @forbidden_method
    def update(cls, model, cursor: Optional[PgCursor] = None):
        """Disabled method. Not allowed for this repository."""
        pass
            
    @classmethod
    @forbidden_method
    def delete(cls, id : int, cursor: Optional[PgCursor] = None):
        """Disabled method. Not allowed for this repository."""
        pass
    
    @classmethod
    @forbidden_method
    def remove(cls, model, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None):
        """Disabled method. Not allowed for this repository."""
        pass

