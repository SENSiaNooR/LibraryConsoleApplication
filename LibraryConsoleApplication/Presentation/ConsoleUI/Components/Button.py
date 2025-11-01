from typing import Callable, Dict, Optional
from Presentation.ConsoleUI.Components.Element import Element
from Presentation.ConsoleUI.Components.ConsoleExtension import ConsoleExtension
from Presentation.ConsoleUI.Components.SizeAndPosition import SizeAndPosition


class Button(Element):
    """
    A UI button element that renders a clickable text-based button in the console.

    This component supports horizontal and vertical alignment and can be focused.
    The button automatically resizes to fit its content.

    Attributes
    ----------
    text : str
        The label displayed on the button.
    position : SizeAndPosition
        The position and size of the button.
    halign : {'l', 'c', 'r'}
        Horizontal alignment of the text inside the button.
    valign : {'t', 'm', 'b'}
        Vertical alignment of the text inside the button.
    click_func : Optional[Callable]
        Function to execute when the button is clicked.

    Methods
    -------
    resize_to_fit()
        Resizes the button to fit the text content.
    render(top_offset=0, left_offset=0)
        Draws the button in the console.
    click(top_offset=0, left_offset=0)
        Executes the associated click function.
    """

    TEXT_HORIZONTAL_ALIGN = ('l', 'c', 'r')
    TEXT_VERTICAL_ALIGN = ('t', 'm', 'b')

    def __init__(
        self,
        text: str,
        position: Optional[SizeAndPosition] = None,
        linked_elements: Optional[Dict[str, Element]] = None,
        halign: str = 'l',
        valign: str = 't',
        click_func: Optional[Callable] = None
    ):
        """
        Initialize a Button element.

        Parameters
        ----------
        text : str
            The button label to display.
        position : Optional[SizeAndPosition], default=None
            The position and size of the button.
        linked_elements : Optional[Dict[str, Element]], default=None
            Navigation links to other focusable elements.
        halign : {'l', 'c', 'r'}, default='l'
            Horizontal alignment of the text.
        valign : {'t', 'm', 'b'}, default='t'
            Vertical alignment of the text.
        click_func : Optional[Callable], default=None
            Function to be called when the button is clicked.

        Raises
        ------
        ValueError
            If an invalid alignment value is provided.
        """
        super().__init__(position=position, linked_elements=linked_elements, focusable=True, clickable=True)

        if halign not in self.TEXT_HORIZONTAL_ALIGN:
            raise ValueError(f"horizontal_align must be one of {self.TEXT_HORIZONTAL_ALIGN}")
        if valign not in self.TEXT_VERTICAL_ALIGN:
            raise ValueError(f"vertical_align must be one of {self.TEXT_VERTICAL_ALIGN}")

        if self.position is None:
            self.position = SizeAndPosition()
            
        self.halign = halign
        self.valign = valign
        self.click_func = click_func
        self._t = ""
        self.text = text  # trigger resize


    @property
    def text(self) -> str:
        """The button label text."""
        return self._t

    @text.setter
    def text(self, value: str):
        """Set button label and resize to fit."""
        self._t = value
        self._height_resize()
        self._width_resize()
        
    def _height_resize(self):
        """Ensure height is large enough to fit the text lines."""
        lines = self._t.splitlines() or [' ']
        text_height = len(lines)
        if self.position.height < text_height:
            self.position.height = text_height

    def _width_resize(self):
        """Ensure width is large enough to fit the widest line."""
        lines = self._t.splitlines() or [' ']
        text_width = max((len(line) for line in lines), default=1) + 4
        text_width = max(text_width, 5)
        if self.position.width < text_width:
            self.position.width = text_width

    def resize_to_fit(self):
        """Resize this button so it fits its text label."""
        self.position.width = 1
        self.position.height = 1
        self._width_resize()
        self._height_resize()

    def render(self, top_offset: int = 0, left_offset: int = 0):
        """
        Render the button at its defined position in the console.

        Parameters
        ----------
        top_offset : int, default=0
            Vertical offset from the top of the console.
        left_offset : int, default=0
            Horizontal offset from the left of the console.
        """
        lines = self._t.splitlines() or ['']

        # Determine vertical alignment
        align_top_offset = self.position.top
        if self.valign == 'm':
            align_top_offset += (self.position.height - len(lines)) // 2
        elif self.valign == 'b':
            align_top_offset += self.position.height - len(lines)

        # Choose color based on focus
        if self._is_focused:
            ConsoleExtension.set_color_focused()
        else:
            ConsoleExtension.set_color_unfocused()

        # Render button lines
        for i, line in enumerate(lines):
            justified_line = f"< {line} >"
            justified_line = ConsoleExtension.optimize_for_farsi(justified_line)

            if self.halign == 'l':
                justified_line = justified_line.ljust(self.position.width)
            elif self.halign == 'c':
                justified_line = justified_line.center(self.position.width)
            else:
                justified_line = justified_line.rjust(self.position.width)

            ConsoleExtension.set_cursor(
                top_offset + align_top_offset + i,
                left_offset + self.position.left
            )
            print(justified_line, end='')

        ConsoleExtension.reset_color()

    def click(self, top_offset: int = 0, left_offset: int = 0):
        """
        Execute the button's click action.

        Parameters
        ----------
        top_offset : int, default=0
            Vertical offset of the page.
        left_offset : int, default=0
            Horizontal offset of the page.
        """
        if self.click_func:
            return self.click_func()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(text={self.text!r}, pos={self.position}, "
            f"halign={self.halign}, valign={self.valign})"
        )
