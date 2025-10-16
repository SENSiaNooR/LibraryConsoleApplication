
from datetime import datetime
from email import message
import os
from pathlib import Path
from zoneinfo import ZoneInfo
from Exceptions.Exceptions import InappropriateRoleError, NotSuchModelInDataBaseError, ReachedToRequestLimitError
from dotenv import load_dotenv
from DataAccess.GuestRepository import GuestRepository
from Models.Models import BookViewModel, GuestModel
from Services.BaseServices import BaseServices
from Services.Decorators import token_required
from DataAccess.BookRepository import BookRepository


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


    def __can_guest_request(self) -> bool:    
        
        model = GuestModel(id = self.user_model.id)
        guest = GuestRepository.get_one(model)
    
        if guest is None:
            raise NotSuchModelInDataBaseError('can not find guest', model)
    
        now = datetime.now(ZoneInfo("Asia/Tehran"))
        delta_minutes = (now - guest.created_time).total_seconds() / 60
            
        if (guest.request_count >= GuestServices.__max_available_request) or (delta_minutes >= GuestServices.__life_time_minute):
            return False
        
        return True
    
    def __increase_guest_request(self):
        model = GuestModel(id = self.user_model.id)
        GuestRepository.increase_request(model)


    @token_required
    def get_all_books(self):
        if not self.__can_guest_request():
            raise ReachedToRequestLimitError()
        self.__increase_guest_request()        
        
        return BookRepository.view_many(BookViewModel())