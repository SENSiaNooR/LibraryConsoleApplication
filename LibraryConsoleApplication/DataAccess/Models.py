from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID
from typing import Optional, Union
from psycopg2.extensions import register_adapter, AsIs


# Unset type

class UnsetType:   
    def __repr__(self) -> str:
        return '<UNSET>'

UNSET = UnsetType()


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
    
def adapt_enum(enum_val):
    return AsIs(f"'{enum_val.value}'")

register_adapter(BorrowRequestStatus, adapt_enum)
register_adapter(LibrarianAction, adapt_enum)
register_adapter(UserType, adapt_enum)

# SQL Table Models

@dataclass
class AdminModel:
    id: Union[int, None, UnsetType] = UNSET

@dataclass
class AuthorModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    biography: Union[str, None, UnsetType] = UNSET

@dataclass
class BookModel:
    id: Union[int, None, UnsetType] = UNSET
    title: Union[str, None, UnsetType] = UNSET
    publisher_id: Union[int, None, UnsetType] = UNSET
    total_copies: Union[int, None, UnsetType] = UNSET
    available_copies: Union[int, None, UnsetType] = UNSET

@dataclass
class BookAuthorModel:
    book_id: Union[int, None, UnsetType] = UNSET
    author_id: Union[int, None, UnsetType] = UNSET

@dataclass
class BookCategoryModel:
    book_id: Union[int, None, UnsetType] = UNSET
    category_id: Union[int, None, UnsetType] = UNSET

@dataclass
class BorrowRequestModel:
    id: Union[int, None, UnsetType] = UNSET
    member_id: Union[int, None, UnsetType] = UNSET
    book_id: Union[int, None, UnsetType] = UNSET
    request_timestamp: Union[datetime, None, UnsetType] = UNSET
    status: Union[BorrowRequestStatus, None, UnsetType] = UNSET
    handled_at: Union[datetime, None, UnsetType] = UNSET
    handled_by: Union[int, None, UnsetType] = UNSET
    note: Union[str, None, UnsetType] = UNSET

@dataclass
class BorrowingModel:
    id: Union[int, None, UnsetType] = UNSET
    member_id: Union[int, None, UnsetType] = UNSET
    book_id: Union[int, None, UnsetType] = UNSET
    start_date: Union[datetime, None, UnsetType] = UNSET
    end_date: Union[datetime, None, UnsetType] = UNSET
    returned: Union[bool, None, UnsetType] = UNSET

@dataclass
class CategoryModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    description: Union[str, None, UnsetType] = UNSET

@dataclass
class GuestModel:
    id: Union[UUID, None, UnsetType] = UNSET
    create_time: Union[datetime, None, UnsetType] = UNSET
    request_count: Union[int, None, UnsetType] = UNSET

@dataclass
class LibrarianModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET

@dataclass
class LibrarianActivityLogModel:
    id: Union[int, None, UnsetType] = UNSET
    librarian_id: Union[int, None, UnsetType] = UNSET
    action_type: Union[LibrarianAction, None, UnsetType] = UNSET
    book_id: Union[int, None, UnsetType] = UNSET
    member_id: Union[int, None, UnsetType] = UNSET
    timestamp: Union[datetime, None, UnsetType] = UNSET

@dataclass
class MemberModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    email: Union[str, None, UnsetType] = UNSET
    join_date: Union[datetime, None, UnsetType] = UNSET
    active: Union[bool, None, UnsetType] = UNSET

@dataclass
class MessageModel:
    id: Union[int, None, UnsetType] = UNSET
    user_id: Union[int, None, UnsetType] = UNSET
    message: Union[str, None, UnsetType] = UNSET
    created_time: Union[datetime, None, UnsetType] = UNSET
    seen: Union[bool, None, UnsetType] = UNSET

@dataclass
class PublisherModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    address: Union[str, None, UnsetType] = UNSET
    contact_email: Union[str, None, UnsetType] = UNSET
    phone: Union[str, None, UnsetType] = UNSET

@dataclass
class UserModel:
    id: Union[int, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET

# SQL View Models

@dataclass
class AdminVeiwModel:
    id: Union[int, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET

@dataclass
class AuthorViewModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    books: Union[str, None, UnsetType] = UNSET
    biography: Union[str, None, UnsetType] = UNSET

@dataclass
class BookViewModel:
    id: Union[int, None, UnsetType] = UNSET
    title: Union[str, None, UnsetType] = UNSET
    publisher: Union[str, None, UnsetType] = UNSET
    author: Union[str, None, UnsetType] = UNSET
    category: Union[str, None, UnsetType] = UNSET
    total_copies: Union[int, None, UnsetType] = UNSET
    available_copies: Union[int, None, UnsetType] = UNSET

@dataclass
class BorrowingViewModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    book: Union[str, None, UnsetType] = UNSET
    start_date: Union[datetime, None, UnsetType] = UNSET
    end_date: Union[datetime, None, UnsetType] = UNSET
    returned: Union[bool, None, UnsetType] = UNSET

@dataclass
class CategoryViewModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    books: Union[str, None, UnsetType] = UNSET
    description: Union[str, None, UnsetType] = UNSET

@dataclass
class LibrarianActivityLogViewModel:
    id: Union[int, None, UnsetType] = UNSET
    librarian_name: Union[str, None, UnsetType] = UNSET
    action_type: Union[LibrarianAction, None, UnsetType] = UNSET
    book: Union[str, None, UnsetType] = UNSET
    member: Union[str, None, UnsetType] = UNSET
    timestamp: Union[datetime, None, UnsetType] = UNSET

@dataclass
class LibrarianViewModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET

@dataclass
class MemberViewModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET
    email: Union[str, None, UnsetType] = UNSET
    join_date: Union[datetime, None, UnsetType] = UNSET
    active: Union[bool, None, UnsetType] = UNSET

@dataclass
class MemberWithoutPasswordViewModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    email: Union[str, None, UnsetType] = UNSET
    join_date: Union[datetime, None, UnsetType] = UNSET
    active: Union[bool, None, UnsetType] = UNSET

@dataclass
class MembersBorrowRequestViewModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    book: Union[str, None, UnsetType] = UNSET
    request_timestamp: Union[datetime, None, UnsetType] = UNSET
    status: Union[BorrowRequestStatus, None, UnsetType] = UNSET
    handled_at: Union[datetime, None, UnsetType] = UNSET
    handled_by: Union[str, None, UnsetType] = UNSET
    note: Union[str, None, UnsetType] = UNSET

@dataclass
class MessageViewModel:
    id: Union[int, None, UnsetType] = UNSET
    to: Union[str, None, UnsetType] = UNSET
    receiver_role: Union[UserType, None, UnsetType] = UNSET
    message: Union[str, None, UnsetType] = UNSET
    created_time: Union[datetime, None, UnsetType] = UNSET
    seen: Union[bool, None, UnsetType] = UNSET

@dataclass
class PublisherViewModel:
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    address: Union[str, None, UnsetType] = UNSET
    contact_email: Union[str, None, UnsetType] = UNSET
    phone: Union[str, None, UnsetType] = UNSET
    books: Union[str, None, UnsetType] = UNSET

@dataclass
class UserViewModel:
    id: Union[int, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    user_type: Union[UserType, None, UnsetType] = UNSET

@dataclass
class UserWithoutPasswordViewModel:
    id: Union[int, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    user_type: Union[UserType, None, UnsetType] = UNSET
    
# Other Models

@dataclass
class PlainUserModel:
    username: Union[str, None, UnsetType] = UNSET
    password: Union[str, None, UnsetType] = UNSET