import time
from turtle import width
import keyboard
from typing import List
from Core.Validations import Validations
from Exceptions.Exceptions import ReachedToRequestLimitError
from Models.Models import AuthorViewModel, BookViewModel, CategoryViewModel, MemberModel, PlainUserModel, PublisherViewModel
from Presentation.ConsoleUI.Components.PageHelper import PageHelper
from Presentation.ConsoleUI.Components.ConsoleExtension import ConsoleExtension
from Presentation.ConsoleUI.Components.Element import Element
from Presentation.ConsoleUI.Components.InputBox import InputBox
from Presentation.ConsoleUI.Components.Button import Button
from Presentation.ConsoleUI.Components.Page import Page
from Presentation.ConsoleUI.Components.SizeAndPosition import SizeAndPosition
from Presentation.ConsoleUI.Components.Table import Table
from Presentation.ConsoleUI.Components.Text import Text
from Services.AuthServices import AuthServices
from Services.GuestServices import GuestServices


class GuestPanel:
    
    _page_position : SizeAndPosition

    def __init__(self, token):
        self.service_provider = GuestServices(token)
        self.token = token
        self._page_position = SizeAndPosition(30,1,36,150)

    def _create_page(self, title: str) -> Page:
        page = Page(self._page_position)
        guest_model = self.service_provider.get_guest_model()
        page.add_element(Text(title, SizeAndPosition(left = (self._page_position.width - 20) // 2, width = 20), halign='c'))
        page.add_element(
            Text(
                content = f'id = {guest_model.id}\nدرخواست ها : {guest_model.request_count}\nکاربر : مهمان',
                position = SizeAndPosition(left = 1, top = 0)
            )
        )
        page.add_element(
            Text(
                content = ' با استفاده از کلید های ← → ↓ ↑ بین گزینه ها جابجا شوید و با کلید Enter گزینه مورد نظر را انتخاب کنید.',
                position = SizeAndPosition(top = self._page_position.height - 1, width = self._page_position.width),
                halign = 'r'
            )
        )
        return page

    #==================================== Home Page =================================
    def get_homepage(self) -> Page:
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()

        page = self._create_page('صفحه اصلی')
        
        #=============================================================================
        #=========================== Elements Initializing ===========================
        
        signup_button = Button(
            text = f'ثبت نام',
            position = SizeAndPosition(left = 124, top = 0, width = 8),
            halign = 'c'
        )
        login_button = Button(
            text = f'ورود',
            position = SizeAndPosition(left = 139, top = 0, width = 5),
            halign = 'c'
        )
        books_button = Button(
            text = f'کتاب ها',
            position = SizeAndPosition(top = 10, width = 150),
            halign = 'c'
        )
        publishers_button = Button(
            text = f'ناشرین',
            position = SizeAndPosition(top = 12, width = 150),
            halign = 'c'
        )
        authors_button = Button(
            text = f'مولفین',
            position = SizeAndPosition(top = 14, width = 150),
            halign = 'c'
        )
        categories_button = Button(
            text = f'دسته بندی ها',
            position = SizeAndPosition(top = 16, width = 150),
            halign = 'c'
        )
        about_us_button = Button(
            text = f'درباره ما',
            position = SizeAndPosition(top = 18, width = 150),
            halign = 'c'
        )
        exit_button = Button(
            text = f'خروج',
            position = SizeAndPosition(top = 20, width = 150),
            halign = 'c'
        )
       
        #=============================================================================
        #=========================== Page Initializing ===============================
        page.elements += [
                books_button, exit_button, about_us_button, categories_button, authors_button,
                publishers_button, login_button, signup_button
        ]
        page.update_focused()
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
        page.auto_link_focusables_angle_base(0.27)  
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        
        def exit():
            page.exit_flag = True
        exit_button.click_func = exit
            
        def signup():
            return self.get_signup_page()
        signup_button.click_func = signup
        
        def login():
            return self.get_login_page()
        login_button.click_func = login
        
        def books():
            return self.get_books_page()
        books_button.click_func = books
        
        def publishers():
            return self.get_publishers_page()
        publishers_button.click_func = publishers

        def authors():
            return self.get_authors_page()
        authors_button.click_func = authors

        def categories():
            return self.get_categories_page()
        categories_button.click_func = categories

        def about_us():
            return self.get_about_us()
        about_us_button.click_func = about_us
            
        return page
       

    #==================================== Request Limited Page =================================
    def get_request_limited_page(self) -> Page:
         
        page = self._create_page('متاسفیم!')

        #=============================================================================
        #=========================== Elements Initializing ===========================
        signup_button = Button(
            text = f'ثبت نام',
            position = SizeAndPosition(left = 124, top = 0, width = 8),
            halign = 'c'
        )
        login_button = Button(
            text = f'ورود',
            position = SizeAndPosition(left = 139, top = 0, width = 5),
            halign = 'c'
        )
        tip = Text(
            content = f'تعداد درخواست های شما از حد مجاز عبور کرده یا مدت زمان شما به اتمام رسیده است.\n'
            'لطفا پس از خروج مجددا وارد شوید یا در برنامه ما ثبت نام کنید تا از کلیه خدمات بهره مند شوید.\n'
            'با تشکر (:',
            position = SizeAndPosition(width = 150, top = 8),
            halign = 'c'
        )
        exit_button = Button(
            text = f'خروج',
            position = SizeAndPosition(top = 16, width = 150),
            halign = 'c'
        )
        #=============================================================================
        #=========================== Page Initializing ===============================
        page.elements += [exit_button, login_button, signup_button, tip]
        page.update_focused()
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
        page.auto_link_focusables_angle_base(0.27)
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        
        def exit():
            page.exit_flag = True
        exit_button.click_func = exit
            
        def signup():
            return self.get_signup_page()
        signup_button.click_func = signup
        
        def login():
            return self.get_login_page()
        login_button.click_func = login
            
        return page
    
    
    #==================================== Signup Page =================================
    def get_signup_page(self) -> Page:
        
        page = self._create_page('صفحه ثبت نام')

        #=============================================================================
        #=========================== Elements Initializing ===========================
        name = Text(
            content = f': نام و نام خانوادگی',
            position = SizeAndPosition(left = 10, top = 8)
        )
        name_input_box = InputBox(
            display_text = 'نام و نام خانوادگی خود را وارد کنید',
            position = SizeAndPosition(left = 32, top = 8)
        )
        email = Text(
            content = f': ایمیل',
            position = SizeAndPosition(left = 10, top = 10)
        )
        email_input_box = InputBox(
            display_text = 'ایمیل خود را وارد کنید',
            checker = Validations.email_validation,
            position = SizeAndPosition(left = 32, top = 10)
        )
        username = Text(
            content = f': نام کاربری',
            position = SizeAndPosition(left = 80, top = 8)
        )
        username_input_box = InputBox(
            display_text = 'نام کاربری دلخواه خود را وارد کنید',
            checker = Validations.username_validation,
            position = SizeAndPosition(left = 95, top = 8)
        )
        password = Text(
            content = f': پسورد',
            position = SizeAndPosition(left = 10, top = 12)
        )
        password_input_box = InputBox(
            display_text = 'پسورد خود را انتخاب کنید',
            checker = Validations.password_validation,
            position = SizeAndPosition(left = 32, top = 12),
            password_mode = True
        )
        repeat_password = Text(
            content = f': تکرار پسورد',
            position = SizeAndPosition(left = 80, top = 12)
        )
        repeat_password_input_box = InputBox(
            display_text = 'پسورد خود را مجددا وارد کنید',
            checker = lambda password : (password_input_box.content == password),
            position = SizeAndPosition(left = 95, top = 12),
            password_mode = True
        )
        helper = Table(
            data = [[Text(
                content = 'توجه\n\n'
                'نام کاربری باید ترکیبی از حروف انگلیسی و علامت _ باشد.\n'
                'رمز عبور بایستی شامل حداقل یک حروف و یک اعداد باشد و طول آن بیش از 8 کاراکتر باشد\n'
                'در صورتی که قبلا ثبت نام کرده اید بر روی گزینه ورود کلیک کنید',
                position = SizeAndPosition(width = 110, height = 6),
                halign = 'c',
                valign = 'm'
            )]],
            position = SizeAndPosition(top = 16, left = 18),
            show_row_id = False
        )
        error_text = Text(
            content = '',
            position = SizeAndPosition(top = 25, width = 150),
            halign = 'c'
        )
        signup_button = Button(
            text = 'ثبت نام',
            position = SizeAndPosition(top = 27, width = 150),
            halign = 'c'
        )
        login_button = Button(
            text = 'قبلا ثبت نام کرده ام (ورود)',
            position = SizeAndPosition(top = 29, width = 150),
            halign = 'c'
        )
        back_button = Button(
            text = 'ادامه دادن در حالت مهمان',
            position = SizeAndPosition(top = 31, width = 150),
            halign = 'c'
        )
        #=============================================================================
        #=========================== Page Initializing ===============================
        page.elements += [
            name, email, username, password, repeat_password,
            name_input_box, email_input_box, username_input_box, password_input_box, repeat_password_input_box,
            signup_button, login_button, back_button, helper, error_text
        ]
        page.update_focused()
        
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
        page.auto_link_focusables_grid_base()
        email_input_box.linked_elements['r'] = username_input_box
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        
        def signup():
            if not email_input_box.check():
                ConsoleExtension.clear_area(error_text.position , page.position)
                error_text.content = 'ایمل وارد شده صحیح نمی باشد'
                return
            
            if not username_input_box.check():
                ConsoleExtension.clear_area(error_text.position , page.position)
                error_text.content = 'نام کاربری وارد شده صحیح نمی‌ باشد'
                return
            
            if not password_input_box.check():
                ConsoleExtension.clear_area(error_text.position , page.position)
                error_text.content = 'رمز عبور وارد شده معتبر نیست'
                return
            
            if password_input_box.content != repeat_password_input_box.content:
                ConsoleExtension.clear_area(error_text.position , page.position)
                error_text.content = 'رمز عبور های وارد شده یکسان نیستند.'
                return
            
            member_model = MemberModel(
                name = name_input_box.content,
                email = email_input_box.content,
            )
            plain_user = PlainUserModel(
                username = username_input_box.content,
                password = password_input_box.content
            )
            
            try:
                token = AuthServices.signup(plain_user, member_model)
            except Exception as ex:
                error_text.content = str(ex)
            else:
                print(token)        
        signup_button.click_func = signup
         
        def login():
            return self.get_login_page()
        login_button.click_func = login
        
        def back():
            return self.get_homepage()
        back_button.click_func = back
        
        return page
    

    #==================================== Login Page =================================
    def get_login_page(self) -> Page:
        
        page = self._create_page('صفحه ورود')
        
        #=============================================================================
        #=========================== Elements Initializing ===========================       
        username = Text(
            content = f': نام کاربری',
            position = SizeAndPosition(left = 50, top = 8)
        )
        username_input_box = InputBox(
            display_text = 'نام کاربری خود را وارد کنید',
            checker = Validations.username_validation,
            position = SizeAndPosition(left = 65, top = 8)
        )
        password = Text(
            content = f': پسورد',
            position = SizeAndPosition(left = 50, top = 10)
        )
        password_input_box = InputBox(
            display_text = 'پسورد خود را وارد کنید',
            checker = lambda p : (len(p) > 0),
            position = SizeAndPosition(left = 65, top = 10),
            password_mode = True
        )
        error_text = Text(
            content = '',
            position = SizeAndPosition(top = 14, width = 150),
            halign = 'c'
        )
        login_button = Button(
            text = 'ورود',
            position = SizeAndPosition(top = 27, width = 150),
            halign = 'c'
        )
        signup_button = Button(
            text = 'حساب ندارم. یک حساب بسازید (ثبت نام)',
            position = SizeAndPosition(top = 29, width = 150),
            halign = 'c'
        )
        back_button = Button(
            text = 'ادامه دادن در حالت مهمان',
            position = SizeAndPosition(top = 31, width = 150),
            halign = 'c'
        )

        #=============================================================================
        #=========================== Page Initializing ===============================
        page.elements += [
            username, password, username_input_box, password_input_box,
            signup_button, login_button, back_button, error_text
        ]
        page.update_focused()
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
        page.auto_link_focusables_grid_base()
        #=============================================================================
        #=========================== Click Functions Initializing ====================

        def signup():
            return self.get_signup_page()    
        signup_button.click_func = signup
         
        def login():
            if not username_input_box.check():
                ConsoleExtension.clear_area(error_text.position , page.position)
                error_text.content = 'نام کاربری یا رمز عبور صحیح نمی باشد'
                return
            
            if not password_input_box.check():
                ConsoleExtension.clear_area(error_text.position , page.position)
                error_text.content = 'رمز عبور نمی تواند خالی باشد'
                return
            
            try:
                plain_user = PlainUserModel(username_input_box.content, password_input_box.content)
                login_res = AuthServices.login(plain_user)
            except Exception as ex:
                error_text.content = str(ex)
                return
            else:
                print(login_res)
                return  
        login_button.click_func = login
        
        def back():
            return self.get_homepage()  
        back_button.click_func = back
        
        return page
    

    #==================================== Books Page =================================
    def get_books_page(self) -> Page:
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()
        
        page = self._create_page('صفحه کتب')
        page.bag_set('table_header', [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')])
        page.bag_set('table_page', 1)
        #=============================================================================
        #=========================== Elements Initializing ===========================       
        book_name_input_box = InputBox(
            display_text = 'نام کتاب را وارد کنید',
            position = SizeAndPosition(left = 63, top = 3)
        )
        search_button = Button(
            text = 'جست و جو',
            position = SizeAndPosition(top = 5, left = 58)
        )
        advance_search_button = Button(
            text = 'جست و جوی پیشرفته',
            position = SizeAndPosition(top = 5, left = 75)
        )
        books_table = Table([[]], SizeAndPosition(top = 7))
        prev_button = Button(
            text = 'قبلی',
            position = SizeAndPosition(top = 31, left = 40)
        )
        cur_page = Text(
            content = f'صفحه {page.bag_get("table_page")}',
            position = SizeAndPosition(top = 31, left = 71)
        )
        next_button = Button(
            text = 'بعدی',
            position = SizeAndPosition(top = 31, left = 100)
        )
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 33, width = 150),
            halign = 'c'
        )
        #=============================================================================
        #=========================== Adding Page Elements ============================
        page.elements += [
            book_name_input_box, search_button, advance_search_button, prev_button, next_button, cur_page, back_button, books_table
        ]
        page.update_focused()
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
        page.auto_link_focusables_grid_base()
        search_button.linked_elements['d'] = prev_button
        advance_search_button.linked_elements['d'] = next_button
        
        prev_button.linked_elements['u'] = search_button
        prev_button.linked_elements['d'] = back_button
        
        next_button.linked_elements['u'] = advance_search_button
        next_button.linked_elements['d'] = back_button
        
        back_button.linked_elements['u'] = next_button
        back_button.linked_elements['r'] = next_button
        back_button.linked_elements['l'] = prev_button
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        
        def refresh_books_table():
            start_row = (page.bag_get("table_page", 1) - 1) * 10
            end_row = (page.bag_get("table_page", 1) * 10)
            end_row = min(len(page.bag_get('fetch')), end_row)
        
            table_content : List[List[Element]] = [
                page.bag_get('table_header')
            ]
            for row in page.bag_get('fetch')[start_row:end_row]:
                table_row = [
                    Text(ConsoleExtension.short_text(row.title, 30),halign='c'),
                    Text(ConsoleExtension.short_text(row.publisher, 20),halign='c'),
                    Text(ConsoleExtension.short_text(row.author, 35),halign='c'),
                    Text(ConsoleExtension.short_text(row.category, 50),halign='c')
                ]
                table_content.append(table_row)
            
            ConsoleExtension.clear_area(books_table.position, page.position)
            
            books_table.update(table_content, start_row_id=start_row)
            books_table.position.left = (150 - books_table.position.width) // 2
        
            ConsoleExtension.clear_area(next_button.position, page.position)
            ConsoleExtension.clear_area(cur_page.position, page.position)
            ConsoleExtension.clear_area(prev_button.position, page.position)
            
            next_button.position.top = books_table.position.bottom + 1
            cur_page.position.top = books_table.position.bottom + 1
            prev_button.position.top = books_table.position.bottom + 1


        def search():
            try:
                page.bag_set('fetch', self.service_provider.book_search(book_name_input_box.content))
            except ReachedToRequestLimitError:
                return self.get_request_limited_page()
                
            page.bag_set('table_page', 1)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        search_button.click_func = search
        
        def advance_search():
            return self.get_advance_book_page()
        advance_search_button.click_func = advance_search

        def next():
            PageHelper.table_next_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        next_button.click_func = next

        def prev():
            PageHelper.table_prev_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()   
        prev_button.click_func = prev

        def back():
            return self.get_homepage()  
        back_button.click_func = back

        search()
        return page
    
    #==================================== Advance Book Page =================================
    def get_advance_book_page(self) -> Page:
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()
        
        try:
            available_categories : List[CategoryViewModel] = self.service_provider.get_all_categories()
        except ReachedToRequestLimitError:
            return self.get_request_limited_page()
        
        page = self._create_page('جست و جوی پیشرفته کتب')
        page.bag_set('table_header', [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')])
        page.bag_set('table_page', 1)
        page.bag_set('category_names', [category.name for category in available_categories]) 
        page.bag_set('selected_categories', [])
        
        #=============================================================================
        #=========================== Elements Initializing ===========================       
        book_name = Text(
            content = 'نام کتاب',
            position = SizeAndPosition(left = 33, top = 2)
        )
        book_name_input_box = InputBox(
            display_text = 'نام کتاب را وارد کنید',
            position = SizeAndPosition(left = 43, top = 2)
        )
        author_name = Text(
            content = 'نام نویسنده',
            position = SizeAndPosition(left = 82, top = 2)
        )
        author_input_box = InputBox(
            display_text = 'نام نویسنده را وارد کنید',
            position = SizeAndPosition(left = 95, top = 2)
        )
        publisher_name = Text(
            content = 'نام ناشر',
            position = SizeAndPosition(left = 33, top = 3)
        )
        publisher_input_box = InputBox(
            display_text = 'نام ناشر را وارد کنید',
            position = SizeAndPosition(left = 43, top = 3)
        )
        category_name = Text(
            content = 'موضوع',
            position = SizeAndPosition(left = 82, top = 3)
        )
        category_input_box = InputBox(
            display_text = 'موضوع را وارد کنید',
            checker = lambda text : (text in page.bag_get('category_names')),
            position = SizeAndPosition(left = 89, top = 3),
        )
        add_category_button = Button(
            text = 'افزودن موضوع',
            position = SizeAndPosition(top = 4, left = 36)
        )
        remove_category_button = Button(
            text = 'حذف موضوع',
            position = SizeAndPosition(top = 4, left = 55)
        )
        clear_categories_button = Button(
            text = 'حذف تمامی موضوعات',
            position = SizeAndPosition(top = 4, left = 71)
        )
        display_categories_button = Button(
            text = 'مشاهده لیست موضوعات',
            position = SizeAndPosition(top = 4, left = 95)
        )
        s_c : List = page.bag_get('selected_categories')
        selected_categories = Text(
            content = ConsoleExtension.short_text(f'موضوعات انتخاب شده: {"تمامی موضوعات" if not s_c else ", ".join(s_c)}', 90),
            position = SizeAndPosition(top = 5, width = 150),
            halign = 'c'
        )
        search_button = Button(
            text = 'جست و جو',
            position = SizeAndPosition(top = 6, left = 58)
        )
        fast_search_button = Button(
            text = 'جست و جوی سریع',
            position = SizeAndPosition(top = 6, left = 75)
        ) 
        prev_button = Button(
            text = 'قبلی',
            position = SizeAndPosition(top = 30, left = 40)
        )
        next_button = Button(
            text = 'بعدی',
            position = SizeAndPosition(top = 30, left = 100)
        )
        cur_page = Text(
            content = f'صفحه {page.bag_get("table_page")}',
            position = SizeAndPosition(top = 30, left = 71)
        )
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 33, width = 150),
            halign = 'c'
        )              
        books_table = Table([[]], SizeAndPosition(top = 8))
        #=============================================================================
        #=========================== Adding Page Elements ============================
        page.elements += [
            book_name, book_name_input_box, author_name, author_input_box, publisher_name, clear_categories_button,
            publisher_input_box, category_name, category_input_box, add_category_button, selected_categories,
            remove_category_button, display_categories_button, search_button, fast_search_button, prev_button, next_button, cur_page, back_button, books_table
        ]
        page.update_focused()
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
        book_name_input_box.linked_elements['d'] = publisher_input_box
        book_name_input_box.linked_elements['r'] = author_input_box
        
        author_input_box.linked_elements['d'] = category_input_box
        author_input_box.linked_elements['l'] = book_name_input_box
        
        publisher_input_box.linked_elements['u'] = book_name_input_box
        publisher_input_box.linked_elements['d'] = add_category_button
        publisher_input_box.linked_elements['r'] = category_input_box
        
        category_input_box.linked_elements['u'] = author_input_box
        category_input_box.linked_elements['d'] = display_categories_button
        category_input_box.linked_elements['l'] = publisher_input_box
        
        add_category_button.linked_elements['u'] = publisher_input_box
        add_category_button.linked_elements['d'] = search_button
        add_category_button.linked_elements['r'] = remove_category_button
        
        remove_category_button.linked_elements['u'] = publisher_input_box
        remove_category_button.linked_elements['d'] = search_button 
        remove_category_button.linked_elements['l'] = add_category_button
        remove_category_button.linked_elements['r'] = clear_categories_button
        
        clear_categories_button.linked_elements['u'] = category_input_box
        clear_categories_button.linked_elements['d'] = fast_search_button
        clear_categories_button.linked_elements['l'] = remove_category_button
        clear_categories_button.linked_elements['r'] = display_categories_button
        
        display_categories_button.linked_elements['u'] = category_input_box
        display_categories_button.linked_elements['d'] = fast_search_button
        display_categories_button.linked_elements['l'] = clear_categories_button
        
        search_button.linked_elements['u'] = remove_category_button
        search_button.linked_elements['d'] = prev_button
        search_button.linked_elements['r'] = fast_search_button
        
        fast_search_button.linked_elements['u'] = clear_categories_button
        fast_search_button.linked_elements['d'] = next_button
        fast_search_button.linked_elements['l'] = search_button
        
        prev_button.linked_elements['u'] = search_button
        prev_button.linked_elements['d'] = back_button
        prev_button.linked_elements['r'] = next_button
        
        next_button.linked_elements['u'] = fast_search_button
        next_button.linked_elements['d'] = back_button
        next_button.linked_elements['l'] = prev_button
        
        back_button.linked_elements['u'] = prev_button
        back_button.linked_elements['l'] = prev_button
        back_button.linked_elements['r'] = next_button
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        def add_category():
            if not category_input_box.check():
                return
            
            s_c : List = page.bag_get('selected_categories')
            if category_input_box.content in s_c:
                return
            s_c.append(category_input_box.content)
            selected_categories.content = ConsoleExtension.short_text(f'موضوعات انتخاب شده: {"تمامی موضوعات" if not s_c else ", ".join(s_c)}', 90)
            page.bag_set('selected_categories', s_c)
            category_input_box.content = ''
        add_category_button.click_func = add_category

        def remove_category():
            if not category_input_box.check():
                return
            
            s_c : List = page.bag_get('selected_categories')
            if not category_input_box.content in s_c:
                return
            s_c.remove(category_input_box.content)
            selected_categories.content = ConsoleExtension.short_text(f'موضوعات انتخاب شده: {"تمامی موضوعات" if not s_c else ", ".join(s_c)}', 90)
            page.bag_set('selected_categories', s_c)
            category_input_box.content = ''
        remove_category_button.click_func = remove_category
        
        def clear_categories():
            if not page.bag_get('selected_categories'):
                return
            page.bag_set('selected_categories', [])
            selected_categories.content = ConsoleExtension.short_text(f'موضوعات انتخاب شده: {"تمامی موضوعات"}', 90) 
        clear_categories_button.click_func = clear_categories

        def refresh_books_table():
            start_row = (page.bag_get("table_page", 1) - 1) * 10
            end_row = (page.bag_get("table_page", 1) * 10)
            end_row = min(len(page.bag_get('fetch')), end_row)
        
            table_content : List[List[Element]] = [
                page.bag_get('table_header')
            ]
            for row in page.bag_get('fetch')[start_row:end_row]:
                table_row = [
                    Text(ConsoleExtension.short_text(row.title, 30),halign='c'),
                    Text(ConsoleExtension.short_text(row.publisher, 20),halign='c'),
                    Text(ConsoleExtension.short_text(row.author, 35),halign='c'),
                    Text(ConsoleExtension.short_text(row.category, 50),halign='c')
                ]
                table_content.append(table_row)
            
            ConsoleExtension.clear_area(books_table.position, page.position)
            
            books_table.update(table_content, start_row_id=start_row)
            books_table.position.left = (150 - books_table.position.width) // 2
        
            ConsoleExtension.clear_area(next_button.position, page.position)
            ConsoleExtension.clear_area(cur_page.position, page.position)
            ConsoleExtension.clear_area(prev_button.position, page.position)
            
            next_button.position.top = books_table.position.bottom
            cur_page.position.top = books_table.position.bottom
            prev_button.position.top = books_table.position.bottom


        def search():
            try:
                fetch : List[BookViewModel] = self.service_provider.book_advance_search(
                    title = book_name_input_box.content,
                    publisher = publisher_input_box.content,
                    author = author_input_box.content,
                    categories = page.bag_get('selected_categories')
                )
                page.bag_set('fetch', fetch)
            except ReachedToRequestLimitError:
                return self.get_request_limited_page()
                
            page.bag_set('table_page', 1)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        search_button.click_func = search
        
        def fast_search():
            return self.get_books_page()
        fast_search_button.click_func = fast_search
        
        def display_categories():
            category_names : List = page.bag_get('category_names')
            
            ConsoleExtension.clear_area(books_table.position, page.position)
            
            display_categories_content = "لیست موضوعات:\n\n"
            for i in range(len(category_names)):
                if (i+1) % 10 == 0:
                    display_categories_content += '\n'
                display_categories_content += f'{category_names[i]}، '
            display_categories_content += '\n\nبرای ادامه یک کلید را بفشارید.'
                    
            display_categories_text = Text(
                content = display_categories_content,
                position = SizeAndPosition(top = books_table.position.top, width = 150),
                halign = 'c'
            )
            display_categories_text.render(page.position.top, page.position.left)
            
            time.sleep(0.3)
            while True:
                event = keyboard.read_event(suppress=True)
                if event.event_type == keyboard.KEY_DOWN:
                    ConsoleExtension.clear_area(display_categories_text.position , page.position)
                    break
        display_categories_button.click_func = display_categories
        
        def next():
            PageHelper.table_next_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        next_button.click_func = next

        def prev():
            PageHelper.table_prev_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()   
        prev_button.click_func = prev

        def back():
            return self.get_homepage()  
        back_button.click_func = back

        search()
        return page

    #==================================== Publishers Page =================================
    def get_publishers_page(self):
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()
        
        page = self._create_page('صفحه ناشرین')
        page.bag_set('table_page', 1)
        page.bag_set('table_header', [
                Text('نام ناشر',halign='c'),
                Text('آدرس',halign='c'),
                Text('ایمیل',halign='c'),
                Text('شماره تماس',halign='c'),
                Text('کتاب ها',halign='c'),
                Text('جزئیات',halign='c')
            ]
        )
        #=============================================================================
        #=========================== Elements Initializing ===========================       
        publisher_name_input_box = InputBox(
            display_text = 'نام ناشر را وارد کنید',
            position = SizeAndPosition(left = 63, top = 3)
        )
        search_button = Button(
            text = 'جست و جو',
            position = SizeAndPosition(top = 5, left = 70)
        )  
        prev_button = Button(
            text = 'قبلی',
            position = SizeAndPosition(top = 31, left = 40)
        )
        next_button = Button(
            text = 'بعدی',
            position = SizeAndPosition(top = 31, left = 100)
        )
        cur_page = Text(
            content = f'صفحه {page.bag_get("table_page")}',
            position = SizeAndPosition(top = 31, left = 71)
        )
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 33, width = 150),
            halign = 'c'
        )
        publishers_table = Table([[]], SizeAndPosition(top = 7))
        #=============================================================================
        #=========================== Adding Page Elements ============================
        page.elements += [
            publisher_name_input_box, search_button, prev_button, next_button, cur_page, back_button, publishers_table
        ]
        page.update_focused()
        #=============================================================================
        #=========================== Link Elemnets Together ==========================             
        publisher_name_input_box.linked_elements['d'] = search_button

        search_button.linked_elements['u'] = publisher_name_input_box
        
        prev_button.linked_elements['r'] = next_button
        prev_button.linked_elements['d'] = back_button
        
        next_button.linked_elements['l'] = prev_button
        next_button.linked_elements['d'] = back_button
        
        back_button.linked_elements['u'] = next_button
        back_button.linked_elements['r'] = next_button
        back_button.linked_elements['l'] = prev_button
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        
        def refresh_books_table():
            start_row = (page.bag_get("table_page", 1) - 1) * 10
            end_row = (page.bag_get("table_page", 1) * 10)
            end_row = min(len(page.bag_get('fetch')), end_row)
        
            table_content : List[List[Element]] = [
                page.bag_get('table_header')
            ]
            for row in page.bag_get('fetch')[start_row:end_row]:
                table_row = [
                    Text(ConsoleExtension.short_text(row.name, 16), halign='c'),
                    Text(ConsoleExtension.short_text(row.address, 30), halign='c'),
                    Text(ConsoleExtension.short_text(row.contact_email, 25), halign='c'),
                    Text(ConsoleExtension.short_text(row.phone, 16), halign='c'),
                    Text(ConsoleExtension.short_text(row.books, 25), halign='c'),
                    Button('مشاهده جزئیات', halign='c', click_func = lambda r=row: self.get_publisher_detail_page(r))
                ]
                table_content.append(table_row) 
            
            ConsoleExtension.clear_area(publishers_table.position, page.position)
            
            publishers_table.update(table_content, start_row_id=start_row)
            publishers_table.position.left = (150 - publishers_table.position.width) // 2
        
            ConsoleExtension.clear_area(next_button.position, page.position)
            ConsoleExtension.clear_area(cur_page.position, page.position)
            ConsoleExtension.clear_area(prev_button.position, page.position)
            
            next_button.position.top = publishers_table.position.bottom + 1
            cur_page.position.top = publishers_table.position.bottom + 1
            prev_button.position.top = publishers_table.position.bottom + 1

            if len(table_content) <= 1:
                return

            for i in range(1, len(table_content)):
                if i == 1:
                    table_content[i][5].linked_elements['u'] = search_button
                    search_button.linked_elements['d'] = table_content[i][5]
                else:
                    table_content[i][5].linked_elements['u'] = table_content[i - 1][5]
                if i == len(table_content) - 1:
                    table_content[i][5].linked_elements['d'] = next_button
                    prev_button.linked_elements['u'] = table_content[i][5]
                    next_button.linked_elements['u'] = table_content[i][5]
                else:
                    table_content[i][5].linked_elements['d'] = table_content[i + 1][5]

        def search():
            try:
                fetch : List[PublisherViewModel] = self.service_provider.publisher_search(publisher_name_input_box.content)
                page.bag_set('fetch', fetch)
            except ReachedToRequestLimitError:
                return self.get_request_limited_page()
                
            page.bag_set('table_page', 1)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        search_button.click_func = search
        
        def next():
            PageHelper.table_next_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        next_button.click_func = next

        def prev():
            PageHelper.table_prev_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()   
        prev_button.click_func = prev

        def back():
            return self.get_homepage()  
        back_button.click_func = back

        search()
        return page
    
    #==================================== Publisher Detail Page =================================
    def get_publisher_detail_page(self, publisher : PublisherViewModel):
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()

        page = self._create_page(publisher.name)
        page.bag_set('table_page', 1)
        page.bag_set('table_header', [Text('عنوان',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')])
                
        #=============================================================================
        #=========================== Elements Initializing ===========================       
        publisher_info = Text(
            content = f'آدرس : {ConsoleExtension.short_text(publisher.address,60)}\n'
            f'ایمیل : {ConsoleExtension.short_text(publisher.contact_email,60)}\n'
            f'شماره تماس : {ConsoleExtension.short_text(publisher.phone,60)}\n'
            f'کتاب ها : {ConsoleExtension.short_text(publisher.books, 60)}\n',
            position = SizeAndPosition(top = 2, left = 44, width = 61),
            halign = 'c'
        ) 
        prev_button = Button(
            text = 'قبلی',
            position = SizeAndPosition(top = 31, left = 40)
        )
        next_button = Button(
            text = 'بعدی',
            position = SizeAndPosition(top = 31, left = 100)
        )
        cur_page = Text(
            content = f'صفحه {page.bag_get("table_page")}',
            position = SizeAndPosition(top = 31, left = 71)
        )
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 33, width = 150),
            halign = 'c'
        )
        books_table = Table([[]], SizeAndPosition(top = 8))            
        #=============================================================================
        #=========================== Adding Page Elements ============================
        page.elements += [
            publisher_info, prev_button, next_button, cur_page, back_button, books_table
        ]
        page.update_focused()
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
        prev_button.linked_elements['r'] = next_button
        prev_button.linked_elements['d'] = back_button
        
        next_button.linked_elements['l'] = prev_button
        next_button.linked_elements['d'] = back_button
        
        back_button.linked_elements['u'] = next_button
        back_button.linked_elements['r'] = next_button
        back_button.linked_elements['l'] = prev_button
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        def refresh_books_table():
            start_row = (page.bag_get("table_page", 1) - 1) * 10
            end_row = (page.bag_get("table_page", 1) * 10)
            end_row = min(len(page.bag_get('fetch')), end_row)

            table_content : List[List[Element]] = [
                page.bag_get('table_header')
            ]
            for row in page.bag_get('fetch')[start_row:end_row]:
                table_row = [
                    Text(ConsoleExtension.short_text(row.title, 30),halign='c'),
                    Text(ConsoleExtension.short_text(row.author, 35),halign='c'),
                    Text(ConsoleExtension.short_text(row.category, 50),halign='c')
                ]
                table_content.append(table_row)
            
            ConsoleExtension.clear_area(books_table.position, page.position)
            
            books_table.update(table_content, start_row_id=start_row)
            books_table.position.left = (150 - books_table.position.width) // 2
        
            ConsoleExtension.clear_area(next_button.position, page.position)
            ConsoleExtension.clear_area(cur_page.position, page.position)
            ConsoleExtension.clear_area(prev_button.position, page.position)
            
            next_button.position.top = books_table.position.bottom
            cur_page.position.top = books_table.position.bottom
            prev_button.position.top = books_table.position.bottom
        
        def search():
            try:
                fetch : List[BookViewModel] = self.service_provider.book_advance_search(publisher = publisher.name)
                page.bag_set('fetch', fetch)
            except ReachedToRequestLimitError:
                return self.get_request_limited_page()
                
            page.bag_set('table_page', 1)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()

        def next():
            PageHelper.table_next_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        next_button.click_func = next

        def prev():
            PageHelper.table_prev_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()   
        prev_button.click_func = prev

        def back():
            return self.get_publishers_page()  
        back_button.click_func = back

        search()
        return page


    #==================================== Authors Page =================================
    def get_authors_page(self):
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()
        
        page = self._create_page('صفحه مولفین')
        page.bag_set('table_page', 1)
        page.bag_set('table_header', [
                Text('نام نویسنده',halign='c'),
                Text('کتاب ها',halign='c'),
                Text('زندگی نامه',halign='c'),
                Text('جزئیات',halign='c')
            ]
        )
        #=============================================================================
        #=========================== Elements Initializing ===========================       
        author_name_input_box = InputBox(
            display_text = 'نام نویسنده را وارد کنید',
            position = SizeAndPosition(left = 63, top = 3)
        )
        search_button = Button(
            text = 'جست و جو',
            position = SizeAndPosition(top = 5, left = 70)
        )  
        prev_button = Button(
            text = 'قبلی',
            position = SizeAndPosition(top = 31, left = 40)
        )
        next_button = Button(
            text = 'بعدی',
            position = SizeAndPosition(top = 31, left = 100)
        )
        cur_page = Text(
            content = f'صفحه {page.bag_get("table_page")}',
            position = SizeAndPosition(top = 31, left = 71)
        )
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 33, width = 150),
            halign = 'c'
        )
        authors_table = Table([[]], SizeAndPosition(top = 7))
        #=============================================================================
        #=========================== Adding Page Elements ============================
        page.elements += [
            author_name_input_box, search_button, prev_button, next_button, cur_page, back_button, authors_table
        ]
        page.update_focused()
        #=============================================================================
        #=========================== Link Elemnets Together ==========================             
        author_name_input_box.linked_elements['d'] = search_button

        search_button.linked_elements['u'] = author_name_input_box
        
        prev_button.linked_elements['r'] = next_button
        prev_button.linked_elements['d'] = back_button
        
        next_button.linked_elements['l'] = prev_button
        next_button.linked_elements['d'] = back_button
        
        back_button.linked_elements['u'] = next_button
        back_button.linked_elements['r'] = next_button
        back_button.linked_elements['l'] = prev_button
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        
        def refresh_books_table():
            start_row = (page.bag_get("table_page", 1) - 1) * 10
            end_row = (page.bag_get("table_page", 1) * 10)
            end_row = min(len(page.bag_get('fetch')), end_row)
        
            table_content : List[List[Element]] = [
                page.bag_get('table_header')
            ]
            for row in page.bag_get('fetch')[start_row:end_row]:
                table_row = [
                    Text(ConsoleExtension.short_text(row.name, 20), halign='c'),
                    Text(ConsoleExtension.short_text(row.books, 35), halign='c'),
                    Text(ConsoleExtension.short_text(row.biography, 60), halign='c'),
                    Button('مشاهده جزئیات', halign='c', click_func = lambda r=row: self.get_author_detail_page(r))
                ]
                table_content.append(table_row) 
            
            ConsoleExtension.clear_area(authors_table.position, page.position)
            
            authors_table.update(table_content, start_row_id=start_row)
            authors_table.position.left = (150 - authors_table.position.width) // 2
        
            ConsoleExtension.clear_area(next_button.position, page.position)
            ConsoleExtension.clear_area(cur_page.position, page.position)
            ConsoleExtension.clear_area(prev_button.position, page.position)
            
            next_button.position.top = authors_table.position.bottom + 1
            cur_page.position.top = authors_table.position.bottom + 1
            prev_button.position.top = authors_table.position.bottom + 1

            if len(table_content) <= 1:
                return

            for i in range(1, len(table_content)):
                if i == 1:
                    table_content[i][3].linked_elements['u'] = search_button
                    search_button.linked_elements['d'] = table_content[i][3]
                else:
                    table_content[i][3].linked_elements['u'] = table_content[i - 1][3]
                if i == len(table_content) - 1:
                    table_content[i][3].linked_elements['d'] = next_button
                    prev_button.linked_elements['u'] = table_content[i][3]
                    next_button.linked_elements['u'] = table_content[i][3]
                else:
                    table_content[i][3].linked_elements['d'] = table_content[i + 1][3]

        def search():
            try:
                fetch : List[AuthorViewModel] = self.service_provider.author_search(author_name_input_box.content)
                page.bag_set('fetch', fetch)
            except ReachedToRequestLimitError:
                return self.get_request_limited_page()
                
            page.bag_set('table_page', 1)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        search_button.click_func = search
        
        def next():
            PageHelper.table_next_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        next_button.click_func = next

        def prev():
            PageHelper.table_prev_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()   
        prev_button.click_func = prev

        def back():
            return self.get_homepage()  
        back_button.click_func = back

        search()
        return page


    #==================================== Author Detail Page =================================
    def get_author_detail_page(self, author : AuthorViewModel):
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()

        page = self._create_page(author.name)
        page.bag_set('table_page', 1)
        page.bag_set('table_header', [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('دسته بندی ها',halign='c')])
                
        #=============================================================================
        #=========================== Elements Initializing ===========================       
        author_info = Text(
            content = f'زندگی نامه : {ConsoleExtension.wrap_text(author.biography, 5, 60)}\n'
            f'کتاب ها : {ConsoleExtension.short_text(author.books,60)}',
            position = SizeAndPosition(top = 2, left = 44, width = 61),
            halign = 'c'
        ) 
        prev_button = Button(
            text = 'قبلی',
            position = SizeAndPosition(top = 31, left = 40)
        )
        next_button = Button(
            text = 'بعدی',
            position = SizeAndPosition(top = 31, left = 100)
        )
        cur_page = Text(
            content = f'صفحه {page.bag_get("table_page")}',
            position = SizeAndPosition(top = 31, left = 71)
        )
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 33, width = 150),
            halign = 'c'
        )
        books_table = Table([[]], SizeAndPosition(top = 8))            
        #=============================================================================
        #=========================== Adding Page Elements ============================
        page.elements += [
            author_info, prev_button, next_button, cur_page, back_button, books_table
        ]
        page.update_focused()
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
        prev_button.linked_elements['r'] = next_button
        prev_button.linked_elements['d'] = back_button
        
        next_button.linked_elements['l'] = prev_button
        next_button.linked_elements['d'] = back_button
        
        back_button.linked_elements['u'] = next_button
        back_button.linked_elements['r'] = next_button
        back_button.linked_elements['l'] = prev_button
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        def refresh_books_table():
            start_row = (page.bag_get("table_page", 1) - 1) * 10
            end_row = (page.bag_get("table_page", 1) * 10)
            end_row = min(len(page.bag_get('fetch')), end_row)

            table_content : List[List[Element]] = [
                page.bag_get('table_header')
            ]
            for row in page.bag_get('fetch')[start_row:end_row]:
                table_row = [
                    Text(ConsoleExtension.short_text(row.title, 30),halign='c'),
                    Text(ConsoleExtension.short_text(row.publisher, 35),halign='c'),
                    Text(ConsoleExtension.short_text(row.category, 50),halign='c')
                ]
                table_content.append(table_row)
            
            ConsoleExtension.clear_area(books_table.position, page.position)
            
            books_table.update(table_content, start_row_id=start_row)
            books_table.position.left = (150 - books_table.position.width) // 2
        
            ConsoleExtension.clear_area(next_button.position, page.position)
            ConsoleExtension.clear_area(cur_page.position, page.position)
            ConsoleExtension.clear_area(prev_button.position, page.position)
            
            next_button.position.top = books_table.position.bottom
            cur_page.position.top = books_table.position.bottom
            prev_button.position.top = books_table.position.bottom
        
        def search():
            try:
                fetch : List[BookViewModel] = self.service_provider.book_advance_search(author= author.name)
                page.bag_set('fetch', fetch)
            except ReachedToRequestLimitError:
                return self.get_request_limited_page()
                
            page.bag_set('table_page', 1)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()

        def next():
            PageHelper.table_next_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        next_button.click_func = next

        def prev():
            PageHelper.table_prev_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()   
        prev_button.click_func = prev

        def back():
            return self.get_authors_page()  
        back_button.click_func = back

        search()
        return page


    #==================================== Categories Page =================================
    def get_categories_page(self) -> Page:
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()
        
        try:
            available_categories : List[CategoryViewModel] = self.service_provider.get_all_categories()
        except ReachedToRequestLimitError:
            return self.get_request_limited_page()
        
        page = self._create_page('دسته بندی ها')
        page.bag_set('table_header', [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')])
        page.bag_set('table_page', 1)
        page.bag_set('category_names', [category.name for category in available_categories]) 
        page.bag_set('selected_category', '')
        page.bag_set('categories_table_start_index', 0)
        
        #=============================================================================
        #=========================== Elements Initializing ===========================       
        categories_table = Table([[]], SizeAndPosition(top = 3))

        prev_button = Button(
            text = 'قبلی',
            position = SizeAndPosition(top = 30, left = 40)
        )
        next_button = Button(
            text = 'بعدی',
            position = SizeAndPosition(top = 30, left = 100)
        )
        cur_page = Text(
            content = f'صفحه {page.bag_get("table_page")}',
            position = SizeAndPosition(top = 30, left = 71)
        )
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 33, width = 150),
            halign = 'c'
        )              
        books_table = Table([[]], SizeAndPosition(top = 8))
        #=============================================================================
        #=========================== Adding Page Elements ============================
        page.elements += [
            categories_table, prev_button, next_button, cur_page, back_button, books_table
        ]
        page.update_focused()
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
        prev_button.linked_elements['d'] = back_button
        prev_button.linked_elements['r'] = next_button
        
        next_button.linked_elements['d'] = back_button
        next_button.linked_elements['l'] = prev_button
        
        back_button.linked_elements['u'] = prev_button
        back_button.linked_elements['l'] = prev_button
        back_button.linked_elements['r'] = next_button
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        def refresh_category_table():
            start_index = page.bag_get("categories_table_start_index", 0)
            end_index = min(len(page.bag_get('category_names')), start_index + 5)

            table_row: List[Element] = [
                    Button(text = 'تمامی دسته بندی ها', halign = 'c', click_func = lambda : select_category('')),
                    Button(text = 'قبل', halign = 'c', click_func = category_prev),
            ]
            for category in page.bag_get('category_names')[start_index:end_index]:
                table_row.append(Button(text = ConsoleExtension.short_text(category, 14), halign='c', click_func = lambda c=category: select_category(c)))
            table_row.append(Button(text = 'بعد', halign = 'c', click_func = category_next))

            for i in range(len(table_row)):
                table_row[i].linked_elements['d'] = prev_button
                if i != 0:
                    table_row[i].linked_elements['l'] = table_row[i - 1]
                if i != len(table_row) - 1:
                    table_row[i].linked_elements['r'] = table_row[i + 1]
            prev_button.linked_elements['u'] = table_row[0]
            next_button.linked_elements['u'] = table_row[-1]

            ConsoleExtension.clear_area(categories_table.position, page.position)

            categories_table.update([table_row], show_row_id=False)
            categories_table.position.left = (150 - categories_table.position.width) // 2
            page.update_focused()


        def select_category(category: str):
            page.bag_set('selected_category', category)
            search()

        def category_prev():
            start_index = page.bag_get("categories_table_start_index", 0)
            if start_index > 0:
                page.bag_set("categories_table_start_index", start_index - 1)
                refresh_category_table()
                page.update_focused(categories_table.data[0][1])


        def category_next():
            start_index = page.bag_get("categories_table_start_index", 0)
            if len(page.bag_get('category_names')) > start_index + 5:
                page.bag_set("categories_table_start_index", start_index + 1)
                refresh_category_table()
                page.update_focused(categories_table.data[0][-1])


        def refresh_books_table():
            start_row = (page.bag_get("table_page", 1) - 1) * 10
            end_row = (page.bag_get("table_page", 1) * 10)
            end_row = min(len(page.bag_get('fetch')), end_row)
        
            table_content : List[List[Element]] = [
                page.bag_get('table_header')
            ]
            for row in page.bag_get('fetch')[start_row:end_row]:
                table_row = [
                    Text(ConsoleExtension.short_text(row.title, 30),halign='c'),
                    Text(ConsoleExtension.short_text(row.publisher, 20),halign='c'),
                    Text(ConsoleExtension.short_text(row.author, 35),halign='c'),
                    Text(ConsoleExtension.short_text(row.category, 50),halign='c')
                ]
                table_content.append(table_row)
            
            ConsoleExtension.clear_area(books_table.position, page.position)
            
            books_table.update(table_content, start_row_id=start_row)
            books_table.position.left = (150 - books_table.position.width) // 2
        
            ConsoleExtension.clear_area(next_button.position, page.position)
            ConsoleExtension.clear_area(cur_page.position, page.position)
            ConsoleExtension.clear_area(prev_button.position, page.position)
            
            next_button.position.top = books_table.position.bottom
            cur_page.position.top = books_table.position.bottom
            prev_button.position.top = books_table.position.bottom

        def search():
            try:
                categories = [page.bag_get('selected_category')] if page.bag_get('selected_category') else None
                fetch : List[BookViewModel] = self.service_provider.book_advance_search(
                    categories = categories
                )
                page.bag_set('fetch', fetch)
            except ReachedToRequestLimitError:
                return self.get_request_limited_page()
                
            page.bag_set('table_page', 1)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        
        def next():
            PageHelper.table_next_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()
        next_button.click_func = next

        def prev():
            PageHelper.table_prev_func(page, 'fetch', 'table_page', 10)
            cur_page.content = f'صفحه {page.bag_get("table_page", 1)}'
            refresh_books_table()   
        prev_button.click_func = prev

        def back():
            return self.get_homepage()  
        back_button.click_func = back

        refresh_category_table()
        search()
        return page


    #==================================== About Us Page =================================
    def get_about_us(self) -> Page:
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()

        page = self._create_page('درباره ما')
        
        #=============================================================================
        #=========================== Elements Initializing ===========================
        
        signup_button = Button(
            text = f'ثبت نام',
            position = SizeAndPosition(left = 124, top = 0, width = 8),
            halign = 'c'
        )
        login_button = Button(
            text = f'ورود',
            position = SizeAndPosition(left = 139, top = 0, width = 5),
            halign = 'c'
        )
        about_us = Text(
            content = ConsoleExtension.wrap_text(self.service_provider.about_us(), 20, 110),
            position = SizeAndPosition(width = 150, height = 20,top = 5),
            halign = 'c',
            valign = 'm'
        )
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 30, width = 150),
            halign = 'c'
        )     
       
        #=============================================================================
        #=========================== Page Initializing ===============================
        page.elements += [
                about_us, login_button, signup_button, back_button
        ]
        page.update_focused()
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
        page.auto_link_focusables_angle_base(0.27)  
        #=============================================================================
        #=========================== Click Functions Initializing ====================
                    
        def signup():
            return self.get_signup_page()
        signup_button.click_func = signup
        
        def login():
            return self.get_login_page()
        login_button.click_func = login
        
        def back():
            return self.get_homepage()  
        back_button.click_func = back
        
            
        return page