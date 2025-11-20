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
    def __str__(self):
        return 'Unassign'

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
    guest = 'guest'
    
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
    """
    Represents an Admin table record stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the admin.
    """
    id: Union[int, None, UnsetType] = UNSET


@dataclass
class AuthorModel(BaseTableModel):
    """
    Represents an Author table record stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the author.
        name (str | None | UnsetType): Author's full name.
        biography (str | None | UnsetType): Short biography text.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    biography: Union[str, None, UnsetType] = UNSET


@dataclass
class BookModel(BaseTableModel):
    """
    Represents a Book table record stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the book.
        title (str | None | UnsetType): Title of the book.
        publisher_id (int | None | UnsetType): Related publisher ID.
        total_copies (int | None | UnsetType): Total number of copies.
        available_copies (int | None | UnsetType): Currently available copies.
    """
    id: Union[int, None, UnsetType] = UNSET
    title: Union[str, None, UnsetType] = UNSET
    publisher_id: Union[int, None, UnsetType] = UNSET
    total_copies: Union[int, None, UnsetType] = UNSET
    available_copies: Union[int, None, UnsetType] = UNSET


@dataclass
class BookAuthorModel(BaseTableModel):
    """
    Represents a BookAuthor table record (many-to-many relation).

    Attributes:
        book_id (int | None | UnsetType): ID of the related book.
        author_id (int | None | UnsetType): ID of the related author.
    """
    book_id: Union[int, None, UnsetType] = UNSET
    author_id: Union[int, None, UnsetType] = UNSET


@dataclass
class BookCategoryModel(BaseTableModel):
    """
    Represents a BookCategory table record (many-to-many relation).

    Attributes:
        book_id (int | None | UnsetType): ID of the related book.
        category_id (int | None | UnsetType): ID of the related category.
    """
    book_id: Union[int, None, UnsetType] = UNSET
    category_id: Union[int, None, UnsetType] = UNSET


@dataclass
class BorrowRequestModel(BaseTableModel):
    """
    Represents a BorrowRequest table record stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the request.
        member_id (int | None | UnsetType): Requesting member ID.
        book_id (int | None | UnsetType): Requested book ID.
        request_timestamp (datetime | None | UnsetType): Time of request.
        status (BorrowRequestStatus | None | UnsetType): Request status.
        handled_at (datetime | None | UnsetType): Handling timestamp.
        handled_by (int | None | UnsetType): Librarian ID who handled it.
        note (str | None | UnsetType): Optional note or comment.
    """
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
    """
    Represents a Borrowing table record stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the borrowing.
        member_id (int | None | UnsetType): Borrowing member ID.
        book_id (int | None | UnsetType): Borrowed book ID.
        start_date (datetime | None | UnsetType): Start date of borrowing.
        end_date (datetime | None | UnsetType): Due date of return.
        returned (bool | None | UnsetType): Whether the book is returned.
    """
    id: Union[int, None, UnsetType] = UNSET
    member_id: Union[int, None, UnsetType] = UNSET
    book_id: Union[int, None, UnsetType] = UNSET
    start_date: Union[datetime, None, UnsetType] = UNSET
    end_date: Union[datetime, None, UnsetType] = UNSET
    returned: Union[bool, None, UnsetType] = UNSET


@dataclass
class CategoryModel(BaseTableModel):
    """
    Represents a Category table record stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the category.
        name (str | None | UnsetType): Category name.
        description (str | None | UnsetType): Description text.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    description: Union[str, None, UnsetType] = UNSET


@dataclass
class GuestModel(BaseTableModel):
    """
    Represents a Guest table record stored in the database.

    Attributes:
        id (UUID | None | UnsetType): Unique guest identifier.
        created_time (datetime | None | UnsetType): Guest creation time.
        request_count (int | None | UnsetType): Number of requests made.
    """
    id: Union[UUID, None, UnsetType] = UNSET
    created_time: Union[datetime, None, UnsetType] = UNSET
    request_count: Union[int, None, UnsetType] = UNSET


