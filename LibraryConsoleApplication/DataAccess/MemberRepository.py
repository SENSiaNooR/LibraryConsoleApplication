from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from DataAccess.BaseRepository import BaseRepository, map_to_model, map_to_single_model
from DataAccess.CommonQueriesRepository import CommonQueriesRepository
from Exceptions.Exceptions import MemberAlreadyActivatedError, MemberAlreadyDeactivatedError
from Models.Models import MemberModel, MemberWithoutPasswordViewModel, PlainUserModel, UnsetType
from Models.Schema import DBTables, DBViews
from psycopg2.extensions import cursor as PgCursor
from DataAccess.UserRepository import UserRepository


class MemberRepository(BaseRepository):
    
    @classmethod
    @map_to_single_model(MemberModel)
    def get_member(cls, model : MemberModel, cursor : Optional[PgCursor] = None) -> MemberModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBTables.MEMBER,
            cursor=cursor
        )
    
    @classmethod
    @map_to_model(MemberModel)
    def get_members(cls, model : MemberModel, cursor : Optional[PgCursor] = None) -> list[MemberModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBTables.MEMBER,
            cursor=cursor
        )

    @classmethod
    @map_to_single_model(MemberWithoutPasswordViewModel)
    def get_member_without_password(cls, model : MemberWithoutPasswordViewModel, cursor : Optional[PgCursor] = None) -> MemberWithoutPasswordViewModel:
        return CommonQueriesRepository.get_record(
            model=model,
            table=DBViews.MEMBER_WITHOUT_PASSWORD_VIEW,
            cursor=cursor
        )
    
    @classmethod
    @map_to_model(MemberWithoutPasswordViewModel)
    def get_members_without_password(cls, model : MemberWithoutPasswordViewModel, cursor : Optional[PgCursor] = None) -> list[MemberWithoutPasswordViewModel]:
        return CommonQueriesRepository.get_records(
            model=model,
            table=DBViews.MEMBER_WITHOUT_PASSWORD_VIEW,
            cursor=cursor
        )
    
    @classmethod
    def _active_or_deactive_member(cls, model : MemberWithoutPasswordViewModel, active : bool, cursor : Optional[PgCursor] = None) -> None:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        member_model = cls.get_member_without_password(model, cursor)
        
        if member_model is None:
            raise ValueError('no any member with this username')
        
        if member_model.active == active:
            if active:
                raise MemberAlreadyActivatedError(f'member {member_model.name} is already active.')
            else:
                raise MemberAlreadyDeactivatedError(f'member {member_model.name} is already inactive.')
        
        updated_model = MemberModel(
            id=member_model.id,
            active=active
        )

        CommonQueriesRepository.update_record(
            model=updated_model,
            table=DBTables.MEMBER,
            cursor=cursor
        )

        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()

    @classmethod
    def deactivate_member(cls, model : MemberWithoutPasswordViewModel, cursor : Optional[PgCursor] = None) -> None:
        return cls._active_or_deactive_member(model, active=False, cursor=cursor)

    @classmethod
    def activate_member(cls, model : MemberWithoutPasswordViewModel, cursor : Optional[PgCursor] = None):
        return cls._active_or_deactive_member(model, active=True, cursor=cursor)
            
    @classmethod
    @map_to_single_model(MemberModel)
    def add_member(cls, plain_user_model : PlainUserModel, member_model : MemberModel, cursor : Optional[PgCursor] = None) -> MemberModel:
        
        commit_and_close = False
        if cursor is None:
            cursor = cls._get_cursor()
            commit_and_close = True

        user_model = UserRepository.hash_password_and_add_user(plain_user_model, cursor)
         
        now = datetime.now(ZoneInfo("Asia/Tehran"))
        active = True
        
        member_model.id = user_model.id
        member_model.join_date = now
        member_model.active = active

        result = CommonQueriesRepository.add_record(
            model=member_model,
            table=DBTables.MEMBER,
            exclude=set(),
            cursor=cursor
        )
        
        if commit_and_close:
            cursor.connection.commit()
            cursor.connection.close()
            
        return result

    @classmethod
    def update_member(cls, model: MemberModel, cursor: Optional[PgCursor] = None) -> None:
        
        model.join_date = UnsetType()
        model.active = UnsetType()
        
        return CommonQueriesRepository.update_record(
            model=model,
            table=DBTables.MEMBER,
            cursor=cursor
        )


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