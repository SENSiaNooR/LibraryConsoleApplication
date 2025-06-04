
class DBTypes:
    BORROW_REQUEST_STATUS = '"BorrowRequestStatus"'
    LIBRARIAN_ACTION = '"LibrarianAction"'
    USER_TYPE = '"UserType"'

class DBTables:
    ADMIN = '"Admin"'
    AUTHOR = '"Author"'
    BOOK = '"Book"'
    BOOK_AUTHOR = '"BookAuthor"'
    BOOK_CATEGORY = '"BookCategory"'
    BORROW_REQUEST = '"BorrowRequest"'
    BORROWING = '"Borrowing"'
    CATEGORY = '"Category"'
    GUEST = '"Guest"'
    LIBRARIAN = '"Librarian"'
    LIBRARIAN_ACTIVITY_LOG = '"LibrarianActivityLog"'
    MEMBER = '"Member"'
    MESSAGE = '"Message"'
    PUBLISHER = '"Publisher"'
    USER = '"User"'

class DBViews:
    ADMIN_VIEW = '"AdminView"'
    AUTHOR_VIEW = '"AuthorView"'
    BOOK_VIEW = '"BookView"'
    BORROWING_VIEW = '"BorrowingView"'
    CATEGORY_VIEW = '"CategoryView"'
    LIBRARIAN_VIEW = '"LibrarianView"'
    MEMBER_VIEW = '"MemberView"'
    MEMBER_WITHOUT_PASSWORD_VIEW = '"MemberWithoutPasswordView"'
    MEMBERS_BORROW_REQUEST_VIEW = '"MembersBorrowRequestView"'
    PUBLISHER_VIEW = '"PublisherView"'
    USER_VIEW = '"UserView"'
    USER_WITHOUT_PASSWORD_VIEW = '"UserWithoutPasswordView"'

class DBTableColumns:
    class Admin:
        USER_ID = "user_id"
    
    class Author:
        ID = "id"
        NAME = "name"
        BIOGRAPHY = "biography"
    
    class Book:
        ID = "id"
        TITLE = "title"
        PUBLISHER_ID = "publisher_id"
        TOTAL_COPIES = "total_copies"
        AVAILABLE_COPIES = "available_copies"
        
    class BookAuthor:
        BOOK_ID = "book_id"
        AUTHOR_ID = "author_id"
      
    class BookCategory:
        BOOK_ID = "book_id"
        CATEGORY_ID = "category_id"
       
    class BorrowRequest:
        ID = "id"
        MEMBER_ID = "member_id"
        BOOK_ID = "book_id"
        REQUEST_TIMESTAMP = "request_timestamp"
        STATUS = "status"
        HANDLED_AT = "handled_at"
        HANDLED_BY = "handled_by"
        NOTE = "note"
        
    class Borrowing:
        ID = "id"
        MEMBER_ID = "member_id"
        BOOK_ID = "book_id"
        START_DATE = "start_date"
        END_DATE = "end_date"
        RETURNED = "returned"
        
    class Category:
        ID = "id"
        NAME = "name"
        DESCRIPTION = "description"
        
    class Guest:
        ID = "id"
        CREATED_TIME = "created_time"
        REQUEST_COUNT = "request_count"
    
    class Librarian:
        USER_ID = "user_id"
        NAME = "name"
    
    class LibrarianActivityLog:
        ID = "id"
        LIBRARIAN_ID = "librarian_id"
        ACTION_TYPE = "action_type"
        BOOK_ID = "book_id"
        MEMBER_ID = "member_id"
        TIMESTAMP = "timestamp"

    class Member:
        USER_ID = "user_id"
        NAME = "name"
        EMAIL = "email"
        JOIN_DATE = "join_date"
        ACTIVE = "active"
      
    class Message:
        ID = "id"
        USER_ID = "user_id"
        MESSAGE = "message"
        CREATED_TIME = "created_time"
        SEEN = "seen"
       
    class Publisher:
        ID = "id"
        NAME = "name"
        ADDRESS = "address"
        CONTACT_EMAIL = "contact_email"
        PHONE = "phone"
        
    class User:
        ID = "id"
        USERNAME = "username"
        HASHED_PASSWORD = "hashed_password"


class DBViewColumns:

    class AdminView:
        ID = "id"
        USERNAME = "username"
        HASHED_PASSWORD = "hashed_password"

    class AuthorView:
        ID = "id"
        NAME = "name"
        BOOKS = "books"
        BIOGRAPHY = "biography"

    class BookView:
        ID = "id"
        TITLE = "title"
        PUBLISHER = "publisher"
        AUTHOR = "author"
        CATEGORY = "category"
        TOTAL_COPIES = "total_copies"
        AVAILABLE_COPIES = "available_copies"

    class BorrowingView:
        ID = "id"
        NAME = "name"
        BOOK = "book"
        START_DATE = "start_date"
        END_DATE = "end_date"
        RETURNED = "returned"

    class CategoryView:
        ID = "id"
        NAME = "name"
        BOOKS = "books"
        DESCRIPTION = "description"

    class LibrarianActivityLogView:
        ID = "id"
        LIBRARIAN_NAME = "librarian_name"
        ACTION_TYPE = "action_type"
        BOOK = "book"
        MEMBER = "member"
        TIMESTAMP = "timestamp"

    class LibrarianView:
        ID = "id"
        NAME = "name"
        USERNAME = "username"
        HASHED_PASSWORD = "hashed_password"

    class MemberView:
        ID = "id"
        NAME = "name"
        USERNAME = "username"
        HASHED_PASSWORD = "hashed_password"
        EMAIL = "email"
        JOIN_DATE = "join_date"
        ACTIVE = "active"
        
    class MemberWithoutPasswordView:
        ID = "id"
        NAME = "name"
        USERNAME = "username"
        EMAIL = "email"
        JOIN_DATE = "join_date"
        ACTIVE = "active"

    class MembersBorrowRequestView:
        ID = "id"
        NAME = "name"
        BOOK = "book"
        REQUEST_TIMESTAMP = "request_timestamp"
        STATUS = "status"
        HANDLED_AT = "handled_at"
        HANDLED_BY = "handled_by"
        NOTE = "note"

    class PublisherView:
        ID = "id"
        NAME = "name"
        ADDRESS = "address"
        CONTACT_EMAIL = "contact_email"
        PHONE = "phone"
        BOOKS = "books"

    class UserView:
        ID = "id"
        USERNAME = "username"
        HASHED_PASSWORD = "hashed_password"
        NAME = "name"
        USER_TYPE = "user_type"

    class UserWithoutPasswordView:
        ID = "id"
        USERNAME = "username"
        NAME = "name"
        USER_TYPE = "user_type"       
