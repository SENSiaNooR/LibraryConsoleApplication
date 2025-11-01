import time
from typing import List

import keyboard
from Core.Validations import Validations
from Exceptions.Exceptions import ReachedToRequestLimitError
from Models.Models import BookViewModel, CategoryViewModel, MemberModel, PlainUserModel, PublisherViewModel
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
    
    def __init__(self, token):
        self.service_provider = GuestServices(token)
        self.token = token

    def _create_page(self, title: str, elements: list[Element]) -> Page:
        guest_model = self.service_provider.get_guest_model()
        
        page = Page(elements, SizeAndPosition(30,1,36,150), auto_resize=False)
        base_elements = [
            Text(title, SizeAndPosition(65, 0, 1, 20), halign='c'),
            Text(
                content = f'id = {guest_model.id}\nدرخواست ها : {guest_model.request_count}\nکاربر : مهمان',
                position = SizeAndPosition(1,0)    
            ),
            Text(
                content = ' با استفاده از کلید های ← → ↓ ↑ بین گزینه ها جابجا شوید و با کلید Enter گزینه مورد نظر را انتخاب کنید.',
                position = SizeAndPosition(top = 35, width = 150),
                halign = 'r'
            )
        ]
        page.elements = base_elements + page.elements
        page.border = True
        return page

    #==================================== Home Page =================================
    def get_homepage(self) -> Page:
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()

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
        #=========================== Link Elemnets Together ==========================
        
        signup_button.linked_elements['r'] = login_button
        signup_button.linked_elements['l'] = books_button
        signup_button.linked_elements['d'] = books_button
        
        login_button.linked_elements['l'] = signup_button
        login_button.linked_elements['d'] = books_button
        
        books_button.linked_elements['u'] = signup_button
        books_button.linked_elements['r'] = signup_button
        books_button.linked_elements['d'] = publishers_button

        publishers_button.linked_elements['u'] = books_button
        publishers_button.linked_elements['r'] = signup_button
        publishers_button.linked_elements['d'] = authors_button
        
        authors_button.linked_elements['u'] = publishers_button
        authors_button.linked_elements['r'] = signup_button
        authors_button.linked_elements['d'] = categories_button

        categories_button.linked_elements['u'] = authors_button
        categories_button.linked_elements['r'] = signup_button
        categories_button.linked_elements['d'] = about_us_button
        
        about_us_button.linked_elements['u'] = categories_button
        about_us_button.linked_elements['r'] = signup_button
        about_us_button.linked_elements['d'] = exit_button
        
        exit_button.linked_elements['u'] = about_us_button
        exit_button.linked_elements['r'] = signup_button
       

        #=============================================================================
        #=========================== Page Initializing ===============================
        elements = [
                books_button, exit_button, about_us_button, categories_button, authors_button,
                publishers_button, login_button, signup_button
        ]
        page = self._create_page('صفحه اصلی', elements)
        
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
            
        return page
       

    #==================================== Request Limited Page =================================
    def get_request_limited_page(self) -> Page:
                
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
        #=========================== Link Elemnets Together ==========================
        
        signup_button.linked_elements['r'] = login_button
        signup_button.linked_elements['l'] = exit_button
        signup_button.linked_elements['d'] = exit_button
        
        login_button.linked_elements['l'] = signup_button
        login_button.linked_elements['d'] = exit_button
        
        exit_button.linked_elements['u'] = signup_button
        exit_button.linked_elements['r'] = signup_button      

        #=============================================================================
        #=========================== Page Initializing ===============================
        elements = [
                exit_button, login_button, signup_button, tip
        ]
        page = self._create_page('متاسفیم!', elements)
        
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
        #=========================== Link Elemnets Together ==========================
        
        name_input_box.linked_elements['d'] = email_input_box
        name_input_box.linked_elements['r'] = username_input_box
        
        username_input_box.linked_elements['l'] = name_input_box
        username_input_box.linked_elements['d'] = repeat_password_input_box
        
        email_input_box.linked_elements['u'] = name_input_box
        email_input_box.linked_elements['d'] = password_input_box
        email_input_box.linked_elements['r'] = username_input_box
        
        password_input_box.linked_elements['u'] = email_input_box
        password_input_box.linked_elements['r'] = repeat_password_input_box
        password_input_box.linked_elements['d'] = signup_button
        
        repeat_password_input_box.linked_elements['l'] = password_input_box
        repeat_password_input_box.linked_elements['u'] = username_input_box
        repeat_password_input_box.linked_elements['d'] = signup_button
        
        signup_button.linked_elements['u'] = password_input_box
        signup_button.linked_elements['d'] = login_button
        
        login_button.linked_elements['u'] = signup_button
        login_button.linked_elements['d'] = back_button
        
        back_button.linked_elements['u'] = login_button


        #=============================================================================
        #=========================== Page Initializing ===============================
        elements = [
            name, email, username, password, repeat_password,
            name_input_box, email_input_box, username_input_box, password_input_box, repeat_password_input_box,
            signup_button, login_button, back_button, helper, error_text
        ]
        page = self._create_page('صفحه ثبت نام', elements)
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
        #=========================== Link Elemnets Together ==========================
                
        username_input_box.linked_elements['d'] = password_input_box
        
        password_input_box.linked_elements['u'] = username_input_box
        password_input_box.linked_elements['d'] = login_button
                
        login_button.linked_elements['u'] = password_input_box
        login_button.linked_elements['d'] = signup_button
        
        signup_button.linked_elements['u'] = login_button
        signup_button.linked_elements['d'] = back_button
        
        back_button.linked_elements['u'] = signup_button


        #=============================================================================
        #=========================== Page Initializing ===============================
        elements = [
            username, password, username_input_box, password_input_box,
            signup_button, login_button, back_button, error_text
        ]
        page = self._create_page('صفحه ورود', elements)
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
        
        prev_button = Button(
            text = 'قبلی',
            position = SizeAndPosition(top = 31, left = 40)
        )
        
        next_button = Button(
            text = 'بعدی',
            position = SizeAndPosition(top = 31, left = 100)
        )
        
        cur_page_number = 1

        cur_page = Text(
            content = f'صفحه {cur_page_number}',
            position = SizeAndPosition(top = 31, left = 71)
        )
        
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 33, width = 150),
            halign = 'c'
        )
        
        fetch : List[BookViewModel] = self.service_provider.book_search()
        start_row = (cur_page_number - 1) * 10
        end_row = (cur_page_number * 10)
        end_row = min(len(fetch), end_row)
        
        table_content : List[List[Element]] = [
            [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')]
        ]
        for row in fetch[start_row:end_row]:
            table_row = [
                Text(ConsoleExtension.short_text(row.title, 30),halign='c'),
                Text(ConsoleExtension.short_text(row.publisher, 20),halign='c'),
                Text(ConsoleExtension.short_text(row.author, 35),halign='c'),
                Text(ConsoleExtension.short_text(row.category, 50),halign='c')
            ]
            table_content.append(table_row)
                
        books_table = Table(table_content, SizeAndPosition(top = 7), start_row_id = start_row)
        books_table.position.left = (150 - books_table.position.width) // 2
        
        next_button.position.top = books_table.position.bottom + 1
        cur_page.position.top = books_table.position.bottom + 1
        prev_button.position.top = books_table.position.bottom + 1
            
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
                
        book_name_input_box.linked_elements['d'] = search_button
        
        search_button.linked_elements['u'] = book_name_input_box
        search_button.linked_elements['r'] = advance_search_button
        search_button.linked_elements['d'] = prev_button
        
        advance_search_button.linked_elements['u'] = book_name_input_box
        advance_search_button.linked_elements['l'] = search_button
        advance_search_button.linked_elements['d'] = next_button
        
        prev_button.linked_elements['u'] = search_button
        prev_button.linked_elements['r'] = next_button
        prev_button.linked_elements['d'] = back_button
        
        next_button.linked_elements['u'] = advance_search_button
        next_button.linked_elements['l'] = prev_button
        next_button.linked_elements['d'] = back_button
        
        back_button.linked_elements['u'] = next_button
        back_button.linked_elements['r'] = next_button
        back_button.linked_elements['l'] = prev_button

        #=============================================================================
        #=========================== Page Initializing ===============================
        elements = [
            book_name_input_box, search_button, advance_search_button, prev_button, next_button, cur_page, back_button, books_table
        ]
        page = self._create_page('صفحه کتب', elements)
        page.cur_page_number = cur_page_number
        page.fetch = fetch
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        
        def search():
            try:
                page.fetch : List[BookViewModel] = self.service_provider.book_search(book_name_input_box.content)
            except ReachedToRequestLimitError:
                return self.get_request_limited_page()
                
            page.cur_page_number = 1
            cur_page.content = f'صفحه {page.cur_page_number}'
        
            start_row = (page.cur_page_number - 1) * 10
            end_row = (page.cur_page_number * 10)
            end_row = min(len(page.fetch), end_row)
        
            table_content : List[List[Element]] = [
                [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')]
            ]
            for row in page.fetch[start_row:end_row]:
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
            
        search_button.click_func = search
        
        def advance_search():
            return self.get_advance_book_page()
        advance_search_button.click_func = advance_search

        def next():
            page.cur_page_number += 1
            cur_page.content = f'صفحه {page.cur_page_number}'
            
            start_row = (page.cur_page_number - 1) * 10
            if start_row >= len(page.fetch):
                page.cur_page_number -= 1
                cur_page.content = f'صفحه {page.cur_page_number}'
                return
            
            end_row = (page.cur_page_number * 10)
            end_row = min(len(page.fetch), end_row)
        
            table_content : List[List[Element]] = [
                [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')]
            ]
            for row in page.fetch[start_row:end_row]:
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

        next_button.click_func = next


        def prev():
            if page.cur_page_number <= 1:
                return
            page.cur_page_number -= 1
            cur_page.content = f'صفحه {page.cur_page_number}'
            
            start_row = (page.cur_page_number - 1) * 10            
            end_row = (page.cur_page_number * 10)
            end_row = min(len(page.fetch), end_row)
        
            table_content : List[List[Element]] = [
                [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')]
            ]
            for row in page.fetch[start_row:end_row]:
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
            
        prev_button.click_func = prev


        def back():
            return self.get_homepage()  
        back_button.click_func = back

        return page
    
    #==================================== Advance Book Page =================================
    def get_advance_book_page(self) -> Page:
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()
        
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
        try:
            available_categories : List[CategoryViewModel] = self.service_provider.get_all_categories()
        except ReachedToRequestLimitError:
            return self.get_request_limited_page()
        
        available_categories = [category.name for category in available_categories]
        
        category_input_box = InputBox(
            display_text = 'موضوع را وارد کنید',
            checker = lambda text : (text in available_categories),
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
        
        categories = []
        selected_categories = Text(
            content = ConsoleExtension.short_text(f'موضوعات انتخاب شده: {"تمامی موضوعات" if not categories else ", ".join(categories)}', 90),
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
        
        cur_page_number = 1

        cur_page = Text(
            content = f'صفحه {cur_page_number}',
            position = SizeAndPosition(top = 30, left = 71)
        )
        
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 33, width = 150),
            halign = 'c'
        )
        
        try:
            fetch : List[BookViewModel] = self.service_provider.book_advance_search()
        except ReachedToRequestLimitError:
            return self.get_request_limited_page()
        
        start_row = (cur_page_number - 1) * 10
        end_row = (cur_page_number * 10)
        end_row = min(len(fetch), end_row)
        
        table_content : List[List[Element]] = [
            [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')]
        ]
        for row in fetch[start_row:end_row]:
            table_row = [
                Text(ConsoleExtension.short_text(row.title, 30),halign='c'),
                Text(ConsoleExtension.short_text(row.publisher, 20),halign='c'),
                Text(ConsoleExtension.short_text(row.author, 35),halign='c'),
                Text(ConsoleExtension.short_text(row.category, 50),halign='c')
            ]
            table_content.append(table_row)
                
        books_table = Table(table_content, SizeAndPosition(top = 8), start_row_id = start_row)
        books_table.position.left = (150 - books_table.position.width) // 2
        
        next_button.position.top = books_table.position.bottom
        cur_page.position.top = books_table.position.bottom
        prev_button.position.top = books_table.position.bottom
            
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
        #=========================== Page Initializing ===============================
        elements = [
            book_name, book_name_input_box, author_name, author_input_box, publisher_name, clear_categories_button,
            publisher_input_box, category_name, category_input_box, add_category_button, selected_categories,
            remove_category_button, display_categories_button, search_button, fast_search_button, prev_button, next_button, cur_page, back_button, books_table
        ]
        page = self._create_page('صفحه کتب', elements)
        page.cur_page_number = cur_page_number
        page.fetch = fetch
        page.categories = categories
        
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        
        def add_category():
            if not category_input_box.check():
                return
            
            if category_input_box.content in page.categories:
                return

            page.categories.append(category_input_box.content)
            selected_categories.content = ConsoleExtension.short_text(f'موضوعات انتخاب شده: {"تمامی موضوعات" if not page.categories else ", ".join(page.categories)}', 90)
            category_input_box.content = ''
        
        add_category_button.click_func = add_category

        def remove_category():
            if not category_input_box.check():
                return
            
            if not category_input_box.content in page.categories:
                return

            page.categories.remove(category_input_box.content)
            selected_categories.content = ConsoleExtension.short_text(f'موضوعات انتخاب شده: {"تمامی موضوعات" if not page.categories else ", ".join(page.categories)}', 90)
            category_input_box.content = ''
        
        remove_category_button.click_func = remove_category
        
        def clear_categories():
            if not page.categories:
                return
            page.categories.clear()
            selected_categories.content = ConsoleExtension.short_text(f'موضوعات انتخاب شده: {"تمامی موضوعات" if not page.categories else ", ".join(page.categories)}', 90)
         
        clear_categories_button.click_func = clear_categories

        def search():
            try:
                page.fetch : List[BookViewModel] = self.service_provider.book_advance_search(
                    title = book_name_input_box.content,
                    publisher = publisher_input_box.content,
                    author = author_input_box.content,
                    categories = page.categories
                )
            except ReachedToRequestLimitError:
                return self.get_request_limited_page()
                
            page.cur_page_number = 1
            cur_page.content = f'صفحه {page.cur_page_number}'
        
            start_row = (page.cur_page_number - 1) * 10
            end_row = (page.cur_page_number * 10)
            end_row = min(len(page.fetch), end_row)
        
            table_content : List[List[Element]] = [
                [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')]
            ]
            for row in page.fetch[start_row:end_row]:
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
            
        search_button.click_func = search
        
        def fast_search():
            return self.get_books_page()
        
        fast_search_button.click_func = fast_search
        
        def display_categories():
            ConsoleExtension.clear_area(books_table.position, page.position)
            
            display_categories_content = "لیست موضوعات:\n\n"
            for i in range(len(available_categories)):
                if (i+1) % 10 == 0:
                    display_categories_content += '\n'
                display_categories_content += f'{available_categories[i]}، '
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
            page.cur_page_number += 1
            cur_page.content = f'صفحه {page.cur_page_number}'
            
            start_row = (page.cur_page_number - 1) * 10
            if start_row >= len(page.fetch):
                page.cur_page_number -= 1
                cur_page.content = f'صفحه {page.cur_page_number}'
                return
            
            end_row = (page.cur_page_number * 10)
            end_row = min(len(page.fetch), end_row)
        
            table_content : List[List[Element]] = [
                [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')]
            ]
            for row in page.fetch[start_row:end_row]:
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

        next_button.click_func = next


        def prev():
            if page.cur_page_number <= 1:
                return
            page.cur_page_number -= 1
            cur_page.content = f'صفحه {page.cur_page_number}'
            
            start_row = (page.cur_page_number - 1) * 10            
            end_row = (page.cur_page_number * 10)
            end_row = min(len(page.fetch), end_row)
        
            table_content : List[List[Element]] = [
                [Text('عنوان',halign='c'), Text('ناشر',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')]
            ]
            for row in page.fetch[start_row:end_row]:
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
            
        prev_button.click_func = prev


        def back():
            return self.get_homepage()  
        back_button.click_func = back

        return page
    

    #==================================== Publishers Page =================================
    def get_publishers_page(self):
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()
        
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
        
        cur_page_number = 1

        cur_page = Text(
            content = f'صفحه {cur_page_number}',
            position = SizeAndPosition(top = 31, left = 71)
        )
        
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 33, width = 150),
            halign = 'c'
        )
        
        fetch : List[PublisherViewModel] = self.service_provider.get_all_publishers()
        start_row = (cur_page_number - 1) * 10
        end_row = (cur_page_number * 10)
        end_row = min(len(fetch), end_row)
        
        table_content : List[List[Element]] = [
            [
                Text('نام ناشر',halign='c'),
                Text('آدرس',halign='c'),
                Text('ایمیل',halign='c'),
                Text('شماره تماس',halign='c'),
                Text('کتاب ها',halign='c'),
                Text('جزئیات',halign='c')
            ]
        ]
        for row in fetch[start_row:end_row]:
            table_row = [
                Text(ConsoleExtension.short_text(row.name, 16), halign='c'),
                Text(ConsoleExtension.short_text(row.address, 30), halign='c'),
                Text(ConsoleExtension.short_text(row.contact_email, 25), halign='c'),
                Text(ConsoleExtension.short_text(row.phone, 16), halign='c'),
                Text(ConsoleExtension.short_text(row.books, 25), halign='c'),
                Button('مشاهده جزئیات', halign='c', click_func = lambda r=row: self.get_publisher_detail_page(r))
            ]
            table_content.append(table_row)          
                
        publishers_table = Table(table_content, SizeAndPosition(top = 7), start_row_id = start_row)
        publishers_table.position.left = (150 - publishers_table.position.width) // 2
        
        next_button.position.top = publishers_table.position.bottom + 1
        cur_page.position.top = publishers_table.position.bottom + 1
        prev_button.position.top = publishers_table.position.bottom + 1
            
        #=============================================================================
        #=========================== Link Elemnets Together ==========================
        
        table_content[1][5].linked_elements['u'] = search_button
        table_content[1][5].linked_elements['d'] = table_content[2][5]
            
        for i in range(2,10):
            table_content[i][5].linked_elements['u'] = table_content[i - 1][5]
            table_content[i][5].linked_elements['d'] = table_content[i + 1][5]
            
        table_content[10][5].linked_elements['u'] = table_content[9][5]
        table_content[10][5].linked_elements['d'] = next_button
                
        publisher_name_input_box.linked_elements['d'] = search_button
        
        search_button.linked_elements['u'] = publisher_name_input_box
        search_button.linked_elements['d'] = table_content[1][5]
        
        prev_button.linked_elements['u'] = table_content[10][5]
        prev_button.linked_elements['r'] = next_button
        prev_button.linked_elements['d'] = back_button
        
        next_button.linked_elements['u'] = table_content[10][5]
        next_button.linked_elements['l'] = prev_button
        next_button.linked_elements['d'] = back_button
        
        back_button.linked_elements['u'] = next_button
        back_button.linked_elements['r'] = next_button
        back_button.linked_elements['l'] = prev_button

        #=============================================================================
        #=========================== Page Initializing ===============================
        elements = [
            publisher_name_input_box, search_button, prev_button, next_button, cur_page, back_button, publishers_table
        ]
        page = self._create_page('صفحه ناشرین', elements)
        page.cur_page_number = cur_page_number
        page.fetch = fetch
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        
        def search():
            try:
                page.fetch : List[PublisherViewModel] = self.service_provider.publisher_search(publisher_name_input_box.content)
            except ReachedToRequestLimitError:
                return self.get_request_limited_page()
                
            page.cur_page_number = 1
            cur_page.content = f'صفحه {page.cur_page_number}'
        
            start_row = (page.cur_page_number - 1) * 10
            end_row = (page.cur_page_number * 10)
            end_row = min(len(page.fetch), end_row)
        
            table_content : List[List[Element]] = [
                [
                    Text('نام ناشر',halign='c'),
                    Text('آدرس',halign='c'),
                    Text('ایمیل',halign='c'),
                    Text('شماره تماس',halign='c'),
                    Text('کتاب ها',halign='c'),
                    Text('جزئیات',halign='c')
                ]
            ]
            for row in page.fetch[start_row:end_row]:
                table_row = [
                    Text(ConsoleExtension.short_text(row.name, 16), halign='c'),
                    Text(ConsoleExtension.short_text(row.address, 30), halign='c'),
                    Text(ConsoleExtension.short_text(row.contact_email, 25), halign='c'),
                    Text(ConsoleExtension.short_text(row.phone, 16), halign='c'),
                    Text(ConsoleExtension.short_text(row.books, 25), halign='c'),
                    Button('مشاهده جزئیات',halign='c', click_func = lambda r=row: self.get_publisher_detail_page(r))
                ]
                table_content.append(table_row)
                
            table_content[1][5].linked_elements['u'] = search_button
            table_content[1][5].linked_elements['d'] = table_content[2][5]
            
            for i in range(2,10):
                table_content[i][5].linked_elements['u'] = table_content[i - 1][5]
                table_content[i][5].linked_elements['d'] = table_content[i + 1][5]
            
            table_content[10][5].linked_elements['u'] = table_content[9][5]
            table_content[10][5].linked_elements['d'] = next_button
            
            search_button.linked_elements['d'] = table_content[1][5]
            prev_button.linked_elements['u'] = table_content[10][5]
            next_button.linked_elements['u'] = table_content[10][5]
            
            ConsoleExtension.clear_area(publishers_table.position, page.position)
            
            publishers_table.update(table_content, start_row_id=start_row)
            publishers_table.position.left = (150 - publishers_table.position.width) // 2
        
            ConsoleExtension.clear_area(next_button.position, page.position)
            ConsoleExtension.clear_area(cur_page.position, page.position)
            ConsoleExtension.clear_area(prev_button.position, page.position)
            
            next_button.position.top = publishers_table.position.bottom + 1
            cur_page.position.top = publishers_table.position.bottom + 1
            prev_button.position.top = publishers_table.position.bottom + 1
            
        search_button.click_func = search
        
        def next():
            page.cur_page_number += 1
            cur_page.content = f'صفحه {page.cur_page_number}'
            
            start_row = (page.cur_page_number - 1) * 10
            if start_row >= len(page.fetch):
                page.cur_page_number -= 1
                cur_page.content = f'صفحه {page.cur_page_number}'
                return
            
            end_row = (page.cur_page_number * 10)
            end_row = min(len(page.fetch), end_row)
        
            table_content : List[List[Element]] = [
                [
                    Text('نام ناشر',halign='c'),
                    Text('آدرس',halign='c'),
                    Text('ایمیل',halign='c'),
                    Text('شماره تماس',halign='c'),
                    Text('کتاب ها',halign='c'),
                    Text('جزئیات',halign='c')
                ]
            ]
            for row in page.fetch[start_row:end_row]:
                table_row = [
                    Text(ConsoleExtension.short_text(row.name, 16), halign='c'),
                    Text(ConsoleExtension.short_text(row.address, 30), halign='c'),
                    Text(ConsoleExtension.short_text(row.contact_email, 25), halign='c'),
                    Text(ConsoleExtension.short_text(row.phone, 16), halign='c'),
                    Text(ConsoleExtension.short_text(row.books, 25), halign='c'),
                    Button('مشاهده جزئیات', halign='c', click_func = lambda r=row: self.get_publisher_detail_page(r))
                ]
                table_content.append(table_row)
                
            table_content[1][5].linked_elements['u'] = search_button
            table_content[1][5].linked_elements['d'] = table_content[2][5]
            
            for i in range(2,10):
                table_content[i][5].linked_elements['u'] = table_content[i - 1][5]
                table_content[i][5].linked_elements['d'] = table_content[i + 1][5]
            
            table_content[10][5].linked_elements['u'] = table_content[9][5]
            table_content[10][5].linked_elements['d'] = next_button
            
            search_button.linked_elements['d'] = table_content[1][5]
            prev_button.linked_elements['u'] = table_content[10][5]
            next_button.linked_elements['u'] = table_content[10][5]
            
            ConsoleExtension.clear_area(publishers_table.position, page.position)
            
            publishers_table.update(table_content, start_row_id=start_row)
            publishers_table.position.left = (150 - publishers_table.position.width) // 2
        
            ConsoleExtension.clear_area(next_button.position, page.position)
            ConsoleExtension.clear_area(cur_page.position, page.position)
            ConsoleExtension.clear_area(prev_button.position, page.position)
            
            next_button.position.top = publishers_table.position.bottom + 1
            cur_page.position.top = publishers_table.position.bottom + 1
            prev_button.position.top = publishers_table.position.bottom + 1

        next_button.click_func = next


        def prev():
            if page.cur_page_number <= 1:
                return
            page.cur_page_number -= 1
            cur_page.content = f'صفحه {page.cur_page_number}'
            
            start_row = (page.cur_page_number - 1) * 10            
            end_row = (page.cur_page_number * 10)
            end_row = min(len(page.fetch), end_row)
        
            table_content : List[List[Element]] = [
                [
                    Text('نام ناشر',halign='c'),
                    Text('آدرس',halign='c'),
                    Text('ایمیل',halign='c'),
                    Text('شماره تماس',halign='c'),
                    Text('کتاب ها',halign='c'),
                    Text('جزئیات',halign='c')
                ]
            ]
            for row in page.fetch[start_row:end_row]:
                table_row = [
                    Text(ConsoleExtension.short_text(row.name, 16), halign='c'),
                    Text(ConsoleExtension.short_text(row.address, 30), halign='c'),
                    Text(ConsoleExtension.short_text(row.contact_email, 25), halign='c'),
                    Text(ConsoleExtension.short_text(row.phone, 16), halign='c'),
                    Text(ConsoleExtension.short_text(row.books, 25), halign='c'),
                    Button('مشاهده جزئیات', halign='c', click_func = lambda r=row: self.get_publisher_detail_page(r))
                ]
                table_content.append(table_row)
            
            table_content[1][5].linked_elements['u'] = search_button
            table_content[1][5].linked_elements['d'] = table_content[2][5]
            
            for i in range(2,10):
                table_content[i][5].linked_elements['u'] = table_content[i - 1][5]
                table_content[i][5].linked_elements['d'] = table_content[i + 1][5]
            
            table_content[10][5].linked_elements['u'] = table_content[9][5]
            table_content[10][5].linked_elements['d'] = next_button
            
            search_button.linked_elements['d'] = table_content[1][5]
            prev_button.linked_elements['u'] = table_content[10][5]
            next_button.linked_elements['u'] = table_content[10][5]

            ConsoleExtension.clear_area(publishers_table.position, page.position)
            
            publishers_table.update(table_content, start_row_id=start_row)
            publishers_table.position.left = (150 - publishers_table.position.width) // 2
        
            ConsoleExtension.clear_area(next_button.position, page.position)
            ConsoleExtension.clear_area(cur_page.position, page.position)
            ConsoleExtension.clear_area(prev_button.position, page.position)
            
            next_button.position.top = publishers_table.position.bottom + 1
            cur_page.position.top = publishers_table.position.bottom + 1
            prev_button.position.top = publishers_table.position.bottom + 1
            
        prev_button.click_func = prev


        def back():
            return self.get_homepage()  
        back_button.click_func = back

        return page
    

    #==================================== Publisher Detail Page =================================
    def get_publisher_detail_page(self, publisher : PublisherViewModel):
        
        if not self.service_provider.can_guest_request():
            return self.get_request_limited_page()
                
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
        
        cur_page_number = 1

        cur_page = Text(
            content = f'صفحه {cur_page_number}',
            position = SizeAndPosition(top = 31, left = 71)
        )
        
        back_button = Button(
            text = 'بازگشت',
            position = SizeAndPosition(top = 33, width = 150),
            halign = 'c'
        )
        
        fetch : List[BookViewModel] = self.service_provider.book_advance_search(publisher = publisher.name)
        start_row = (cur_page_number - 1) * 10
        end_row = (cur_page_number * 10)
        end_row = min(len(fetch), end_row)
        
        table_content : List[List[Element]] = [
            [Text('عنوان',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')]
        ]
        for row in fetch[start_row:end_row]:
            table_row = [
                Text(ConsoleExtension.short_text(row.title, 30),halign='c'),
                Text(ConsoleExtension.short_text(row.author, 35),halign='c'),
                Text(ConsoleExtension.short_text(row.category, 50),halign='c')
            ]
            table_content.append(table_row)
                
        books_table = Table(table_content, SizeAndPosition(top = 8), start_row_id = start_row)
        books_table.position.left = (150 - books_table.position.width) // 2
        
        next_button.position.top = books_table.position.bottom
        cur_page.position.top = books_table.position.bottom
        prev_button.position.top = books_table.position.bottom
            
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
        #=========================== Page Initializing ===============================
        elements = [
            publisher_info, prev_button, next_button, cur_page, back_button, books_table
        ]
        page = self._create_page(f'{publisher.name}', elements)
        page.cur_page_number = cur_page_number
        page.fetch = fetch
        #=============================================================================
        #=========================== Click Functions Initializing ====================
        
        def next():
            page.cur_page_number += 1
            cur_page.content = f'صفحه {page.cur_page_number}'
            
            start_row = (page.cur_page_number - 1) * 10
            if start_row >= len(page.fetch):
                page.cur_page_number -= 1
                cur_page.content = f'صفحه {page.cur_page_number}'
                return
            
            end_row = (page.cur_page_number * 10)
            end_row = min(len(page.fetch), end_row)
        
            table_content : List[List[Element]] = [
                [Text('عنوان',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')]
            ]
            for row in page.fetch[start_row:end_row]:
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
            
            next_button.position.top = books_table.position.bottom + 1
            cur_page.position.top = books_table.position.bottom + 1
            prev_button.position.top = books_table.position.bottom + 1

        next_button.click_func = next


        def prev():
            if page.cur_page_number <= 1:
                return
            page.cur_page_number -= 1
            cur_page.content = f'صفحه {page.cur_page_number}'
            
            start_row = (page.cur_page_number - 1) * 10            
            end_row = (page.cur_page_number * 10)
            end_row = min(len(page.fetch), end_row)
        
            table_content : List[List[Element]] = [
                [Text('عنوان',halign='c'), Text('نویسندگان',halign='c'), Text('دسته بندی ها',halign='c')]
            ]
            for row in page.fetch[start_row:end_row]:
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
            
            next_button.position.top = books_table.position.bottom + 1
            cur_page.position.top = books_table.position.bottom + 1
            prev_button.position.top = books_table.position.bottom + 1
            
        prev_button.click_func = prev


        def back():
            return self.get_publishers_page()  
        back_button.click_func = back

        return page