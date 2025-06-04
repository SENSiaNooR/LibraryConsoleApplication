
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
    MEMBERS_BORROW_REQUEST_VIEW = '"MembersBorrowRequestView"'
    PUBLISHER_VIEW = '"PublisherView"'
    USER_VIEW = '"UserView"'
    USER_WITHOUT_PASSWORD_VIEW = '"UserWithoutPasswordView"'

class DBColumns:
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
        