@dataclass
class LibrarianModel(BaseTableModel):
    """
    Represents a Librarian table record stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the librarian.
        name (str | None | UnsetType): Librarian's name.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET


@dataclass
class LibrarianActivityLogModel(BaseTableModel):
    """
    Represents a LibrarianActivityLog table record stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the log entry.
        librarian_id (int | None | UnsetType): Related librarian ID.
        action_type (LibrarianAction | None | UnsetType): Type of action.
        book_id (int | None | UnsetType): Related book ID.
        member_id (int | None | UnsetType): Related member ID.
        timestamp (datetime | None | UnsetType): Time of the action.
    """
    id: Union[int, None, UnsetType] = UNSET
    librarian_id: Union[int, None, UnsetType] = UNSET
    action_type: Union[LibrarianAction, None, UnsetType] = UNSET
    book_id: Union[int, None, UnsetType] = UNSET
    member_id: Union[int, None, UnsetType] = UNSET
    timestamp: Union[datetime, None, UnsetType] = UNSET


@dataclass
class MemberModel(BaseTableModel):
    """
    Represents a Member table record stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the member.
        name (str | None | UnsetType): Member's name.
        email (str | None | UnsetType): Member's email address.
        join_date (datetime | None | UnsetType): Date of joining.
        active (bool | None | UnsetType): Membership activity status.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    email: Union[str, None, UnsetType] = UNSET
    join_date: Union[datetime, None, UnsetType] = UNSET
    active: Union[bool, None, UnsetType] = UNSET


@dataclass
class MessageModel(BaseTableModel):
    """
    Represents a Message table record stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the message.
        user_id (int | None | UnsetType): ID of the related user.
        message (str | None | UnsetType): Message content.
        created_time (datetime | None | UnsetType): Message creation time.
        seen (bool | None | UnsetType): Whether the message is seen.
    """
    id: Union[int, None, UnsetType] = UNSET
    user_id: Union[int, None, UnsetType] = UNSET
    message: Union[str, None, UnsetType] = UNSET
    created_time: Union[datetime, None, UnsetType] = UNSET
    seen: Union[bool, None, UnsetType] = UNSET


@dataclass
class PublisherModel(BaseTableModel):
    """
    Represents a Publisher table record stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the publisher.
        name (str | None | UnsetType): Publisher name.
        address (str | None | UnsetType): Publisher address.
        contact_email (str | None | UnsetType): Contact email address.
        phone (str | None | UnsetType): Contact phone number.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    address: Union[str, None, UnsetType] = UNSET
    contact_email: Union[str, None, UnsetType] = UNSET
    phone: Union[str, None, UnsetType] = UNSET

@dataclass
class UserModel(BaseTableModel):
    """
    Represents a User table records stored in the database.

    Attributes:
        id (int | None | UnsetType): Unique identifier for the user.
        username (str | None | UnsetType): User's unique login name.
        hashed_password (str | None | UnsetType): Securely hashed version of the user's password.
    """
    id: Union[int, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET
    
@dataclass
class TestingModel(BaseTableModel):
    """
    Test model for testing. Not actual representation of main application tables.

    Attributes:
        id (int | None | UnsetType) 
        name (str | None | UnsetType) 
        age (int | None | UnsetType)
        description (str | None | UnsetType) 
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    age: Union[int, None, UnsetType] = UNSET
    description: Union[str, None, UnsetType] = UNSET


# SQL View Models
class BaseViewModel:
    pass

