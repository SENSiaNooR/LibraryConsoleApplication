
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from Exceptions.Exceptions import NotSuchModelInDataBaseError
from DataAccess.UserRepository import UserRepository
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from Models.Models import MessageModel, MessageViewModel, UserModel
from Models.Schema import DBTableColumns, DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor


class MessageRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(MessageModel)
    def get_message(cls, model : MessageModel, cursor : Optional[PgCursor] = None) -> MessageModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBTables.MESSAGE,
            cursor=cursor
        )
        
    @classmethod
    @map_to_single_model(MessageViewModel)
    def get_message_view(cls, model : MessageViewModel, cursor : Optional[PgCursor] = None) -> MessageViewModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBViews.MESSAGE_VIEW,
            cursor=cursor
        )
       
    @classmethod
    @map_to_model(MessageModel)
    def get_messages(cls, model : MessageModel, cursor : Optional[PgCursor] = None) -> list[MessageModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBTables.MESSAGE,
            cursor=cursor
        )
    
    @classmethod
    @map_to_model(MessageViewModel)
    def get_messages_view(cls, model : MessageViewModel, cursor : Optional[PgCursor] = None) -> list[MessageViewModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBViews.MESSAGE_VIEW,
            cursor=cursor
        )

    def _prepare_message_model(cls, receiver_model : UserModel, message : str, cursor : Optional[PgCursor] = None) -> MessageModel:
        user_model = UserRepository.get_user(receiver_model, cursor)
    
        if user_model is None:
            raise NotSuchModelInDataBaseError('can not found user', receiver_model)
    
        now = datetime.now(ZoneInfo("Asia/Tehran"))

        return MessageModel(
            user_id=user_model.id,
            message=message,
            created_time=now,
            seen=False
        )

    @classmethod
    @map_to_single_model(MessageModel)
    def send_message(cls, receiver_model : UserModel, message : str, cursor : Optional[PgCursor] = None) -> MessageModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True
        
        message_model = cls._prepare_message_model(receiver_model, message, cursor)

        result = CommonQueriesRepository.add_record(
            model=message_model,
            table=DBTables.MESSAGE,
            cursor=cursor
        )
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result
    
    @classmethod
    def _update_seen(cls, user_model: UserModel, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True 
        
        model = UserRepository.get_user(user_model, cursor)
        
        if model is None:
            raise NotSuchModelInDataBaseError('can not found user', user_model)
        
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
    def get_inbox(cls, user_model: UserModel, cursor: Optional[PgCursor] = None) -> list[MessageViewModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        model = UserRepository.get_user(user_model, cursor)
        
        if model is None:
            raise NotSuchModelInDataBaseError('can not found user', user_model)
        
        message_model = MessageViewModel(to=model.username)
        
        result = cls.get_messages_view(message_model, cursor)
        
        cls._update_seen(user_model, cursor)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

        return result

    @classmethod
    @map_to_model(MessageViewModel)
    def get_unread_inbox(cls, user_model: UserModel, cursor: Optional[PgCursor] = None) -> list[MessageViewModel]:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        model = UserRepository.get_user(user_model, cursor)
        
        if model is None:
            raise NotSuchModelInDataBaseError('can not found user', user_model)
        
        message_model = MessageViewModel(to=model.username, seen=False)
        
        result = cls.get_messages_view(message_model, cursor)
        
        cls._update_seen(user_model, cursor)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

        return result
    
    @classmethod
    def clear_table(cls, cursor: Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        query = f"""
            DELETE FROM {DBTables.MESSAGE}
        """
    
        cursor.execute(query)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()