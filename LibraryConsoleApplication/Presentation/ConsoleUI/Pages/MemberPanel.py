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
from Services.MemberServices import MemberServices


class MemberPanel:
    
    _page_position : SizeAndPosition

    def __init__(self, token):
        self.service_provider = MemberServices(token)
        self.token = token
        self._page_position = SizeAndPosition(30,1,36,150)

    def _create_page(self, title: str) -> Page:
        page = Page(self._page_position)
        page.add_element(Text(title, SizeAndPosition(left = (self._page_position.width - 20) // 2, width = 20), halign='c'))
        return page

    def get_homepage(self):
        page = self._create_page('صفحه اصلی')
        page.add_element(Text('سلام ممبر عزیز'))
        return page