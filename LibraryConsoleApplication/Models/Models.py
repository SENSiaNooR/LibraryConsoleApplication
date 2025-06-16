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
class BaseTableModel:
    pass


@dataclass
class AdminModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET

@dataclass
class AuthorModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    biography: Union[str, None, UnsetType] = UNSET

@dataclass
class BookModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET
    title: Union[str, None, UnsetType] = UNSET
    publisher_id: Union[int, None, UnsetType] = UNSET
    total_copies: Union[int, None, UnsetType] = UNSET
    available_copies: Union[int, None, UnsetType] = UNSET

@dataclass
class BookAuthorModel(BaseTableModel):
    book_id: Union[int, None, UnsetType] = UNSET
    author_id: Union[int, None, UnsetType] = UNSET

@dataclass
class BookCategoryModel(BaseTableModel):
    book_id: Union[int, None, UnsetType] = UNSET
    category_id: Union[int, None, UnsetType] = UNSET

@dataclass
class BorrowRequestModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET
    member_id: Union[int, None, UnsetType] = UNSET
    book_id: Union[int, None, UnsetType] = UNSET
    request_timestamp: Union[datetime, None, UnsetType] = UNSET
    status: Union[BorrowRequestStatus, None, UnsetType] = UNSET
    handled_at: Union[datetime, None, UnsetType] = UNSET
    handled_by: Union[int, None, UnsetType] = UNSET
    note: Union[str, None, UnsetType] = UNSET

@dataclass
class BorrowingModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET
    member_id: Union[int, None, UnsetType] = UNSET
    book_id: Union[int, None, UnsetType] = UNSET
    start_date: Union[datetime, None, UnsetType] = UNSET
    end_date: Union[datetime, None, UnsetType] = UNSET
    returned: Union[bool, None, UnsetType] = UNSET

@dataclass
class CategoryModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    description: Union[str, None, UnsetType] = UNSET

@dataclass
class GuestModel(BaseTableModel):
    id: Union[UUID, None, UnsetType] = UNSET
    created_time: Union[datetime, None, UnsetType] = UNSET
    request_count: Union[int, None, UnsetType] = UNSET

@dataclass
class LibrarianModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET

@dataclass
class LibrarianActivityLogModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET
    librarian_id: Union[int, None, UnsetType] = UNSET
    action_type: Union[LibrarianAction, None, UnsetType] = UNSET
    book_id: Union[int, None, UnsetType] = UNSET
    member_id: Union[int, None, UnsetType] = UNSET
    timestamp: Union[datetime, None, UnsetType] = UNSET

@dataclass
class MemberModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    email: Union[str, None, UnsetType] = UNSET
    join_date: Union[datetime, None, UnsetType] = UNSET
    active: Union[bool, None, UnsetType] = UNSET

@dataclass
class MessageModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET
    user_id: Union[int, None, UnsetType] = UNSET
    message: Union[str, None, UnsetType] = UNSET
    created_time: Union[datetime, None, UnsetType] = UNSET
    seen: Union[bool, None, UnsetType] = UNSET

@dataclass
class PublisherModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    address: Union[str, None, UnsetType] = UNSET
    contact_email: Union[str, None, UnsetType] = UNSET
    phone: Union[str, None, UnsetType] = UNSET

@dataclass
class UserModel(BaseTableModel):
    id: Union[int, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET

# SQL View Models
class BaseViewModel:
    pass

@dataclass
class AdminVeiwModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET

@dataclass
class AuthorViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    books: Union[str, None, UnsetType] = UNSET
    biography: Union[str, None, UnsetType] = UNSET

@dataclass
class BookViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    title: Union[str, None, UnsetType] = UNSET
    publisher: Union[str, None, UnsetType] = UNSET
    author: Union[str, None, UnsetType] = UNSET
    category: Union[str, None, UnsetType] = UNSET
    total_copies: Union[int, None, UnsetType] = UNSET
    available_copies: Union[int, None, UnsetType] = UNSET

@dataclass
class BorrowingViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    book: Union[str, None, UnsetType] = UNSET
    start_date: Union[datetime, None, UnsetType] = UNSET
    end_date: Union[datetime, None, UnsetType] = UNSET
    returned: Union[bool, None, UnsetType] = UNSET

@dataclass
class CategoryViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    books: Union[str, None, UnsetType] = UNSET
    description: Union[str, None, UnsetType] = UNSET

@dataclass
class LibrarianActivityLogViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    librarian_name: Union[str, None, UnsetType] = UNSET
    action_type: Union[LibrarianAction, None, UnsetType] = UNSET
    book: Union[str, None, UnsetType] = UNSET
    member: Union[str, None, UnsetType] = UNSET
    timestamp: Union[datetime, None, UnsetType] = UNSET

@dataclass
class LibrarianViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET

@dataclass
class MemberViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET
    email: Union[str, None, UnsetType] = UNSET
    join_date: Union[datetime, None, UnsetType] = UNSET
    active: Union[bool, None, UnsetType] = UNSET

@dataclass
class MemberWithoutPasswordViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    email: Union[str, None, UnsetType] = UNSET
    join_date: Union[datetime, None, UnsetType] = UNSET
    active: Union[bool, None, UnsetType] = UNSET

@dataclass
class MembersBorrowRequestViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    book: Union[str, None, UnsetType] = UNSET
    request_timestamp: Union[datetime, None, UnsetType] = UNSET
    status: Union[BorrowRequestStatus, None, UnsetType] = UNSET
    handled_at: Union[datetime, None, UnsetType] = UNSET
    handled_by: Union[str, None, UnsetType] = UNSET
    note: Union[str, None, UnsetType] = UNSET

@dataclass
class MessageViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    to: Union[str, None, UnsetType] = UNSET
    receiver_role: Union[UserType, None, UnsetType] = UNSET
    message: Union[str, None, UnsetType] = UNSET
    created_time: Union[datetime, None, UnsetType] = UNSET
    seen: Union[bool, None, UnsetType] = UNSET

@dataclass
class PublisherViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    address: Union[str, None, UnsetType] = UNSET
    contact_email: Union[str, None, UnsetType] = UNSET
    phone: Union[str, None, UnsetType] = UNSET
    books: Union[str, None, UnsetType] = UNSET

@dataclass
class UserViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    user_type: Union[UserType, None, UnsetType] = UNSET

@dataclass
class UserWithoutPasswordViewModel(BaseViewModel):
    id: Union[int, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    user_type: Union[UserType, None, UnsetType] = UNSET
    
# Other Models

@dataclass
class PlainUserModel:
    username: Union[str, None, UnsetType] = UNSET
    password: Union[str, None, UnsetType] = UNSET