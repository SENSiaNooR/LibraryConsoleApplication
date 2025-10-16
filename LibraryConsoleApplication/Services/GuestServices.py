
import os
from pathlib import Path
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from Models.Models import GuestModel
from Services.BaseServices import BaseServices
from Services.Decorators import guest_request_limit, token_required
from DataAccess.GuestRepository import GuestRepository
from Exceptions.Exceptions import InappropriateRoleError, NotSuchModelInDataBaseError, ReachedToRequestLimitError


class GuestServices(BaseServices):
    
    __life_time_minute : int
    __max_available_request : int
    __env_loaded = False

    def __init__(self, token):
        super().__init__(token)
        if self.user_model.user_type != 'guest':
            raise InappropriateRoleError()
        
        if not GuestServices.__env_loaded:
            current_dir = Path(__file__).resolve().parent
            dotenv_path = current_dir.parent / ".env"
            load_dotenv(dotenv_path=dotenv_path)
            GuestServices.__life_time_minute = int(os.getenv("LIFE_TIME_MINUTE"))
            GuestServices.__max_available_request = int(os.getenv("MAX_AVAILABLE_REQUEST"))
            GuestServices.__env_loaded = True


    def can_guest_request(self) -> bool:
        
        model = GuestModel(id = self.user_model.id)
        guest = GuestRepository.get_one(model)
    
        if guest is None:
            raise NotSuchModelInDataBaseError('can not find guest', model)
    
        now = datetime.now(ZoneInfo("Asia/Tehran"))
        delta_minutes = (now - guest.created_time).total_seconds() / 60
            
        if (guest.request_count >= GuestServices.__max_available_request) or (delta_minutes >= GuestServices.__life_time_minute):
            return False
        
        return True
    
    def increase_guest_request(self):
        model = GuestModel(id = self.user_model.id)
        GuestRepository.increase_request(model)


    @guest_request_limit
    @token_required
    def get_all_books(self):      
        return super().get_all_books()
    
    @guest_request_limit
    @token_required
    def get_all_publishers(self):     
        return super().get_all_publishers()

    @guest_request_limit
    @token_required
    def publisher_search(self, name : str = ''):     
        return super().publisher_search(name)
    
    @guest_request_limit
    @token_required
    def get_all_authors(self):
        if not self.can_guest_request():
            raise ReachedToRequestLimitError()
        self.increase_guest_request()        
        return super().get_all_authors()
    
    @guest_request_limit
    @token_required
    def author_search(self, name : str = ''):
        return super().author_search(name)

    @guest_request_limit
    @token_required
    def get_all_categories(self):       
        return super().get_all_categories()
    
    @guest_request_limit
    @token_required
    def book_advance_search(
        self,
        title : str = '',
        publisher : str = '',
        author : str = '',
        categories: Optional[list[str]] = None,
        just_available: bool = False
    ):
        return super().book_advance_search(title, publisher, author, categories, just_available)

    @guest_request_limit
    @token_required
    def book_search(self, title : str = ''):
        return super().book_search(title)

    