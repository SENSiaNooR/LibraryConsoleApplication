import time
import keyboard
from Presentation.ConsoleUI.Components.ConsoleExtension import ConsoleExtension
from Presentation.ConsoleUI.Components.Page import Page
from Presentation.ConsoleUI.Pages.GuestPanel import GuestPanel
from Services.AuthServices import AuthServices

class ConsoleApp:
    def __init__(self):
        self.token = AuthServices.login_as_guest()
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
                        self.page = res
                        ConsoleExtension.clear_console()
                        ConsoleExtension.set_cursor(0,0)
                        
        ConsoleExtension.clear_console()
        ConsoleExtension.set_cursor(0,0)
        print('Good Bye!')
        time.sleep(1)