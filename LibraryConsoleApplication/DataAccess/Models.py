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
    
class UserType(Enum):
    admin = 'admin'
    librarian = 'librarian'
    member = 'member'



# SQL Table Models

@dataclass
class AdminModel:
    user_id : int

@dataclass
class AuthorModel:
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
    timestamp : Optional[datetime] = None

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
    created_time : Optional[datetime] = None
    seen : bool = False
    
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



# SQL View Models

@dataclass
class AdminVeiwModel:
    id : int
    username : str
    hashed_password : str
   
@dataclass
class AuthorViewModel:
    id : int
    name : str
    books : Optional[str] = None
    biography : Optional[str] = None

@dataclass
class BookViewModel:
    id : int
    title : str
    publisher : str
    author : str    
    category : str
    total_copies : int
    available_copies : int
    
@dataclass
class BorrowingViewModel:
    id : int
    name : str
    book : str
    start_date : datetime
    end_date : Optional[datetime] = None
    returned : bool = False
    
@dataclass
class CategoryViewModel:
    id : int
    name : str
    books : Optional[str] = None
    description : Optional[str] = None
    
@dataclass
class LibrarianActivityLogViewModel:
    id : int
    librarian_name : str
    action_type : LibrarianAction
    book : Optional[str] = None
    member : Optional[str] = None
    timestamp : Optional[datetime] = None

@dataclass
class LibrarianViewModel:
    id : int
    name : str
    username : str
    hashed_password : str
    
@dataclass
class MemberViewModel:
    id : int
    name : str
    username : str
    hashed_password : str
    email : str
    join_date : datetime
    active : bool
    
@dataclass
class MemberWithoutPasswordViewModel:
    id : int
    name : str
    username : str
    email : str
    join_date : datetime
    active : bool
    
@dataclass
class MembersBorrowRequestViewModel:
    id : int
    name : str
    book : str
    request_timestamp : datetime
    status : BorrowRequestStatus
    handled_at : Optional[datetime] = None
    handled_by : Optional[str] = None
    note : Optional[str] = None
    
@dataclass
class PublisherViewModel:
    id : int
    name : str
    address : Optional[str] = None
    contact_email : Optional[str] = None
    phone : Optional[str] = None
    books : Optional[str] = None

@dataclass
class UserViewModel:
    id : int
    username : str
    hashed_password : str
    name : Optional[str] = None
    user_type : Optional[UserType] = None
    
@dataclass
class UserWithoutPasswordViewModel:
    id : int
    username : str
    name : Optional[str] = None
    user_type : Optional[UserType] = None