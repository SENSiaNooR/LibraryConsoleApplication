from typing import Optional
from Presentation.ConsoleUI.Components.ConsoleExtension import ConsoleExtension
from Presentation.ConsoleUI.Components.SizeAndPosition import SizeAndPosition
from Presentation.ConsoleUI.Components.Element import Element


class Text(Element):
    """
    A UI element that displays and aligns text within a defined rectangular area.

    This component handles automatic resizing to fit the content and supports
    both horizontal and vertical text alignment. It is console-based and
    respects both left-to-right and right-to-left text directions (e.g. Persian).

    Attributes
    ----------
    content : str
        The string content to render.
    position : SizeAndPosition
        The position and size of the text block.
    halign : {'l', 'c', 'r'}
        Horizontal alignment: left, center, or right.
    valign : {'t', 'm', 'b'}
        Vertical alignment: top, middle, or bottom.

    Methods
    -------
    resize_to_fit()
        Resizes the text block to fit the content exactly.
    render(top_offset=0, left_offset=0)
        Renders the text at its position with alignment applied.
    """

    TEXT_HORIZONTAL_ALIGN = ('l', 'c', 'r')
    TEXT_VERTICAL_ALIGN = ('t', 'm', 'b')

    def __init__(
        self,
        content: str,
        position: Optional[SizeAndPosition] = None,
        halign: str = 'l',
        valign: str = 't'
    ):
        """
        Initialize a text element.

        Parameters
        ----------
        content : str
            The string to be displayed.
        position : Optional[SizeAndPosition], default=None
            The position and size of the element in the console.
        halign : {'l', 'c', 'r'}, default='l'
            Horizontal text alignment (left, center, right).
        valign : {'t', 'm', 'b'}, default='t'
            Vertical text alignment (top, middle, bottom).

        Raises
        ------
        ValueError
            If alignment values are not one of the accepted choices.
        """
        super().__init__(position=position, linked_elements=None, focusable=False, clickable=False)

        if halign not in self.TEXT_HORIZONTAL_ALIGN:
            raise ValueError(f"horizontal_align must be one of {self.TEXT_HORIZONTAL_ALIGN}")
        if valign not in self.TEXT_VERTICAL_ALIGN:
            raise ValueError(f"vertical_align must be one of {self.TEXT_VERTICAL_ALIGN}")

        if self.position is None:
            self.position = SizeAndPosition()

        self._c = ""
        self.halign = halign
        self.valign = valign
        self.content = content  # triggers height/width adjustment

    def _height_resize(self):
        """Ensure height is large enough to fit the text lines."""
        lines = self._c.splitlines() or [' ']
        content_height = len(lines)
        if self.position.height < content_height:
            self.position.height = content_height

    def _width_resize(self):
        """Ensure width is large enough to fit the widest line."""
        lines = self._c.splitlines() or [' ']
        content_width = max((len(line) for line in lines), default=1)
        if self.position.width < content_width:
            self.position.width = content_width

    @property
    def content(self) -> str:
        """The textual content of this element."""
        return self._c

    @content.setter
    def content(self, content: str):
        """Update content and adjust the element’s size automatically."""
        self._c = content
        self._height_resize()
        self._width_resize()

    def resize_to_fit(self):
        """Resize this Text element so it exactly fits its content."""
        self.position.width = 1
        self.position.height = 1
        self._width_resize()
        self._height_resize()

    def render(self, top_offset: int = 0, left_offset: int = 0):
        """
        Render the text in the console at the given position with applied alignment.

        Parameters
        ----------
        top_offset : int, default=0
            Vertical offset for rendering.
        left_offset : int, default=0
            Horizontal offset for rendering.
        """
        lines = self.content.splitlines() or ['']

        # Determine top alignment offset
        align_top_offset = self.position.top
        if self.valign == 'm':
            align_top_offset += (self.position.height - len(lines)) // 2
        elif self.valign == 'b':
            align_top_offset += self.position.height - len(lines)

        for i, line in enumerate(lines):
            justified_line = ConsoleExtension.optimize_for_farsi(line)

            if self.halign == 'l':
                justified_line = justified_line.ljust(self.position.width)
            elif self.halign == 'c':
                justified_line = justified_line.center(self.position.width)
            else:
                justified_line = justified_line.rjust(self.position.width)

            ConsoleExtension.reset_color()
            ConsoleExtension.set_cursor(
                top_offset + align_top_offset + i,
                left_offset + self.position.left
            )
            print(justified_line, end='')

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(text={self.content!r}, pos={self.position}, "
            f"halign={self.halign}, valign={self.valign})"
        )
