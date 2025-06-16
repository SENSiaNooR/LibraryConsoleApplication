from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from DataAccess.Decorators import forbidden_method
from Exceptions.Exceptions import MemberAlreadyActivatedError, MemberAlreadyDeactivatedError, NotSuchModelInDataBaseError
from Models.Models import MemberModel, MemberWithoutPasswordViewModel, PlainUserModel, UnsetType
from Models.Schema import DBTableColumns, DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor
from DataAccess.UserRepository import UserRepository


class MemberRepository(CommonQueriesRepository):
    
    table_name = DBTables.MEMBER
    view_name = DBViews.MEMBER_WITHOUT_PASSWORD_VIEW
    model_class = MemberModel
    view_model_class = MemberWithoutPasswordViewModel
    insert_clause_exclude = {
        DBTableColumns.Member.ACTIVE
    }
    set_clause_exclude = {
        DBTableColumns.Member.ID,
        DBTableColumns.Member.JOIN_DATE
    }
    where_clause_exclude = set()
    

    # Methods
    
    @classmethod
    def add(cls, plain_user_model : PlainUserModel, model : model_class, cursor : Optional[PgCursor] = None) -> model_class:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        user_model = UserRepository.hash_password_and_add_user(plain_user_model, cursor)
         
        now = datetime.now(ZoneInfo("Asia/Tehran"))
        
        model.id = user_model.id
        model.join_date = now

        result = super().add(model, cursor)
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result

    @classmethod
    def update(cls, model : model_class, cursor: Optional[PgCursor] = None) -> None:
        model.active = UnsetType()
        return super().update(model, cursor)
    
    @classmethod
    def _active_or_deactive_member(cls, model : model_class, active : bool, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        db_model = cls.get_one(model, cursor)
        
        if db_model is None:
            raise NotSuchModelInDataBaseError('cannot find member', model)
        
        if db_model.active == active:
            if active:
                raise MemberAlreadyActivatedError(f'member {db_model.name} is already active.')
            else:
                raise MemberAlreadyDeactivatedError(f'member {db_model.name} is already inactive.')
        
        updated_model = MemberModel(
            id=db_model.id,
            active=active
        )
        
        super().update(updated_model, cursor)

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
    @classmethod
    def deactivate_member(cls, model : model_class, cursor : Optional[PgCursor] = None) -> None:
        return cls._active_or_deactive_member(model, active=False, cursor=cursor)

    @classmethod
    def activate_member(cls, model : model_class, cursor : Optional[PgCursor] = None):
        return cls._active_or_deactive_member(model, active=True, cursor=cursor)
    


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
    

    # Forbidden Methods
                
    @classmethod
    @forbidden_method
    def delete(cls, id : int, cursor: Optional[PgCursor] = None):
        pass
    
    @classmethod
    @forbidden_method
    def remove(cls, model, use_like_for_strings : bool = True, cursor: Optional[PgCursor] = None):
        pass

    @classmethod
    @forbidden_method
    def clear(cls, cursor: Optional[PgCursor] = None):
        pass

      



if __name__ == '__main__':
    
    UserRepository.delete_user('rezaGang')

    p1 = PlainUserModel(username='rezaGang', password='6456QWER')
    m1 = MemberModel(name='رضا پلنگ', email='rezapalang@gmail.com')
    res1 = MemberRepository.add_member(p1,m1)
    print(f'res1 = {res1}\n')
    
    res2 = UserRepository.verify_user(p1)
    print(f'res2 = {res2}\n')
    
    res1.email = 'rezapalang2@gmail.com'
    MemberRepository.update_member(res1)
    
    MemberRepository.deactivate_member(MemberWithoutPasswordViewModel(name = 'رضا پلنگ'))
    
    res3 = MemberRepository.get_members_without_password(MemberWithoutPasswordViewModel())
    print('res3 = [')
    for row in res3:
        print(f'\t{row}')
    print(']\n')