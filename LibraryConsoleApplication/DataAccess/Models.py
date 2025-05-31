from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID
from typing import Optional



# SQL Types

class BorrowRequestStatus(Enum):
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'

class LibrarianAction(Enum):
    create_member = 'create_member'
    update_member_password = 'update_member_password'
    deactivate_member = 'deactivate_member'
    activate_member = 'activate_member'
    create_book = 'create_book'
    update_book = 'update_book'
    delete_book = 'delete_book'
    accept_borrow_request = 'accept_borrow_request'
    reject_borrow_request = 'reject_borrow_request'
    send_message = 'send_message'



# SQL Tables

@dataclass
class AdminModel:
    user_id : int

@dataclass
class AuthoModel:
    id : int
    name : str
    biography : Optional[str] = None
    
@dataclass
class BookModel:
    id : int
    title : str
    publisher_id : int
    total_copy : int
    available_copies : int
    
@dataclass
class BookAuthorModel:
    book_id : int
    author_id : int
    
@dataclass
class BookCategoryModel:
    book_id : int
    category_id : int
    
@dataclass
class BorrowRequestModel:
    id : int
    member_id : int
    book_id : int
    request_timestamp : datetime
    status : BorrowRequestStatus
    handled_at : Optional[datetime] = None
    handled_by : Optional[int] = None
    note : Optional[str] = None
    
@dataclass
class BorrowingModel:
    id : int
    member_id : int
    book_id : int
    start_date : datetime
    end_date : Optional[datetime] = None
    returned : bool = False
    
@dataclass
class CategoryModel:
    id : int
    name : str
    description : Optional[str] = None
    
@dataclass
class GuestModel:
    id : UUID
    create_time : datetime
    request_count : int
    
@dataclass
class LibrarianModel:
    user_id : int
    name : str
    
@dataclass
class LibrarianActivityLogModel:
    id : int
    librarian_id : int
    action_type : LibrarianAction
    book_id : Optional[int] = None
    member_id : Optional[int] = None
    timestamp : datetime

@dataclass
class MemberModel:
    user_id : int
    name : str
    email : str
    join_date : datetime
    active : bool

@dataclass
class MessageModel:
    id : int
    user_id : int
    message : Optional[str] = None
    created_time : datetime
    seen : bool
    
@dataclass
class PublisherModel:
    id : int
    name : str
    address : Optional[str] = None
    contact_email : Optional[str] = None
    phone : Optional[str] = None
    
@dataclass
class UserModel:
    id : int
    username : str
    hashed_password : str
   