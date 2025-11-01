from __future__ import annotations
from typing import Optional
from Exceptions.Exceptions import NotClickableElementError, NotFocusableElementError
from Presentation.ConsoleUI.Components.SizeAndPosition import SizeAndPosition
from typing import Optional, Dict
from abc import ABC, abstractmethod


class Element(ABC):
    """
    Abstract base class for all UI elements.

    Each element has:
      - a `position` (instance of SizeAndPosition)
      - optional `linked_elements` that define navigation links
        (e.g., 'u', 'd', 'l', 'r' for up/down/left/right)
      - `focusable` and `clickable` flags controlling interactivity.

    Subclasses (e.g. Text, InputBox, Button) should override
    the abstract methods: focus(), unfocus(), click(), render().
    """

    VALID_DIRECTIONS = ('u', 'd', 'l', 'r')

    def __init__(
        self,
        position: Optional[SizeAndPosition] = None,
        linked_elements: Optional[Dict[str, Element]] = None,
        focusable: bool = True,
        clickable: bool = True
    ):
        self.position: Optional[SizeAndPosition] = position
        self.linked_elements: Dict[str, Optional[Element]] = {
            key: None for key in self.VALID_DIRECTIONS
        }
        if linked_elements:
            self._set_linked_elements(linked_elements)

        self.focusable: bool = focusable
        self.clickable: bool = clickable
        self._is_focused: bool = False


    def _set_linked_elements(self, linked_elements: Dict[str, Optional[Element]]):
        """Safely updates the element's directional links."""
        for key in self.VALID_DIRECTIONS:
            value = linked_elements.get(key)
            if value is not None and not isinstance(value, Element):
                raise TypeError(f"linked element '{key}' must be an Element or None")
            self.linked_elements[key] = value

    def focus(self):
        """Called when the element gains focus."""
        if not self.focusable:
            raise NotFocusableElementError()
        self._is_focused = True

    def unfocus(self):
        """Called when the element loses focus."""
        if not self.focusable:
            raise NotFocusableElementError()
        self._is_focused = False
        
    def is_focused(self):
        return self._is_focused

    def click(self, top_offset = 0, left_offset = 0):
        """Executes the element’s click action if clickable."""
        if not self.clickable:
            raise NotClickableElementError()

    def render(self, top_offset = 0, left_offset = 0):
        """Renders the element."""
        pass

    def __repr__(self):
        pos = f"{self.position}" if self.position else "None"
        return (
            f"{self.__class__.__name__}(position={pos}, "
            f"focusable={self.focusable}, clickable={self.clickable})"
        )

    def __str__(self):
        return f"<{self.__class__.__name__}: focused={self._is_focused}>"

    def is_focused(self) -> bool:
        """Returns whether the element is currently focused."""
        return self._is_focused