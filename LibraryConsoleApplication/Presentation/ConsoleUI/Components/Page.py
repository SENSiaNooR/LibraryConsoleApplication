from typing import List
from Components.Element import Element
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

    def render(self):
        """Renders all elements that fit inside the page area."""
        if self.auto_resize:
            self.resize()

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