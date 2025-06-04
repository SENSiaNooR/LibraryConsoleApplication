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
    user_id: Optional[int] = None

@dataclass
class AuthorModel:
    id: Optional[int] = None
    name: Optional[str] = None
    biography: Optional[str] = None

@dataclass
class BookModel:
    id: Optional[int] = None
    title: Optional[str] = None
    publisher_id: Optional[int] = None
    total_copy: Optional[int] = None
    available_copies: Optional[int] = None

@dataclass
class BookAuthorModel:
    book_id: Optional[int] = None
    author_id: Optional[int] = None

@dataclass
class BookCategoryModel:
    book_id: Optional[int] = None
    category_id: Optional[int] = None

@dataclass
class BorrowRequestModel:
    id: Optional[int] = None
    member_id: Optional[int] = None
    book_id: Optional[int] = None
    request_timestamp: Optional[datetime] = None
    status: Optional[BorrowRequestStatus] = None
    handled_at: Optional[datetime] = None
    handled_by: Optional[int] = None
    note: Optional[str] = None

@dataclass
class BorrowingModel:
    id: Optional[int] = None
    member_id: Optional[int] = None
    book_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    returned: Optional[bool] = None

@dataclass
class CategoryModel:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None

@dataclass
class GuestModel:
    id: Optional[UUID] = None
    create_time: Optional[datetime] = None
    request_count: Optional[int] = None

@dataclass
class LibrarianModel:
    user_id: Optional[int] = None
    name: Optional[str] = None

@dataclass
class LibrarianActivityLogModel:
    id: Optional[int] = None
    librarian_id: Optional[int] = None
    action_type: Optional[LibrarianAction] = None
    book_id: Optional[int] = None
    member_id: Optional[int] = None
    timestamp: Optional[datetime] = None

@dataclass
class MemberModel:
    user_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    join_date: Optional[datetime] = None
    active: Optional[bool] = None

@dataclass
class MessageModel:
    id: Optional[int] = None
    user_id: Optional[int] = None
    message: Optional[str] = None
    created_time: Optional[datetime] = None
    seen: Optional[bool] = None

@dataclass
class PublisherModel:
    id: Optional[int] = None
    name: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    phone: Optional[str] = None

@dataclass
class UserModel:
    id: Optional[int] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None

# SQL View Models

@dataclass
class AdminVeiwModel:
    id: Optional[int] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None

@dataclass
class AuthorViewModel:
    id: Optional[int] = None
    name: Optional[str] = None
    books: Optional[str] = None
    biography: Optional[str] = None

@dataclass
class BookViewModel:
    id: Optional[int] = None
    title: Optional[str] = None
    publisher: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None

@dataclass
class BorrowingViewModel:
    id: Optional[int] = None
    name: Optional[str] = None
    book: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    returned: Optional[bool] = None

@dataclass
class CategoryViewModel:
    id: Optional[int] = None
    name: Optional[str] = None
    books: Optional[str] = None
    description: Optional[str] = None

@dataclass
class LibrarianActivityLogViewModel:
    id: Optional[int] = None
    librarian_name: Optional[str] = None
    action_type: Optional[LibrarianAction] = None
    book: Optional[str] = None
    member: Optional[str] = None
    timestamp: Optional[datetime] = None

@dataclass
class LibrarianViewModel:
    id: Optional[int] = None
    name: Optional[str] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None

@dataclass
class MemberViewModel:
    id: Optional[int] = None
    name: Optional[str] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None
    email: Optional[str] = None
    join_date: Optional[datetime] = None
    active: Optional[bool] = None

@dataclass
class MemberWithoutPasswordViewModel:
    id: Optional[int] = None
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    join_date: Optional[datetime] = None
    active: Optional[bool] = None

@dataclass
class MembersBorrowRequestViewModel:
    id: Optional[int] = None
    name: Optional[str] = None
    book: Optional[str] = None
    request_timestamp: Optional[datetime] = None
    status: Optional[BorrowRequestStatus] = None
    handled_at: Optional[datetime] = None
    handled_by: Optional[str] = None
    note: Optional[str] = None

@dataclass
class PublisherViewModel:
    id: Optional[int] = None
    name: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    books: Optional[str] = None

@dataclass
class UserViewModel:
    id: Optional[int] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None
    name: Optional[str] = None
    user_type: Optional[UserType] = None

@dataclass
class UserWithoutPasswordViewModel:
    id: Optional[int] = None
    username: Optional[str] = None
    name: Optional[str] = None
    user_type: Optional[UserType] = None
