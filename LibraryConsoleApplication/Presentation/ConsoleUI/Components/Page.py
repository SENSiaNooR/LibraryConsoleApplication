from typing import List
import time
import shutil
from Presentation.ConsoleUI.Components.ConsoleExtension import ConsoleExtension
from Presentation.ConsoleUI.Components.Element import Element
from Presentation.ConsoleUI.Components.Table import Table
from Presentation.ConsoleUI.Components.SizeAndPosition import SizeAndPosition


class Page:
    """
    Represents a UI page that contains and manages multiple elements.

    Attributes
    ----------
    elements : list[Element]
        The list of elements to render (positions are relative to page).
    position : SizeAndPosition
        The absolute position and size of the page itself.
    auto_resize : bool
        Whether the page should automatically resize to fit its elements.
    """

    def __init__(
        self,
        elements: List[Element],
        position: SizeAndPosition,
        auto_resize: bool = True
    ):
        if not isinstance(position, SizeAndPosition):
            raise TypeError("position must be an instance of SizeAndPosition")

        self.elements = elements
        self.position = position
        self.auto_resize = auto_resize
        self.border = False
        self.exit_flag = False
        
        focusables = self.__get_focusables()
        if focusables:
            for e in focusables:
                e.unfocus()
            focusables[0].focus()
            
        if auto_resize:
            self.resize()
            
    def __get_focusables(self):
        focusables = [element for element in self.elements if element.focusable]
        tables_elements = [table.elements for table in self.elements if isinstance(table, Table)]
        for elements in tables_elements:
            focusables += [element for element in elements if element.focusable]
        return focusables
    
    def __get_clickables(self):
        clickables = [element for element in self.elements if element.clickable]
        tables_elements = [table.elements for table in self.elements if isinstance(table, Table)]
        for elements in tables_elements:
            clickables += [element for element in elements if element.clickable]
        return clickables


    def render(self):
        """Renders all elements that fit inside the page area."""
        if self.auto_resize:
            self.resize()

        term_size = shutil.get_terminal_size((80, 24))
        term_width, term_height = term_size.columns, term_size.lines

        if (
            self.position.width + self.position.left > term_width or
            self.position.height + self.position.top > term_height
        ):
            ConsoleExtension.clear_console()
            ConsoleExtension.set_cursor(2, 5)
            print("\033[91m⚠️  Please zoom out or enlarge the console window.\033[0m")

            while True:
                time.sleep(0.3)
                new_size = shutil.get_terminal_size((80, 24))
                if (
                    self.position.width + self.position.left <= new_size.columns and
                    self.position.height + self.position.top <= new_size.lines
                ):
                    ConsoleExtension.clear_console()
                    break
            return self.render()

        if self.border:
            if self.position.top == 0 or self.position.left == 0:
                raise ValueError('Page dont have enough space to have border.')
            ConsoleExtension.print_table(
                self.position.top - 1,
                self.position.left - 1,
                [self.position.width],
                [self.position.height]
            )

        for element in self.elements:
            if (
                element.position.bottom > self.position.height or
                element.position.right > self.position.width
            ):
                continue

            element.render(
                top_offset=self.position.top,
                left_offset=self.position.left
            )

    def resize(self):
        """Adjusts the page size to fit all its elements (relative layout)."""
        if not self.elements:
            return

        max_bottom = max(el.position.bottom for el in self.elements)
        max_right = max(el.position.right for el in self.elements)

        self.position.height = max_bottom
        self.position.width = max_right

    def __repr__(self):
        return (
            f"Page(num_elements={len(self.elements)}, "
            f"pos={self.position}, auto_resize={self.auto_resize})"
        )
    
    def _arrowkey_event(self, arrow):
        focusables = self.__get_focusables()
        focused = [element for element in focusables if element.is_focused()]
        if (not focused) or len(focused) > 1:
            raise Exception(f'{focused=}')
        focused = focused[0]
        if focused.linked_elements:
            linked = focused.linked_elements.get(arrow)
            if linked:
                linked.focus()
                focused.unfocus()

    def up_event(self):
        self._arrowkey_event('u')
            
    def down_event(self):
        self._arrowkey_event('d')
        
    def left_event(self):
        self._arrowkey_event('l')
        
    def right_event(self):
        self._arrowkey_event('r')
        
    def click_event(self):
        clickables = self.__get_clickables()
        focused = [element for element in clickables if element.is_focused()]
        if (not focused) or len(focused) > 1:
            raise Exception()        
        focused = focused[0]
        return focused.click(self.position.top, self.position.left)