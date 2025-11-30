import time
import keyboard
from Models.Models import UserType
from Presentation.ConsoleUI.Components.ConsoleExtension import ConsoleExtension
from Presentation.ConsoleUI.Components.Page import Page
from Presentation.ConsoleUI.Pages.AdminPanel import AdminPanel
from Presentation.ConsoleUI.Pages.LibrarianPanel import LibrarianPanel
from Presentation.ConsoleUI.Pages.MemberPanel import MemberPanel
from Presentation.ConsoleUI.Pages.GuestPanel import GuestPanel
from Services.AuthServices import AuthServices, LoginResult

class ConsoleApp:
    def __init__(self):
        self.token = AuthServices.login_as_guest().token
        self.panel = GuestPanel(self.token)
        self.page : Page = self.panel.get_homepage()
        
    def run(self):
        ConsoleExtension.clear_console()
        while True:
            if self.page.exit_flag:
                break
            self.page.render()
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'up':
                    self.page.up_event()
                if event.name == 'down':
                    self.page.down_event()
                if event.name == 'left':
                    self.page.left_event()
                if event.name == 'right':
                    self.page.right_event()   
                if event.name == 'enter':
                    res = self.page.click_event()
                    if isinstance(res, Page):
                        self._change_page(res)
                    elif isinstance(res, LoginResult):
                        self._change_panel(res)

                        
        ConsoleExtension.clear_console()
        ConsoleExtension.set_cursor(0,0)
        print('Good Bye!')
        time.sleep(1)

    def _change_page(self, page: Page):
        self.page = page
        ConsoleExtension.clear_console()
        ConsoleExtension.set_cursor(0,0)

    def _change_panel(self, login_res: LoginResult):
        if login_res.user_info.user_type == 'member':
            self.panel = MemberPanel(login_res.token)
        elif login_res.user_info.user_type == 'librarian':
            self.panel = LibrarianPanel(login_res.token)
        elif login_res.user_info.user_type == 'admin':
            self.panel = AdminPanel(login_res.token) 
        elif login_res.user_info.user_type == 'guest':
            self.panel = GuestPanel(login_res.token) 
            
        self._change_page(self.panel.get_homepage())