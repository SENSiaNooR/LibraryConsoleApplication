from typing import List, Any
import time
import shutil
from Presentation.ConsoleUI.Components.ConsoleExtension import ConsoleExtension
from Presentation.ConsoleUI.Components.Element import Element
from Presentation.ConsoleUI.Components.Table import Table
from Presentation.ConsoleUI.Components.SizeAndPosition import SizeAndPosition


class Page:
    """
    Represents a logical UI page that can render and manage multiple console elements.

    The Page acts as a container for `Element` objects (such as `Text`, `Button`, or `Table`),
    controlling layout, focus navigation, and rendering boundaries relative to the terminal window.

    It can also store dynamic per-page data in an internal key-value bag (similar to ASP.NET's ViewBag).

    Attributes
    ----------
    elements : list[Element]
        The list of UI elements belonging to this page.
    position : SizeAndPosition
        The absolute position and dimensions of the page within the console.
    auto_resize : bool
        Whether the page automatically adjusts its size to fit contained elements.
    border : bool
        If True, a border is drawn around the page during rendering.
    exit_flag : bool
        A flag used for controlling page-level exit or termination signals.
    bag : dict[str, Any]
        A dictionary for arbitrary per-page data (temporary state, cached fetch results, etc.).

    Methods
    -------
    bag_set(key, value)
        Store a key-value pair in the page's internal data bag.
    bag_get(key, default=None)
        Retrieve a value from the bag with an optional default.
    add_element(element)
        Add a new UI element to the page.
    remove_element(element)
        Remove an existing element from the page.
    render()
        Render the page and all visible elements, ensuring console bounds are respected.
    resize()
        Recalculate the page’s dimensions based on contained elements.
    up_event() / down_event() / left_event() / right_event()
        Move focus among focusable elements based on arrow-key input.
    click_event()
        Trigger a click event on the currently focused clickable element.
    """

    def __init__(
        self,
        position: SizeAndPosition,
        elements: List[Element] = None,
        auto_resize: bool = True,
        border: bool = True
    ):
        if not isinstance(position, SizeAndPosition):
            raise TypeError("position must be an instance of SizeAndPosition")

        if elements is None:
            elements = []

        self.bag: dict[str, Any] = {}
        self.elements = elements
        self.position = position
        self.auto_resize = auto_resize
        self.border = border
        self.exit_flag = False
        
        self.__update_focused()
            
        if auto_resize:
            self.resize()
            
    def bag_set(self, key, value):
        """Store a key-value pair in the page’s internal data bag."""
        self.bag[key] = value

    def bag_get(self, key, default=None):
        """Retrieve a value from the data bag, returning `default` if missing."""
        return self.bag.get(key, default)
            
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

    def __update_focused(self):
        """Ensure exactly one focusable element is active (if any exist)."""
        focusables = self.__get_focusables()
        if not focusables:
            return

        focused_elements = [focused for focused in focusables if focused.is_focused()]
        if not focused_elements:
            focusables[0].focus()
            return

        if len(focused_elements) == 1:
            return

        for e in focused_elements:
            e.unfocus()
        focusables[0].focus()

    def add_element(self, element: Element):
        """Add a new element to the page and optionally resize."""
        self.elements.append(element)
        self.__update_focused()
        if self.auto_resize:
            self.resize()
            
    def remove_element(self, element: Element):
        """Remove an existing element from the page and optionally resize."""
        self.elements.remove(element)
        self.__update_focused()
        if self.auto_resize:
            self.resize()

    def render(self):
        """
        Render the page and all contained elements, respecting console boundaries.

        If the page is larger than the terminal window, a warning message is shown
        prompting the user to zoom out or enlarge the console window. Once the terminal
        size becomes sufficient, the page is re-rendered automatically.
        """
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
                raise ValueError('Page does not have enough space for border.')
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
        """Recalculate and adjust the page size to fit all its elements."""
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
        """Internal handler for navigating focus using arrow keys."""
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

    def up_event(self): self._arrowkey_event('u')
    def down_event(self): self._arrowkey_event('d')
    def left_event(self): self._arrowkey_event('l')
    def right_event(self): self._arrowkey_event('r')

    def click_event(self):
        """Trigger the click event of the currently focused clickable element."""
        clickables = self.__get_clickables()
        focused = [element for element in clickables if element.is_focused()]
        if (not focused) or len(focused) > 1:
            raise Exception()        
        focused = focused[0]
        return focused.click(self.position.top, self.position.left)
