from abc import ABC
from uuid import UUID
from typing import Optional
from Core.JWT import JWTManager
from Services.Decorators import token_required
from DataAccess.BookRepository import BookRepository
from Models.Models import UserWithoutPasswordViewModel
from DataAccess.AuthorRepository import AuthorRepository
from DataAccess.CategoryRepository import CategoryRepository
from DataAccess.PublisherRepository import PublisherRepository
from Models.Models import UNSET, AuthorViewModel, BookViewModel, CategoryModel, CategoryViewModel, PublisherViewModel


class BaseServices(ABC):
    
    def __init__(self, token):
        self.token = token
        jwt_manager = JWTManager()
        payload = jwt_manager.decode_token(self.token)
        try:
            payload["id"] = UUID(payload["id"])
        except:
            pass
        self.user_model = UserWithoutPasswordViewModel(payload['id'], payload['username'], payload['name'], payload['user_type'])
        

    def my_info(self):
        return f'hi {self.user_model.name}. your username is {self.user_model.username} and your role is {self.user_model.user_type}'
    
    def get_all_books(self):
        return BookRepository.view_many(BookViewModel())
    
    def get_all_publishers(self):
        return PublisherRepository.view_many(PublisherViewModel())

    def publisher_search(self, name : str = ''):
        if name == '':
            name = UNSET
        return PublisherRepository.view_many(PublisherViewModel(name = name))
    
    def get_all_authors(self):
        return AuthorRepository.view_many(AuthorViewModel())
    
    def author_search(self, name : str = ''):
        if name == '':
            name = UNSET
        return AuthorRepository.view_many(AuthorViewModel(name = name))

    def get_all_categories(self):
        return CategoryRepository.view_many(CategoryViewModel())
    
    def categories_list(self):
        l = CategoryRepository.get_many(CategoryModel())
        return [c.name for c in l]

    def book_advance_search(
        self,
        title : str = '',
        publisher : str = '',
        author : str = '',
        categories: Optional[list[str]] = None,
        just_available: bool = False
    ):
        if categories is None:
            categories = []

        if title == '':
            title = UNSET

        if publisher == '':
            publisher = UNSET
            
        if author == '':
            author = UNSET

        result = []
            
        if not categories:
            book_model = BookViewModel(
                title = title,
                publisher = publisher,
                author = author
            )
            result = BookRepository.view_many(book_model)
        
        else:
            for category in categories:
                book_model = BookViewModel(
                    title = title,
                    publisher = publisher,
                    author = author,
                    category = category
                )
                result += BookRepository.view_many(book_model)
                
            books_dict = {book.id : book for book in result}
            result = list(books_dict.values())

        if just_available:
            result = [book for book in result if book.available_copies != 0]
            
        return result
    
    def book_search(self, title : str = ''):
        if title == '':
            title = UNSET
        book_model = BookViewModel(title = title)
        return BookRepository.view_many(book_model)
    
    def about_us(self):
        # بعدا یه جدول در دیتابیس مختص داده های این مدلی درست میکنم که از دیتا بیس اطلاعات برگردونده شه
        return f'برنامه مدیریت کتابخانه که توسط SENSIAN ساخته شده\n'\
            f'Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.\n'\
            f'Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.\n'\
            f'لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد، تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی، و فرهنگ پیشرو در زبان فارسی ایجاد کرد، در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها، و شرایط سخت تایپ به پایان رسد و زمان مورد نیاز شامل حروفچینی دستاوردهای اصلی، و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد.'

        