@dataclass
class AdminViewModel(BaseViewModel):
    """
    Represents a view of joined user and admin details.

    Attributes:
        id (int | None | UnsetType): Unique identifier of the admin.
        username (str | None | UnsetType): Admin's username.
        hashed_password (str | None | UnsetType): Hashed password.
    """
    id: Union[int, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET


@dataclass
class AuthorViewModel(BaseViewModel):
    """
    Represents a view of author details along with related books.

    Attributes:
        id (int | None | UnsetType): Author ID.
        name (str | None | UnsetType): Author's name.
        books (str | None | UnsetType): Comma-separated list of book titles.
        biography (str | None | UnsetType): Author biography.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    books: Union[str, None, UnsetType] = UNSET
    biography: Union[str, None, UnsetType] = UNSET


@dataclass
class BookViewModel(BaseViewModel):
    """
    Represents a view of book details including authors, category, and publisher.

    Attributes:
        id (int | None | UnsetType): Book ID.
        title (str | None | UnsetType): Book title.
        publisher (str | None | UnsetType): Publisher name.
        author (str | None | UnsetType): Author name(s).
        category (str | None | UnsetType): Category name(s).
        total_copies (int | None | UnsetType): Total copies.
        available_copies (int | None | UnsetType): Available copies.
    """
    id: Union[int, None, UnsetType] = UNSET
    title: Union[str, None, UnsetType] = UNSET
    publisher: Union[str, None, UnsetType] = UNSET
    author: Union[str, None, UnsetType] = UNSET
    category: Union[str, None, UnsetType] = UNSET
    total_copies: Union[int, None, UnsetType] = UNSET
    available_copies: Union[int, None, UnsetType] = UNSET


@dataclass
class BorrowingViewModel(BaseViewModel):
    """
    Represents a view of borrowing records.

    Attributes:
        id (int | None | UnsetType): Borrowing record ID.
        name (str | None | UnsetType): Member name.
        book (str | None | UnsetType): Borrowed book title.
        start_date (datetime | None | UnsetType): Borrow start date.
        end_date (datetime | None | UnsetType): Borrow end date.
        returned (bool | None | UnsetType): Return status.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    book: Union[str, None, UnsetType] = UNSET
    start_date: Union[datetime, None, UnsetType] = UNSET
    end_date: Union[datetime, None, UnsetType] = UNSET
    returned: Union[bool, None, UnsetType] = UNSET


@dataclass
class CategoryViewModel(BaseViewModel):
    """
    Represents a view of category details including related books.

    Attributes:
        id (int | None | UnsetType): Category ID.
        name (str | None | UnsetType): Category name.
        books (str | None | UnsetType): Comma-separated book titles.
        description (str | None | UnsetType): Category description.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    books: Union[str, None, UnsetType] = UNSET
    description: Union[str, None, UnsetType] = UNSET


@dataclass
class LibrarianActivityLogViewModel(BaseViewModel):
    """
    Represents a view of librarian activity logs.

    Attributes:
        id (int | None | UnsetType): Log entry ID.
        librarian_name (str | None | UnsetType): Librarian name.
        action_type (LibrarianAction | None | UnsetType): Type of action.
        book (str | None | UnsetType): Related book title.
        member (str | None | UnsetType): Related member name.
        timestamp (datetime | None | UnsetType): Time of action.
    """
    id: Union[int, None, UnsetType] = UNSET
    librarian_name: Union[str, None, UnsetType] = UNSET
    action_type: Union[LibrarianAction, None, UnsetType] = UNSET
    book: Union[str, None, UnsetType] = UNSET
    member: Union[str, None, UnsetType] = UNSET
    timestamp: Union[datetime, None, UnsetType] = UNSET


@dataclass
class LibrarianViewModel(BaseViewModel):
    """
    Represents a view of librarian details including user account.

    Attributes:
        id (int | None | UnsetType): Librarian ID.
        name (str | None | UnsetType): Librarian name.
        username (str | None | UnsetType): User account username.
        hashed_password (str | None | UnsetType): Hashed password.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET


@dataclass
class MemberViewModel(BaseViewModel):
    """
    Represents a view of member details including user account.

    Attributes:
        id (int | None | UnsetType): Member ID.
        name (str | None | UnsetType): Member name.
        username (str | None | UnsetType): User account username.
        hashed_password (str | None | UnsetType): Hashed password.
        email (str | None | UnsetType): Member email.
        join_date (datetime | None | UnsetType): Join date.
        active (bool | None | UnsetType): Membership status.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET
    email: Union[str, None, UnsetType] = UNSET
    join_date: Union[datetime, None, UnsetType] = UNSET
    active: Union[bool, None, UnsetType] = UNSET


@dataclass
class MemberWithoutPasswordViewModel(BaseViewModel):
    """
    Represents a view of member details excluding password.

    Attributes:
        id (int | None | UnsetType): Member ID.
        name (str | None | UnsetType): Member name.
        username (str | None | UnsetType): User account username.
        email (str | None | UnsetType): Member email.
        join_date (datetime | None | UnsetType): Join date.
        active (bool | None | UnsetType): Membership status.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    email: Union[str, None, UnsetType] = UNSET
    join_date: Union[datetime, None, UnsetType] = UNSET
    active: Union[bool, None, UnsetType] = UNSET


@dataclass
class MembersBorrowRequestViewModel(BaseViewModel):
    """
    Represents a view of members' borrow requests.

    Attributes:
        id (int | None | UnsetType): Borrow request ID.
        name (str | None | UnsetType): Member name.
        book (str | None | UnsetType): Requested book title.
        request_timestamp (datetime | None | UnsetType): Request timestamp.
        status (BorrowRequestStatus | None | UnsetType): Request status.
        handled_at (datetime | None | UnsetType): Handling timestamp.
        handled_by (str | None | UnsetType): Librarian name who handled it.
        note (str | None | UnsetType): Optional note.
    """
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
    """
    Represents a view of messages for a user.

    Attributes:
        id (int | None | UnsetType): Message ID.
        to (str | None | UnsetType): Receiver username.
        receiver_role (UserType | None | UnsetType): Role of receiver.
        message (str | None | UnsetType): Message content.
        created_time (datetime | None | UnsetType): Time of creation.
        seen (bool | None | UnsetType): Seen status.
    """
    id: Union[int, None, UnsetType] = UNSET
    to: Union[str, None, UnsetType] = UNSET
    receiver_role: Union[UserType, None, UnsetType] = UNSET
    message: Union[str, None, UnsetType] = UNSET
    created_time: Union[datetime, None, UnsetType] = UNSET
    seen: Union[bool, None, UnsetType] = UNSET


@dataclass
class PublisherViewModel(BaseViewModel):
    """
    Represents a view of publisher details including related books.

    Attributes:
        id (int | None | UnsetType): Publisher ID.
        name (str | None | UnsetType): Publisher name.
        address (str | None | UnsetType): Publisher address.
        contact_email (str | None | UnsetType): Contact email.
        phone (str | None | UnsetType): Contact phone.
        books (str | None | UnsetType): Comma-separated book titles.
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    address: Union[str, None, UnsetType] = UNSET
    contact_email: Union[str, None, UnsetType] = UNSET
    phone: Union[str, None, UnsetType] = UNSET
    books: Union[str, None, UnsetType] = UNSET


@dataclass
class UserViewModel(BaseViewModel):
    """
    Represents a view of user details with role info.

    Attributes:
        id (int | None | UnsetType): User ID.
        username (str | None | UnsetType): User account username.
        hashed_password (str | None | UnsetType): Hashed password.
        name (str | None | UnsetType): Full name.
        user_type (UserType | None | UnsetType): Role type.
    """
    id: Union[int, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    hashed_password: Union[str, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    user_type: Union[UserType, None, UnsetType] = UNSET


@dataclass
class UserWithoutPasswordViewModel(BaseViewModel):
    """
    Represents a view of user details excluding password.

    Attributes:
        id (int | UUID | None | UnsetType): User ID.
        username (str | None | UnsetType): Username.
        name (str | None | UnsetType): Full name.
        user_type (UserType | None | UnsetType): Role type.
    """
    id: Union[int, UUID, None, UnsetType] = UNSET
    username: Union[str, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    user_type: Union[UserType, None, UnsetType] = UNSET
    
@dataclass
class TestingViewModel(BaseViewModel):
    """
    Represents a view of Test model for testing. Not actual representation of main application views.

    Attributes:
        id (int | None | UnsetType) 
        name (str | None | UnsetType) 
        age (int | None | UnsetType)
        description (str | None | UnsetType) 
    """
    id: Union[int, None, UnsetType] = UNSET
    name: Union[str, None, UnsetType] = UNSET
    age: Union[int, None, UnsetType] = UNSET
    description: Union[str, None, UnsetType] = UNSET
    
# Other Models

@dataclass
class PlainUserModel:
    """
    Represents a plain user input model containing raw username and password.
    
    Attributes:
        username (str): User's unique login name.
        password (str): User's raw password.
    """
    username: Union[str, None, UnsetType] = UNSET
    password: Union[str, None, UnsetType] = UNSET